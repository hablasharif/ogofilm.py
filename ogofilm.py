import streamlit as st
import requests
import random
from bs4 import BeautifulSoup
from lxml import html

# User agents to mimic different browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/94.0.992.50",
]

# Define a function to extract a link from a URL
def extract_link(url):
    try:
        # Check if the URL contains the specified text
        if "https://expeditesimplicity.com/safe.php?link=" in url:
            # Extract the part after the specified text
            link = url.split("https://expeditesimplicity.com/safe.php?link=")[1]
            return link
        else:
            # Create a custom session with a random user agent
            session = requests.Session()
            session.verify = False
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            session.headers.update(headers)

            # Send an HTTP GET request to the URL with retries
            for _ in range(3):
                response = session.get(url)
                if response.status_code == 200:
                    # Parse the HTML content of the page
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find the element with the data-drive attribute
                    episode_item = soup.find('li', {'data-drive': True})

                    # Extract the URL from the data-drive attribute
                    if episode_item:
                        link = episode_item['data-drive']
                        return link

            return None
    except Exception as e:
        return None

# Define a function to fetch and display the source code of a URL using dynamically extracted XPath
def show_source_code(link):
    try:
        # Create a custom session with a random user agent
        session = requests.Session()
        session.verify = False
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        session.headers.update(headers)

        # Send an HTTP GET request to the link with retries
        for _ in range(3):
            response = session.get(link)
            if response.status_code == 200:
                # Parse the HTML content of the page using lxml
                tree = html.fromstring(response.content)

                # Use XPath expression to find all href URLs
                href_urls = tree.xpath('//a/@href')
                if href_urls:
                    st.subheader("Href URLs Extracted Using Dynamically Detected XPath:")
                    for url in href_urls:
                        # Split the URL by "=" and print the part after "="
                        parts = url.split("=")
                        if len(parts) > 1:
                            st.write(parts[1])
                    return

        st.error("Failed to fetch href URLs using dynamically detected XPath after multiple attempts.")
    except Exception as e:
        st.error("An error occurred while fetching the content.")

# Define the Streamlit app
def main():
    st.title("Link Extractor")

    # User input for multiple URLs
    urls = st.text_area("Enter multiple URLs (one URL per line):")

    if st.button("Extract Links"):
        urls_list = urls.split('\n')
        for url in urls_list:
            url = url.strip()
            if url:
                extracted_link = extract_link(url)
                if extracted_link:
                    st.success(f"Extracted Link from {url}:")
                    st.write(extracted_link)
                    show_source_code(extracted_link)
                else:
                    st.error(f"Link not found on the page: {url}")

if __name__ == "__main__":
    main()
