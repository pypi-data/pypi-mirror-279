# This will import the `add` and `subtract` functions from module.py
# and make them available directly from mypackage.

from FindYourProfessor import extract_urls, scrape_urls, extract_emails


def extract_emails(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

def extract_urls(primary_url):
    try:
        response = requests.get(primary_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            urls = []
            for link in links:
                url = link.get('href')
                if url:
                    absolute_url = urljoin(primary_url, url)
                    if absolute_url.startswith('http://') or absolute_url.startswith('https://'):
                        urls.append(absolute_url)
            return urls
        else:
            print(f"Error fetching {primary_url}: Status Code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {primary_url}: {e}")
        return []
    except Exception as e:
        print(f"Error processing {primary_url}: {e}")
        return []

def scrape_urls(urls, keywords):
    visited_urls = set()
    for url in urls:
        if url not in visited_urls:
            visited_urls.add(url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.text.strip() if soup.title else "No title"
                    found_keywords = []
                    for keyword in keywords:
                        if soup.body and soup.body.find_all(string=re.compile(r'\b{}\b'.format(re.escape(keyword))), recursive=True):
                            found_keywords.append(keyword)
                    emails_in_page = extract_emails(html)
                    if found_keywords:
                        print(f"URL: {url}")
                        print(f"Title: {title}")
                        print(f"Keywords found: {', '.join(found_keywords)}")
                        print(f"Emails found: {', '.join(set(emails_in_page))}")
                        print("---------------------------------------------")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {url}")
                print(e)
            except Exception as e:
                print(f"Error processing URL: {url}")
                print(e)
