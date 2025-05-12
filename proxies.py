import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Cache for working proxies
WORKING_PROXIES_CACHE = []
LAST_FETCH_TIME = 0
CACHE_DURATION = 3600  # 1 hour cache

def fetch_proxies():
    """Fetch proxies from ProxyScrape API"""
    global LAST_FETCH_TIME, WORKING_PROXIES_CACHE
    
    # Return cached proxies if they're still fresh
    if time.time() - LAST_FETCH_TIME < CACHE_DURATION and WORKING_PROXIES_CACHE:
        return WORKING_PROXIES_CACHE
    
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.split('\r\n') if '\r\n' in response.text else response.text.split('\n')
            WORKING_PROXIES_CACHE = [p.strip() for p in proxies if p.strip()]
            LAST_FETCH_TIME = time.time()
            return WORKING_PROXIES_CACHE
        else:
            print(f"Failed to fetch proxies. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def get_ems_headers():
    """Return the exact headers used by EMS.DZ website"""
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,es;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'cookiesession1=678A3E652FE94EB1143F5871441DFD29; perf_dv6Tr4n=1',
        'Host': 'www.ems.dz',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"'
    }

def test_proxy(proxy, test_url="https://www.ems.dz/track/index.php", timeout=5):
    """Test if a proxy is working by connecting to EMS.DZ with exact headers"""
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    headers = get_ems_headers()
    
    try:
        start_time = time.time()
        response = requests.get(
            test_url,
            proxies=proxies,
            headers=headers,
            timeout=timeout,
            allow_redirects=True
        )
        latency = int((time.time() - start_time) * 1000)  # in milliseconds
        
        if response.status_code == 200:
            print(f"Working proxy: {proxy} (Latency: {latency}ms)")
            return {'proxy': proxy, 'latency': latency, 'working': True}
    except Exception as e:
        pass
    
    return {'proxy': proxy, 'latency': None, 'working': False}

def check_proxies(proxies, max_workers=20):
    """Check multiple proxies concurrently"""
    working_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(test_proxy, proxies)
        
        for result in results:
            if result['working']:
                working_proxies.append(result)
    
    return working_proxies
