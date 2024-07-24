"""
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.

"""
import requests
from lxml import html
import csv

def scrape_yahoo_finance_trending(url):
    # Set User-Agent header to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        tree = html.fromstring(response.content)
        
        
        table_rows = tree.xpath("//tr[contains(@class, 'simpTblRow')]")
        
        data = []
        for row in table_rows:
            try:
                symbol = row.xpath(".//td[@aria-label='Symbol']/a/text()")[0].strip()
                name = row.xpath(".//td[@aria-label='Name']/text()")[0].strip()
                last_price = row.xpath(".//td[@aria-label='Last Price']/fin-streamer/text()")[0].strip()
                market_time = row.xpath(".//td[@aria-label='Market Time']/fin-streamer/text()")[0].strip()
                change = row.xpath(".//td[@aria-label='Change']/fin-streamer/span/text()")[0].strip()
                percent_change = row.xpath(".//td[@aria-label='% Change']/fin-streamer/span/text()")[0].strip()
                volume = row.xpath(".//td[@aria-label='Volume']/fin-streamer/text()")[0].strip()
                market_cap = row.xpath(".//td[@aria-label='Market Cap']/fin-streamer/text()")[0].strip()

                data.append({
                    'Symbol': symbol,
                    'Name': name,
                    'Last Price': last_price,
                    'Market Time': market_time,
                    'Change': change,
                    '% Change': percent_change,
                    'Volume': volume,
                    'Market Cap': market_cap
                })
            except IndexError as e:
                print(f"Failed to extract data from row: {e}")
        
        return data
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def save_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    url = "https://finance.yahoo.com/trending-tickers/"
    data = scrape_yahoo_finance_trending(url)
    
    if data:
        csv_filename = "yahoo_finance_trending.csv"
        save_to_csv(data, csv_filename)
        print(f"Data successfully scraped and saved to {csv_filename}")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()
