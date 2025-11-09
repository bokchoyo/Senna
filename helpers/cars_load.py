import gspread
import pandas as pd
from config import Config
import json
from oauth2client.service_account import ServiceAccountCredentials

config = Config()


def authorize_spreadsheet(credentials):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(credentials)
    return client


def load_spreadsheet(client, spreadsheet_url, worksheet_name):
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df


def sort_specific_levels(d, level=0):
    """
    Sorts only the make, model, trim, and year levels in alphabetical order.
    Keeps the ordering of keys under the 'year' level.
    """
    if isinstance(d, dict):
        if level < 4:
            return {k: sort_specific_levels(v, level + 1) for k, v in sorted(d.items())}
        else:
            return {k: v for k, v in d.items()}
    return d


def merge_json_data(existing_data, new_data):
    """
    Merge new_data into existing_data, preserving the 'url' key in existing_data.
    """
    if isinstance(new_data, dict) and isinstance(existing_data, dict):
        for key, value in new_data.items():
            if key in existing_data:
                existing_data[key] = merge_json_data(existing_data[key], value)
            else:
                existing_data[key] = value
        return existing_data
    return new_data


def spreadsheet_to_json(df, json_path):
    data_dict = {}

    # Build the nested dictionary structure from the DataFrame
    for _, row in df.iterrows():
        make = row['make']
        model = row['model']
        trim = row['trim']
        year = row['year']

        data_dict.setdefault(make, {}).setdefault(model, {}).setdefault(trim, {})[year] = row.to_dict()

    # Sort only the make, model, trim, and year keys
    sorted_data_dict = sort_specific_levels(data_dict)

    # Overwrite the JSON file with sorted data
    with open(json_path, 'w') as json_file:
        json.dump(sorted_data_dict, json_file, indent=4)

    print(f"Data has been cleared and written to {json_path} as JSON.")


def main():
    credentials = config.get_google_api_credentials()
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xji7Igiyazu8N1LDneVwm0MwtSF6dVxi5_uHevSDZQg'
    worksheet_name = 'Cars'
    json_path = r'C:\Users\bokch\PyCharm\W1\data\cars.json'

    client = authorize_spreadsheet(credentials)
    df = load_spreadsheet(client, spreadsheet_url, worksheet_name)

    spreadsheet_to_json(df, json_path)


if __name__ == "__main__":
    main()
