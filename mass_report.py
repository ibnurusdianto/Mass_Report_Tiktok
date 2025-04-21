import requests
import random
import time
import logging
from requests.exceptions import RequestException, ProxyError, SSLError, ConnectTimeout

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_proxies(filename='proxy.txt'):
    try:
        with open(filename, 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        if not proxies:
            logging.error("No proxies found in proxy.txt")
        return proxies
    except FileNotFoundError:
        logging.error("proxy.txt file not found")
        return []

def generate_random_params():
    browser_names = ['Mozilla', 'Chrome', 'Safari', 'Firefox']
    browser_platforms = ['Win32', 'Mac', 'Linux']
    current_regions = ['US', 'UK', 'CA', 'AU', 'IN', 'BR', 'FR', 'DE', 'IT', 'ES']
    os_options = ['windows', 'mac', 'linux']
    tz_names = ['America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney', 'Asia/Kolkata', 'America/Los_Angeles', 'Europe/Paris', 'Asia/Dubai', 'America/Sao_Paulo', 'Asia/Shanghai']
    webcast_languages = ['en', 'es', 'fr', 'de', 'ja', 'pt', 'it', 'ru', 'ar', 'hi']
    aid_values = ['9101', '91011', '9009', '90093', '90097', '90095', '90064', '90061', '90063', '9006', '9008', '90081', '90082', '9007', '1001', '1002', '1003', '1004', '9002', '90011', '90010', '9001', '9010', '9011', '90112', '90113', '90114', '90115', '90116', '9003', '90031', '90032', '90033', '90034', '90035', '90036', '9004', '9005', '9012', '910121', '910122', '91012', '91013', '910131', '910132', '910133', '910134', '910135', '91014', '9013', '9102']

    browser_name = random.choice(browser_names)
    browser_platform = random.choice(browser_platforms)
    browser_version = f"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {browser_name}/{random.randint(80, 120)}.0 Safari/537.36"
    current_region = random.choice(current_regions)
    device_id = str(random.randint(10**18, 10**19))
    is_fullscreen = str(random.choice([True, False])).lower()
    os = random.choice(os_options)
    priority_region = random.choice(current_regions)
    region = random.choice(current_regions)
    screen_height = str(random.randint(600, 1080))
    screen_width = str(random.randint(800, 1920))
    tz_name = random.choice(tz_names)
    webcast_language = random.choice(webcast_languages)
    aid = random.choice(aid_values)

    return {
        'aid': aid,
        'app_language': 'en',
        'app_name': 'tiktok_web',
        'browser_language': 'en-US',
        'browser_name': browser_name,
        'browser_online': 'true',
        'browser_platform': browser_platform,
        'browser_version': browser_version,
        'channel': 'tiktok_web',
        'cookie_enabled': 'true',
        'current_region': current_region,
        'device_id': device_id,
        'device_platform': 'web_pc',
        'focus_state': 'true',
        'from_page': 'user',
        'history_len': '1',
        'is_fullscreen': is_fullscreen,
        'is_page_visible': 'true',
        'lang': 'en',
        'nickname': '',
        'object_id': '',
        'os': os,
        'priority_region': priority_region,
        'reason': '9010', 
        'referer': 'https://www.tiktok.com/',
        'region': region,
        'report_type': 'user',
        'reporter_id': '',
        'root_referer': 'https://www.tiktok.com/',
        'screen_height': screen_height,
        'screen_width': screen_width,
        'secUid': '',
        'target': '',
        'tz_name': tz_name,
        'webcast_language': webcast_language
    }

def generate_report_url(username, user_id, secUid):
    base_url = 'https://www.tiktok.com/aweme/v2/aweme/feedback/?'
    params = generate_random_params()
    params['nickname'] = username
    params['object_id'] = user_id
    params['reporter_id'] = user_id
    params['secUid'] = secUid
    params['target'] = user_id

    report_url = base_url + '&'.join([f"{k}={v}" for k, v in params.items()])
    return report_url

def get_user_id_and_secUid(username):
    user_id = str(random.randint(10**10, 10**11))
    secUid = f"MS4wLjABAAAA{random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=24)}"
    return user_id, secUid

def send_report(report_url, proxy):
    try:
        response = requests.post(report_url, proxies=proxy, timeout=10, verify=False)  # Mematikan verifikasi SSL untuk tujuan pengujian
        response.raise_for_status()
        logging.info(f"Report sent successfully: {response.status_code}, {response.text}")
        return response.json()
    except RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def handle_rate_limiting():
    logging.info("Rate limit reached, waiting for 60 seconds...")
    time.sleep(60)

def process_usernames(usernames):
    proxies = load_proxies()
    if not proxies:
        logging.error("No proxies available, exiting.")
        return

    for username in usernames:
        user_id, secUid = get_user_id_and_secUid(username)
        report_url = generate_report_url(username, user_id, secUid)
        logging.info(f"Generated Report URL for {username}: {report_url}")

        all_proxies_tried = False
        for proxy in proxies:
            proxy_dict = {'http': proxy, 'https': proxy}
            response = send_report(report_url, proxy_dict)

            if response and response.get('status_code') == 0:
                logging.info(f"Successfully reported {username} using proxy {proxy}")
            else:
                logging.error(f"Failed to report {username} using proxy {proxy}")

            wait_time = random.uniform(1, 5)
            logging.info(f"Waiting for {wait_time} seconds before next proxy attempt...")
            time.sleep(wait_time)

        logging.info(f"All proxies tried for {username}. Moving to next username.")

        wait_time_between_usernames = random.uniform(10, 20)
        logging.info(f"Waiting for {wait_time_between_usernames} seconds before next username...")
        time.sleep(wait_time_between_usernames)

if __name__ == "__main__":

    usernames_to_report = ['username_target']

    process_usernames(usernames_to_report)
