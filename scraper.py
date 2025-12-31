import requests
from bs4 import BeautifulSoup

def scrape_hacker_news():
    """
    Scrapes the Hacker News homepage and prints the titles and links of the articles.
    """
    url = "https://news.ycombinator.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the story links
    storylinks = soup.select('.titleline > a')

    if not storylinks:
        print("No story links found. The website structure might have changed.")
        return

    print("Hacker News Top Stories:")
    for i, link in enumerate(storylinks, 1):
        title = link.get_text(strip=True)
        href = link.get('href')
        print(f"{i}. {title}")
        print(f"   Link: {href}")

if __name__ == "__main__":
    scrape_hacker_news()
