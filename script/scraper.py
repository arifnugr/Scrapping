import requests
from bs4 import BeautifulSoup
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# URL dasar halaman GARUDA
base_url = 'https://garuda.kemdikbud.go.id/journal?page='

# Fungsi untuk mengambil jumlah total halaman secara otomatis
def get_total_pages():
    # Mengirim request ke halaman pertama untuk mengambil informasi jumlah halaman
    try:
        response = requests.get(base_url + '1', timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menemukan elemen yang menunjukkan halaman terakhir
        last_page_link = soup.find('a', class_='page-button', href=True)

        if last_page_link:
            # Ekstrak nomor halaman terakhir dari href, misalnya ?page=2541
            total_pages = int(last_page_link['href'].split('=')[-1])  # Mengambil angka setelah 'page='
            return total_pages
        else:
            print("Tidak dapat menemukan informasi pagination.")
            return 1  # Default ke 1 jika tidak ditemukan
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error saat mengambil halaman pertama: {e}")
        return 1  # Default ke 1 jika terjadi kesalahan

# Fungsi untuk melakukan scraping pada satu halaman
def scrape_page(page):
    url = base_url + str(page)
    print(f"Scraping halaman {page}...")  # Menampilkan nomor halaman yang sedang diproses

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Mengirim request HTTP ke halaman yang sesuai dengan timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        journals = soup.find_all('a', class_='title-journal')

        titles = [journal.get_text(strip=True) for journal in journals]
        return titles
    except requests.exceptions.RequestException as e:
        print(f"Request untuk halaman {page} gagal: {e}")
        return []  # Mengembalikan daftar kosong jika terjadi kesalahan

# Mendapatkan jumlah total halaman secara otomatis
total_pages = get_total_pages()
print(f"Total halaman yang akan di-scrape: {total_pages}")

# Membuka file CSV untuk menyimpan data dengan encoding 'utf-8-sig' agar bisa dibaca dengan baik di Excel
output_path = os.path.join('data', 'raw_data.csv')

with open(output_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Journal Title'])  # Menulis header CSV

    # Menggunakan ThreadPoolExecutor untuk meng-scrape beberapa halaman secara paralel
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scrape_page, page): page for page in range(1, total_pages + 1)}

        # Mengumpulkan hasil dan menulis ke file CSV
        for future in as_completed(futures):
            page = futures[future]
            try:
                result = future.result()
                if result:
                    for title in result:
                        writer.writerow([title])  # Menulis ke CSV
            except Exception as e:
                print(f"Error saat memproses halaman {page}: {e}")

        # Menambahkan sedikit penundaan antara permintaan untuk menghindari pembatasan
        time.sleep(1)

print("\nScraping selesai! Semua judul jurnal telah disimpan dalam 'data/raw_data.csv'.")

