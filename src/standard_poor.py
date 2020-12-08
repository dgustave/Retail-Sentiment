import pandas as pd
from selenium import webdriver                   
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def standardPoor():
    driver = webdriver.Firefox(executable_path= "geckodriver.exe")
    driver.maximize_window()
    driver.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    # Read Html to generate S&P 500 table: 
    table = driver.find_element_by_id("mw-content-text").get_attribute('innerHTML')
    tables  = pd.read_html(table)
    sp500_ticker_df = tables[0]

    vsymbol_df = sp500_ticker_df.loc[:, ['Symbol', 'Security', 'GICS Sector']]


    vsymbol_df.rename(columns = {'GICS Sector': 'Sector'}, inplace=True)


    driver.quit()
    return list(vsymbol_df['Symbol'])