# web-link-extractor
**LandingLens**
**Landing Page Link Extractor**

This Python script helps you analyze a website's landing page and categorize its links based on their content.

**Features:**

User-friendly: Prompts you for the landing page URL.
Robust: Handles retries and timeouts for unreliable network connections.
Categorization: Analyzes links and categorizes them as "Blog Post," "About," "Contact Us," or "Other."
Clear Output: Presents categorized links in a readable format.
Installation:

Ensure you have Python 3 and requests and beautifulsoup4 libraries installed:

Bash
pip install requests beautifulsoup4
Usage:

Run the script:

Bash
python landing_page_reader.py
Use code with caution.
Enter the URL of the landing page you want to analyze.

**Explanation:**

The script utilizes the requests library to fetch the landing page content and BeautifulSoup for parsing HTML. Here's a breakdown of the key functionalities:

LandingPageReader class:
Manages the URL, content retrieval, and link categorization.
Handles retries and timeouts for robust error handling.
Provides methods to retrieve content, categorize links, and display results.
get_user_input: Prompts the user for the landing page URL.
retrieve_page: Fetches the content of the landing page with retries and timeouts.
get_categorized_links: Parses the content, extracts links, and categorizes them based on heuristics in the URL and anchor text (can be further customized for more specific rules).
categorize_link: Assigns a category ("Blog Post," "About," "Contact Us," or "Other") to a link based on URL and text analysis.
display_categorized_links: Prints the extracted links organized by category.

**Further Improvements:**

Implement error handling for potential exceptions during parsing.
Provide options for specifying the maximum number of retries and timeout values.
