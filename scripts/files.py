r"""
Contains information about the Axograph files being analysed, and
is used to help load the files into the appropriate data structures
with the correct experimental settings.
"""

#
# DATA FILES
#

CONTROLS = [
    "66_Data 015.axgd"
]

FILES = [
    # EX44 - Costim4 - Cell 4
    ["44_Data 033.axgd", 8, 1650, 1750, 135, 150, True, 4404, 0],  #0
    ["44_Data 035.axgd", 8, 1700, 1750, 125, 150, True, 4404, 0],  #1

    # EX44 - Costim4 - Cell 5
    ["44_Data 044.axgd", 11, 1800, 1900, 200, 210, True, 4405, 0],  #2
    ["44_Data 045.axgd", 11, 1800, 1900, 190, 210, True, 4405, 0],  #3
    ["44_Data 046.axgd", 11, 1800, 1900, 180, 210, True, 4405, 0],  #4
    ["44_Data 047.axgd", 11, 1700, 1900, 180, 210, True, 4405, 0],  #5
    ["44_Data 048.axgd", 11, 1700, 1900, 180, 210, False, 4405, 0],  #6
    ["44_Data 049.axgd", 11, 1700, 1900, 190, 210, False, 4405, 0],  #7
    ["44_Data 050.axgd", 11, 1700, 1900, 200, 210, False, 4405, 0],  #8
    ["44_Data 051.axgd", 11, 1750, 1900, 200, 210, True, 4405, 0],  #9
    ["44_Data 052.axgd", 11, 1700, 1900, 210, 210, False, 4405, 0],  #10
    ["44_Data 053.axgd", 11, 1700, 1900, 220, 210, True, 4405, 0],  #11
    ["44_Data 054.axgd", 11, 1650, 1900, 220, 210, False, 4405, 0],  #12
    ["44_Data 055.axgd", 11, 1650, 1900, 230, 210, True, 4405, 0],  #13
    ["44_Data 056.axgd", 11, 1800, 1900, 190, 210, True, 4405, 0],  #14

    # EX45 - Costim5 - Cell 4
    ["45_Data 062.axgd", 13, 2150, 2200, 220, 230, True, 4504, 1],  #15
    ["45_Data 063.axgd", 13, 2100, 2200, 200, 230, True, 4504, 1],  #16
    ["45_Data 065.axgd", 13, 2000, 2200, 190, 230, True, 4504, 1],  #17
    ["45_Data 066.axgd", 13, 2000, 2200, 180, 230, True, 4504, 1],  #18
    ["45_Data 067.axgd", 13, 2000, 2200, 170, 230, True, 4504, 1],  #19
    ["45_Data 068.axgd", 13, 2000, 2200, 170, 230, True, 4504, 2],  #20
    ["45_Data 069.axgd", 13, 2000, 2200, 160, 230, True, 4504, 1],  #21
    ["45_Data 070.axgd", 13, 2000, 2200, 150, 230, True, 4504, 1],  #22
    ["45_Data 071.axgd", 13, 2000, 2200, 140, 230, True, 4504, 1],  #23
    ["45_Data 072.axgd", 13, 2000, 2200, 130, 230, True, 4504, 1],  #24
    ["45_Data 073.axgd", 13, 2000, 2200, 110, 230, True, 4504, 1],  #25
    ["45_Data 074.axgd", 13, 1900, 2200, 110, 230, True, 4504, 1],  #26
    ["45_Data 075.axgd", 13, 0, 2200, 110, 230, False, 4504, 1],  #27
    ["45_Data 076.axgd", 13, 1800, 2200, 110, 230, False, 4504, 1],  #28
    ["45_Data 077.axgd", 13, 1800, 2200, 130, 230, True, 4504, 1],  #29
    ["45_Data 078.axgd", 13, 1800, 2200, 120, 230, True, 4504, 1],  #30
    ["45_Data 079.axgd", 13, 1850, 2200, 120, 230, True, 4504, 1],  #31
    ["45_Data 080.axgd", 13, 1750, 2200, 130, 230, False, 4504, 1],  #32
    ["45_Data 081.axgd", 13, 1750, 2200, 150, 230, True, 4504, 1],  #33

    # EX48 - Costim6 - Cell 1
    ["48_Data 008.axgd", 7, 1775, 1800, 150, 190, True, 4801, 4],  #34 - Missing optical column
    ["48_Data 009.axgd", 7, 1750, 1800, 150, 190, True, 4801, 4],  #35 - Missing optical column
    ["48_Data 010.axgd", 7, 1750, 1800, 130, 190, True, 4801, 4],  #36 - Missing optical column
    # ["48_Data 011.axgd", 7, 1700, 1800, 130, 190, True, 4801, 4],  #37 - Missing optical column - dodgy cell?
    # ["48_Data 012.axgd", 7, 1680, 1800, 130, 190, False, 4801, 4],  #38 - Missing optical column - dodgy cell?
    # ["48_Data 013.axgd", 7, 1680, 1800, 140, 190, True, 4801, 4],  #39 - Missing optical column - dodgy cell?
    # ["48_Data 014.axgd", 7, 1680, 1800, 150, 190, True, 4801, 4],  #40 - Missing optical column - dodgy cell?
    # ["48_Data 015.axgd", 7, 1680, 1800, 160, 190, True, 4801, 4],  #41 - Missing optical column - dodgy cell?
    # ["48_Data 016.axgd", 7, 1660, 1800, 160, 190, True, 4801, 4],  #42 - Missing optical column - dodgy cell?
    ["48_Data 018.axgd", 7, 1750, 1800, 100, 190, True, 4801, 4],  #43 - Missing optical column
    ["48_Data 019.axgd", 7, 1750, 1800, 90, 190, True, 4801, 4],  #44 - Missing optical column
    ["48_Data 020.axgd", 7, 1750, 1800, 80, 190, True, 4801, 4],  #45 - Missing optical column
    ["48_Data 021.axgd", 7, 1750, 1800, 70, 190, True, 4801, 4],  #46 - Missing optical column
    ["48_Data 023.axgd", 7, 1750, 1800, 60, 190, True, 4801, 4],  #47 - Missing optical column
    ["48_Data 024.axgd", 7, 1750, 1800, 50, 190, True, 4801, 4],  #48 - Missing optical column
    ["48_Data 025.axgd", 7, 1730, 1800, 50, 190, True, 4801, 4],  #49 - Missing optical column
    ["48_Data 026.axgd", 7, 1710, 1800, 50, 190, True, 4801, 4],  #50 - Missing optical column
    ["48_Data 027.axgd", 7, 1710, 1800, 60, 190, True, 4801, 4],  #51 - Missing optical column
    # ["48_Data 028.axgd", 7, 1710, 1800, 80, 190, True, 4801, 4],  #52 - Missing optical column - dodgy cell?

    # EX48 - Costim6 - Cell 3
    ["48_Data 038.axgd", 11, 1900, 2000, 200, 270, True, 4803, 4],  #53 - Missing optical column
    ["48_Data 039.axgd", 11, 1850, 2000, 200, 270, True, 4803, 4],  #54 - Missing optical column
    ["48_Data 040.axgd", 11, 1890, 2000, 200, 270, True, 4803, 4],  #55 - Missing optical column
    ["48_Data 041.axgd", 11, 1700, 2000, 200, 270, False, 4803, 4], #56 - Missing optical column
    ["48_Data 042.axgd", 11, 1750, 2000, 200, 270, True, 4803, 4],  #57 - Missing optical column
    ["48_Data 043.axgd", 11, 1750, 2000, 180, 270, True, 4803, 4],  #58 - Missing optical column
    ["48_Data 044.axgd", 11, 1700, 2000, 180, 270, False, 4803, 4], #59 - Missing optical column
    ["48_Data 045.axgd", 11, 1700, 2000, 220, 270, True, 4803, 4],  #60 - Missing optical column

    # EX48 - Costim6 - Cell 6
    ["48_Data 076.axgd", 6, 1700, 1740, 100, 190, True, 4806, 4],  #61 - Missing optical column
    # ["48_Data 077.axgd", 6, 1650, 1740, 100, 190, False, 4806, 4], #62 - Missing optical column - dodgy cell?
    # ["48_Data 078.axgd", 6, 1675, 1740, 100, 190, True, 4806, 4],  #63 - Missing optical column - dodgy cell?
    # ["48_Data 079.axgd", 6, 1685, 1740, 100, 190, True, 4806, 4],  #64 - Missing optical column - dodgy cell?
    ["48_Data 080.axgd", 6, 1685, 1740, 110, 190, True, 4806, 4],  #65 - Missing optical column
    # ["48_Data 085.axgd", 6, 1660, 1740, 110, 190, False, 4806, 3], #66 - dodgy cell?

    # EX49 - Costim7 - Cell 4
    ["49_Data 039.axgd", 8, 2200, 2450, 90, 130, True, 4904, 3],  #67
    ["49_Data 040.axgd", 8, 2150, 2450, 90, 130, True, 4904, 3],  #68
    ["49_Data 041.axgd", 8, 2100, 2450, 90, 130, True, 4904, 3],  #69
    ["49_Data 042.axgd", 8, 2050, 2450, 90, 130, True, 4904, 3],  #70

    # EX50 - Costim8 - Cell 6
    ["50_Data 040.axgd", 8, 1650, 1675, 96, 160, True, 5006, 3],  #71
    ["50_Data 041.axgd", 8, 1650, 1675, 80, 160, True, 5006, 3],  #72
    ["50_Data 042.axgd", 8, 1650, 1675, 64, 160, True, 5006, 3],  #73
    ["50_Data 043.axgd", 8, 1650, 1675, 48, 160, True, 5006, 3],  #74
    ["50_Data 044.axgd", 8, 1650, 1675, 32, 160, True, 5006, 3],  #75
    ["50_Data 045.axgd", 8, 1650, 1675, 16, 160, True, 5006, 3],  #76

    # EX52 - Costim 10 - Cell 5
    ["52_Data 078.axgd", 13, 1720, 1810, 55, 110, True, 5205, 3],
    ["52_Data 079.axgd", 13, 1720, 1810, 66, 110, True, 5205, 3],
    ["52_Data 080.axgd", 13, 1680, 1810, 66, 110, True, 5205, 3],
    ["52_Data 081.axgd", 13, 1680, 1810, 88, 110, True, 5205, 3],
    ["52_Data 082.axgd", 13, 1680, 1810, 77, 110, True, 5205, 3],

    # EX52 - Costim 10 - Cell 7, cell threshold very close to laser threshold, maybe remove?
    ["52_Data 109.axgd", 9, 1660, 1675, 144, 160, True, 5207, 3],
    ["52_Data 110.axgd", 9, 1660, 1675, 112, 160, True, 5207, 3],
    ["52_Data 111.axgd", 9, 0, 1675, 112, 160, True, 5207, 3],
    ["52_Data 112.axgd", 9, 1660, 1675, 48, 160, True, 5207, 3],
    ["52_Data 113.axgd", 9, 1660, 1675, 64, 160, True, 5207, 3],
    ["52_Data 114.axgd", 9, 1660, 1675, 80, 160, True, 5207, 3],
    ["52_Data 115.axgd", 9, 1660, 1675, 96, 160, True, 5207, 3],

    # EX 56 - Costim 14 - Cell 4
    ["56_Data 037.axgd", 8, 1756, 1845, 60, 120, True, 5504, 3],
    ["56_Data 038.axgd", 8, 1756, 1845, 72, 120, True, 5504, 3],
    ["56_Data 039.axgd", 8, 1756, 1845, 84, 120, True, 5504, 3],
    ["56_Data 040.axgd", 8, 1756, 1845, 96, 120, True, 5504, 3],
    ["56_Data 041.axgd", 8, 1756, 1845, 108, 120, True, 5504, 3],
    ["56_Data 042.axgd", 8, 1769, 1845, 96, 120, True, 5504, 3],
    ["56_Data 044.axgd", 8, 1769, 1845, 84, 120, True, 5504, 3],
    ["56_Data 045.axgd", 8, 1782, 1845, 60, 120, True, 5504, 3],
    ["56_Data 046.axgd", 8, 1782, 1845, 72, 120, True, 5504, 3],
    ["56_Data 047.axgd", 8, 1782, 1845, 84, 120, True, 5504, 3],
    ["56_Data 048.axgd", 8, 1782, 1845, 96, 120, True, 5504, 3],
    ["56_Data 049.axgd", 8, 1782, 1845, 108, 120, True, 5504, 3],

    # EX 67 - Costim 18 - Cell 3
    ["67_Data 030.axgd", 9, 1943, 2468, 171, 240, True, 6703, 3],
    ["67_Data 031.axgd", 9, 1943, 2468, 151, 240, True, 6703, 3],
    ["67_Data 032.axgd", 9, 1868, 2468, 171, 240, True, 6703, 3],
    ["67_Data 033.axgd", 9, 2393, 2468, 57, 240, True, 6703, 3],
    ["67_Data 034.axgd", 9, 2393, 2468, 76, 240, True, 6703, 3],
    ["67_Data 035.axgd", 9, 1793, 2468, 171, 240, True, 6703, 3],
    ["67_Data 036.axgd", 9, 2243, 2468, 171, 240, True, 6703, 5],
    ["67_Data 037.axgd", 9, 2318, 2468, 171, 240, True, 6703, 5],
#     ["67_Data 038.axgd", 9, 2393, 2468, 171, 240, True, 6703, 5], # no results, ignore

    # EX 67 - Costim 18 - Cell 8
    ["67_Data 092.axgd", 10, 1755, 1840, 96, 120, True, 6708, 6],
    ["67_Data 093.axgd", 10, 1755, 1840, 108, 120, True, 6708, 6],
    ["67_Data 094.axgd", 10, 1742, 1840, 108, 120, True, 6708, 6],
    ["67_Data 095.axgd", 10, 1828, 1840, 108, 120, True, 6708, 6],

    # EX 67 - Costim 18 - Cell 9
    ["67_Data 108.axgd", 10, 1756, 1765, 76, 190, True, 6709, 6],
    ["67_Data 109.axgd", 10, 1756, 1765, 95, 190, True, 6709, 6],
    ["67_Data 110.axgd", 10, 1760, 1765, 95, 190, True, 6709, 6],
]

