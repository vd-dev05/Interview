from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# Nhập số trang bắt đầu muốn lấy ASIN
choice = int(input("Nhập số trang muốn lấy ASIN: "))

chrome_options = Options()
chrome_options.add_argument("--disable-web-security")  # Bỏ qua CSP
chrome_options.add_argument("--disable-site-isolation-trials")  # Fix lỗi tải CSS
# chrome_options.add_argument("--headless")  # Chạy chế độ không giao diện (tuỳ chọn)
service = Service(ChromeDriverManager().install())

# Cookie mẫu (đảm bảo cookie này hợp lệ cho phiên làm việc của bạn)
cookie = {
    'name': 'AMCV_7742037254C95E840A4C98A6@AdobeOrg',
    'value': '1585540135|MCIDTS|20151|MCMID|40915963003577767423945822436398070887|MCAAMLH-1741564971|9|MCAAMB-1741564971|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1740967371s|NONE|MCAID|NONE|vVersion|4.4.0',
    'domain': '.amazon.com',
    'path': '/',
    'expiry': 1738534971  # thời gian hết hạn dạng Unix timestamp nếu có
}

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.amazon.com")
sleep(5)
driver.add_cookie(cookie)
sleep(10)

# Load trang tìm kiếm với trang 'choice'
driver.get(f"https://www.amazon.com/s?k=t-shirts")
sleep(10)

while True:
    print("Đang reset cookie...")
    driver.refresh()
    
    # Thử click vào banner nếu có (giả sử banner có <img id="d">)
    try:
        image = driver.find_element(By.ID, "d")
        # Lấy phần tử cha của <img> (giả sử đó là thẻ <a>)
    
        link = image.find_element(By.XPATH, "/html/body/div/div/a")
        link.click()
        # Sau khi click, quay lại trang tìm kiếm hiện tại
        driver.get(f"https://www.amazon.com/s?k=t-shirts&page={choice}")
        sleep(3)
    except Exception as e:
        print("Không tìm thấy banner hoặc không thể click:", e)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Tìm tất cả các sản phẩm có thuộc tính data-asin không rỗng
    product_divs = soup.find_all(lambda tag: tag.has_attr('data-asin') and tag.get('data-asin').strip() != "")
    
    filtered_products = []
    min_rating = 4.0
    min_reviews = 100
    
    for div in product_divs:
        # Loại bỏ sản phẩm quảng cáo (nếu container chứa chữ "Sponsored")
        if div.find(text=lambda t: "Sponsored" in t):
            continue
        
        asin = div.get('data-asin')
        
        # Lấy điểm đánh giá (ví dụ chuỗi: "4.5 out of 5 stars")
        rating_elem = div.find("span", {"class": "a-icon-alt"})
        if rating_elem:
            rating_text = rating_elem.get_text().strip()
            match = re.search(r"([\d.]+)\s+out of 5", rating_text)
            if match:
                rating = float(match.group(1))
            else:
                rating = 0
        else:
            rating = 0
        
        # Lấy số lượng đánh giá
        review_elem = div.find("span", {"class": "a-size-base"})
        if review_elem:
            review_text = review_elem.get_text().strip().replace(",", "")
            try:
                review_count = int(review_text)
            except ValueError:
                review_count = 0
        else:
            review_count = 0
        
        if rating >= min_rating and review_count >= min_reviews:
            filtered_products.append({
                "asin": asin,
                "rating": rating,
                "review_count": review_count
            })
    
    print(f"Các sản phẩm lọc được trên trang {choice}:")
    print(json.dumps(filtered_products, indent=2))
    
    text = input("Nhập 'a' để tăng trang, nhập 'b' để lưu vào json, nhập c để tìm các chi tiết sản phẩm để seo, không nhập để dừng: ")
    if text.strip().lower() == "a":
        choice += 1
        driver.get(f"https://www.amazon.com/s?k=t-shirts&page={choice}")
        sleep(10)
    elif text.strip().lower() == "b":
        with open("filtered_products.json", "w") as f:
            json.dump(filtered_products, f, indent=2)
        print("Đã lưu vào filtered_products.json")
    elif text.strip().lower() == "c":
        for product in filtered_products:
            asin = product["asin"]
            driver.get(f"https://www.amazon.com/dp/{asin}")
            sleep(5)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Tìm tên sản phẩm
            product_name_elem = soup.find("span", {"id": "productTitle"})
            if product_name_elem:
                product_name = product_name_elem.get_text().strip()
            else:
                product_name = "N/A"
            
            # Tìm giá sản phẩm
            product_price_elem = soup.find("span", {"id": "priceblock_ourprice"})
            if product_price_elem:
                product_price = product_price_elem.get_text().strip()
            else:
                product_price = "N/A"
            # Tìm chi tiết sản phẩm 
            details_title = soup.find("h3", class_="product-facts-title", string=lambda t: "Product details" in t)
            if details_title:
                ul = details_title.find_next("ul", class_="a-nostyle")
                product_details = {}
                if ul:
                    for li in ul.find_all("li"):
                         key_elem = li.find("div", class_="a-fixed-left-grid-col a-col-left")
                         key_text = key_elem.get_text(strip=True) if key_elem else ""
                         value_elem = li.find("div", class_="a-fixed-left-grid-col a-col-right")
                         value_text = value_elem.get_text(strip=True) if value_elem else ""
                         if key_text and value_text:
                              product_details[key_text] = value_text
            # Tìm mô tả sản phẩm
            product_description_elem = soup.find("div", {"id": "productDescription"})
            if product_description_elem:
                product_description = product_description_elem.get_text().strip()
            else:
                product_description = "N/A"
            
            print(f"Tên sản phẩm: {product_name}")
            print(f"Giá sản phẩm: {product_price}")
            print("Product Details:")
            for key, value in product_details.items():
                print(f"{key}: {value}")
            print(f"Mô tả sản phẩm: {product_description}")
            print("--------------------------------------------------")
            
            # Lưu thông tin sản phẩm
            product["name"] = product_name
            product["price"] = product_price
            product["description"] = product_description
        
        with open("filtered_products_with_details.json", "w") as f:
            json.dump(filtered_products, f, indent=2)
        print("Đã lưu vào filtered_products_with_details.json") 
    else:
        break

driver.quit()
