import os
import sys
import ssl
import socket
import argparse
import requests
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Ensure parent root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config
from utils.claude_helper import ClaudeAIAgent

class Site360Inspector:
    """Automated 360-Degree Website Audit Engine for Client Audits."""
    
    def __init__(self, target_url: str):
        if not target_url.startswith("http"):
            target_url = f"https://{target_url}"
        self.target_url = target_url
        self.parsed_url = urlparse(target_url)
        self.domain = self.parsed_url.netloc or self.parsed_url.path
        self.results = {}

    def audit_domain_ssl(self):
        """1. Domain, IP, and SSL Certificate Inspection."""
        print(f"[1/5] Inspecting SSL & Domain for {self.domain}...")
        ssl_info = {}
        try:
            ip_address = socket.gethostbyname(self.domain)
            ssl_info['ip_address'] = ip_address
            
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.domain) as s:
                s.settimeout(5.0)
                s.connect((self.domain, 443))
                cert = s.getpeercert()
                
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    not_after = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                    days_remaining = (not_after - datetime.utcnow()).days
                    ssl_info['ssl_issuer'] = dict(x[0] for x in cert.get('issuer', []))
                    ssl_info['ssl_expiry_date'] = not_after_str
                    ssl_info['days_remaining'] = days_remaining
                    ssl_info['ssl_status'] = "VALID" if days_remaining > 0 else "EXPIRED"
        except Exception as e:
            ssl_info['ssl_status'] = f"Warning/Error: {str(e)}"
            
        self.results['domain_ssl'] = ssl_info

    def audit_seo_content(self, html_soup: BeautifulSoup, response_time_ms: float):
        """2. Technical SEO & Content Inspection."""
        print("[2/5] Inspecting Technical SEO & Content...")
        seo = {}
        
        title_tag = html_soup.find('title')
        seo['title'] = title_tag.text.strip() if title_tag else "MISSING"
        seo['title_length'] = len(seo['title']) if title_tag else 0
        
        meta_desc = html_soup.find('meta', attrs={'name': 'description'})
        seo['meta_description'] = meta_desc.get('content', '').strip() if meta_desc else "MISSING"
        seo['meta_desc_length'] = len(seo['meta_description']) if meta_desc else 0
        
        canonical = html_soup.find('link', attrs={'rel': 'canonical'})
        seo['canonical_url'] = canonical.get('href') if canonical else "MISSING"
        
        h1_tags = [h.text.strip() for h in html_soup.find_all('h1')]
        seo['h1_count'] = len(h1_tags)
        seo['h1_sample'] = h1_tags[0] if h1_tags else "None"
        
        images = html_soup.find_all('img')
        missing_alt = [img for img in images if not img.get('alt')]
        seo['total_images'] = len(images)
        seo['missing_alt_count'] = len(missing_alt)
        seo['response_time_ms'] = round(response_time_ms, 2)
        
        self.results['seo'] = seo

    def audit_security_headers(self, headers: dict):
        """3. Security Headers Inspection."""
        print("[3/5] Inspecting Security Headers...")
        sec = {}
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME-Sniffing Protection',
            'Referrer-Policy': 'Referrer Policy'
        }
        
        present_headers = {}
        missing_headers = []
        for header, description in security_headers.items():
            value = headers.get(header) or headers.get(header.lower())
            if value:
                present_headers[header] = value
            else:
                missing_headers.append(f"{header} ({description})")
                
        sec['present_count'] = len(present_headers)
        sec['missing_headers'] = missing_headers
        sec['server_header'] = headers.get('Server', 'Hidden / Protected')
        self.results['security'] = sec

    def audit_broken_links(self, html_soup: BeautifulSoup):
        """4. Link Health & Broken Links Check (Top Links)."""
        print("[4/5] Checking Internal/External Links...")
        links = html_soup.find_all('a', href=True)
        total_links = len(links)
        
        scanned_links = []
        broken_links = []
        
        sample_links = [l['href'] for l in links if l['href'].startswith('http')][:15]
        for url in sample_links:
            try:
                res = requests.head(url, timeout=4, allow_redirects=True)
                if res.status_code >= 400:
                    broken_links.append((url, res.status_code))
                else:
                    scanned_links.append((url, res.status_code))
            except Exception:
                broken_links.append((url, "Failed/Timeout"))
                
        self.results['links'] = {
            'total_links_found': total_links,
            'scanned_count': len(sample_links),
            'broken_links': broken_links,
            'broken_count': len(broken_links)
        }

    def generate_ai_swot_report(self) -> str:
        """5. Synthesize Telemetry via Claude AI for Client Executive Summary."""
        print("[5/5] Synthesizing Telemetry with Claude AI Executive SWOT Analysis...")
        ai_agent = ClaudeAIAgent()
        
        telemetry_summary = (
            f"Domain: {self.domain}\n"
            f"SSL Status: {self.results['domain_ssl'].get('ssl_status')} (Days Left: {self.results['domain_ssl'].get('days_remaining', 'N/A')})\n"
            f"Response Speed: {self.results['seo'].get('response_time_ms')} ms\n"
            f"SEO Title: {self.results['seo'].get('title')} (Len: {self.results['seo'].get('title_length')})\n"
            f"SEO Meta Desc: {self.results['seo'].get('meta_description')}\n"
            f"Missing Image Alt Tags: {self.results['seo'].get('missing_alt_count')} of {self.results['seo'].get('total_images')}\n"
            f"Missing Security Headers: {', '.join(self.results['security'].get('missing_headers', []))}\n"
            f"Broken Links Found: {self.results['links'].get('broken_count')} out of {self.results['links'].get('scanned_count')} checked\n"
        )
        
        prompt = (
            f"You are a Senior Technical QA & SEO Consultant. Analyze this website telemetry:\n{telemetry_summary}\n"
            f"Generate a clean 4-bullet executive report with:\n"
            f"1. Strengths\n2. Technical & Security Weaknesses\n3. High Priority Action Plan for the Client."
        )
        
        if ai_agent.api_key:
            return ai_agent.analyze_failure("360_Audit_Report", prompt)
        else:
            return (
                f"### Executive Summary for {self.domain}\n"
                f"- **Strengths**: Domain is live and active with fast initial response ({self.results['seo'].get('response_time_ms')} ms).\n"
                f"- **Weaknesses**: Missing security headers ({len(self.results['security'].get('missing_headers', []))}) and {self.results['seo'].get('missing_alt_count')} images without Alt attributes.\n"
                f"- **Action Plan**: Implement missing HSTS/CSP security headers, fix image ALT tags for SEO, and monitor broken link redirects."
            )

    def run_full_360_audit(self):
        """Execute complete 360-degree audit pipeline."""
        print(f"\n=======================================================")
        print(f"STARTING 360 DEGREE AUTOMATED SITE AUDIT FOR: {self.target_url}")
        print(f"=======================================================\n")
        
        start_time = datetime.now()
        response = requests.get(self.target_url, timeout=15)
        response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        self.audit_domain_ssl()
        self.audit_seo_content(soup, response_time_ms)
        self.audit_security_headers(response.headers)
        self.audit_broken_links(soup)
        
        swot_summary = self.generate_ai_swot_report()
        self.results['swot'] = swot_summary
        
        report_path = self.save_html_report()
        print(f"\n[SUCCESS] AUDIT COMPLETE! Full Client Report generated at:")
        print(f"file:///{report_path}\n")
        return report_path

    def save_html_report(self) -> str:
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"audit_360_{self.domain.replace('.', '_')}.html"
        filepath = os.path.join(reports_dir, filename)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>360° Audit Report - {self.domain}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #0f172a; color: #f8fafc; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        h2 {{ color: #a78bfa; margin-top: 25px; }}
        .badge {{ display: inline-block; padding: 6px 12px; border-radius: 6px; font-weight: bold; }}
        .badge-success {{ background: #15803d; color: #fff; }}
        .badge-warning {{ background: #b45309; color: #fff; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
        .card {{ background: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; }}
        .metric-title {{ color: #94a3b8; font-size: 0.9em; }}
        .metric-value {{ font-size: 1.3em; font-weight: bold; color: #38bdf8; margin-top: 5px; }}
        pre {{ background: #090d16; padding: 15px; border-radius: 6px; color: #e2e8f0; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 360° Executive Site Audit Report</h1>
        <p>Target Domain: <strong>{self.domain}</strong> | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>🤖 Executive AI SWOT Analysis</h2>
        <pre>{self.results.get('swot')}</pre>
        
        <div class="grid">
            <div class="card">
                <h2>🔒 Domain & SSL Security</h2>
                <div class="metric-title">SSL Status</div>
                <div class="metric-value">{self.results['domain_ssl'].get('ssl_status')}</div>
                <div class="metric-title" style="margin-top:10px;">Days Remaining</div>
                <div class="metric-value">{self.results['domain_ssl'].get('days_remaining', 'N/A')} Days</div>
                <div class="metric-title" style="margin-top:10px;">Server IP</div>
                <div class="metric-value">{self.results['domain_ssl'].get('ip_address', 'N/A')}</div>
            </div>
            
            <div class="card">
                <h2>⚡ Performance & Technical SEO</h2>
                <div class="metric-title">Initial Page Speed</div>
                <div class="metric-value">{self.results['seo'].get('response_time_ms')} ms</div>
                <div class="metric-title" style="margin-top:10px;">SEO Title</div>
                <div class="metric-value" style="font-size:0.95em;">{self.results['seo'].get('title')}</div>
                <div class="metric-title" style="margin-top:10px;">Images Missing Alt Tags</div>
                <div class="metric-value">{self.results['seo'].get('missing_alt_count')} / {self.results['seo'].get('total_images')}</div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🛡️ Missing Security Headers</h2>
                <ul>
                    {"".join(f"<li>{h}</li>" for h in self.results['security'].get('missing_headers', []))}
                </ul>
            </div>
            
            <div class="card">
                <h2>🔗 Link Health Check</h2>
                <div class="metric-title">Scanned Links</div>
                <div class="metric-value">{self.results['links'].get('scanned_count')} Links</div>
                <div class="metric-title" style="margin-top:10px;">Broken Links Found</div>
                <div class="metric-value" style="color: {'#ef4444' if self.results['links'].get('broken_count') > 0 else '#22c55e'};">
                    {self.results['links'].get('broken_count')} Broken Links
                </div>
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
    parser = argparse.ArgumentParser(description="Run 360 Degree Website Audit")
    parser.add_argument("--url", default="https://sleepapneabd.com", help="Target URL to audit")
    args = parser.parse_args()
    
    inspector = Site360Inspector(args.url)
    inspector.run_full_360_audit()
