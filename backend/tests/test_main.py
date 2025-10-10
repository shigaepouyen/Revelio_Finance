import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import os

# No need to modify sys.path when running pytest from the root directory

from backend.main import app
from backend.schemas import CategorizationResponse

client = TestClient(app)

# A sample valid OFX content string for testing
SAMPLE_OFX_CONTENT = b"""
OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
  <SIGNONMSGSRSV1>
    <SONRS>
      <STATUS>
        <CODE>0
        <SEVERITY>INFO
      </STATUS>
      <DTSERVER>20240101120000
      <LANGUAGE>FRA
    </SONRS>
  </SIGNONMSGSRSV1>
  <BANKMSGSRSV1>
    <STMTTRNRS>
      <TRNUID>1
      <STATUS>
        <CODE>0
        <SEVERITY>INFO
      </STATUS>
      <STMTRS>
        <CURDEF>EUR
        <BANKACCTFROM>
          <BANKID>12345
          <ACCTID>987654321
          <ACCTTYPE>CHECKING
        </BANKACCTFROM>
        <BANKTRANLIST>
          <DTSTART>20240101000000
          <DTEND>20240101000000
          <STMTTRN>
            <TRNTYPE>DEBIT
            <DTPOSTED>20240101120000
            <TRNAMT>-15.00
            <FITID>12345
            <MEMO>PAIEMENT CB 22/07 STARBUCKS PARIS 11
          </STMTTRN>
        </BANKTRANLIST>
        <LEDGERBAL>
          <BALAMT>1000.00
          <DTASOF>20240101120000
        </LEDGERBAL>
      </STMTRS>
    </STMTTRNRS>
  </BANKMSGSRSV1>
</OFX>
"""

@pytest.fixture
def mock_ai_service():
    """Fixture to mock the AI categorization service."""
    # This is the mock response the AI service will return
    mock_response = CategorizationResponse(
        marchand_probable="Starbucks",
        categorie_suggeree="Restauration",
        ville="Paris 11"
    )
    # Patch the function in the 'backend.main' module where it's imported and used
    with patch('backend.main.categorize_transaction', new_callable=AsyncMock) as mock_func:
        mock_func.return_value = mock_response
        yield mock_func

def test_upload_ofx_file_success(mock_ai_service):
    """
    Tests the successful upload and processing of an OFX file.
    It verifies that the AI service is called and the response is enriched.
    """
    # Create a mock file
    files = {'file': ('test.ofx', SAMPLE_OFX_CONTENT, 'application/ofx')}

    # Make the request
    response = client.post("/upload-ofx/", files=files)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.ofx"
    assert data["transaction_count"] == 1

    # Check that the transaction is enriched
    transaction = data["transactions"][0]
    assert transaction["description"] == "PAIEMENT CB 22/07 STARBUCKS PARIS 11"
    assert transaction["marchand_probable"] == "Starbucks"
    assert transaction["categorie_suggeree"] == "Restauration"
    assert transaction["ville"] == "Paris 11"

    # Verify that the mocked AI service was called once
    mock_ai_service.assert_called_once_with("PAIEMENT CB 22/07 STARBUCKS PARIS 11")

def test_upload_invalid_file_type():
    """
    Tests that the endpoint correctly rejects a file with an invalid extension.
    """
    files = {'file': ('test.txt', b'some content', 'text/plain')}
    response = client.post("/upload-ofx/", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_get_index_html():
    """
    Tests that the root endpoint successfully serves the index.html file.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert "<h1>Revelio Finance ✨</h1>".encode('utf-8') in response.content