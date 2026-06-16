import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("LeaveRequests").worksheet("Balances")


def approve_leave(employee, leave_type, days):

    records = sheet.get_all_records()

    for row in records:

        if row["Employee"].lower() == employee.lower():

            available = int(row[leave_type.capitalize()])

            if available >= days:

                new_balance = available - days

                cell = sheet.find(employee)

                if leave_type.lower() == "sick":
                    sheet.update_cell(cell.row, 2, new_balance)

                elif leave_type.lower() == "casual":
                    sheet.update_cell(cell.row, 3, new_balance)

                return True, new_balance

            else:
                return False, available

    return False, 0
