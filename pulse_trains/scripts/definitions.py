r"""
Gives several definitions used in the import / analysis process
"""

import quantities as q

#
# The location of files
#
BASE_PATH = "../Data" # the files are stored in the parent directory

#
# DATA INDICES INTO FILES.PY
#
PATH = 0    # the path to the data file
CAP = 1     # the capacitance of the cell
O_P = 2     # The optical pulse power in DACs
O_W = 3     # The optical pulse width in ms
O_I = 4     # The optical inter-stimulus interval in ms
E_M = 5     # The minimum injected electrical current in pA
E_X = 6     # The maximum injected electrical current in pA
E_W = 7     # The electrical pulse width in ms
LVL = 8     # The number of electrical current levels
O_T = 9     # The optical threshold
E_T = 10    # The electrical threshold
CELL = 11   # The cell ID

JNC_POT = -12.8 * q.mV
