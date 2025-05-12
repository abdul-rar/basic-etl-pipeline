# Proyek ETL Pipeline

Deskripsi
Proyek ini mencakup pembuatan ETL pipeline untuk mengambil, mengolah, dan menyimpan data dari sumber eksternal ke berbagai tujuan seperti CSV, Google Sheets, dan PostgreSQL. Pipeline ini terdiri dari beberapa langkah utama, yaitu ekstraksi data, transformasi data, dan pemuatan data ke dalam berbagai format.

## Cara Menjalankan Skrip ETL Pipeline
1. Persiapan Lingkungan Virtual (venv)
Sebelum menjalankan pipeline, masuk ke directory tempat folder ETL pipeline berada dengan perintah
```
cd <directory folder>
```
kemudian buatlah lingkungan virtual untuk memastikan semua dependensi terisolasi. Jalankan perintah berikut untuk membuat lingkungan virtual:
```
python -m venv .env
```
2. Aktivasi Lingkungan Virtual
Setelah lingkungan virtual dibuat, Anda perlu mengaktifkannya:

Pada Windows:
```
.env\Scripts\activate.bat
```
3. Instalasi Dependensi
Setelah mengaktifkan lingkungan virtual, instal semua dependensi yang dibutuhkan dengan menjalankan perintah berikut:
```
pip install -r requirements.txt
```
4. Membuat database di PostgreSQL agar dapat menyimpan dan melihat data di PostgreSQL
pada command prompt jalankan perintah-perintah berikut
```
psql --username postgres
```
lalu setelah masuk ke postgreSQL, jalankan program berikut
```
CREATE USER developer WITH ENCRYPTED PASSWORD 'supersecretpassword';
CREATE DATABASE fashionproductsdb;
GRANT ALL ON DATABASE fashionproductsdb TO developer;
ALTER DATABASE fashionproductsdb OWNER TO developer;
```
4. Menjalankan Skrip ETL
Setelah semua dependensi diinstal, Anda dapat menjalankan skrip utama pipeline ETL dengan perintah berikut pada command prompt:
```
python main.py
```
## Cara Menjalankan Unit Test
1. Aktivasi Lingkungan Virtual
Pastikan lingkungan virtual telah aktif dengan mengikuti langkah-langkah di bagian sebelumnya.

2. Instalasi Dependensi untuk Testing
Untuk menjalankan unit test, Anda memerlukan pytest. Instal dependensi testing dengan perintah berikut:
```
pip install pytest pytest-cov
```
3. Menjalankan Unit Test
Untuk menjalankan unit test, gunakan perintah berikut:
```
pytest
```
Perintah ini akan mengeksekusi semua file yang memiliki nama diawali dengan test_ di dalam folder tests/ dan menampilkan hasil dari unit test.

## Cara Menjalankan Test Coverage
1. Aktivasi Lingkungan Virtual
   Pastikan lingkungan virtual telah aktif.

3. Menjalankan Test Coverage
  Untuk menjalankan test coverage dan menghasilkan laporan dalam format HTML, gunakan perintah berikut:
  ```
  set PYTHONPATH=.
  pytest --cov=utils --cov-report=html tests/
  ```
  
  Penjelasan:
  
  --cov=utils: Menentukan direktori yang ingin diuji (misalnya direktori utils).
  
  --cov-report=html: Membuat laporan coverage dalam format HTML.
  
  Laporan akan disimpan di folder htmlcov/. Anda bisa membuka laporan tersebut dengan mengakses file htmlcov/index.html di browser.
  
