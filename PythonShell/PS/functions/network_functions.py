import requests
def check_site(url):
  if not url.startswith(("http://", "https://")):
    url = f"https://{url}"
  try:
    response = requests.head(url, timeout=5)
    if response.status_code == 200:
      print(f"Site {url} active and aviable (Status: {response.status_code})")
    else:
      print(
          f"Site {url} (Status:"
          f" {response.status_code})")
  except requests.ConnectionError:
    print(f"Site {url} not aviable (Error connection)")
  except requests.Timeout:
    print(f"Site {url} (Time-out)")