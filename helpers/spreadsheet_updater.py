import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from helpers.config import Config

# Paths and credentials
json_path = r'C:\Users\bokch\PyCharm\W1\data\cars.json'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xji7Igiyazu8N1LDneVwm0MwtSF6dVxi5_uHevSDZQg'
worksheet_name = 'Cars'
config = Config()

def convert_values_to_string(data):
    """
    Recursively convert all values in a nested dictionary or list to strings.
    """
    if isinstance(data, dict):
        return {key: convert_values_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_values_to_string(item) for item in data]
    else:
        return str(data)

# Google Sheets authorization
def authorize_spreadsheet(credentials):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(credentials)
    return client

# Update the Google Spreadsheet
def update_google_sheet(client, json_data):
    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(worksheet_name)

    # Convert all JSON values to strings
    json_data = convert_values_to_string(json_data)

    # Convert JSON data to a flat list for spreadsheet compatibility
    rows_to_update = []
    for make, models in json_data.items():
        for model, trims in models.items():
            for trim, years in trims.items():
                for year, details in years.items():
                    row = {
                        'make': make,
                        'model': model,
                        'trim': trim,
                        'year': year,  # Already converted to string
                        'url': details.get('url', '')  # Add 'url' field
                    }
                    rows_to_update.append(row)

    # Convert to DataFrame
    new_data = pd.DataFrame(rows_to_update)

    # Fetch existing data including formulas
    existing_data_values = worksheet.get_all_values(value_render_option='FORMULA')
    existing_headers = existing_data_values[0]
    existing_data = pd.DataFrame(existing_data_values[1:], columns=existing_headers)

    # Merge the new data with the existing data
    key_columns = ['make', 'model', 'trim', 'year']
    merged_data = pd.merge(
        existing_data,
        new_data,
        on=key_columns,
        how='outer',  # Keeps all rows from both DataFrames
        suffixes=('', '_new')
    )

    # Update the 'url' column with new values where applicable
    if 'url_new' in merged_data.columns:
        merged_data['url'] = merged_data['url_new'].combine_first(merged_data['url'])
        merged_data.drop(columns=['url_new'], inplace=True)

    # Preserve formulas in non-updated columns
    for col in existing_headers:
        if col not in key_columns + ['url']:  # Skip columns with new data
            merged_data[col] = existing_data[col]

    # Sort by key columns to preserve logical ordering
    merged_data.sort_values(by=key_columns, inplace=True)

    # Write back the merged data
    worksheet.clear()  # Clear existing data
    worksheet.update(
        [merged_data.columns.values.tolist()] + merged_data.values.tolist(),
        value_input_option='USER_ENTERED'
    )

# Main function
def main():
    # Load JSON data
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Authorize and update
    credentials = config.get_google_api_credentials()
    client = authorize_spreadsheet(credentials)
    update_google_sheet(client, json_data)
    print("Google Spreadsheet has been updated successfully.")

if __name__ == "__main__":
    main()
