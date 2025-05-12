import pytest
import pandas as pd
import numpy as np
from utils.transform import transform_to_DataFrame, transform_data

# Data untuk pengujian
test_data = [
    {
        "Title": "Product A",
        "Price": "$20.00",
        "Rating": "Rating: ⭐4/5",
        "Color": "5 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Unisex"
    },
    {
        "Title": "Product B",
        "Price": "$15.50",
        "Rating": "Rating: ⭐3/5",
        "Color": "3 Colors",
        "Size": "Size: L",
        "Gender": "Gender: Male"
    },
    {
        "Title": "Unknown Product",
        "Price": "Price Unavailable",
        "Rating": "Not Rated",
        "Color": "2 Colors",
        "Size": "Size: S",
        "Gender": "Gender: Female"
    }
]

# Test transform_to_DataFrame
def test_transform_to_dataframe():
    df = transform_to_DataFrame(test_data)
    assert isinstance(df, pd.DataFrame), "Output harus berupa DataFrame"
    assert df.shape[0] == len(test_data), f"Jumlah baris DataFrame harus {len(test_data)}"

# Test transform_data
def test_transform_data():
    df = transform_to_DataFrame(test_data)
    exchange_rate = 16000  # Misal, kurs dari USD ke IDR

    transformed_df = transform_data(df, exchange_rate)

    # Karena 'Unknown Product' dan 'Price Unavailable' di-drop, indexnya berubah
    # Jadi pakai reset_index biar aman
    transformed_df = transformed_df.reset_index(drop=True)

    # Test jika semua kolom sudah bersih
    assert transformed_df['Title'].isna().sum() == 0, "Tidak boleh ada Title yang NaN"
    assert transformed_df['Price'].isna().sum() == 0, "Tidak boleh ada Price yang NaN"

    # Test jika harga konversi dilakukan dengan benar
    assert transformed_df['Price'].iloc[0] == 320000, "Harga konversi dari $20.00 harus sesuai dengan kurs"

    # Test jika rating bersih
    assert transformed_df['Rating'].iloc[0] == 4.0, "Rating harus sesuai (4.0)"

    # Test jika kolom 'Color' diekstraksi dengan benar
    assert transformed_df['Color'].iloc[0] == 5, "Color harus berupa angka yang sesuai"

    # Test jika kolom 'Size' dan 'Gender' diproses dengan benar
    assert transformed_df['Size'].iloc[0] == "M", "Size harus diproses dengan benar"
    assert transformed_df['Gender'].iloc[0] == "Unisex", "Gender harus diproses dengan benar"

    # Test jika tidak ada duplikat
    assert transformed_df.duplicated().sum() == 0, "DataFrame harus bebas duplikat"

    # Test jika kolom 'Price_in_Dollar' telah dihapus
    assert 'Price_in_Dollar' not in transformed_df.columns, "'Price_in_Dollar' harus dihapus setelah transformasi"

# Test untuk harga invalid => cek jadi NaN, bukan error
def test_transform_data_invalid_price():
    # Data dengan harga yang tidak valid
    invalid_data = [
        {
            "Title": "Product C",
            "Price": "$invalid",
            "Rating": "Rating: ⭐5/5",
            "Color": "4 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Female"
        }
    ]
    df = transform_to_DataFrame(invalid_data)
    exchange_rate = 16000

    df_transformed = transform_data(df, exchange_rate)

    # Karena harga invalid dan di-drop, DataFrame harus kosong
    assert df_transformed.empty, "Data harus kosong setelah drop baris dengan harga invalid"
