import pytest
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_login_with_valid_data(driver):

    driver.get("https://demo.opencart.com/")
    # lấy ra my account element dưới phần footer
    my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")
    # thực hiện câu lệnh này để cuộn trang đến element được chỉ định
    driver.execute_script("arguments[0].scrollIntoView();", my_account_link)

    # xử lý popup đã ngăn chặn hành động click vào my account element
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
        )
        close_button.click()
    except Exception:
        pass  # Nếu không có popup, tiếp tục

    my_account_link.click()
    time.sleep(20)

    # truyền vào email và password
    driver.find_element(By.ID, "input-email").send_keys("testZoe@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("123456")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(3)

    # chọn ra subscriptions element để cuộn trang sao cho không bị mất logout element
    subscriptions = driver.find_element(By.XPATH, "//a[@class='list-group-item' and normalize-space()='Subscriptions']")
    driver.execute_script("arguments[0].scrollIntoView();", subscriptions)
    time.sleep(3)
    driver.find_element(By.XPATH, "//a[@class='list-group-item' and normalize-space()='Logout']").click()

    # Nếu sau khi click vào log out hiển thị Account Logout thì thành công
    account_header = driver.find_element(By.XPATH, "//h1[normalize-space()='Account Logout']")
    assert account_header.is_displayed()

def test_login_with_invalid_data(driver):

    driver.get("https://demo.opencart.com/")

    # lấy ra my account element dưới phần footer
    my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")
    # thực hiện câu lệnh này để cuộn trang đến element được chỉ định
    driver.execute_script("arguments[0].scrollIntoView();", my_account_link)
    # xử lý popup đã ngăn chặn hành động click vào my account element
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
        )
        close_button.click()
    except Exception:
        pass  # Nếu không có popup, tiếp tục

    my_account_link.click()
    time.sleep(20)
    # truyền vào email và password
    driver.find_element(By.ID, "input-email").send_keys("admin@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("1")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(3)
    # chọn ra message element
    error_message_element = driver.find_element(By.CSS_SELECTOR, ".alert.alert-danger.alert-dismissible")
    error_message = error_message_element.text
    time.sleep(3)
    # so sánh với nội dung của message đã lấy ra
    assert "Warning: No match for E-Mail Address and/or Password." in error_message

def test_form_submission(driver):

    driver.get("https://demo.opencart.com/")
    # lấy ra my return element dưới phần footer
    return_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/returns.add')]")
    # thực hiện câu lệnh này để cuộn trang đến element được chỉ định
    driver.execute_script("arguments[0].scrollIntoView();", return_link)

    # xử lý popup đã ngăn chặn hành động click vào return element
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
        )
        close_button.click()
    except Exception:
        pass  # Nếu không có popup, tiếp tục

    return_link.click()
    time.sleep(20)

    # truyền data vào form
    driver.find_element(By.ID, "input-firstname").send_keys("Zoe")
    driver.find_element(By.ID, "input-lastname").send_keys("Nguyen")
    driver.find_element(By.ID, "input-email").send_keys("testZoe@gmail.com")
    driver.find_element(By.ID, "input-telephone").send_keys("0123456789")
    driver.find_element(By.ID, "input-order-id").send_keys("11111")
    order_date = driver.find_element(By.ID, "input-date-ordered")
    driver.execute_script("arguments[0].scrollIntoView();", order_date)
    order_date.send_keys("2024-10-26")
    time.sleep(3)
    driver.find_element(By.ID, "input-product").send_keys("iphone")
    driver.find_element(By.ID, "input-model").send_keys("product 11")
    driver.find_element(By.XPATH, "//input[@name='return_reason_id' and @value='2']").click()
    driver.find_element(By.ID, "input-opened-yes").click()
    time.sleep(3)
    # chọn nút submit
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
    time.sleep(5)
    # Nếu sau khi click vào log out hiển thị Product Returns thì thành công
    product_returns = driver.find_element(By.XPATH, "//h1[normalize-space()='Product Returns']")
    assert product_returns.is_displayed()

