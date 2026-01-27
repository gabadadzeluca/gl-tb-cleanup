COLUMNS_GL_2C = {
    "date": "თარიღი",
    "acc_debit": "სადებ.ანგარიში",
    "name_debit": "დასახელება (დებ.)",
    "acc_credit": "საკრედ.ანგარიში",
    "description": "დანიშნულება",
}

COLUMNS_GL_1C = {
    "date": "პერიოდი",
    "registrator": "რეგისტრატორი",
    
    "acc_debit": "ანგარიში დტ",
    "name_debit": "სუბკონტო 1 დტ",
    "subconto_dr_2":"სუბკონტო 2 დტ",
    "subconto_dr_3":"სუბკონტო 3 დტ",

    "acc_credit": "ანგარიში კტ",
    "name_credit": "სუბკონტო 1 კტ",
    "subconto_cr_2":"სუბკონტო 2 კტ",
    "subconto_cr_3":"სუბკონტო 3 კტ",

    "amount": "თანხა",
    "basis": "შინაარსი",
    "comment": "კომენტარი",
    "description": "დანიშნულება",
}


# Needs to be updated to a RAW TB TODO
# Version 1
COLUMNS_TB = {
    "acc": "ანგარიში +", # Needs to be checked if that is the case for each TB
    "name": "დასახელება",
    "start_dr": "საწყისი/დებეტი",
    "start_cr": "საწყისი/კრედიტი",
    "movement_dr": "ბრუნვა/დებეტი",
    "movement_cr": "ბრუნვა/კრედიტი",
    "end_dr": "საბოლოო/დებეტი",
    "end_cr": "საბოლოო/კრედიტი"
}

# Version 2, where there is no single column for balances
# COLUMNS_TB = {
#     "acc": "ანგარიში",
#     "name": "დასახელება",
#     "start_balance": "საწყისი ნაშთი",
#     "movement_dr": "ბრუნვა/დებეტი",
#     "movement_cr": "ბრუნვა/კრედიტი",
#     "end_balance": "საბოლოო ნაშთი",
# }