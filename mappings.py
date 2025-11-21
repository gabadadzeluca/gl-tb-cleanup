# file to store the CF mappings dr left and cr left

"""NEEDS PPE MAPPINGS"""
# TODO RESOLVE CONFLICTS
MAPPINGS = {
    #Cash Dr:
    "Cash return from paid to suppliers": [("1", "1430"), ("1", "1480"), ("1", "311"), ("1", "3132")],
    "Cash return from taxes paid": [("1", "33")],
    "Dividend Received": [("1", "1810")],
    "Interest received": [("1", "1820"), ("1", "8310"), ("1", "")],
    "Repayment of loans issued": [("1", "2310")],
    "Cash receipts from customers": [("1", "14"), ("1", "1510"), ("1", "3120")],
    "Cash return from paid to employees": [("1", "3130"), ("1", "3131")],
    "Proceeds from borrowings": [("1", "4110"), ("1", "4120")],
    "Exchange rate gain": [("1", "8235"), ("1", "8320"), ("1", "8220"), ("1", "9150"), ("1", "B")],

    #Cash Cr:
    # 3110 is PPE SOMETIMES; Need to add TB Check for PPE additions
    # Same for 1480
    "Cash paid to suppliers": [("1430", "1"), ("1480", "1"), ("311", "1"), ("3190", "1"), ("7190", "1"), ("8420", "1"), ("8440", "1"), ("1", "B600"), ("B600", "1")],
    "Cash paid to employees": [("3130", "1"), ("3131", "1")],
    "Taxes paid": [("33", "1")],
    "Repayment of borrowings": [("4110", "1"), ("4120", "1")],
    "Exchange rate loss": [("8235", "1"), ("8220", "1"), ("9150", "1"), ("B", "1")],
}

# Each rule: (dr_prefix, cr_prefix, mapping)
LOOKUP_MAP = {
    (str(dr).strip(), str(cr).strip()): mapping
    for mapping, pairs in MAPPINGS.items()
    for dr, cr in pairs
    if dr and cr  # skip empty entries
}