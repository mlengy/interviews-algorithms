# OO
# OO
_CASE_1 = [
    "OO",
    "OO"
]
CASE_1 = (2, 2, [])

# OX
# OO
_CASE_2 = [
    "OX",
    "OO"
]
CASE_2 = (2, 2, [(1, 2)])

# OX
# XO
_CASE_3 = [
    "OX",
    "XO"
]
CASE_3 = (2, 2, [(1, 2), (2, 1)])

# OO
# OX
_CASE_4 = [
    "OO",
    "OX"
]
CASE_4 = (2, 2, [(2, 2)])

# OXO
# OOX
# OOO
_CASE_5 = [
    "OXO",
    "OOX",
    "OOO"
]
CASE_5 = (3, 3, [(1, 2), (2, 3)])

# OOOX
# XXOX
# OXOX
# OXOX
# OXOX
# OOOO
_CASE_6 = [
    "OOOX",
    "XXOX",
    "OXOX",
    "OXOX",
    "OXOX",
    "OOOO"
]
CASE_6 = (6, 4, [(1, 4), (2, 1), (2, 2), (2, 4), (3, 2), (3, 4), (4, 2), (4, 4), (5, 2), (5, 4)])

CASE = [
    CASE_1,
    CASE_2,
    CASE_3,
    CASE_4,
    CASE_5,
    CASE_6
]

CASE_EXPECTED = [
    2,
    1,
    0,
    0,
    2,
    1
]
