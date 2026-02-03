# task: given a website of an company/individual, create a brochure for it
from openai import OpenAI
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=api_key)

# utils
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}


def fetch_website_links(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get the domain of the input URL
    base_domain = urlparse(url).netloc
    print(f"Base domain: {base_domain}")  # Debug: check domain

    links = []
    all_links = soup.find_all("a")
    # Debug: check if any links found
    print(f"Found {len(all_links)} total <a> tags")

    for link in all_links:
        href = link.get("href")
        if href:
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(url, href)
            # Parse the absolute URL
            parsed = urlparse(absolute_url)

            # Debug: see all links
            print(f"Link: {href} -> {absolute_url} (domain: {parsed.netloc})")

            # Only include HTTP/HTTPS links from the same domain
            if parsed.scheme in ('http', 'https') and parsed.netloc == base_domain:
                links.append(absolute_url)

    return links


def fetch_website_contents(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.get_text()


# steps:
# 1. scrape the website for all links
website = "https://huggingface.co"
links = fetch_website_links(website)

# 2, identify the most relevant links using ai
system_prompt = "You are a helpful assistant that identifies the most relevant links on a website for a brochure."
user_prompt = f"""
# Here are the links on the website {website}: {links}
# Please identify the most relevant links for a brochure.
# Reply in JSON format.
# Example: 
{{
    "links": [
        {{"type": "about page", "url": "https://full.url/goes/here/about"}},
        {{"type": "careers page", "url": "https://another.full.url/careers"}}
    ]
}}
"""

response = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    response_format={"type": "json_object"}
)

result = json.loads(response.choices[0].message.content)
print(result)
# # 3. scrape the most relevant links for the content
brochure_text = ""
for link in result["links"]:
    print(f"Scraping {link['url']}, type: {link['type']}")
    contents = fetch_website_contents(link["url"])
    brochure_text += f"## {link['type']}\n\n{contents}\n\n"


# # 4. generate brochure using ai as md format
system_prompt = "You are a helpful assistant that generates a brochure for a company/individual."
user_prompt = f"""
# Here is the brochure text: {brochure_text}
# Please generate a brochure for a company/individual.
# Reply in markdown format.
"""
response = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
print(response.choices[0].message.content)
# output in file md
with open("week1/brochure.md", "w") as f:
    f.write(response.choices[0].message.content)
