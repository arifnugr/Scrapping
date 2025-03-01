import os
import pandas as pd
import nltk
import string
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import logging

# Unduh resource NLTK yang diperlukan
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCleaner:
    """Kelas untuk membersihkan judul penelitian menggunakan teknik NLP."""
    
    def __init__(self, input_file, output_file=None, language='Indonesian'):
        """
        Inisialisasi pembersih data.
        
        Args:
            input_file (str): Path ke file CSV input
            output_file (str): Path ke file CSV output (default: None)
            language (str): Bahasa untuk stopwords dan lemmatization (default: 'Indonesian')
        """
        self.input_file = input_file
        self.output_file = output_file if output_file else self._generate_output_filename()
        self.language = language

        # Inisialisasi komponen NLP
        if self.language == 'Indonesian':
            self.stopwords = self.get_indonesian_stopwords()
        else:
            self.stopwords = set(stopwords.words(self.language))

        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = set(string.punctuation)  # Semua tanda baca umum

    def _generate_output_filename(self):
        """Membuat nama file output berdasarkan file input."""
        base, ext = os.path.splitext(self.input_file)
        return f"{base}_cleaned{ext}"

    def get_indonesian_stopwords(self):
        """Menggunakan daftar stopwords Indonesia dari NLTK atau tambahan manual."""
        return set([
            'dan', 'di', 'yang', 'untuk', 'dari', 'dengan', 'pada', 'sebagai', 'adalah',
            'jurnal', 'studi', 'tentang', 'ilmu', 'penelitian', 'pengabdian', 'kepada', 'masyarakat'
        ])

    def clean_text(self, text):
        """
        Membersihkan teks dengan teknik NLP.
        
        Args:
            text (str): Teks input yang akan dibersihkan
            
        Returns:
            str: Teks yang telah dibersihkan
        """
        if not isinstance(text, str):
            return ""  # Jika input bukan string, kembalikan string kosong
        
        # Ubah ke huruf kecil
        text = text.lower()

        # Hilangkan karakter khusus seperti @, ', ", (, ), :, -, dll.
        text = re.sub(r"[^\w\s]", " ", text)  # Menghapus semua tanda baca
        text = re.sub(r"\s+", " ", text).strip()  # Hilangkan spasi berlebih

        # Tokenisasi
        tokens = word_tokenize(text)

        # Hapus stopwords dan lemmatize
        clean_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stopwords
        ]
        
        # Gabungkan kembali token yang telah dibersihkan
        clean_text = ' '.join(clean_tokens)

        return clean_text.strip()
    
    def process_csv(self):
        """
        Membaca CSV input, membersihkan datanya, dan menyimpannya ke CSV output.
        
        Returns:
            pandas.DataFrame: Data yang telah dibersihkan
        """
        try:
            # Baca file CSV
            logger.info(f"Membaca data dari {self.input_file}")
            df = pd.read_csv(self.input_file)

            # Periksa apakah kolom 'Title' ada, jika tidak coba 'Journal Title'
            if 'Title' not in df.columns:
                if 'Journal Title' in df.columns:
                    df.rename(columns={'Journal Title': 'Title'}, inplace=True)
                else:
                    raise ValueError(f"CSV input harus memiliki kolom 'Title'. Kolom ditemukan: {df.columns.tolist()}")
            
            # Bersihkan judul
            logger.info("Membersihkan judul...")
            df['CleanedTitle'] = df['Title'].apply(self.clean_text)
            
            # Simpan ke file output
            logger.info(f"Menyimpan data yang telah dibersihkan ke {self.output_file}")
            df.to_csv(self.output_file, index=False, quoting=csv.QUOTE_ALL)
            
            logger.info(f"Berhasil membersihkan {len(df)} judul")
            return df
            
        except Exception as e:
            logger.error(f"Terjadi kesalahan dalam pembersihan data: {e}")
            raise

if __name__ == "__main__":
    input_file = "data/raw_data.csv"  # Sesuaikan dengan lokasi file Anda
    output_file = "data/cleaned_data.csv"

    cleaner = DataCleaner(input_file=input_file, output_file=output_file, language='Indonesian')
    
    try:
        cleaner.process_csv()
        print(f"Berhasil membersihkan data dan menyimpan ke {cleaner.output_file}")
    except Exception as e:
        print(f"Error: {e}")

