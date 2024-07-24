import scrapy
from urllib.parse import urljoin

class BooksSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        base_url = 'http://books.toscrape.com/catalogue/'
        
        for article in response.xpath('//article[@class="product_pod"]'):
            book_data = {}

            # Извлечение названия книги
            book_title = article.xpath('.//h3/a/@title').get()
            book_data['title'] = book_title if book_title else ''

            # Извлечение цены книги
            price_text = article.xpath('.//p[@class="price_color"]/text()').get()
            book_data['price'] = float(price_text.strip()[1:]) if price_text else 0.0

            # Извлечение наличия (статус на складе)
            availability_text = article.xpath('.//p[@class="instock availability"]/text()').getall()
            # Объединение всех частей текста и удаление лишних пробелов
            availability_text = ' '.join([text.strip() for text in availability_text]).strip()
            # Для отладки: Выводим availability_text
            self.log(f'Availability text: "{availability_text}"')
            book_data['quantity'] = 'In stock' if 'In stock' in availability_text else 'Out of stock'

            # Извлечение ссылки на книгу
            book_url = article.xpath('.//h3/a/@href').get()
            book_url = urljoin(base_url, book_url) if book_url else ''
            
            if book_url:
                request = scrapy.Request(book_url, callback=self.parse_book_description)
                request.meta['book_data'] = book_data
                yield request

        # Переход на следующую страницу
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_book_description(self, response):
        book_data = response.meta['book_data']
        
        # Извлечение описания книги
        product_description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        book_data['description'] = product_description.strip() if product_description else ''
        
        yield book_data
    