FAKE_COSTIM_FILES = [
    ["50_Data 012.axgd", 5003],
    ["50_Data 053.axgd", 5006],
    ["50_Data 054.axgd", 5006],
    ["52_Data 068.axgd", 5205],
    ["52_Data 069.axgd", 5205],
    ["52_Data 070.axgd", 5205],
    ["52_Data 071.axgd", 5205],
    ["52_Data 104.axgd", 5207],
    ["52_Data 105.axgd", 5207],
    ["52_Data 106.axgd", 5207],
    ["52_Data 107.axgd", 5207],
    ["52_Data 108.axgd", 5207],
    ["52_Data 130.axgd", 5208],
    ["52_Data 131.axgd", 5208],
    ["52_Data 132.axgd", 5208],
    ["52_Data 133.axgd", 5208],
    ["54_Data 058.axgd", 5404],
    ["54_Data 059.axgd", 5404],
    ["54_Data 060.axgd", 5404],
    ["54_Data 061.axgd", 5404],
    ["54_Data 097.axgd", 5406],
    ["54_Data 098.axgd", 5406],
]

# Files from finding the electrical threshold - used for characterising sub- / suprathreshold time constants
ELEC_ONLY_FILES = [
    # EX44 - Costim4 - Cell 4
    ["44_Data 027.axgd", 8, 1750, 150, 4404],  #0

    # EX44 - Costim4 - Cell 5
    ["44_Data 039.axgd", 11, 1900, 210, 4405],  #0
    ["44_Data 040.axgd", 11, 1900, 210, 4405],  #0

    # EX45 - Costim5 - Cell 1
    ["45_Data 005.axgd", 8, 1750, 150, 4501],  #0
    ["45_Data 011.axgd", 8, 1750, 150, 4501],  #new
    ["45_Data 026.axgd", 8, 1750, 150, 4501],  #0

    # EX45 - Costim5 - Cell 4
    ["45_Data 057.axgd", 13, 2200, 230, 4504],  #15
    ["45_Data 064.axgd", 13, 2200, 230, 4504],  #new

    # EX48 - Costim6 - Cell 1
    ["48_Data 002.axgd", 7, 1800, 190, 4801],  #new
    ["48_Data 017.axgd", 7, 1800, 190, 4801],  #new

    # EX48 - Costim6 - Cell 3
    ["48_Data 031.axgd", 11, 2000, 270, 4803],  #new
    ["48_Data 037.axgd", 11, 2000, 270, 4803],  #new

    # EX48 - Costim6 - Cell 4
    ["48_Data 049.axgd", 7, 4000, 190, 4804],  #new
    ["48_Data 050.axgd", 7, 4000, 190, 4804],  #new

    # EX48 - Costim6 - Cell 5
    ["48_Data 062.axgd", 11, 4000, 250, 4805],  #new

    # EX48 - Costim6 - Cell 6
    ["48_Data 068.axgd", 6, 1740, 190, 4806],  #new

    # Ex50 - Costim8 - Cell 3
    ["50_Data 001.axgd", 8, 1675, 230, 5003],  #71
    ["50_Data 021.axgd", 8, 1675, 190, 5003],  #71
    ["50_Data 035.axgd", 8, 1675, 190, 5006],  #71
]

