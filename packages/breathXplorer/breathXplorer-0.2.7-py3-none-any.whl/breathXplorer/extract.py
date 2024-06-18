from pathlib import Path
from typing import Sequence, List, Union

import pandas as pd

from .cluster import cluster_merge
from .container import FeatureSet, Sample
from .file_io import cluster_ms, gen_df
from .utils import score, time_union, interpolate_time


# a single task
def find_feature(ms: Union[Path, str], line: bool, quantity: float, method: str, n_peak: int = 1) -> FeatureSet:
    """
    Calculate the feature table of a single MS file (mzML or mzXML).
    :param ms:  Path of the mzML file.
    :param line:  Whether to use line mode.
    :param quantity: control the quality of peak
    :param method:  The method used to find peaks ('Topological' or 'Gaussian').
    :param n_peak:  Number of peaks to be picked
    :return:  Feature table
    """
    ms = Path(ms)
    scanned = cluster_ms(str(ms.absolute()), line, quantity, method, n_peak)
    try:
        scores = score(scanned, scanned['peak_time'])
    except ZeroDivisionError:
        scores = score(scanned)
    return FeatureSet(gen_df(scanned, [('intensity', scores)]))


# merge all the result files of single tasks in the target folder
def merge_result(tbs: Sequence[FeatureSet], names: List[str]) -> Sample:
    """
    Merge the feature tables of multiple MS files (mzML or mzXML).
    :param tbs:  Feature tables
    :param names:  Names of the mzML files
    :return:  Merged feature table
    """
    sub_results = [dict(zip(tb.mz, tb.intensity)) for tb in tbs]
    result = cluster_merge(sub_results)
    return Sample(pd.DataFrame(data=list(result.values()), index=list(result.keys()), columns=names))


def time_align(tbs: Sequence[FeatureSet]) -> Sequence[FeatureSet]:
    """
    Align the time of multiple feature tables.
    :param tbs:  Feature tables
    :return:  Aligned feature tables
    """
    if len(tbs) == 1:
        return tbs
    common_time = time_union([tb.table for tb in tbs])
    return [FeatureSet(interpolate_time(tb.table, common_time)) for tb in tbs]
