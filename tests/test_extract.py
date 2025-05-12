import pytest
import requests
from unittest.mock import patch, Mock
from utils.extract import fetching_content, extract_fashion_data, scrape_fashion
from bs4 import BeautifulSoup

# ===== Test fetching_content =====
@patch('utils.extract.requests.Session.get')
def test_fetching_content_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<html></html>"
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    content = fetching_content("https://example.com")
    assert content == b"<html></html>"
    mock_get.assert_called_once()

@patch('utils.extract.requests.Session.get')
def test_fetching_content_failure(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

    content = fetching_content("https://example.com", retries=2, delay=0)
    assert content is None


# ===== Test extract_fashion_data =====
def test_extract_fashion_data_valid_html():
    html = """
    <div class="collection-card">
        <h3>Fashion T-Shirt</h3>
        <span class="price">$15.00</span>
        <p style="color:red">Rating: ⭐ 4.2 / 5</p>
        <p style="color:blue">Color: 2</p>
        <p style="font-weight:bold">Size: M</p>
        <p style="font-style:italic">Gender: Male</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="collection-card")

    data = extract_fashion_data(div)
    assert data["Title"] == "Fashion T-Shirt"
    assert data["Price"] == "$15.00"
    assert "Rating" in data
    assert "Color" in data
    assert "Size" in data
    assert "Gender" in data
    assert "Timestamp" in data


# ===== Test scrape_fashion =====
@patch('utils.extract.fetching_content')
def test_scrape_fashion_one_page(mock_fetch):
    html = """
    <html>
        <div class="collection-card">
            <h3>Test Product</h3>
            <span class="price">$20</span>
            <p style="...">Rating: ⭐ 3.9 / 5</p>
            <p style="...">Color: 3</p>
            <p style="...">Size: L</p>
            <p style="...">Gender: Female</p>
        </div>
    </html>
    """
    mock_fetch.return_value = html.encode("utf-8")

    data = scrape_fashion("https://fake-url.com", delay=0)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["Title"] == "Test Product"
    assert data[0]["Price"] == "$20"
