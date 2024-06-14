import os

proxies_list = [
    '64.137.49.237:6778:gfhvklsn:v78ya89gpt7a',
    '45.192.150.143:6326:gfhvklsn:v78ya89gpt7a'
]

folder_path = os.path.join("..", "data")
zip_filename = "data.zip"

base_url = "https://news.google.com/"

google_news = "https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US%3Aen"

DuckDuckGo_base_url = 'https://html.duckduckgo.com/html'

ddg_u_a = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 " \
          "Safari/537.36 "

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    "Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux i686; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
]

MINIO_HOST = os.getenv("MINIO_HOST", "172.16.184.73")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "bucket-rd-google-news")


