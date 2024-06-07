# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set up access to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("X_Config/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet with ID
spreadsheet_id = "1Getoqe8Gsleuo9Lu96J8FCXbzUxPHiMQoL5YbArY2_U"  # Replace with your Google Sheets ID
try:
    sheet = client.open_by_key(spreadsheet_id).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    logging.error("Google Sheets doesn't exist or the service account doesn't have access permissions. Check your ID and access rights again.")
    exit(1)

# Set up column headers if they don't already exist
def initialize_sheet():
    headers = ["ID Checking", "UserName", "Number of attendance times", "Detection time", "Address to save the image"]
    existing_headers = sheet.row_values(1)
    if not existing_headers:
        sheet.append_row(headers)
    elif existing_headers != headers:
        logging.warning("Existing column headings do not match expected headings. Please check Google Sheets.")

# Use clipboard to reduce reads from Google Sheets
cached_user_records = None
pending_updates = []

def log_to_google_sheets(user_id, name, image_url):
    global cached_user_records, pending_updates

    # Check and refresh the cache if necessary
    if cached_user_records is None:
        cached_user_records = sheet.get_all_records()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Search users by ID
    for index, record in enumerate(cached_user_records):
        if record.get("ID Checking") == user_id:
            # The user already exists, updates attendance and detection time
            new_count = record["Number of attendance times"] + 1
            new_timestamp = f"{record['Detection time']}, {timestamp}"
            pending_updates.append({
                "index": index + 2,  # Row number in the sheet (1-based index)
                "values": [user_id, name, new_count, new_timestamp, image_url]
            })
            logging.debug(f"Updating existing user: {user_id}, {name}, {new_count}, {new_timestamp}, {image_url}")

            # Update cache
            cached_user_records[index]["Number of attendance times"] = new_count
            cached_user_records[index]["Detection time"] = new_timestamp
            cached_user_records[index]["Address to save the image"] = image_url
            return

    # User does not exist yet, add new one
    new_row = [user_id, name, 1, timestamp, image_url]
    cached_user_records.append({
        "ID Checking": user_id,
        "UserName": name,
        "Number of attendance times": 1,
        "Detection time": timestamp,
        "Address to save the image": image_url
    })
    pending_updates.append({
        "index": 2,  # Insert at row 2
        "values": new_row
    })
    logging.debug(f"Adding new user: {user_id}, {name}, 1, {timestamp}, {image_url}")

def batch_update_google_sheets():
    global pending_updates
    if pending_updates:
        logging.debug(f"Updating Google Sheets with: {pending_updates}")
        for update in pending_updates:
            try:
                sheet.insert_row(update["values"], update["index"])
            except gspread.exceptions.APIError as e:
                logging.error(f"APIError during sheet update: {e}")
        pending_updates = []

# Calling function to update periodically (e.g. every minute)
def periodic_batch_update(interval=3):
    while True:
        try:
            logging.debug("Running batch update")
            batch_update_google_sheets()
        except Exception as e:
            logging.error(f"Error during batch update: {e}")
        time.sleep(interval)

# Start a periodic update stream
initialize_sheet()
update_thread = threading.Thread(target=periodic_batch_update, args=(3,))
update_thread.daemon = True
update_thread.start()
logging.debug("Update thread started")
