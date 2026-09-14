TRUE = "TRUE"
FALSE = "FALSE"
UNKNOWN = "UNKNOWN"

def tri_and(values):
    values = list(values)
    if any(v == FALSE for v in values): return FALSE
    if any(v == UNKNOWN for v in values): return UNKNOWN
    return TRUE

def tri_or(values):
    values = list(values)
    if any(v == TRUE for v in values): return TRUE
    if any(v == UNKNOWN for v in values): return UNKNOWN
    return FALSE

def hard_pass(value):
    return value == TRUE
