from logging import getLogger
from pathlib import Path
from typing import Callable

import pandas as pd

from .compare import RunOrderResults, get_log_exp_obs_counts
from .em import EmClustering
from ..core import path

logger = getLogger(__name__)

PRECISION = 6  # number of digits behind the decimal point


def get_table_path(top: Path,
                   sample: str,
                   ref: str,
                   sect: str,
                   table: str,
                   k: int,
                   run: int):
    """ Build a path for a table of clustering results. """
    return path.buildpar(*path.CLUST_TAB_SEGS,
                         top=top,
                         cmd=path.CMD_CLUST_DIR,
                         sample=sample,
                         ref=ref,
                         sect=sect,
                         table=table,
                         k=k,
                         run=run,
                         ext=path.CSV_EXT)


def write_single_run_table(run: EmClustering,
                           top: Path,
                           sample: str,
                           ref: str,
                           sect: str,
                           rank: int, *,
                           output_func: Callable[[EmClustering], pd.DataFrame],
                           table: str):
    """ Write a DataFrame of one type of data from one independent run
    of EM clustering to a CSV file. """
    data = output_func(run)
    file = get_table_path(top, sample, ref, sect, table, run.order, rank)
    data.round(PRECISION).to_csv(file, header=True, index=True)
    logger.info(f"Wrote {table} of {run} to {file}")
    return file


def write_props(run: EmClustering,
                top: Path,
                sample: str,
                ref: str,
                sect: str,
                rank: int):
    return write_single_run_table(run,
                                  top,
                                  sample,
                                  ref,
                                  sect,
                                  rank,
                                  output_func=EmClustering.get_props,
                                  table=path.CLUST_PROP_RUN_TABLE)


def write_mus(run: EmClustering,
              top: Path,
              sample: str,
              ref: str,
              sect: str,
              rank: int):
    return write_single_run_table(run,
                                  top,
                                  sample,
                                  ref,
                                  sect,
                                  rank,
                                  output_func=EmClustering.get_mus,
                                  table=path.CLUST_MUS_RUN_TABLE)


def get_count_path(top: Path, sample: str, ref: str, sect: str):
    """ Build a path for a table of bit vector counts. """
    return path.buildpar(*path.CLUST_COUNT_SEGS,
                         top=top,
                         cmd=path.CMD_CLUST_DIR,
                         sample=sample,
                         ref=ref,
                         sect=sect,
                         ext=path.CSVZIP_EXT)


def write_log_counts(orders: list[RunOrderResults],
                     top: Path,
                     sample: str,
                     ref: str,
                     sect: str):
    """ Write the expected and observed log counts of unique bit vectors
    to a CSV file. """
    # Calculate the log expected and observed counts.
    log_counts = get_log_exp_obs_counts(orders).sort_index()
    # Build the path for the output file.
    file = get_count_path(top, sample, ref, sect)
    # Write the log counts to the file.
    log_counts.to_csv(file)
    return file

########################################################################
#                                                                      #
# © Copyright 2024, the Rouskin Lab.                                   #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
