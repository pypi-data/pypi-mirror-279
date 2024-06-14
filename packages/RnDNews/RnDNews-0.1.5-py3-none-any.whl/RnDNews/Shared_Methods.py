import json
import os
import time
import shutil
import zipfile
import requests
from minio import Minio
from requests.exceptions import RequestException
from urllib3.exceptions import NameResolutionError, NewConnectionError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SharedMethods:
    @staticmethod
    def get_redirected_url(url):
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                redirected_url = response.url
                return redirected_url
            except (RequestException, NameResolutionError, NewConnectionError) as e:
                print(f"Failed to get redirected URL for {url}: {e}")
                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(1)
        return None

    @staticmethod
    def retry_with_selenium(url):
        chrome_options = Options()
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--verbose')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            html_content = driver.page_source
            return html_content
        except WebDriverException as e:
            print(f"Selenium WebDriverException occurred: {e}")
            return None, url, None
        finally:
            driver.quit()

    @staticmethod
    def save_json(company_name, status_code, url, html_content):
        if html_content is not None:
            directory_path = os.path.join("..", "data")
            os.makedirs(directory_path, exist_ok=True)
            json_file_path = os.path.join(directory_path, f"{company_name}.json")
            if not os.path.exists(json_file_path):
                data = {}
            else:
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
            data[url] = {"status_code": status_code, "html_content": html_content}
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    @staticmethod
    def upload_zip_to_minio(zip_filepath, minio_host, minio_port, minio_access_key, minio_secret_key, minio_bucket):
        try:
            # Initialize MinIO client
            client = Minio(
                endpoint=f"{minio_host}:{minio_port}",
                access_key=minio_access_key,
                secret_key=minio_secret_key,
                secure=False
            )

            # Check if the bucket exists, if not, create it
            if not client.bucket_exists(minio_bucket):
                client.make_bucket(minio_bucket)
                print(f"Bucket '{minio_bucket}' created successfully.")

            # Upload the zip file to MinIO
            zip_filename = os.path.basename(zip_filepath)
            with open(zip_filepath, 'rb') as data:
                client.put_object(minio_bucket, zip_filename, data, length=os.stat(zip_filepath).st_size)
            print(f"ZIP file '{zip_filename}' uploaded to MinIO bucket '{minio_bucket}' successfully.")

            # Cleanup: remove the local zip file
            os.remove(zip_filepath)
            print("Zip file removed successfully.")

        except Exception as err:
            print(f"An error occurred: {err}")
