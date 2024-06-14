import random
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import SSLError, ConnectionError, Timeout
from RnDNews.config import base_url, USER_AGENTS, google_news
from requests.exceptions import RequestException
from RnDNews.Scraper import SearchEngineScraper
from RnDNews.Shared_Methods import SharedMethods


class GoogleScraper(SearchEngineScraper):
    def scrape(self, company_names):
        for company_name in company_names:
            company_name = company_name.replace('/', '_')
            print(f"Traitement de l'entreprise : '{company_name}'...")
            search_url = google_news.format(company_name.replace(" ", "%20"))

            try:
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept-Language": "*",
                    "Referer": search_url,
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                    "server": "cloudflare",
                }
                response = requests.get(search_url, headers=headers, timeout=30)
                if response.status_code == 200:
                    search_content = response.text
                    self.scrape_links(company_name, search_content)
                elif response.status_code == 429:
                    print(
                        f"La requête GET a échoué pour l'entreprise '{company_name}'. Statut de la réponse : {response.status_code}. Too Many Requests. Réessayer dans quelques instants.")
                    time.sleep(10)
                    self.scrape([company_name])
                else:
                    print(
                        f"La requête GET a échoué pour l'entreprise '{company_name}'. Statut de la réponse : {response.status_code}")
            except (RequestException, SSLError, ConnectionError, Timeout) as e:
                print(f"Skipping {company_name} due to request exception: {e}")

    @staticmethod
    def scrape_links(company_name, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        main_element = soup.find('main', class_='IKXQhd')
        links = main_element.find_all('a', class_='JtKRv')
        count = 0
        for i, link in enumerate(links[:50], 1):
            relative_url = link.get('href')
            absolute_url = urljoin(base_url, relative_url)
            try:
                print("Get redirect url")
                redirect_url = SharedMethods.get_redirected_url(absolute_url)
                if redirect_url is not None:
                    status_code, url, html_content = GoogleScraper.get_html(redirect_url)
                    print(f"Scrapping {company_name}: {count} URLs scrapped")
                    SharedMethods.save_json(company_name, status_code, url, html_content)
                    count += 1
            except (requests.exceptions.RequestException, SSLError, ConnectionError, Timeout) as e:
                print(f"Skipping URL {absolute_url} due to request exception: {e}")
                continue
            except ValueError as ve:
                print(f"Invalid proxy string: {ve}")
                continue
        print(f"Nombre d'URLs scrappées pour l'entreprise '{company_name}': {len(links[:50])}")

    @staticmethod
    def get_html(url):
        retries = 3
        for attempt in range(retries):
            try:
                headers = {
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept-Language": "*",
                    "Referer": url,
                }
                response = requests.get(url, headers=headers, timeout=10)
                status_code = str(response.status_code)
                response_url = response.url

                if status_code == '403':
                    print("Status Code 403 detected. Using Selenium.")
                    html_content = SharedMethods.retry_with_selenium(url)
                    return None, response_url, html_content

                html_content = response.text
                return status_code, response_url, html_content
            except Timeout as timeout_error:
                print(f"Timeout error occurred for URL {url}: {timeout_error}")
                if attempt == retries - 1:
                    print("Maximum retries reached. Skipping...")
                    return "599", url, None
                else:
                    print("Retrying...")
            except (SSLError, ConnectionError) as other_error:
                print(f"Skipping URL {url} due to request exception: {other_error}")
                if attempt == retries - 1:
                    print("Maximum retries reached. Skipping...")
                    return "599", url, None
                else:
                    print("Retrying...")

