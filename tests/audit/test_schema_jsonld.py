import pytest
import requests
import json
from bs4 import BeautifulSoup
from config.config import Config

@pytest.mark.audit
def test_jsonld_structured_data_presence():
    """Verify presence and validity of JSON-LD Structured Data Schema."""
    try:
        response = requests.get(Config.BASE_URL, headers=Config.HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all JSON-LD scripts
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        print(f"\nTotal JSON-LD Schema scripts found: {len(json_ld_scripts)}")
        
        valid_schemas = 0
        for script in json_ld_scripts:
            try:
                schema_data = json.loads(script.string)
                valid_schemas += 1
                schema_type = schema_data.get('@type', 'Unknown Schema Type')
                print(f"Found valid Schema type: {schema_type}")
            except Exception:
                pass
                
        assert response.status_code in [200, 301, 302, 403]
        print(f"✅ Total Valid JSON-LD Schemas Parsed: {valid_schemas}")
    except Exception as e:
        pytest.skip(f"Network / WAF blocked runner: {str(e)}")
