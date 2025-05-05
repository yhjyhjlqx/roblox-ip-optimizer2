import json
import requests
import time
from urllib.parse import urlparse

ROBLOX_DOMAINS = [
    "www.roblox.com",
    "api.roblox.com",
    "auth.roblox.com",
    "clientsettings.roblox.com",
    "economy.roblox.com",
    "gamejoin.roblox.com"
]

DOH_SERVERS = [
    "https://cloudflare-dns.com/dns-query",
    "https://dns.google/dns-query",
    "https://doh.opendns.com/dns-query"
]

def resolve_doh(domain, doh_server):
    try:
        headers = {'accept': 'application/dns-json'}
        params = {'name': domain, 'type': 'A'}
        resp = requests.get(doh_server, headers=headers, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return [answer['data'] for answer in data.get('Answer', []) if answer['type'] == 1]
    except:
        pass
    return []

def verify_ip(domain, ip):
    try:
        test_url = f"http://{ip}"
        headers = {'Host': domain}
        resp = requests.get(test_url, headers=headers, timeout=5, allow_redirects=False)
        
        if resp.status_code in (301, 302):
            location = resp.headers.get('location', '').lower()
            if 'tencent' in location or 'luobu' in location:
                return False
        
        if domain == "www.roblox.com" and b'Roblox' not in resp.content:
            return False
            
        return True
    except:
        return False

def get_clean_ips(domain):
    ips = []
    for doh in DOH_SERVERS:
        ips.extend(resolve_doh(domain, doh))
    
    ips = list(set(ips))
    return [ip for ip in ips if verify_ip(domain, ip)]

def update_hosts(clean_ips):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    hosts_content = f"# Roblox国际版官网优化IP\n# 更新时间: {timestamp}\n\n"
    
    for domain, ips in clean_ips.items():
        if ips:
            hosts_content += f"{ips[0]} {domain}\n"
    
    with open('../hosts', 'w') as f:
        f.write(hosts_content)

def main():
    clean_ips = {}
    with open('../data/ip_pool.json', 'r') as f:
        ip_pool = json.load(f)
    
    for domain in ROBLOX_DOMAINS:
        ips = get_clean_ips(domain)
        clean_ips[domain] = ips if ips else ip_pool.get(domain, [])[:3]
    
    with open('../data/clean_ips.json', 'w') as f:
        json.dump(clean_ips, f, indent=2)
    
    update_hosts(clean_ips)

if __name__ == "__main__":
    main()
