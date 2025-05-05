import json
import time

def update_hosts():
    with open('../data/clean_ips.json', 'r') as f:
        clean_ips = json.load(f)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    hosts_content = f"# Roblox国际版官网优化IP\n# 更新时间: {timestamp}\n\n"
    
    for domain, ips in clean_ips.items():
        if ips:
            hosts_content += f"{ips[0]} {domain}\n"
    
    with open('../hosts', 'w') as f:
        f.write(hosts_content)

if __name__ == "__main__":
    update_hosts()
