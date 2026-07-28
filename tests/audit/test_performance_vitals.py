import time
import pytest
from playwright.sync_api import Page
from config.config import Config

@pytest.mark.audit
def test_page_load_speed_performance(page: Page):
    """Audit page load speed and assert duration is under 2.5 seconds threshold."""
    start_time = time.time()
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    load_time = time.time() - start_time
    
    # Assert page load speed threshold (< 2.5s)
    print(f"\n⚡ Page Load Duration: {load_time:.2f} seconds")
    assert load_time < 2.5, f"Page load exceeded 2.5s performance budget! Took {load_time:.2f}s"
    print("✅ Performance Test: Page load duration passed < 2.5s SLA target!")

@pytest.mark.audit
def test_core_web_vitals_timing(page: Page):
    """Extract navigation performance metrics via Performance Navigation API."""
    page.goto(Config.BASE_URL, wait_until="domcontentloaded")
    
    timing = page.evaluate("""() => {
        const nav = performance.getEntriesByType('navigation')[0];
        if (nav) {
            return {
                ttfb: nav.responseStart - nav.requestStart,
                domInteractive: nav.domInteractive - nav.startTime,
                domComplete: nav.domComplete - nav.startTime
            };
        }
        return null;
    }""")
    
    if timing:
        print(f"📊 Navigation Vitals -> TTFB: {timing['ttfb']:.1f}ms, DOM Interactive: {timing['domInteractive']:.1f}ms")
        assert timing['domInteractive'] >= 0
        print("✅ Core Web Vitals Audit: Navigation metrics successfully retrieved!")
    else:
        print("ℹ️ Navigation API entries not available on light DOM load.")
