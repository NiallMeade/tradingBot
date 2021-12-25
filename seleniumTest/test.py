from selenium import webdriver
import time as t
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Firefox(executable_path=r'/home/niall/Downloads/geckodriver')

username = ""
password = ""

driver.get("https://www.trading212.com/en/login")

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'submit-button_input__3s_QD')))

driver.find_element_by_name("email").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("submit-button_input__3s_QD").click()

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'portfolio-tab')))
t.sleep(3)

def buyValue():

    cycleCount = 0

    driver.find_element_by_class_name("portfolio-tab").click()
    driver.find_element_by_class_name("account-status-header-label").click()
    funds = driver.find_elements_by_class_name("formatted-price-part")

    print(len(funds))
    fundsText = []

    for f in funds:
        fundsText.append(f.text)
        # print(f.text)

    # print(len(fundsText))
    # print(fundsText)

    listLen = len(fundsText)

    freeFundsStr = "".join(fundsText[4:6])
    freeFundsStr = "".join(fundsText[listLen-5:listLen-3])
    portfolioFundsStr = "".join(fundsText[7:9])
    portfolioFundsStr = "".join(fundsText[listLen-2:listLen])
    totalFundsStr = "".join(fundsText[listLen-8:listLen-6])
    
    freeFunds = float(freeFundsStr)
    portfolioFunds = float(portfolioFundsStr)
    totalFunds = float(totalFundsStr)
    fundsRatio = freeFunds/totalFunds

    if totalFunds == freeFunds:
        value = freeFunds/3
        return value
    elif fundsRatio > 0.56 :
        value = freeFunds/2
        return value
    elif freeFunds > 1.5:
        value = freeFunds
        return value
    else:
        value = 0
        return value

for i in range(100) :
    print(buyValue())

driver.quit()
