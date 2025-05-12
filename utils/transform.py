import pandas as pd
import numpy as np

def transform_to_DataFrame(data):
    """Mengubah data list of dict menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def transform_data(df, exchange_rate):
    """Membersihkan dan mentransformasi data fashion."""

    # Define dirty patterns
    dirty_patterns = {
        "Title": ["Unknown Product"],
        "Rating": ["Invalid Rating / 5", "Not Rated"],
        "Price": ["Price Unavailable", None]
    }

    # --- Handle dirty patterns ---
    # Ganti nilai yang cocok dengan dirty patterns dengan NaN
    df['Title'] = df['Title'].apply(lambda x: np.nan if x in dirty_patterns["Title"] else x)
    df['Rating'] = df['Rating'].apply(lambda x: np.nan if x in dirty_patterns["Rating"] else x)
    df['Price'] = df['Price'].apply(lambda x: np.nan if x in dirty_patterns["Price"] else x)

    # --- Harga ---
    # Hilangkan simbol $ dan ubah ke float jika valid
    try:
        df['Price_in_Dollar'] = (
            df['Price']
            .astype(str)
            .str.replace('$', '', regex=False)
            .apply(lambda x: float(x) if x.replace('.', '', 1).isdigit() else np.nan)
        )
    except Exception as e:
        raise ValueError(f"Error saat mengonversi harga: {e}")

    # Hitung harga dalam rupiah
    df['Price'] = (df['Price_in_Dollar'] * exchange_rate).round(0).astype('float64')

    # --- Rating ---
    def clean_rating(text):
        if isinstance(text, str) and "Rating:" in text and "/" in text:
            try:
                return float(text.replace("Rating: ⭐", "").split("/")[0].strip())
            except:
                return np.nan
        return np.nan

    df['Rating'] = df['Rating'].apply(clean_rating).astype('float64')

    # --- Color ---
    # Ekstrak angka dari warna
    df['Color'] = df['Color'].str.extract(r'(\d+)').astype('Int64')

    # --- Size & Gender ---
    df['Size'] = df['Size'].str.replace("Size: ", "", regex=False)
    df['Gender'] = df['Gender'].str.replace("Gender: ", "", regex=False)

    # --- Handle missing values ---
    df = df.dropna(subset=['Title'])
    df = df.dropna(subset=['Price'])
    df.fillna({
        'Rating': 2.5, # Nilai default untuk rating
        'Color': 0, # Nilai default untuk warna
        'Size': 'Unknown',
        'Gender': 'Unknown'
    }, inplace=True)

    # --- Hapus duplikat berdasarkan semua kolom ---
    df.drop_duplicates(inplace=True)

    # Hapus kolom lama jika tidak dibutuhkan
    df = df.drop(columns=['Price_in_Dollar'])
    
    return df