"""
网络连接修复工具
Network Connection Fix Tool

解决Windows环境下的SSL和网络连接问题
"""

import os
import ssl
import certifi
import urllib3
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def apply_network_fixes():
    """Apply network and SSL fixes for Windows"""
    
    # Disable SSL warnings (for debugging only)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Set up SSL context for better compatibility
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE  # Only for debugging
    
    # Set environment variables for better SSL handling
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    print("🔧 网络修复设置已应用")

def create_robust_session():
    """Create a more robust requests session"""
    session = requests.Session()
    
    # More aggressive retry strategy
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    return session

def test_connection():
    """Test network connectivity with different approaches"""
    print("🔍 测试网络连接...")
    
    session = create_robust_session()
    
    test_urls = [
        "https://httpbin.org/get",
        "https://api.exchangerate.host/latest",
        "https://jsonplaceholder.typicode.com/posts/1"
    ]
    
    for url in test_urls:
        try:
            response = session.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                print(f"✅ {url} - 连接成功")
                return True
            else:
                print(f"⚠️  {url} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - 连接失败: {str(e)[:50]}...")
    
    print("❌ 所有测试URL都无法连接")
    return False

if __name__ == '__main__':
    apply_network_fixes()
    test_connection()