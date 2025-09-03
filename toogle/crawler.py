# import necessary libraries
import requests
from bs4 import BeautifulSoup

# define the seed url
url = "https://www.google.com"

# send a HTTP request to the url
response = requests.get(url)

# parse the HTML content of the page
hmtl_content = response.text
soup = BeautifulSoup(hmtl_content, 'html.parser')

# discovering and saving links inside the HTML content

links = [] # creating a list where the urls to scan will go
for a_tag in soup.find_all('a'):
    href = a_tag.get('href')
    if href: # checking that href actually exists
        links.append(href)

print("Discovered Links: ")
print(*links)
