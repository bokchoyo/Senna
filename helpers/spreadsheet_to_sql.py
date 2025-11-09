import gspread
import sqlite3
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def authorize_spreadsheet(credentials):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
    client = gspread.authorize(credentials)
    return client


def load_spreadsheet(client, spreadsheet_url, worksheet_name):
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df


def spreadsheet_to_sql(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data has been inserted into the {table_name} table in {db_name} database.")


def main():
    credentials = r'C:\Users\bokch\PyCharm\W1\data\credentials.json'
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xji7Igiyazu8N1LDneVwm0MwtSF6dVxi5_uHevSDZQg'
    worksheet_name = 'Cars'
    db_name = r'C:\Users\bokch\PyCharm\W1\data\car_database.users'
    table_name = 'car_database'

    client = authorize_spreadsheet(credentials)
    df = load_spreadsheet(client, spreadsheet_url, worksheet_name)

    spreadsheet_to_sql(df, db_name, table_name)


if __name__ == "__main__":
    main()
