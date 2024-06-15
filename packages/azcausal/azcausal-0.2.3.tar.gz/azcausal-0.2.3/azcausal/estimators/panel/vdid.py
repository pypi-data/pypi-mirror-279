from typing import Iterator

import pandas as pd
import numpy as np

import scipy
from numpy.random import RandomState


def set_to_obj(obj, k, v):
    setattr(obj, k, v)
    return obj


def did_equation(dx):
    dy = dx.unstack(['post', 'treatment', 'target'])

    pre_contr = dy[('N', 'C')]
    post_contr = dy[('Y', 'C')]
    pre_treat = dy[('N', 'T')]
    post_treat = dy[('Y', 'T')]

    did = (post_treat - pre_treat) - (post_contr - pre_contr)

    return did.stack()


def f_sign(row):
    if row['avg_lb'] < 0 and row['avg_ub'] < 0:
        return '-'
    elif row['avg_lb'] > 0 and row['avg_ub'] > 0:
        return '+'
    else:
        return '+/-'


class StandardError(object):
    def sample(self, treatment: pd.Series) -> Iterator[pd.Series]:
        pass

    def fit(self, dx: pd.DataFrame):
        n = len(dx)
        return np.sqrt((n - 1) / n) * dx.std(ddof=1, numeric_only=True)


class Jackknife(StandardError):

    def sample(self, treatment: pd.Series) -> Iterator[pd.Series]:
        treat, contr = treatment['T'], treatment['C']

        if len(contr) > 1:
            for i in range(len(contr)):
                yield pd.Series(dict(T=treat, C=np.delete(contr, i)))

        if len(treat) > 1:
            for i in range(len(treat)):
                yield pd.Series(dict(T=np.delete(treat, i), C=contr))

    def fit(self, dx: pd.DataFrame):
        n = len(dx)
        var = dx.var(ddof=1, numeric_only=True)
        return np.sqrt(((n - 1) / n) * (n - 1) * var)


class Bootstrap(StandardError):
    def __init__(self, n_samples=500, seed=1, balanced=False):
        super().__init__()
        self.seed = seed
        self.n_samples = n_samples
        self.balanced = balanced

    def sample(self, treatment: pd.Series) -> Iterator[pd.Series]:

        if self.balanced:
            for i in range(self.n_samples):
                yield treatment.map(lambda x: RandomState(self.seed + i).choice(x, size=len(x), replace=True))
        else:
            H = dict()
            for unit in treatment['T']:
                H[unit] = 'T'
            for unit in treatment['C']:
                H[unit] = 'C'
            H = pd.Series(H, name='treatment').rename_axis('region', axis='index')

            cnt = 0
            max_cnt = self.n_samples

            random_state = RandomState(self.seed)

            while cnt < max_cnt:

                ss = sorted(random_state.choice(list(H.keys()), size=len(H), replace=True))
                tt = H.loc[ss].to_frame().reset_index().groupby('treatment')['region'].apply(lambda x: list(x))

                # if we have at least one treatment and one control
                if tt.map(lambda x: len(x) > 0).all():
                    yield tt
                    cnt += 1


def cols_to_index(cols):
    H = {label: i for i, label in enumerate(cols)}

    def f(x):
        return [H.get(label, None) for label in x]

    return f


def dot_by_columns(ds, columns, name, weights=None):

    if weights is None:
        weights = columns.map(lambda x: np.full(len(x), 1 / len(x)))
    else:
        weights = columns.map(lambda x: weights.loc[x].values).map(lambda x: x / np.sum(x))

    return pd.DataFrame({k: ds[v].values @ weights[k] for k, v in columns.items()}, index=ds.index).rename_axis(name, axis=1)


