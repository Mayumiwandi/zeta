import requests

def check_proxy(ip, port):
    """
    Mengecek status proxy dengan mengirim request ke http://httpbin.org/ip
    Mengembalikan True jika proxy aktif, False jika tidak
    """
    try:
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }
        # Timeout 10 detik (sesuaikan jika perlu)
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        return response.status_code == 200
    except Exception as e:
        return False

# Baca file rawproxy.txt
with open('rawproxy.txt', 'r') as file:
    proxies = [line.strip().split(',') for line in file]

alive_proxies = []
dead_proxies = []

for proxy in proxies:
    if len(proxy) != 4:  # Skip baris yang tidak valid
        continue
    
    ip, port, country, org = proxy
    if check_proxy(ip, port):
        alive_proxies.append(proxy)
    else:
        dead_proxies.append(proxy)

# Tulis hasil ke file alive_proxy.txt
with open('alive_proxy.txt', 'w') as file:
    for proxy in alive_proxies:
        file.write(','.join(proxy) + '\n')

# Tulis hasil ke file dead_proxy.txt
with open('dead_proxy.txt', 'w') as file:
    for proxy in dead_proxies:
        file.write(','.join(proxy) + '\n')

print(f"Proses selesai! {len(alive_proxies)} proxy aktif dan {len(dead_proxies)} proxy mati.")
