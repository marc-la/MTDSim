from scipy.stats import expon
from scipy.stats import norm
from scipy.stats import uniform
from scipy.stats import weibull_min
from scipy.stats import poisson

# Timing-distribution regime for every exponential draw in the substrate
# (D-08 ruling, 2026-08-13 — docs/implementation/intent_conformance_audit.md):
#
#   'shifted'      loc + Exp(scale): mean ~= loc + scale, sigma = scale. The
#                  inherited baseline, faithful to Zhang Table 3's printed
#                  (mean, 0.5) rows; at scale 0.5 the draw is quasi-periodic.
#   'exponential'  Exp(loc): a true exponential whose MEAN is the nominal
#                  value, sigma = mean, memoryless — Zhang §4.5's reading
#                  (µ the historical average); the scale argument is unused.
#
# The default stays 'shifted' so every golden and recorded figure is
# unchanged; a run opts into 'exponential' as a declared input (see
# baseline/run_baseline.py --timing-regime). Both regimes consume exactly one
# variate per call, so switching never desynchronises the seeded RNG stream
# shared with other draw sites.

EXPONENTIAL_REGIMES = ('shifted', 'exponential')
_exponential_regime = 'shifted'


def set_exponential_regime(regime):
    global _exponential_regime
    if regime not in EXPONENTIAL_REGIMES:
        raise ValueError('unknown exponential regime %r (expected one of %s)'
                         % (regime, ', '.join(EXPONENTIAL_REGIMES)))
    _exponential_regime = regime


def get_exponential_regime():
    return _exponential_regime


def exponential_variates(loc, scale):
    if _exponential_regime == 'exponential':
        return expon.rvs(scale=loc, size=1)[0]
    return expon.rvs(loc=loc, scale=scale, size=1)[0]


def normal_variates(loc, scale):
    return norm.rvs(loc=loc, scale=scale, size=1)[0]


def uniform_variates(loc, scale):
    return uniform.rvs(loc=loc, scale=scale, size=1)[0]


def weibull_variates(loc, scale):
    return weibull_min.rvs(loc=loc, scale=scale, size=1)[0]


def poisson_variates(loc, scale):
    return poisson.rvs(loc=loc, scale=scale, size=1)[0]
