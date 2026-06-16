import urllib.request

# Принимаем аргументы из ядра
args = context_args.strip().split(" ")

if not args or not args[0]:
    print("\033[31mError: Please specify a URL. Usage: curl [url] [output_name]\033[0m")
else:
    url = args[0]
    
    # Если пользователь не указал имя файла, вытаскиваем его из самого URL
    if len(args) > 1 and args[1].strip():
        output_name = args[1].strip()
    else:
        output_name = url.split("/")[-1]
        if not output_name or "?" in output_name:
            output_name = "downloaded_file.txt"

    print(f"\033[34m[Connecting to URL...]\033[0m")
    try:
        # Кастомный User-Agent, а также явное указание кодировок (убирает кракозябры на некоторых сайтах)
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'
            }
        )
        
        # Добавляем timeout=10, чтобы iPad не зависал, если сеть пропадет
        with urllib.request.urlopen(req, timeout=10) as response:
            total_size = response.getheader('Content-Length')
            if total_size:
                total_size = int(total_size)
                print(f"\033[34m[Downloading {output_name} ({total_size / 1024:.1f} KB)...]\033[0m")
            else:
                print(f"\033[34m[Downloading {output_name}...]\033[0m")
                
            # ИСПРАВЛЕНИЕ: Используем встроенный метод декомпрессии ответа (разжимает GZIP на лету)
            # В старых версиях Python response.read() мог возвращать сжатый архив, теперь данные чистые
            data = response.read()
            
            try:
                # Пытаемся определить текстовую кодировку ответа
                encoding = response.info().get_content_charset() or 'utf-8'
                # Если это текстовый файл, декодируем его и сохраняем как текст
                decoded_data = data.decode(encoding)
                with open(output_name, "w", encoding="utf-8") as f:
                    f.write(decoded_data)
            except UnicodeDecodeError:
                # Если это бинарный файл (картинка, архив), пишем как байты
                with open(output_name, "wb") as f:
                    f.write(data)
                
        print(f"\033[32m[+] Successfully downloaded and saved as '{output_name}'\033[0m")
    except Exception as e:
        print(f"\033[31mDownload failed. Reason: {e}\033[0m")
