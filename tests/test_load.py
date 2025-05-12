import pandas as pd
import pytest
from unittest.mock import patch, MagicMock, mock_open
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgre

# Dummy DataFrame untuk pengujian
df_dummy = pd.DataFrame({"Name": ["Baju A"], "Price": ["Rp100.000"]})


def test_save_to_csv_success(tmp_path):
    filename = tmp_path / "dummy.csv"
    save_to_csv(df_dummy, filename)
    assert filename.exists()
    assert filename.read_text().startswith("Name,Price")


@patch("pandas.DataFrame.to_csv", side_effect=Exception("Write error"))
def test_save_to_csv_failure(mock_to_csv):
    save_to_csv(df_dummy, "invalid/path.csv")  # Hanya memastikan exception ditangani, tidak melempar


@patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
@patch("utils.load.gspread.authorize")
def test_save_to_google_sheets_success(mock_gspread, mock_creds):
    mock_ws = MagicMock()
    mock_sheet = MagicMock()
    mock_sheet.worksheet.return_value = mock_ws
    mock_gspread.return_value.open.return_value = mock_sheet

    save_to_google_sheets(df_dummy, "dummy.json", "SheetTest", "Sheet1")
    mock_ws.update.assert_called_once()


@patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name", side_effect=Exception("Auth error"))
@patch("utils.load.gspread.authorize")
def test_save_to_google_sheets_auth_error(mock_gspread, mock_creds):
    save_to_google_sheets(df_dummy, "wrong.json", "SheetTest")


@patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
@patch("utils.load.gspread.authorize")
def test_save_to_google_sheets_update_error(mock_gspread, mock_creds):
    mock_ws = MagicMock()
    mock_ws.update.side_effect = Exception("Update failed")
    mock_sheet = MagicMock()
    mock_sheet.worksheet.return_value = mock_ws
    mock_gspread.return_value.open.return_value = mock_sheet

    save_to_google_sheets(df_dummy, "dummy.json", "SheetTest")


@patch("utils.load.create_engine")
def test_save_to_postgre_success(mock_engine):
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    save_to_postgre(df_dummy, "postgresql+psycopg2://test:test@localhost/db")
    mock_conn.__enter__().execute.assert_not_called()  # tidak perlu execute, karena to_sql


@patch("utils.load.create_engine", side_effect=Exception("Connection error"))
def test_save_to_postgre_failure(mock_engine):
    save_to_postgre(df_dummy, "postgresql+pyscopg2://invalid")
