from datetime import date

from waveapp.models import Loans, Collaterals


def generate_loan_id():
    current_year = str(date.today().year)[2:]
    current_month = str(date.today().month)
    if len(current_month) < 2:
        current_month = '0' + current_month

    id_format = f"STL{current_year}-{current_month}-"
    final_id_format = None
    if Loans.objects.filter(loan_id__contains=id_format).exists():
        latest_loan = Loans.objects.filter(loan_id__contains=id_format).latest()
        latest_id = latest_loan.loan_id[-4:]
        latest_id_int = int(latest_id)
        current_id = latest_id_int + 1
        current_id_str = str(current_id)
        if len(current_id_str) == 3:
            current_id_str = '0' + current_id_str
            final_id_format = id_format + current_id_str
        elif len(current_id_str) == 2:
            current_id_str = '00' + current_id_str
            final_id_format = id_format + current_id_str
        elif len(current_id_str) == 1:
            current_id_str = '000' + current_id_str
            final_id_format = id_format + current_id_str
    else:
        final_id_format = id_format + '0001'
    return final_id_format


def generate_collateral_id():
    current_year = str(date.today().year)[2:]
    current_month = str(date.today().month)
    if len(current_month) < 2:
        current_month = '0' + current_month

    id_format = f"STC{current_year}-{current_month}-"
    final_id_format = None
    if Collaterals.objects.filter(collateral_id__contains=id_format).exists():
        latest_collateral = Collaterals.objects.filter(collateral_id__contains=id_format).latest()
        latest_id = latest_collateral.collateral_id[-4:]
        latest_id_int = int(latest_id)
        current_id = latest_id_int + 1
        current_id_str = str(current_id)
        if len(current_id_str) == 3:
            current_id_str = '0' + current_id_str
            final_id_format = id_format + current_id_str
        elif len(current_id_str) == 2:
            current_id_str = '00' + current_id_str
            final_id_format = id_format + current_id_str
        elif len(current_id_str) == 1:
            current_id_str = '000' + current_id_str
            final_id_format = id_format + current_id_str
    else:
        final_id_format = id_format + '0001'
    return final_id_format
