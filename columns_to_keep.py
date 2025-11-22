COLUMNS_GL = {
    "date": "თარიღი",
    "acc_debit": "სადებ.ანგარიში",
    "name_debit": "დასახელება (დებ.)",
    "acc_credit": "საკრედ.ანგარიში",
    "description": "დანიშნულება",
    "name_credit": "დასახელება (კრედ.)",
    "amount": "თანხა",
    "basis": "საფუძველი",
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