"""
Урок 6. Scrapy. Парсинг фото и файлов
Создайте новый проект Scrapy. Дайте ему подходящее имя и убедитесь, что ваше окружение правильно настроено для работы с проектом.
Создайте нового паука, способного перемещаться по сайту www.unsplash.com. Ваш паук должен уметь перемещаться по категориям фотографий и получать доступ к страницам отдельных фотографий.
Определите элемент (Item) в Scrapy, который будет представлять изображение. Ваш элемент должен включать такие детали, как URL изображения, название изображения и категорию, к которой оно принадлежит.
Используйте Scrapy ImagesPipeline для загрузки изображений. Обязательно установите параметр IMAGES_STORE в файле settings.py. Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. Каждая строка должна соответствовать одному изображению и содержать URL изображения, локальный путь к файлу (после загрузки), название и категорию.
"""
import scrapy
import os
import csv

class GratisographySpider(scrapy.Spider):
    name = "gratisography"
    allowed_domains = ["gratisography.com"]
    start_urls = ["https://gratisography.com/"]

    def __init__(self, *args, **kwargs):
        super(GratisographySpider, self).__init__(*args, **kwargs)
        self.csv_file = open('gratisography.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Image URL', 'Local File Path', 'Title', 'Category'])

    def close(self, reason):
        self.csv_file.close()
        super(GratisographySpider, self).close(reason)

    def parse(self, response):
        self.logger.info(f'Parsing URL: {response.url}')
        
        # Получаем ссылки на изображения на текущей странице
        for image_page in response.xpath("//article[not(@id='sstk-inline-ad')]/div//a/@href").extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

        # Ищем ссылку на следующую страницу и отправляем запрос
        next_page = response.xpath('//a[./i[contains(@class, "fa-long-arrow-alt-right")]]/@href').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f'Found next page URL: {next_page_url}')
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_image_page(self, response):
        self.logger.info(f'Parsing image page URL: {response.url}')
        full_image_url = response.xpath('//span[@itemprop="image"]/img[@itemprop="contentUrl"]/@src').extract_first()
        title = response.xpath('//h1/text()').extract_first() or 'No Title'
        
        # Извлекаем категорию из родительского div
        category = response.xpath('//span[@class="meta-title" and contains(text(), "Categories:")]/following-sibling::a[@rel="tag"]/text()').extract_first() or 'No Category'

        if full_image_url:
            full_image_url = response.urljoin(full_image_url)
            self.logger.info(f'Found image URL: {full_image_url}')
            filename = full_image_url.split('/')[-1]
            self.logger.info(f'Saving image with filename: {filename}')
            yield scrapy.Request(full_image_url, callback=self.save_image, meta={
                'filename': filename,
                'full_image_url': full_image_url,
                'title': title,
                'category': category
            })

    def save_image(self, response):
        filename = response.meta['filename']
        filepath = os.path.join('images', filename)
        self.logger.info(f'Saving image {filename} to {filepath}')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure the directory exists
        with open(filepath, 'wb') as f:
            f.write(response.body)
        self.logger.info(f'Image saved successfully: {filepath}')

        # Write image details to CSV
        self.csv_writer.writerow([
            response.meta['full_image_url'],
            filepath,
            response.meta['title'],
            response.meta['category']
        ])
