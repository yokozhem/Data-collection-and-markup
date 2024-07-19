from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import json

base_url = 'http://books.toscrape.com/catalogue/'
url = base_url + 'page-1.html'
page_counter = 1
data = []

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        book_data = {}

        # Extracting book title
        book_title = article.find('h3').find('a')
        book_data['title'] = book_title['title'] if book_title else ''

        # Extracting book price
        price_elem = article.find('p', class_='price_color')
        price_text = price_elem.text.strip() if price_elem else ''
        book_data['price'] = float(re.search(r'[\d.]+', price_text).group()) if price_text else 0.0

        # Extracting availability (quantity in stock)
        availability_elem = article.find('p', class_='instock availability')
        availability_text = availability_elem.text.strip() if availability_elem else ''
        qty_match = re.search(r'\d+', availability_text)
        book_data['quantity'] = int(qty_match.group()) if qty_match else 0

        # Extracting book description
        book_url = urllib.parse.urljoin(base_url, book_title['href']) if book_title else ''
        if book_url:
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.content, 'html.parser')
            product_description = book_soup.find('div', id='product_description')
            book_data['description'] = product_description.find_next('p').text.strip() if product_description else ''
        else:
            book_data['description'] = ''

        # Append the book data to the list
        data.append(book_data)

    # Checking for the next page link
    next_page = soup.find('li', class_='next')
    if next_page:
        url = urllib.parse.urljoin(base_url, next_page.find('a')['href'])
        page_counter += 1
        print(f'Processing page {page_counter}')
    else:
        break

# Save data to JSON file
with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f'Scraping completed. {len(data)} books scraped and saved to books_data.json')