# Files from finding the optical threshold - used for characterising sub- / suprathreshold time constants
OPT_ONLY_FILES = [
    ["44_Data 015.axgd", 4403],
    ["44_Data 016.axgd", 4403],
    ["44_Data 017.axgd", 4403],
    ["44_Data 018.axgd", 4403],
    ["44_Data 020.axgd", 4403],
    ["44_Data 021.axgd", 4403],
    ["44_Data 028.axgd", 4404],
    ["44_Data 029.axgd", 4404],
    ["44_Data 030.axgd", 4404],
    ["44_Data 031.axgd", 4404],
    ["44_Data 032.axgd", 4404],
    ["44_Data 041.axgd", 4405],
    ["44_Data 042.axgd", 4405],
    ["44_Data 043.axgd", 4405],

    ["45_Data 033.axgd", 4502],
    ["45_Data 034.axgd", 4502],
    ["45_Data 035.axgd", 4502],
    ["45_Data 036.axgd", 4502],
    ["45_Data 037.axgd", 4502],
    ["45_Data 058.axgd", 4504],
    ["45_Data 059.axgd", 4504],
    ["45_Data 060.axgd", 4504],
    ["45_Data 061.axgd", 4504],

    ["48_Data 003.axgd", 4801],
    ["48_Data 004.axgd", 4801],
    ["48_Data 005.axgd", 4801],
    ["48_Data 006.axgd", 4801],
    ["48_Data 007.axgd", 4801],
    ["48_Data 033.axgd", 4803],
    ["48_Data 034.axgd", 4803],
    ["48_Data 035.axgd", 4803],
    ["48_Data 036.axgd", 4803],
    ["48_Data 051.axgd", 4804],
    ["48_Data 052.axgd", 4804],
    ["48_Data 053.axgd", 4804],
    ["48_Data 054.axgd", 4804],
    ["48_Data 055.axgd", 4804],
    ["48_Data 056.axgd", 4804],
    ["48_Data 057.axgd", 4804],
    ["48_Data 063.axgd", 4805],
    ["48_Data 064.axgd", 4805],
    ["48_Data 065.axgd", 4805],
    ["48_Data 069.axgd", 4806],
    ["48_Data 070.axgd", 4806],
    ["48_Data 071.axgd", 4806],
    ["48_Data 072.axgd", 4806],
    ["48_Data 073.axgd", 4806],
    ["48_Data 074.axgd", 4806],
    ["48_Data 075.axgd", 4806],

    ["49_Data 009.axgd", 4903],
    ["49_Data 010.axgd", 4903],
    ["49_Data 011.axgd", 4903],
    ["49_Data 019.axgd", 4904],
    ["49_Data 020.axgd", 4904],
    ["49_Data 021.axgd", 4904],
    ["49_Data 022.axgd", 4904],
    ["49_Data 023.axgd", 4904],
    ["49_Data 024.axgd", 4904],
    ["49_Data 025.axgd", 4904],
    ["49_Data 026.axgd", 4904],
    ["49_Data 027.axgd", 4904],
    ["49_Data 035.axgd", 4904],
    ["49_Data 036.axgd", 4904],
    ["49_Data 037.axgd", 4904],
    ["49_Data 038.axgd", 4904],

    ["50_Data 002.axgd", 5003],
    ["50_Data 003.axgd", 5003],
    ["50_Data 004.axgd", 5003],
    ["50_Data 005.axgd", 5003],
    ["50_Data 006.axgd", 5003],
    ["50_Data 008.axgd", 5003],
    ["50_Data 038.axgd", 5006],
    ["50_Data 039.axgd", 5006],
    ["50_Data 040.axgd", 5006],
    ["50_Data 041.axgd", 5006],
    ["50_Data 042.axgd", 5006],
    ["50_Data 043.axgd", 5006],
    ["50_Data 044.axgd", 5006],
    ["50_Data 057.axgd", 5007],
    ["50_Data 058.axgd", 5007],

    ["52_Data 008.axgd", 5202],
    ["52_Data 012.axgd", 5202],
    ["52_Data 018.axgd", 5203],
    ["52_Data 020.axgd", 5203],
    ["52_Data 021.axgd", 5203],
    ["52_Data 022.axgd", 5203],
    ["52_Data 023.axgd", 5203],
    ["52_Data 025.axgd", 5203],
    ["52_Data 046.axgd", 5204],
    ["52_Data 053.axgd", 5205],
    ["52_Data 089.axgd", 5207],
    ["52_Data 090.axgd", 5207],
    ["52_Data 091.axgd", 5207],
    ["52_Data 092.axgd", 5207],
    ["52_Data 117.axgd", 5208],
    ["52_Data 118.axgd", 5208],
    ["52_Data 120.axgd", 5208]
]

# cells used for costim single pulse protocol
CELLS = [
    [8, 1750, 150, 4404],
    [11, 1900, 210, 4405],
    [13, 2200, 230, 4504],
    [7, 1800, 190, 4801],
    [11, 2000, 270, 4803],
    [6, 1740, 190, 4806],
    [8, 2450, 130, 4904],
    [8, 1675, 160, 5006],
    [13, 1810, 110, 5205],
    [9, 1675, 160, 5207],
    [8, 1845, 120, 5504],
    [9, 2468, 240, 6703],
    [10, 1840, 120, 6708],
    [10, 1765, 190, 6709]
]
