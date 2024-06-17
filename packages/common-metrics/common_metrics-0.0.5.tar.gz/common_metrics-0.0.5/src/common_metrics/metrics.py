from typing import List
import numpy as np
from numpy.typing import NDArray


def eer(
    genuine: NDArray | List[float | int],
    imposter: NDArray | List[float | int],
    bins: int = 10_001,
) -> float:
    """
    Calculates Equal Error Rate (eer).
    Remember: Genuine scores provided must be greater in value compared to
    imposter.
    Can be used to calculate D-EER, by replacing imposter scores to morph
    scores.

    Parameters
    ----------------------------------------------------------------------
    genuine : List[float] | NDArray
        The list of genuine scores.

    imposter : List[float] | NDArray
        The list of imposter scores.

    Returns
    ----------------------------------------------------------------------
    eer : float
        Equal Error Rate (eer) calculated from given genuine and imposter
        scores.

    Example
    ----------------------------------------------------------------------
    import common_metrics

    genuine_scores = ... # genuine is a 1D numpy array or List of float
    imposter_scores = ... # imposter is a 1D numpy array or List of float
    eer = common_metrics.eer(
        genuine_scores,
        imposter_scores,
        bins=10_001,
    )

    ----------------------------------------------------------------------

    """
    genuine = np.squeeze(np.array(genuine))
    imposter = np.squeeze(np.array(imposter))
    far = np.ones(bins)
    frr = np.ones(bins)
    mi = np.min(imposter)
    mx = np.max(genuine)
    thresholds = np.linspace(mi, mx, bins)
    for id, threshold in enumerate(thresholds):
        fr = np.where(genuine <= threshold)[0].shape[0]
        fa = np.where(imposter >= threshold)[0].shape[0]
        frr[id] = fr * 100 / genuine.shape[0]
        far[id] = fa * 100 / imposter.shape[0]

    di = np.argmin(np.abs(far - frr))

    eer = (far[di] + frr[di]) / 2
    return eer


def frr(
    genuine: NDArray | List[float | int],
    thresholds: float | List[float],
) -> float | List[float]:
    """
    Calculates False Reject Rate (frr).
    Remember: Genuine scores provided must be greater in value compared to
    imposter.

    Parameters
    ----------------------------------------------------------------------
    genuine : List[float] | NDArray
        The list of genuine scores.

    Returns
    ----------------------------------------------------------------------
    frr : float | List[float]
        False Reject Rate (eer) calculated from given genuine scores.

    Example
    ----------------------------------------------------------------------
    Let's say you want to calculate FRR at FMR == 0.1% and 0.01%.

    import common_metrics

    genuine_scores = ... # genuine is a 1D numpy array or List of float
    thresholds = common_metrics.threshold(
        imposter_scores,
        [1e-3, 1e-4], # supply the thresholds in 0-1 scale
        bins=10_001,
    )
    frrs = common_metrics.frr(genuine_scores, thresholds)
    print('FRR at FMR = 0.1%:', frrs[0])
    print('FRR at FMR = 0.01%:', frrs[1])

    ----------------------------------------------------------------------

    """
    if not isinstance(thresholds, list) and not isinstance(thresholds, float):
        raise TypeError(
            f"Expected thresholds of type List[float] or float but got: {type(thresholds)}"
        )

    genuine = np.squeeze(np.array(genuine))
    if isinstance(thresholds, float):
        return len(np.where(genuine <= thresholds)[0]) / genuine.shape[0]
    if isinstance(thresholds, list):
        resutls: List[float] = []
        for thres in thresholds:
            resutls.append(len(np.where(genuine <= thres)[0]) / genuine.shape[0])
        return resutls


def iapar(
    morph: NDArray | List[float | int],
    thresholds: float | List[float],
) -> float | List[float]:
    """
    Calculates Impostor Attack Presentation Acceptance Rate (iapar).

    Parameters
    ----------------------------------------------------------------------
    genuine : List[float] | NDArray
        The list of genuine scores.

    Returns
    ----------------------------------------------------------------------
    eer : float
        Equal Error Rate (eer) calculated from given genuine and imposter
        scores

    Example
    ----------------------------------------------------------------------
    Let's say you want to calculate FRR at FMR == 0.1% and 0.01%.

    import common_metrics

    impostor_scores = ... # impostor is a 1D numpy array or List of float
    morph_scores = ... # morph is a 1D numpy array or List of float
    thresholds = common_metrics.threshold(
        imposter_scores,
        [1e-3, 1e-4], # supply the thresholds in 0-1 scale
        bins=10_001,
    )
    iapars = common_metrics.frr(morph_scores, thresholds)
    print('IAPAR at FMR = 0.1%:', iapars[0])
    print('IAPAR at FMR = 0.01%:', iapars[1])

    ----------------------------------------------------------------------

    """
    if not isinstance(thresholds, list) and not isinstance(thresholds, float):
        raise TypeError(
            f"Expected thresholds of type List[float] or float but got: {type(thresholds)}"
        )

    morph = np.squeeze(np.array(morph))
    if isinstance(thresholds, float):
        return len(np.where(morph >= thresholds)[0]) / morph.shape[0]
    if isinstance(thresholds, list):
        resutls: List[float] = []
        for thres in thresholds:
            resutls.append(len(np.where(morph <= thres)[0]) / morph.shape[0])
        return resutls


def threshold(
    data: NDArray | List[float | int],
    thresholds: List[float] | float,
    bins: int = 10_001,
) -> List[float]:
    """
    Calculates Equal Error Rate (eer).
    Remember: Genuine scores provided must be greater in value compared to
    imposter.
    Can be used to calculate D-EER, by replacing imposter scores to morph
    scores.

    Parameters
    ----------------------------------------------------------------------
    data : List[float] | NDArray
        The list of data for which you want to calculate threshold.
    thresholds : List[float] | NDArray
        The list of thresholds in 0-1 scale.
    bins : int
        The number of bins to be considered while calculating thresholds.
        Default is 10_001.

    Returns
    ----------------------------------------------------------------------
    thresholds : float | List[float]
        Threshold score values for given thresholds.

    Example
    ----------------------------------------------------------------------
    Let's say you want to calculate thresholds at FMR == 0.1% and 0.01%.

    import common_metrics

    imposter_scores = ... # imposter is a 1D numpy array or List of float
    thresholds = common_metrics.threshold(
        imposter_scores,
        [1e-3, 1e-4], # supply the thresholds in 0-1 scale
        bins=10_001,
    )

    ----------------------------------------------------------------------

    """
    if not isinstance(thresholds, list) and not isinstance(thresholds, float):
        raise TypeError(
            f"Expected thresholds of type List[float] or float but got: {type(thresholds)}"
        )

    data = np.array(sorted(data, reverse=True))

    mi = np.min(data)
    mx = np.max(data)

    total_thresholds = np.linspace(mi, mx, bins)
    far = []
    for threshold in total_thresholds:
        fa = np.where(data >= threshold)[0].shape[0]
        far.append(fa / data.shape[0])

    far = np.array(far)

    if isinstance(thresholds, float):
        return total_thresholds[np.argmin(np.abs(far - thresholds))]

    if isinstance(thresholds, list):
        result: List[float] = []
        for threshold in thresholds:
            result.append(total_thresholds[np.argmin(np.abs(far - threshold))])

        return result
