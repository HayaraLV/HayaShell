import requests
def check_site(url):
  if not url.startswith(("http://", "https://")):
    url = f"https://{url}"
  try:
    response = requests.head(url, timeout=5)
    if response.status_code == 200:
      print(f"Сайт {url} активен и доступен (Код: {response.status_code})")
    else:
      print(
          f"Сайт {url} вернул ошибку или перенаправление (Код:"
          f" {response.status_code})")
  except requests.ConnectionError:
    print(f"Сайт {url} недоступен (Ошибка подключения/Не существует)")
  except requests.Timeout:
    print(f"Сайт {url} не ответил вовремя (Тайм-аут)")
