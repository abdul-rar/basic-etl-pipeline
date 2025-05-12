from utils.extract import scrape_fashion
from utils.transform import transform_data, transform_to_DataFrame
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgre

def main():
    # ----------------------Extract Data--------------------------
    # Step 1: Ambil data dari sumber (misal web scraping atau API)
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    try:
        raw_data = scrape_fashion(BASE_URL)  # pastikan fungsi ini mengembalikan list of dict
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return
    
    # Step 2: Ubah ke DataFrame
    try:
        df_raw = transform_to_DataFrame(raw_data)
        print("\n--- Data Mentah (sebelum transformasi) ---")
        print(df_raw)  # tampilkan 5 baris pertama
        print(df_raw.info())  # info tentang DataFrame
    except Exception as e:
        print(f"Gagal mengubah data ke DataFrame: {e}")
        return

    #---------------------- Transformasi Data --------------------
    # Step 3: Transformasi Data
    EXCHANGE_RATE = 16000
    try:
        df_clean = transform_data(df_raw, EXCHANGE_RATE)
    except Exception as e:
        print(f"Gagal mentransformasi data: {e}")
        return
    
    # Step 4: Tampilkan hasil setelah transformasi
    print("\n--- Data Setelah Transformasi ---")
    print(df_clean)  # tampilkan 5 baris pertama
    print(df_clean.info())  # info tentang DataFrame

    #-------------------------Load Data------------------------------
    # Step 5: Simpan ke CSV
    filename = 'fashion-products.csv'
    save_to_csv(df_clean, filename)

    # Step 6: Simpan ke Google Sheets (jika sudah punya credentials JSON)
    sheet_name = 'fashion-products'
    save_to_google_sheets(
        df_clean,
        json_keyfile='google-sheets-api.json',
        sheet_name=sheet_name,
        worksheet_name='Sheet1'
    )

    # Step 7: Simpan ke PostgreSQL
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashionproductsdb'
    save_to_postgre(df_clean, db_url)

if __name__ == "__main__":
    main()