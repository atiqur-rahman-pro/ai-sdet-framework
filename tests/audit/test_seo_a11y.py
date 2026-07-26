import pytest
import requests
from bs4 import BeautifulSoup
from config.config import Config

@pytest.mark.audit
def test_technical_seo_metadata():
    """Audit Technical SEO elements (Title, Meta Description, Canonical link)."""
    response = requests.get(Config.BASE_URL, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Title tag presence
    title_tag = soup.find('title')
    assert title_tag is not None, "Missing <title> tag!"
    print("\nSEO Title:", title_tag.text)
    
    # 2. Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        print("Meta Description:", meta_desc.get('content'))
    
    # 3. Canonical tag
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        print("Canonical URL:", canonical.get('href'))
    
    # 4. Heading 1 (h1) presence
    h1_tags = soup.find_all('h1')
    print(f"Total H1 tags found: {len(h1_tags)}")
