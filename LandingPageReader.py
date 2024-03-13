import requests
from bs4 import BeautifulSoup
import time

class LandingPageReader:
  """
  A class for retrieving landing pages and extracting categorized links.
  """

  def __init__(self):
    self.url = None
    self.content = None
    self.max_retries = 3  # Maximum number of retries for failed requests
    self.timeout = 10  # Timeout in seconds for requests

  def get_user_input(self):
    """
    Prompts the user to enter the URL of the landing page.
    """
    while True:
      self.url = input("Enter the URL of the landing page to analyze: ")
      if self.url.strip():  # Check if user entered a non-empty URL
        break
      print("Please enter a valid URL.")

  def retrieve_page(self):
    """
    Fetches the content of the landing page with retries and timeouts.
    """
    for attempt in range(self.max_retries + 1):
      try:
        # Ensure URL has a trailing slash for requests library (if not already present)
        if not self.url.endswith("/"):
          self.url += "/"
        response = requests.get(self.url, timeout=self.timeout)
        response.raise_for_status()  # Raise exception for unsuccessful requests
        self.content = response.content
        return  # Successful retrieval, exit the loop
      except requests.exceptions.RequestException as e:
        if attempt == self.max_retries:
          print(f"Error retrieving page after {self.max_retries} attempts: {e}")
          return  # All retries exhausted, exit the loop
        else:
          print(f"Error retrieving page (attempt {attempt+1}/{self.max_retries}): {e}")
          time.sleep(2)  # Wait 2 seconds before retry

  def get_categorized_links(self):
    """
    Parses the landing page content, extracts links, and categorizes them.
    """
    if self.content is None:
      self.retrieve_page()

    if self.content:
      soup = BeautifulSoup(self.content, "html.parser")
      categorized_links = {}
      for a in soup.find_all("a", href=True):
        link = a["href"]
        # Handle relative URLs (starting without http or https)
        if not link.startswith("http"):
          link = self.url + link  # Prepend base URL for relative links
        category = self.categorize_link(link, a.text.lower())  # Analyze link and text for category
        if category:
          categorized_links.setdefault(category, []).append(link)
      return categorized_links
    else:
      return {}

  def categorize_link(self, link, text):
    """
    Attempts to categorize a link based on heuristics in the URL and anchor text.
    """
    if "/blog/" in link or "blog" in text:
      return "Blog Post"
    elif "/about/" in link or ("about" in text and "about" in text):
      return "About"
    elif "/contact/" in link or ("contact" in text and ("us" or "form" in text)):
      return "Contact Us"
    else:
      return "Other"  # Unclassified link

  def display_categorized_links(self):
    """
    Prints the extracted links categorized by content type.
    """
    categorized_links = self.get_categorized_links()
    if categorized_links:
      for category, links in categorized_links.items():
        print(f"\nCategory: {category}")
        for link in links:
          print(link)
    else:
      print(f"No links found on {self.url}")


reader = LandingPageReader()
reader.get_user_input()
reader.display_categorized_links()
