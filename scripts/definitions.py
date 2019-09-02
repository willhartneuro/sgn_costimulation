r"""
Gives several definitions used in the import / analysis process
"""

from protocol import Protocol

#
# The location of files
#
BASE_PATH = "../Papers/001 Costim letter/Data" # the files are stored in the parent directory

#
# DATA INDICES INTO FILES.PY
#
PATH = 0   # the path to the data file
CAP = 1    # the capacitance of the cell
O_P = 2    # the value of optical power in DACs
O_T = 3    # the value of the optical power threshold for this particular cell
E_P = 4    # the value of injected electrical current in pA
E_T = 5    # the value of the electrical threshold for this particular cell
APS = 6    # true if action potentials were visually evident during recording
CEL = 7    # the cell number
PAR = 8    # the offset data set, 1 = 1ms, 2 = 2ms, 3 = 3ms shift in electrical onset

#
# Data indices into the CELLS object in files.py
#
C_CAP = 0   # The cell capacitance
C_OPT = 1   # The cell optical threshold (DACs)
C_ELC = 2   # The cell electrical threshold (pA)


# ID, First offset, num offsets, offset delta
PARAMS = [
    Protocol(0, -5, 18, 1),
    Protocol(1, -5, 18, 2, column_count=2),
    Protocol(2, -5, 18, 3, column_count=2),
    Protocol(3, -5, 18, 2, column_count=2, optical_onset=1.5),
    Protocol(4, -5, 18, 2, column_count=1, optical_onset=1.5),
    Protocol(5, 10, 9, 4, column_count=2, optical_onset=1.5),
    Protocol(6, -3, 9, 4, column_count=2, optical_onset=1.5),
]

JNC_POT = -12.8 / 1000.