def test_navigation(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(3)
    # Chọn vào Desktop element để chuyển sang trang Desktop
    desktop_menu = driver.find_element(By.LINK_TEXT, "Desktops")
    desktop_menu.click()
    mac_option = driver.find_element(By.LINK_TEXT, "Mac (1)")
    mac_option.click()
    time.sleep(10)

    # Chọn vào Laptops & Notebooks element để chuyển sang trang Laptops & Notebooks
    lap_note_menu = driver.find_element(By.LINK_TEXT, "Laptops & Notebooks")
    lap_note_menu.click()
    time.sleep(5)


    # Chọn vào Components element để chuyển sang trang Components
    components_menu = driver.find_element(By.LINK_TEXT, "Components")
    components_menu.click()
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Show All Components").click()
    time.sleep(5)

    # Chọn vào Tablets element để chuyển sang trang Tablets
    tablets_menu = driver.find_element(By.LINK_TEXT, "Tablets")
    tablets_menu.click()
    time.sleep(5)

    # Chọn vào Software element để chuyển sang trang Software
    tablets_menu = driver.find_element(By.LINK_TEXT, "Software")
    tablets_menu.click()
    time.sleep(5)

    # Chọn vào Phones & PDAs element để chuyển sang trang Phones & PDAs
    p_PDA_menu = driver.find_element(By.LINK_TEXT, "Phones & PDAs")
    p_PDA_menu.click()
    time.sleep(5)

    # Chọn vào Cameras element để chuyển sang trang Cameras
    p_PDA_menu = driver.find_element(By.LINK_TEXT, "Cameras")
    p_PDA_menu.click()
    time.sleep(5)

    # Chọn vào MP3 Players element để chuyển sang trang MP3 Players
    mp3_menu = driver.find_element(By.LINK_TEXT, "MP3 Players")
    mp3_menu.click()
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Show All MP3 Players").click()
    time.sleep(5)

def test_search_functionality(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(3)
    # lấy ô search và truyền vào keyword iphone để test cho trường hợp keyword hợp lệ
    search_element = driver.find_element(By.NAME, "search")
    search_element.clear()
    search_element.send_keys("iphone")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(10)

    # lấy hết tất cả các sản phẩm theo keyword
    product_items = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
    time.sleep(3)

    # lấy ô search và truyền vào khoảng trắng để test cho trường hợp keyword không hợp lệ
    my_account_link = driver.find_element(By.NAME, "search")
    my_account_link.clear()
    my_account_link.send_keys("")
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(3)
    # lấy dòng text khi tìm kiếm bằng khoảng trắng
    message = driver.find_element(By.XPATH, "//p[normalize-space()='There is no product that matches the search criteria.']")
    # nếu danh sách sản phẩm > 0 và lấy được dòng text thì mới pass search functionality
    assert len(product_items) > 0 and message.is_displayed(), "Không tìm thấy sản phẩm."

def test_addtoCart(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(3)
    # thêm sản phẩm bằng cách tìm từ khóa
    my_account_link = driver.find_element(By.NAME, "search")
    my_account_link.clear()
    my_account_link.send_keys("iphone")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(5)

    # lấy ra danh sách sản phẩm và cuộn trang đến sản phẩm hiển thị đầu tiên
    product_items = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
    driver.execute_script("arguments[0].scrollIntoView();", product_items[0])
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "iPhone").click()
    time.sleep(5)
    # xóa ô quantity và nhập số lượng sau đó chọn thêm sản phẩm
    quantity = driver.find_element(By.ID, "input-quantity")
    quantity.clear()
    quantity.send_keys("2")
    time.sleep(5)
    driver.find_element(By.ID, "button-cart").click()
    time.sleep(10)
    # sau khi thêm sản phẩm thì chọn vào nút giỏ hàng để xem giỏ hàng thu nhỏ bên góc trên phải
    cart_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-inverse.btn-block.dropdown-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", cart_button)
    cart_button.click()
    time.sleep(3)
    # chọn vào nút View Cart để chuyển qua trang chi tiết giỏ hàng
    driver.find_element(By.CSS_SELECTOR, ".fa-solid.fa-cart-shopping").click()
    time.sleep(5)
    # lấy tên sản phẩm vừa thêm vào giỏ hàng
    td_element = driver.find_element(By.CSS_SELECTOR, "td.text-start.text-wrap")
    td_text = td_element.text
    # so sánh xem tên sản phẩm đã đúng hay chưa
    assert td_text == "iPhone"

def test_checkout(driver):
    driver.get("https://demo.opencart.com/")
    # đăng nhập vào tài khoản đã có địa chỉ sẵn trước khi thanh toán
    my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'route=account/account')]")

    driver.execute_script("arguments[0].scrollIntoView();", my_account_link)

    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close-button-class')]"))
        )
        close_button.click()
    except Exception:
        pass  # Nếu không có popup, tiếp tục

    my_account_link.click()
    time.sleep(10)
    driver.find_element(By.ID, "input-email").send_keys("testZoe@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("123456")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(3)
    # thêm sản phẩm vào giỏ hàng bằng cách tìm từ khóa
    my_account_link = driver.find_element(By.NAME, "search")
    my_account_link.clear()
    my_account_link.send_keys("iphone")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(10)

    product_items = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
    driver.execute_script("arguments[0].scrollIntoView();", product_items[0])
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "iPhone").click()
    time.sleep(5)
    quantity = driver.find_element(By.ID, "input-quantity")
    quantity.clear()
    quantity.send_keys("2")
    time.sleep(3)
    driver.find_element(By.ID, "button-cart").click()
    time.sleep(10)
    # sau khi thêm sản phẩm thì chọn vào nút giỏ hàng để xem giỏ hàng thu nhỏ bên góc trên phải
    cart_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-inverse.btn-block.dropdown-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", cart_button)
    cart_button.click()
    time.sleep(3)
    # chọn vào checkout element
    driver.find_element(By.CSS_SELECTOR, ".fa-solid.fa-share").click()
    time.sleep(5)
    # chọn địa chỉ đã có sẵn trước đó
    select = Select(driver.find_element(By.CSS_SELECTOR, "#input-shipping-address"))
    select.select_by_value("561")
    # chọn phương thức giao hàng
    driver.find_element(By.ID, "button-shipping-methods").click()
    time.sleep(5)
    driver.find_element(By.ID, "input-shipping-method-flat-flat").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='text-end']/button[@id='button-shipping-method']").click()
    # chọn phương thức thanh toán
    time.sleep(7)
    driver.find_element(By.ID, "button-payment-methods").click()
    time.sleep(3)
    driver.find_element(By.ID, "input-payment-method-cod-cod").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='text-end']/button[@id='button-payment-method']").click()
    # cuộn trang để có thể chọn vào confirm button
    td_element = driver.find_element(By.XPATH, "//td[@class='text-start' and text()='Product Name']")
    driver.execute_script("arguments[0].scrollIntoView();", td_element)
    time.sleep(3)
    driver.find_element(By.ID, "button-confirm").click()
    time.sleep(3)
    # sẽ lấy được thông báo nếu đơn hàng đã được đặt
    account_header = driver.find_element(By.XPATH, "//h1[normalize-space()='Your order has been placed!']")
    assert account_header.is_displayed()

