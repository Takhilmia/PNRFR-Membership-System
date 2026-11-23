# PNRFR Membership Registration System

A public English-language membership application website built with Python and Streamlit. It generates a PDF styled after the supplied PNRFR paper form and stores application data in Google Sheets, with uploaded photographs, signatures, and PDFs in Google Drive.

## Project files
- `app.py` — Streamlit website, form validation, PDF generation, Google Sheets/Drive integration, admin view.
- `requirements.txt` — Python dependencies.
- `.streamlit/secrets.toml.example` — configuration template.

## 1. Create Google Sheet
1. Create a Google Sheet named `PNRFR Membership Applications`.
2. Copy the spreadsheet ID from its URL (the long value between `/d/` and `/edit`).
3. Create a Google Cloud project and enable **Google Sheets API** and **Google Drive API**.
4. Create a Service Account and download its JSON key.
5. Share the Google Sheet with the service-account email as **Editor**.
6. Create a Google Drive folder for uploaded photos/signatures/PDFs and share it with the service-account email as **Editor**. Copy the folder ID.
7. Keep the service-account JSON private. Never publish it in your repository.

## 2. Configure Streamlit secrets
In Streamlit Community Cloud, open your app's **Settings → Secrets** and paste the following, replacing example values:

```toml
[google]
spreadsheet_id = "YOUR_GOOGLE_SHEET_ID"
drive_folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID"

[gcp_service_account]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_CONTENT
-----END PRIVATE KEY-----"""
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CLIENT_CERTIFICATE_URL"

[admin]
password = "CHANGE_TO_A_LONG_UNIQUE_ADMIN_PASSWORD"
```

Do not share the Secrets page or service-account key. The app makes uploaded Drive files viewable by link so office staff can open them from the Sheet; anyone who obtains those links may be able to view the files. If you need stricter privacy, remove the `drive.permissions().create(...)` call in `app.py` and manage access only through the private Drive folder.

## 3. Deploy online
1. Create a private or public GitHub repository and upload `app.py`, `requirements.txt`, and `.streamlit/secrets.toml.example` (rename the example to `secrets.toml` only for local testing; do NOT commit real credentials).
2. Sign in to Streamlit Community Cloud and connect the repository.
3. Choose `app.py` as the main file.
4. Add the secrets from section 2 in app settings.
5. Deploy. Streamlit will provide a public URL. Anyone with the URL can open the form; no Google sign-in is required to submit.

## 4. Run locally (optional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important notes
- The current PDF is a clean, printable recreation of the supplied form's structure: PNRFR heading/address, membership category, applicant fields, photo/signature area, and fee receipt section. It is not a pixel-perfect scan or exact copy of the original typography.
- The form currently requires a photograph, while signature upload is optional.
- Membership fees are prefilled from the category but can be edited by the applicant. If fees must be fixed, change `st.number_input(...)` to a read-only display and always use `CATEGORIES[category]`.
- This project does not itself verify payment. Add payment verification or an office approval workflow before issuing an official paid-membership receipt.
- The admin password is a basic gate for the admin page. Use a strong password and keep Streamlit secrets private.
- Public registration links are accessible without Google authentication. Do not collect sensitive information unless the organization has an appropriate privacy notice and secure access policy.
