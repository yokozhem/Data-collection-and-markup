from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

def login_to_target(driver, username, password):
    driver.get("https://www.target.com/")
    time.sleep(3)  # Ждем загрузки страницы

    # Нажимаем на кнопку входа
    login_button = driver.find_element(By.XPATH, "//a[@data-test='accountLink']")
    login_button.click()
    time.sleep(3)  # Ждем загрузки страницы входа

    # Вводим логин и пароль
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    email_field.send_keys(username)
    password_field.send_keys(password)
    
    # Нажимаем на кнопку логина
    login_submit_button = driver.find_element(By.ID, "login")
    login_submit_button.click()
    time.sleep(5)  # Ждем завершения процесса входа

def scrape_target_cart(url, username, password):
    # Указываем путь к веб-драйверу
    driver_path = 'path/to/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Выполняем логин
    login_to_target(driver, username, password)

    # Переходим на страницу корзины
    driver.get(url)
    time.sleep(5)  # Ждем загрузки страницы корзины

    # Извлекаем данные о товарах в корзине
    cart_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'CartItem__StyledCartItem')]")
    
    data = []
    for item in cart_items:
        try:
            # Извлекаем данные о каждом товаре
            product_name = item.find_element(By.XPATH, ".//a[contains(@class, 'CartItem__ProductName')]/span").text
            product_price = item.find_element(By.XPATH, ".//span[contains(@class, 'Price__StyledPrice')]").text
            product_quantity = item.find_element(By.XPATH, ".//span[contains(@class, 'CartItem__Quantity')]").text

            data.append({
                'Product Name': product_name,
                'Product Price': product_price,
                'Product Quantity': product_quantity
            })
        except Exception as e:
            print(f"Failed to extract data from item: {e}")

    driver.quit()
    return data

def save_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    url = "https://www.target.com/cart"
    username = "your_username"
    password = "your_password"
    data = scrape_target_cart(url, username, password)
    
    if data:
        csv_filename = "target_cart.csv"
        save_to_csv(data, csv_filename)
        print(f"Data successfully scraped and saved to {csv_filename}")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()