def test_data_validation(driver):
    driver.get("https://demo.opencart.com/")
    # thêm sản phẩm bằng cách tìm từ khóa
    my_account_link = driver.find_element(By.NAME, "search")
    my_account_link.clear()
    my_account_link.send_keys("iphone")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-light.btn-lg").click()
    time.sleep(10)

    product_items = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
    driver.execute_script("arguments[0].scrollIntoView();", product_items[0])
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "iPhone").click()
    time.sleep(5)
    quantity = driver.find_element(By.ID, "input-quantity")
    quantity.clear()
    # nhập random quantity để tính toán tổng tiền có chính xác hay không
    random_integer = random.randint(1, 100)
    random_integer_str = str(random_integer)

    quantity.send_keys(random_integer_str)
    time.sleep(3)
    # lấy giá hiển thị trong trang thông tin chi tiết sản phẩm
    price = driver.find_element(By.CLASS_NAME, "price-new")
    # tách để lấy phần giá
    numeric_value = float(price.text.replace("$", ""))

    driver.find_element(By.ID, "button-cart").click()
    time.sleep(10)
    # sau khi thêm sản phẩm thì chọn vào nút giỏ hàng để xem giỏ hàng thu nhỏ bên góc trên phải
    cart_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-inverse.btn-block.dropdown-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", cart_button)
    cart_button.click()
    time.sleep(3)
    # lấy ra tổng giá trị đã tính toán
    total_value_element = driver.find_element(By.XPATH, "//td[.='Total']/following-sibling::td")
    total_value = total_value_element.text

    # Lấy giá trị số từ chuỗi actual_value và làm tròn
    total = random_integer*numeric_value
    formatted_value = f"${total:,.2f}"
    # so sánh xem tổng giá trị có khớp khi lấy quantity nhân với giá sản phẩm hay không
    assert total_value == formatted_value, f"Expected {formatted_value} but got {total_value}"
