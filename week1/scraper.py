from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_vietstock_contents(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the article title (usually in an <h1> tag)
        title = soup.find('h1').get_text(
            strip=True) if soup.find('h1') else "No title found"

        # Get the main content (Vietstock usually puts content in specific div classes)
        # You might need to inspect the page to find the exact class name
        content = soup.find('div', class_='article-content')

        if content:
            text_content = content.get_text(separator='\n', strip=True)
        else:
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            text_content = '\n'.join([p.get_text() for p in paragraphs])

        return f"TITLE: {title}\n\n{text_content}"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
