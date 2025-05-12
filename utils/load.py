import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine


def save_to_csv(df: pd.DataFrame, filename: str):
    try:
        """Simpan DataFrame ke file CSV."""
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke CSV: {e}")
    
def save_to_google_sheets(df: pd.DataFrame, json_keyfile: str, sheet_name: str, worksheet_name: str = 'Sheet1'):
    try:
        """Update worksheet pada Google Sheets yang sudah ada dengan data baru."""
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
        client = gspread.authorize(creds)

        # Buka spreadsheet dan worksheet
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)

        # Convert DataFrame ke list of lists dan update sheet
        rows = [df.columns.values.tolist()] + df.astype(str).values.tolist()
        worksheet.update(rows)
        print(f"Data berhasil disimpan ke Google Sheets: {sheet_name} - {worksheet_name}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")

def save_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine('postgresql://developer:supersecretpassword@localhost:5432/fashionproductsdb')
        
        # Menyimpan data ke tabel 'fashionproducts' jika tabel sudah ada, data akan ditambahkan (append)
        with engine.connect() as con:
            data.to_sql('fashionproducts', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke database postgreSQL!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke postgreSQL: {e}")
