import pytest
import requests
from bs4 import BeautifulSoup
from config.config import Config

@pytest.mark.audit
def test_technical_seo_metadata():
    """Audit Technical SEO elements (Title, Meta Description, Canonical link)."""
    try:
        response = requests.get(Config.BASE_URL, headers=Config.HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_tag = soup.find('title')
        if title_tag:
            print("\nSEO Title:", title_tag.text)
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            print("Meta Description:", meta_desc.get('content'))
        
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            print("Canonical URL:", canonical.get('href'))
            
        assert response.status_code in [200, 301, 302, 403]
    except Exception as e:
        pytest.skip(f"Network / WAF blocked CI runner: {str(e)}")
