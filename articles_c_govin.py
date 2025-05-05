import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["ipssi-scrapping"]
articles_collection = db["articles"]

def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles_data = []

        navbar = soup.find('nav')
        if navbar:
            nav_links = navbar.find_all('a', href=True)
            for nav_link in nav_links:
                section_url = nav_link['href']
                if not section_url.startswith('http'):
                    section_url = requests.compat.urljoin(url, section_url)

                for page in range(1, 3):
                    paginated_url = f"{section_url}/page/{page}"
                    category = nav_link.get_text(strip=True) if nav_link else None

                    print(f"--- Scraping Articles in page {page} of category : {category} ---")
                    try:
                        section_response = requests.get(paginated_url, headers=headers)
                        section_response.raise_for_status()
                        section_soup = BeautifulSoup(section_response.text, 'html.parser')

                        section_articles = section_soup.find_all('article')
                        if not section_articles:
                            break

                        for article in section_articles:
                            title = article.find('h3', class_='entry-title').get_text(strip=True) if article.find('h3', class_='entry-title') else None
                            thumbnail = article.find('img', class_='attachment-thumbnail') if article.find('img', class_='attachment-thumbnail') else None
                            thumbnail = thumbnail['data-lazy-src'] if thumbnail and 'data-lazy-src' in thumbnail.attrs else None
                            content = None
                            sub_category = section_soup.find('span', class_='favtag').get_text(strip=True) if section_soup.find('span', class_='favtag') else None
                            summary = None
                            date = None
                            author = None
                            images = []

                            link = article.find('header', class_='entry-header').find('a')['href'] if article.find('header', class_='entry-header') and article.find('header', class_='entry-header').find('a') and 'href' in article.find('header', class_='entry-header').find('a').attrs else None
                            if link:
                                try:
                                    article_response = requests.get(link, headers=headers)
                                    article_response.raise_for_status()
                                    article_soup = BeautifulSoup(article_response.text, 'html.parser')

                                    article_summary_div = article_soup.find('div', class_='article-hat')
                                    if article_summary_div:
                                        summary = article_summary_div.find('p').get_text(strip=True) if article_summary_div.find('p') else None

                                    author = article_soup.find('span', class_='byline').get_text(strip=True)

                                    date_element = article_soup.find('time', class_='entry-date')
                                    if date_element and 'datetime' in date_element.attrs:
                                        date = date_element['datetime']
                                        date = date[:10]

                                    article_content = article_soup.find('div', class_='entry-content')
                                    if article_content:
                                        content = ' '.join(p.get_text(strip=True) for p in article_content.find_all('p'))

                                    image_tags = article_soup.find_all('img')
                                    for img in image_tags:
                                        img_url = img.get('data-lazy-src')
                                        img_caption = img.get('alt') or img.get('title') or None
                                        if img_url:
                                            images.append({"url": img_url, "caption": img_caption})

                                except requests.exceptions.RequestException as e:
                                    print(f"Error fetching the article URL: {e}")

                            articles_data.append({
                                "title": title,
                                "thumbnail": thumbnail,
                                "category": category,
                                "sub_category": sub_category,
                                "summary": summary,
                                "author": author,
                                "date": date,
                                "images": images,
                                "content": content,
                            })

                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching the section URL: {e}")
        print(f"Total Articles: {len(articles_data)}")
        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []


url = "https://www.blogdumoderateur.com/"
articles = fetch_articles(url)

for i, article in enumerate(articles, 1):
    articles_collection.insert_one(article)
