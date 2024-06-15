
from pathlib import Path

import pandas as pd

from ..core import path
from ..core.seq import DNA
from ..relate.write import calc_reads_per_batch, mib_to_bytes


def sim_whole(out_dir: Path,
              sample: str,
              ref: str,
              refseq: DNA,
              reads: int,
              batch_size: int,
              ploq: pd.Series,
              pmut: pd.Series):
    n_per_batch = calc_reads_per_batch(mib_to_bytes(batch_size), len(refseq))

    relvecs = sim_relvecs(refseq, ploq, pmut)


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
