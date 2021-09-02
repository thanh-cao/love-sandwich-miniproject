import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDENTIALS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDENTIALS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDENTIALS)
SHEET = GSPREAD_CLIENT.open('love-sandwiches')

def get_sales_data():
    '''Get sales figure input from the user'''
    print('Please enter sales data from the last market day')
    print('Data should be six numbers seperated by comma')
    print('Example: 40, 20, 55, 65, 11, 45')

    data_str = input('Please enter sales data from the last market day: ')
    sales_data = data_str.split(',')
    validate_data(sales_data)

def validate_data(values):
    '''Inside the try, converts all string values into integers. Raises ValurError if strings cannot be converted into int, or if there aren't exactly 6 values'''
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')


get_sales_data()