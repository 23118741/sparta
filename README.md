# Sparta Automation Project

This project automates the processing of participant registrations using Google Sheets and Email. It processes a main spreadsheet, adds people to a waiting list based on their age category if applicable, sends relevant emails, and updates the spreadsheet to reflect that actions have been taken (e.g., updating the `mail1_verstuurd` and `wachtlijst` columns).

## Prerequisites

- **Python 3.7+**
- **Google Cloud Console Project** with the **Google Sheets API** and **Google Drive API** enabled.
- A **Service Account** with access to the Google Sheet (share the sheet with the service account email).

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/23118741/sparta.git
   cd sparta
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   The project requires `gspread`, `google-auth`, and `python-dotenv`. Install them via pip:
   ```bash
   pip install gspread google-auth python-dotenv
   ```
   *(Alternatively, if a `requirements.txt` is added later, run `pip install -r requirements.txt`)*

## Configuration

1. **Google Sheets Credentials:**
   - Download your Service Account JSON key from Google Cloud Console.
   - Rename it to `credentials.json`.
   - Place `credentials.json` in the root directory of this project.

2. **Environment Variables:**
   - Create a file named `.env` in the root directory.
   - Add the following variables:
     ```env
     GMAIL_USER=your_email@gmail.com
     GMAIL_PASSWORD=your_app_password
     SPREADSHEET_ID=your_google_spreadsheet_id
     ```
   *(Note: For Gmail, it's highly recommended to use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2-Step Verification is enabled).*

## Usage

To run the automation script, execute the main file:

```bash
python main.py
```

### What the script does:
1. Connects to the configured Google Spreadsheet.
2. Initializes the headers on the waiting list ("wachtlijst") if it's empty.
3. Iterates over all rows (starting from row 2).
4. **Waiting List Logic:** Checks if a person needs to be on the waiting list. If so, and their age is valid, they are added to the waiting list sheet along with their calculated position, and the main sheet is marked as "toegevoegd" (added).
5. **Email Logic:** Determines if a specific email should be sent using `mail_assingment.py`. If successfully sent, it updates the `mail1_verstuurd` column in the sheet to "ja" (yes).

## Project Structure

- `main.py`: The entry point that orchestrates the flow.
- `sheets_config.py`: Handles Google Sheets authentication and configuration settings.
- `sheet_updater.py`: Contains methods for reading/writing data from/to the Google Sheet.
- `email_sender.py`: Handles SMTP connections and sending emails.
- `mail_assingment.py`: Contains the logic to determine which email to send based on row data.
