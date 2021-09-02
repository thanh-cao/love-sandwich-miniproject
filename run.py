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
    '''
    Get sales figure input from the user
    '''
    while True:
        print('Please enter sales data from the last market day')
        print('Data should be six numbers seperated by comma')
        print('Example: 40, 20, 55, 65, 11, 45\n')

        data_str = input('Please enter sales data from the last market day: ')
        sales_data = data_str.split(',')
        validate_data(sales_data)

        if validate_data(sales_data):
            print('Data is valid')
            break
    
    return sales_data

def validate_data(values):
    '''
    Inside the try, converts all string values into integers. Raises ValurError if strings cannot be converted into int, or if there aren't exactly 6 values
    '''
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')
        return False
    
    return True

# def update_sales_worksheet(data):
#     '''
#     Update sales worksheet, add new row with the list data provided
#     '''
#     print('Updating sales worksheet...\n')
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print('Sales worksheet updated successfully.\n')

def calculate_surplus_data(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    '''
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

# def update_surplus_worksheet(data):
#     '''
#     Update surplus worksheet, add new row with the list data provided
#     '''
#     print('Updating surplus worksheet...\n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print('Surplus worksheet updated successfully.\n')

def update_data_to_worksheet(data, worksheet):
    '''
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with data provided
    '''
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')

def main_function():
    '''
    Run all program functions
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_data_to_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_data_to_worksheet(new_surplus_data, 'surplus')

print('Welcome to Love Sandwiches Data Automation')
main_function()