def vdid(dx: pd.DataFrame,
         post: pd.Series,
         treatment: pd.Series,
         ratio=None,
         ci: bool = False,
         conf: float = 0.9,
         se: StandardError = Jackknife(),
         weights=None,
         drop_missing_units=False,
         drop_missing_times=False):
    """

    Parameters
    ----------
    dx : pd.DataFrame
        The data on which we want to apply Difference-in-Difference.
    post : pd.Series
        A mapping consisting of `Y` to map to post days and `N` for pre.
    treatment : pd.Series
        A mapping consisting of `C` to map to control days and `T` for treatment.
    ci : bool
        Whether confidence intervals should be calculated.
    conf : float
        The confidence for the CI calculation.
    se : StandardError
        The object to calculate the standard error and confidence intervals.
    drop_missing_units : bool
        Whether units in the treatment array should be dropped if not present in the data frame.
    drop_missing_times : bool
        Whether times in the post array should be dropped if not present in the data frame.

    Returns
    -------
    pd.DataFrame
        A data frame consisting of all treatment effects for each key.

    """

    keys = list(dx.index.names)
    dx = dx.reset_index()

    # get the units and times used in the data set
    units = set(dx[treatment.name].unique())
    times = set(dx[post.name].unique())

    if weights is None:
        weights = dict(time=None, units=None)

    if weights.get('units', None) is not None:
        w = weights['units']
        weights['units'] = pd.Series({u: w.get(u, 0.0) for u in list(units)})

    if weights.get('time', None) is not None:
        w = weights['time']
        weights['time'] = pd.Series({t: w.get(t, 0.0) for t in list(times)})

    # only consider treatment units that are present in the data set (either in pre or post)
    if drop_missing_units:
        treatment = treatment.map(lambda x: [e for e in x if e in units])

    if drop_missing_times:
        post = post.map(lambda x: [e for e in x if e in times])

    # get the values necessary for normalization within post and treatment
    dn = (treatment.map(lambda x: len(x)).to_frame('n_units').reset_index()
          .merge(post.map(lambda x: len(x)).to_frame('n_time').reset_index(), how='cross')
          .set_index(['post', 'treatment'])
          .assign(count=lambda dx: dx['n_units'] * dx['n_time'])
          )

    # melt the outcomes into one column
    dx = pd.melt(dx, id_vars=keys, var_name='target', value_name='value').set_index(keys + ['target'])['value']

    # average over time and summarize to post
    dt = dx.unstack(post.name).fillna(0.0)
    dtp = dot_by_columns(dt, post, 'post', weights=weights.get('time', None)).stack()

    # average over regions and summarize to treatment
    dr = dtp.unstack(treatment.name).fillna(0.0)

    # add the ratio metrics to the data frame
    def r(dy):
        if ratio is not None:
            dy = dy.unstack('target')
            for label, (numerator, denominator) in ratio.items():
                dy = dy.assign(**{label: lambda dd: dd[numerator].values / dd[denominator].replace(0, np.nan).values})
            dy = dy.stack()
        return dy

    davg = r(dot_by_columns(dr, treatment, 'treatment', weights=weights.get('units', None)).stack())

    # a function to calculate the average, cumulative and percentage treatment effects
    def f(dy):

        # average treatment effect
        avg_te = did_equation(dy)

        # cumulative treatment effect
        scale = dn['count'][('Y', 'T')]
        cum_te = avg_te.multiply(scale)

        # percentage treatment effect
        avg_post_treat = dy.xs('Y', level='post').xs('T', level='treatment')
        pct_te = avg_te / (avg_post_treat - avg_te)

        return pd.DataFrame(dict(avg_te=avg_te.values, pct_te=pct_te, cum_te=cum_te.values), index=avg_te.index)

    # treatment effects for all keys and targets provided
    dte = f(davg)

    # if confidence intervals should be calculated
    if ci:

        # simulate based on the standard error method
        dse = {}
        for sample, treatment_mod in enumerate(se.sample(treatment)):
            dse[sample] = dot_by_columns(dr, treatment_mod, 'treatment', weights=weights.get('units', None)).stack()
        dse = f(r(pd.DataFrame(dse).rename_axis('sample', axis=1).stack()))

        # collect all simulations within one data frame
        se = dse.reset_index(level='sample', drop=True).pipe(lambda dx: dx.groupby(level=list(range(len(dx.index.names)))).apply(se.fit))

        # confidence intervals
        for s in ['avg', 'cum', 'pct']:
            lb, ub = scipy.stats.norm.interval(conf, loc=dte[f'{s}_te'], scale=(se[f'{s}_te'] + 1e-16))
            dte = dte.assign(**{f'{s}_se': se[f'{s}_te'], f'{s}_lb': lb, f'{s}_ub': ub})

        # finally add the statistically significant sign
        dte = dte.assign(sign=lambda dx: dx.apply(f_sign, axis=1))

    # get the totals for pre/post and treatment/contr (for average and total)
    def ff(dy, prefix):
        f_map = lambda x: f"{'pre' if x[0] == 'N' else 'post'}_{'contr' if x[1] == 'C' else 'treat'}"
        return dy.unstack(['post', 'treatment']).pipe(lambda dx: set_to_obj(dx, 'columns', dx.columns.map(f_map))).add_prefix(prefix)

    dte = dte.join(ff(davg, 'avg_')).join(ff(davg.multiply(dn['count'], axis=0), 'cum_'))

    # replace the cumulative values of ratios to averages
    if ratio is not None:
        dte = dte.unstack('target')
        for label in ratio.keys():
            for col in [e for e in dte.columns.get_level_values(0) if e.startswith('cum_')]:
                dte[(col, label)] = dte[(col.replace('cum_', 'avg_'), label)]
        dte = dte.stack('target')

    # sort the columns to be more consistent
    cols = ['sign'] if ci else []
    for x in ['cum', 'pct', 'avg']:
        cols += [e for e in dte.columns if e.startswith(x)]
    cols += [e for e in dte.columns if e not in cols]
    dte = dte[cols]

    return dte
