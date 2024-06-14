import random
from bs4 import BeautifulSoup
from requests.exceptions import SSLError, ConnectionError, Timeout
from RnDNews.config import DuckDuckGo_base_url, ddg_u_a, USER_AGENTS
from RnDNews.Scraper import SearchEngineScraper
from RnDNews.Shared_Methods import SharedMethods
import requests


class DuckDuckGoScraper(SearchEngineScraper):
    def scrape(self, company_names):
        for company_name in company_names:
            company_name = company_name.replace('/', '_')
            print(f"Traitement de l'entreprise : '{company_name}'...")
            search_query = company_name.replace(" ", "+")
            search_url = DuckDuckGo_base_url

            try:
                header = {
                    "User-Agent": ddg_u_a,
                }
                response = requests.get(search_url, data={'q': {search_query}}, headers=header, timeout=30)
                print(response)
                if response.status_code == 200:
                    search_content = response.text
                    self.scrape_links(company_name, search_content)
                else:
                    print(
                        f"La requête GET a échoué pour l'entreprise '{company_name}'. Statut de la réponse : {response.status_code}")
            except (requests.exceptions.RequestException, SSLError, ConnectionError, Timeout) as e:
                if isinstance(e, SSLError):
                    print(
                        "Impossible de vérifier le certificat SSL sur {} - Détails supplémentaires : {}, réessai...".format(
                            search_url, e))
                elif isinstance(e, ConnectionError) and "Remote end closed connection without response" in str(e):
                    print(f"Skipping {company_name} due to request exception: {e}")
                else:
                    print("Erreur {} sur {}, réessai...".format(type(e).__name__, search_url))
                print(f"Skipping {company_name} due to request exception: {e}")

    @staticmethod
    def scrape_links(company_name, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = soup.find_all('div', class_='result')
        links = []
        for result in results:
            url_element = result.find('a', class_='result__a')
            link = url_element['href'] if url_element else None
            if link:
                links.append(link)
        count = 0
        for i, link in enumerate(links[:50], 1):
            try:
                status_code, url, html_content = DuckDuckGoScraper.get_html(link)
                print(f"Scrapping {company_name}: {count} URLs scrapped")
                SharedMethods.save_json(company_name, status_code, url, html_content)
                count += 1
            except (requests.exceptions.RequestException, SSLError, ConnectionError, Timeout) as e:
                print(f"Skipping URL {link} due to request exception: {e}")
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
