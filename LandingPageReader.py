import requests
from bs4 import BeautifulSoup
import time
import json


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
    Fetches the content of the URL with retries and timeouts.
    """
    for attempt in range(self.max_retries + 1):  # Ensure colon after loop condition
        try:
            # Ensure URL has a trailing slash for requests library (if not already present)
            # if not self.url.endswith("/"):
            #     self.url += "/"
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()  # Raise exception for unsuccessful requests
            self.content = response.content
            # Check content type (HTML or JSON) and set data type accordingly
            content_type = response.headers.get("Content-Type")
            if content_type and "json" in content_type.lower():
                self.data_type = "json"
            else:
                self.data_type = "html"
            return  # Successful retrieval, exit the loop
        except requests.exceptions.RequestException as e:
            if attempt == self.max_retries:
                print(f"Error retrieving data after {self.max_retries} attempts: {e}")
                return  # All retries exhausted, exit the loop
            else:
                print(f"Error retrieving data (attempt {attempt+1}/{self.max_retries}): {e}")
                time.sleep(2)  # Wait 2 seconds before retry

  def get_categorized_links(self):
            """
            Parses the content, extracts links (if applicable), and categorizes them.
            """
            if self.content is None:
                self.retrieve_page()

            if self.content:
                if self.data_type == "html":  # Handle HTML content
                    soup = BeautifulSoup(self.content, "html.parser")
                    categorized_links = {}
                    for a in soup.find_all("a", href=True):
                        link = a["href"]
                        # Handle relative URLs (starting without http or https)
                        if not link.startswith("http"):
                            link = self.url + link
                        category = self.categorize_link(link, a.text.lower())
                        if category:
                            categorized_links.setdefault(category, []).append(link)
                    return categorized_links
                elif self.data_type == "json":  # Handle JSON content
                    json_data = json.loads(self.content)
                    links = json_data.get("links")  # Access the list of links objects
                    if links:
                      categorized_links = {}
                      for link in links:
                          category = link.get("type")  
                          if category:
                              categorized_links.setdefault(category, []).append(link.get("href"))
                      return categorized_links  # Now return categorized links
                    else:
                      print("No links found in JSON data")
                      return {}
                else:
                    print(f"Unsupported data type: {self.data_type}")
                    return {}  # Return empty dictionary for unsupported data types
            else:
                return {}  # Return empty dictionary if no content retrieved

              
        
          

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
