import time
from datetime import datetime
 
import pandas as pd
import requests
from bs4 import BeautifulSoup
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
 
 
def fetching_content(url, retries=3, delay=2):
    """Mengambil konten HTML dari URL yang diberikan, dengan retry jika gagal."""
    session = requests.Session()
    attempt = 0

    while attempt < retries:
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"[{attempt}/{retries}] Error request ke {url}: {e}")
            if attempt < retries:
                print(f"Menunggu {delay} detik sebelum mencoba lagi...")
                time.sleep(delay)
            else:
                print(f"Gagal mengakses {url} setelah {retries} percobaan.")
                return None
 
 
def extract_fashion_data(div):
    """Mengambil data fashion berupa judul, harga, ketersediaan, dan rating dari div (element html)."""
    title = div.find('h3').text

    # Cari elemen harga: prioritas ke <span class="price">, fallback ke <p class="price">
    price_tag = div.find('span', class_='price')
    if not price_tag:
        price_tag = div.find('p', class_='price')

    price = price_tag.text.strip() if price_tag else None
 
    info = div.find_all("p", style=True)
    rating = info[0].text.strip()
    color = info[1].text.strip()
    size = info[2].text.strip()
    gender = info[3].text.strip()
    timestamp = datetime.now().isoformat()

    fashions = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Color": color,
        "Size": size,
        "Gender" : gender,
        "Timestamp": timestamp
    }
 
    return fashions
 
 
def scrape_fashion(base_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = start_page
 
    while True:
        if page_number == 1:
            url = base_url  # tanpa /page1.html
        else:
            url = f"{base_url}/page{page_number}.html"
        print(f"Scraping halaman: {url}")
 
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            divs_element = soup.find_all('div', class_='collection-card')
            for div in divs_element:
                try:
                    fashion = extract_fashion_data(div)
                    data.append(fashion)
                except Exception as e:
                    print(f"Gagal memproses 1 item: {e}")

            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay) # Delay sebelum halaman berikutnya
            else:
                break # Berhenti jika sudah tidak ada next button
        else:
            break # Berhenti jika ada kesalahan
 
    return data