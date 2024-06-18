from scipy.stats import chi2, norm, t

from .classes.enums import HypothesisType


def _check_norm(z: float, _df: int, alfa: float, _type: HypothesisType):
    if _type == HypothesisType.BOTH:
        return z < -norm.ppf(1 - alfa / 2) or z > norm.ppf(1 - alfa / 2)
    elif _type == HypothesisType.RIGHT:
        return z > norm.ppf(1 - alfa)
    elif _type == HypothesisType.LEFT:
        return z < -norm.ppf(1 - alfa)


def _check_t(z: float, df: int, alfa: float, _type: HypothesisType):
    if _type == HypothesisType.BOTH:
        return z < -t.ppf(1 - alfa / 2, df) or z > t.ppf(1 - alfa / 2, df)
    elif _type == HypothesisType.RIGHT:
        return z > t.ppf(1 - alfa, df)
    elif _type == HypothesisType.LEFT:
        return z < -t.ppf(1 - alfa, df)


def _check_chi(z: float, df: int, alfa: float, _type: HypothesisType):
    if _type == HypothesisType.BOTH:
        return z < chi2.ppf(alfa / 2, df) or z > chi2.ppf(1 - alfa / 2, df)
    elif _type == HypothesisType.RIGHT:
        return z > chi2.ppf(1 - alfa, df)
    elif _type == HypothesisType.LEFT:
        return z < chi2.ppf(alfa, df)


def _check_norm_t(z: float, df: int, alfa: float, _type: HypothesisType, use_norm: bool):
    return _check_norm(z, df, alfa, _type) if use_norm else _check_t(z, df, alfa, _type)
