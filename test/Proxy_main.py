import requests, os, csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def cek_proxy(raw, url_template, file_alive, file_dead):
  raws = raw[0].strip(), raw[1].strip()
  api_url = url_template.format(ip=ip, port=port)
  try:
    respon = requests.get(api_url, timeout = 60)
    respon.raise_for_status()
    data = respon.json()

    if data.get("status", "").lower() == "active":
      print(f"porxy {ip}, dan port {port} AKTIF")
      with open(file_alive, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
      return True


    else:
      print(f"porxy {ip}, dan port {port} TIDAK AKTIF")
      with open(file_dead, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        
      return False

  except requests.exceptions.RequestException as e:
    print(f" Error {ip}:{port} : {e} ")
  except ValueError as ve:
    print(f" Error JSON {ip}:{port} : {ve} ")
  return False
  

def main():
  file_input = "proxyList.txt"
  file_alive = "alive.txt"
  file_dead = "dead.txt"
  url_template = 'https://check.installer.us.kg/check?ip={dom}:{rt}'
  

  open(file_alive, "w").close()
  open(file_dead, "w").close()
 
  try:
      with open(file_input, "r") as f:
          reader = csv.reader(f)
          rows = list(reader)
  except FileNotFoundError:
      print(f"File {file_input} tidak ditemukan.")
      return

  with ThreadPoolExecutor(max_workers=50) as executor:
      futures = [
          executor.submit(cek_proxy, row, url_template, file_alive, file_dead)
          for row in rows if len(row) >= 2
      ]
      for future in as_completed(futures):
          future.result()  # Tunggu setiap proses selesai

  print(f"Semua proxy yang ALIVE telah disimpan di {file_alive}.")
  print(f"Semua proxy yang DEAD telah disimpan di {file_dead}.")

if __name__ == "__main__":
    main()
