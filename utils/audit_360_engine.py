import os
import sys
import ssl
import socket
import argparse
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Ensure parent root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config
from utils.claude_helper import ClaudeAIAgent

class Site360Inspector:
    """Enhanced 360-Degree Executive Website Audit Engine with Scores & Article Analysis."""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def __init__(self, target_url: str):
        if not target_url.startswith("http"):
            target_url = f"https://{target_url}"
        self.target_url = target_url
        self.parsed_url = urlparse(target_url)
        self.domain = self.parsed_url.netloc or self.parsed_url.path
        self.results = {}

    def audit_domain_ssl(self):
        """1. Domain, IP, and SSL Security Inspection."""
        print(f"[1/6] Inspecting SSL & Security for {self.domain}...")
        ssl_info = {}
        try:
            ip_address = socket.gethostbyname(self.domain)
            ssl_info['ip_address'] = ip_address
            
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.domain) as s:
                s.settimeout(10.0)
                s.connect((self.domain, 443))
                cert = s.getpeercert()
                
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    not_after = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
                    days_remaining = (not_after - datetime.now(timezone.utc)).days
                    ssl_info['ssl_issuer'] = dict(x[0] for x in cert.get('issuer', []))
                    ssl_info['ssl_expiry_date'] = not_after_str
                    ssl_info['days_remaining'] = days_remaining
                    ssl_info['ssl_status'] = "VALID" if days_remaining > 0 else "EXPIRED"
                    ssl_info['score'] = 100 if days_remaining > 30 else (50 if days_remaining > 0 else 0)
        except Exception as e:
            ssl_info['ssl_status'] = f"Warning: {str(e)}"
            ssl_info['days_remaining'] = 0
            ssl_info['score'] = 0
            
        self.results['domain_ssl'] = ssl_info

    def audit_article_and_seo(self, html_soup: BeautifulSoup, response_time_ms: float):
        """2. Deep Article SEO & On-Page Content Analysis."""
        print("[2/6] Analyzing Article SEO, Keyword Metrics & Structure...")
        seo = {}
        
        title_tag = html_soup.find('title')
        seo['title'] = title_tag.text.strip() if title_tag else "MISSING"
        title_len = len(seo['title'])
        seo['title_score'] = 100 if 30 <= title_len <= 60 else (60 if title_len > 0 else 0)
        
        meta_desc = html_soup.find('meta', attrs={'name': 'description'})
        seo['meta_description'] = meta_desc.get('content', '').strip() if meta_desc else "MISSING"
        desc_len = len(seo['meta_description'])
        seo['desc_score'] = 100 if 120 <= desc_len <= 160 else (60 if desc_len > 0 else 0)
        
        canonical = html_soup.find('link', attrs={'rel': 'canonical'})
        seo['canonical_url'] = canonical.get('href') if canonical else "MISSING"
        
        h1s = [h.text.strip() for h in html_soup.find_all('h1')]
        h2s = [h.text.strip() for h in html_soup.find_all('h2')]
        h3s = [h.text.strip() for h in html_soup.find_all('h3')]
        seo['h1_count'] = len(h1s)
        seo['h2_count'] = len(h2s)
        seo['h3_count'] = len(h3s)
        seo['heading_structure_score'] = 100 if len(h1s) == 1 else (50 if len(h1s) > 1 else 20)
        
        text_content = html_soup.get_text(separator=' ')
        words = [w.lower() for w in text_content.split() if w.isalpha() and len(w) > 2]
        word_count = len(words)
        seo['word_count'] = word_count
        seo['content_length_rating'] = "Comprehensive" if word_count > 1000 else ("Moderate" if word_count > 400 else "Thin Content")
        
        images = html_soup.find_all('img')
        missing_alt = [img for img in images if not img.get('alt')]
        seo['total_images'] = len(images)
        seo['missing_alt_count'] = len(missing_alt)
        seo['image_alt_score'] = round(((len(images) - len(missing_alt)) / len(images) * 100), 1) if images else 100
        
        seo['response_time_ms'] = round(response_time_ms, 2)
        seo['overall_seo_score'] = round((seo['title_score'] + seo['desc_score'] + seo['heading_structure_score'] + seo['image_alt_score']) / 4, 1)
        
        self.results['seo'] = seo

    def audit_coding_quality(self, html_soup: BeautifulSoup, raw_html: str):
        """3. HTML5 Coding Style, Semantic Structure & Script Load Inspection."""
        print("[3/6] Inspecting HTML5 Coding Style & Code Quality...")
        code = {}
        
        semantic_tags = ['header', 'nav', 'main', 'article', 'aside', 'footer']
        found_semantics = [tag for tag in semantic_tags if html_soup.find(tag)]
        code['semantic_score'] = round((len(found_semantics) / len(semantic_tags)) * 100, 1)
        code['found_semantics'] = found_semantics
        
        inline_style_tags = len(html_soup.find_all(style=True))
        external_css = len(html_soup.find_all('link', attrs={'rel': 'stylesheet'}))
        code['inline_styles_count'] = inline_style_tags
        code['external_stylesheets_count'] = external_css
        
        script_tags = html_soup.find_all('script')
        async_defer_scripts = [s for s in script_tags if s.get('async') is not None or s.get('defer') is not None]
        code['total_scripts'] = len(script_tags)
        code['optimized_scripts'] = len(async_defer_scripts)
        code['script_optimization_score'] = round((len(async_defer_scripts) / len(script_tags) * 100), 1) if script_tags else 100
        
        all_elements = len(html_soup.find_all())
        code['dom_element_count'] = all_elements
        code['dom_health'] = "Optimal (< 1500)" if all_elements < 1500 else "Excessive DOM Size (> 1500)"
        
        code['code_quality_score'] = round((code['semantic_score'] + code['script_optimization_score']) / 2, 1)
        self.results['code_quality'] = code

    def audit_security_headers(self, headers: dict):
        """4. Security & Vulnerability Scan."""
        print("[4/6] Inspecting Security Headers & Protection...")
        sec = {}
        security_headers = {
            'Strict-Transport-Security': 'HSTS Header',
            'Content-Security-Policy': 'CSP Policy',
            'X-Frame-Options': 'Clickjacking Defense',
            'X-Content-Type-Options': 'MIME-Sniffing Defense',
            'Referrer-Policy': 'Referrer Policy'
        }
        
        present = []
        missing = []
        for header, desc in security_headers.items():
            if headers.get(header) or headers.get(header.lower()):
                present.append(desc)
            else:
                missing.append(desc)
                
        sec['present_count'] = len(present)
        sec['missing_headers'] = missing
        sec['security_score'] = round((len(present) / len(security_headers)) * 100, 1)
        self.results['security'] = sec

    def audit_link_health(self, html_soup: BeautifulSoup):
        """5. Broken Links & Redirection Inspection."""
        print("[5/6] Checking Link Health & Status Codes...")
        links = html_soup.find_all('a', href=True)
        sample_links = [l['href'] for l in links if l['href'].startswith('http')][:15]
        
        broken = []
        for url in sample_links:
            try:
                res = requests.head(url, headers=self.HEADERS, timeout=5, allow_redirects=True)
                if res.status_code >= 400:
                    broken.append((url, res.status_code))
            except Exception:
                broken.append((url, "Timeout/Error"))
                
        self.results['links'] = {
            'scanned_count': len(sample_links),
            'broken_count': len(broken),
            'link_health_score': round(((len(sample_links) - len(broken)) / len(sample_links) * 100), 1) if sample_links else 100
        }

    def compute_overall_health_score(self) -> float:
        """Calculate Weighted Overall Website Health Score (0-100)."""
        ssl_score = self.results['domain_ssl'].get('score', 0)
        seo_score = self.results['seo'].get('overall_seo_score', 0)
        code_score = self.results['code_quality'].get('code_quality_score', 0)
        sec_score = self.results['security'].get('security_score', 0)
        link_score = self.results['links'].get('link_health_score', 0)
        
        overall = (ssl_score * 0.20) + (seo_score * 0.30) + (code_score * 0.20) + (sec_score * 0.15) + (link_score * 0.15)
        return round(overall, 1)

    def generate_ai_swot_report(self, overall_score: float) -> str:
        """6. Synthesize Telemetry with Claude AI Executive SWOT Analysis."""
        print("[6/6] Generating Executive AI SWOT Analysis...")
        ai_agent = ClaudeAIAgent()
        
        telemetry_summary = (
            f"Domain: {self.domain}\n"
            f"Overall Health Score: {overall_score}/100\n"
            f"SEO Score: {self.results['seo'].get('overall_seo_score')}/100 (Title: {self.results['seo'].get('title')})\n"
            f"Article Word Count: {self.results['seo'].get('word_count')} words ({self.results['seo'].get('content_length_rating')})\n"
            f"Code Quality Score: {self.results['code_quality'].get('code_quality_score')}/100\n"
            f"Missing Security Headers: {', '.join(self.results['security'].get('missing_headers', []))}\n"
            f"Broken Links: {self.results['links'].get('broken_count')} of {self.results['links'].get('scanned_count')} checked\n"
        )
        
        prompt = (
            f"You are an Executive QA & Technical SEO Consultant. Analyze this website audit telemetry:\n{telemetry_summary}\n"
            f"Provide a 4-point C-level executive summary covering: Strengths, SEO/Code Weaknesses, Security Risks, and Immediate ROI Improvements."
        )
        
        if ai_agent.api_key:
            return ai_agent.analyze_failure("Executive_360_Report", prompt)
        else:
            return (
                f"### Executive SWOT Analysis for {self.domain}\n"
                f"- **Overall Health Score**: {overall_score}/100\n"
                f"- **Strengths**: Solid initial load performance ({self.results['seo'].get('response_time_ms')} ms) with valid SSL security.\n"
                f"- **Weaknesses**: Missing security headers ({len(self.results['security'].get('missing_headers', []))}) and {self.results['seo'].get('missing_alt_count')} images without Alt attributes.\n"
                f"- **Action Plan**: Implement missing HSTS/CSP security headers, fix image ALT tags for SEO, and structure H1 headings."
            )

    def run_full_360_audit(self):
        """Execute complete enhanced 360-degree audit pipeline."""
        print(f"\n=======================================================")
        print(f"STARTING ENHANCED 360 DEGREE AUDIT FOR: {self.target_url}")
        print(f"=======================================================\n")
        
        start_time = datetime.now()
        response = requests.get(self.target_url, headers=self.HEADERS, timeout=25)
        response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        self.audit_domain_ssl()
        self.audit_article_and_seo(soup, response_time_ms)
        self.audit_coding_quality(soup, response.text)
        self.audit_security_headers(response.headers)
        self.audit_link_health(soup)
        
        overall_score = self.compute_overall_health_score()
        self.results['overall_score'] = overall_score
        
        swot_summary = self.generate_ai_swot_report(overall_score)
        self.results['swot'] = swot_summary
        
        report_path = self.save_html_report()
        print(f"\n[SUCCESS] ENHANCED 360 AUDIT COMPLETE!")
        print(f"Overall Site Health Score: {overall_score} / 100")
        print(f"Client HTML Report generated at:")
        print(f"file:///{report_path}\n")
        return report_path

    def save_html_report(self) -> str:
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"audit_360_{self.domain.replace('.', '_')}.html"
        filepath = os.path.join(reports_dir, filename)
        
        overall_score = self.results.get('overall_score', 0)
        score_color = "#22c55e" if overall_score >= 80 else ("#eab308" if overall_score >= 60 else "#ef4444")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>360° Site Audit - {self.domain}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 25px; background: #0b0f19; color: #f1f5f9; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: #161e2e; padding: 35px; border-radius: 16px; border: 1px solid #1e293b; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1e293b; padding-bottom: 20px; }}
        .title-area h1 {{ margin: 0; color: #38bdf8; font-size: 2em; }}
        .score-box {{ background: #0f172a; padding: 15px 30px; border-radius: 12px; text-align: center; border: 2px solid {score_color}; }}
        .score-num {{ font-size: 2.5em; font-weight: 800; color: {score_color}; }}
        .score-label {{ font-size: 0.8em; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }}
        h2 {{ color: #c084fc; margin-top: 30px; font-size: 1.3em; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }}
        .card {{ background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; }}
        .metric-title {{ color: #94a3b8; font-size: 0.85em; font-weight: 600; text-transform: uppercase; }}
        .metric-value {{ font-size: 1.4em; font-weight: bold; color: #38bdf8; margin-top: 6px; }}
        .sub-text {{ font-size: 0.85em; color: #64748b; margin-top: 4px; }}
        pre {{ background: #070a12; padding: 20px; border-radius: 10px; color: #e2e8f0; border: 1px solid #1e293b; font-family: inherit; line-height: 1.6; white-space: pre-wrap; }}
        ul {{ padding-left: 20px; color: #cbd5e1; }}
        li {{ margin-bottom: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title-area">
                <h1>🌐 360° Executive Website Audit</h1>
                <p style="color:#94a3b8; margin-top:5px;">Target Domain: <strong>{self.domain}</strong> | Audited: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div class="score-box">
                <div class="score-num">{overall_score}</div>
                <div class="score-label">Overall Health Score</div>
            </div>
        </div>
        
        <h2>🤖 Executive AI SWOT Summary</h2>
        <pre>{self.results.get('swot')}</pre>
        
        <h2>📊 Comprehensive Audit Breakdown</h2>
        <div class="grid">
            <div class="card">
                <div class="metric-title">SEO Score</div>
                <div class="metric-value">{self.results['seo'].get('overall_seo_score')} / 100</div>
                <div class="sub-text">H1: {self.results['seo'].get('h1_count')} | H2: {self.results['seo'].get('h2_count')} | H3: {self.results['seo'].get('h3_count')}</div>
            </div>
            
            <div class="card">
                <div class="metric-title">Article Word Count</div>
                <div class="metric-value">{self.results['seo'].get('word_count')} Words</div>
                <div class="sub-text">Rating: {self.results['seo'].get('content_length_rating')}</div>
            </div>
            
            <div class="card">
                <div class="metric-title">HTML5 Code Quality</div>
                <div class="metric-value">{self.results['code_quality'].get('code_quality_score')} / 100</div>
                <div class="sub-text">DOM Nodes: {self.results['code_quality'].get('dom_element_count')}</div>
            </div>
            
            <div class="card">
                <div class="metric-title">Security Score</div>
                <div class="metric-value">{self.results['security'].get('security_score')} / 100</div>
                <div class="sub-text">Missing Headers: {len(self.results['security'].get('missing_headers', []))}</div>
            </div>
        </div>
        
        <div class="grid" style="margin-top: 20px;">
            <div class="card">
                <h2>📝 Article & SEO Metadata</h2>
                <p><strong>Title:</strong> {self.results['seo'].get('title')} ({self.results['seo'].get('title_length')} chars)</p>
                <p><strong>Meta Description:</strong> {self.results['seo'].get('meta_description')}</p>
                <p><strong>Images Missing Alt Tags:</strong> {self.results['seo'].get('missing_alt_count')} of {self.results['seo'].get('total_images')}</p>
            </div>
            
            <div class="card">
                <h2>💻 Code Style & Optimization</h2>
                <p><strong>Semantic HTML Tags Found:</strong> {', '.join(self.results['code_quality'].get('found_semantics', []))}</p>
                <p><strong>Scripts (Async/Defer Optimized):</strong> {self.results['code_quality'].get('optimized_scripts')} / {self.results['code_quality'].get('total_scripts')}</p>
                <p><strong>DOM Health:</strong> {self.results['code_quality'].get('dom_health')}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Enhanced 360 Degree Website Audit")
    parser.add_argument("--url", default="https://sleepapneabd.com", help="Target URL to audit")
    args = parser.parse_args()
    
    inspector = Site360Inspector(args.url)
    inspector.run_full_360_audit()
