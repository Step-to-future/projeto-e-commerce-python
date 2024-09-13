import re
from Crud_manipulation import CrudManipulation

class Buy:
    def __init__(self, buy_code: int, buy_date: str, product_code: int, buying_amount: int):
        self.buy_code = buy_code
        self.buy_date = buy_date
        self.product_code = product_code
        self.buying_amount = buying_amount


def validate_date(buy_date: str) -> bool:
    # REGEX to validate date format as dd/mm/yyyy
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
    return re.match(pattern, buy_date) is not None

def new_request():
    # Example implementation of a new request
    # (You need to add implementation here based on your needs)
    pass