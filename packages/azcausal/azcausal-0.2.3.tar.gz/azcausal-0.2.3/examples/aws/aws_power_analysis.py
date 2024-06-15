import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from botocore.config import Config

from azcausal.core.parallelize import Joblib
from azcausal.remote.client import AWSLambda, Client
from azcausal.util import parse_arn
from azcausal.util.analysis import f_power

if __name__ == "__main__":
    arn = "arn:aws:lambda:us-east-1:112353327285:function:azcausal-lambda-run:$LATEST"

    config = Config(connect_timeout=300, read_timeout=300)
    lambda_client = boto3.client('lambda', region_name=parse_arn(arn)['region'], config=config)

    endpoint = AWSLambda(lambda_client, arn)
    client = Client(endpoint)

    class Function:

        def __init__(self, att, seed) -> None:
            super().__init__()
            self.att = att
            self.seed = seed

        def __call__(self, *args, **kwargs):
            from azcausal.data import CaliforniaProp99
            from numpy.random import RandomState
            from azcausal.core.effect import get_true_effect
            from azcausal.core.error import JackKnife
            from azcausal.core.panel import CausalPanel
            from azcausal.util import zeros_like
            from azcausal.estimators.panel.sdid import SDID
            import numpy as np

            # parameters
            seed = self.seed
            att = self.att

            # constants
            panel = CaliforniaProp99(cache=False).panel().filter(contr=True)
            conf = 90
            n_treat = 5
            n_post = 12

            # random seed for reproducibility
            random_state = RandomState(seed)

            # define what is treated and when
            treat_units = random_state.choice(np.arange(panel.n_units()), replace=False, size=n_treat)

            intervention = zeros_like(panel.intervention)
            intervention.iloc[-n_post:, treat_units] = 1

            te = panel.outcome * intervention * (att / 100)
            outcome = panel.outcome + te

            # create the new panel with the new intervention
            panel = CausalPanel(data=dict(intervention=intervention, te=te, outcome=outcome)).setup()

            # use the estimator to get the effect
            true_effect = get_true_effect(panel)

            # run the estimator to get the predicted effect
            estimator = SDID()
            result = estimator.fit(panel)
            estimator.error(result, JackKnife())
            pred_effect = result.effect

            # create an output dictionary of what is true and what we have measured
            res = dict(**pred_effect.to_dict(prefix='pred_', conf=conf), **true_effect.to_dict(prefix='true_', conf=conf))
            res.update(dict(att=att, seed=seed))

            return res


    def f(z):
        att, seed = z
        function = Function(att, seed)
        return client.send(function)


    n_samples = 100

    # create all runs for this analysis (this can potentially include more dimensions as well)
    def g():
        for att in np.linspace(-30, 30, 13):
            for seed in range(n_samples):
                yield att, seed

    # run the simulation in parallel
    parallelize = Joblib(n_jobs=500, prefer='threads', progress=True)
    results = parallelize.run(g(), func=f)

    dx = (pd.DataFrame(results)
          .assign(true_in_ci=lambda dd: dd['true_avg_te'].between(dd['pred_avg_ci_lb'], dd['pred_avg_ci_ub']))
          .assign(rel_te_error=lambda dd: dd['true_rel_te'] - dd['pred_rel_te'])
          )

    # get the power for all different treatment effects
    pw = dx.assign(sign=lambda dd: dd['pred_sign']).groupby('att').apply(f_power).sort_index().reset_index()
    coverage = dx.groupby('att')['true_in_ci'].mean()

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(12, 8))

    fig.suptitle(f'CaliforniaProp99', fontsize=16)

    top.plot(pw['att'], pw['-'], "-o", color="red", label='-')
    top.plot(pw['att'], pw['+'], "-o", color="green", label='+')
    top.plot(pw['att'], pw['+/-'], "-o", color="black", label='+/-', alpha=0.5)
    top.axhline(1.0, color="black", alpha=0.15)
    top.axhline(0.9, color="black", alpha=0.15, linestyle='--')
    top.axhline(0.0, color="black", alpha=0.15)
    top.set_ylim(-0.05, 1.05)
    top.set_xlabel("ATT (%)")
    top.set_ylabel("Statistical Power")
    top.legend()

    bottom.plot(coverage.index, coverage.values, "-o", color="black", label="coverage")
    bottom.axhline(1.0, color="black", alpha=0.15)
    bottom.axhline(0.0, color="black", alpha=0.15)
    bottom.set_ylim(-0.05, 1.05)
    bottom.set_xlabel("ATT (%)")
    bottom.set_ylabel("Coverage")
    bottom.legend()

    plt.show()
