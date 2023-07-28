from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import pandas as  pd
import re

import numpy as np
from datetime import datetime, date

# to run in cmd by adding arg
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--chromedriver_path', type=str, help="Check where the Chromedriver is in your PC and share the path")
args = parser.parse_args()

def scroll_to_current_endheight(driver): 
    '''module to scroll until end of the current page height is reached'''
    
    time.sleep(1)  # Allow seconds for the web page to open
    scroll_pause_time = 2.1 
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if ((screen_height) * i > scroll_height):
            break


def ready_page(driver, url) :
    '''all the tedious work to get dynamic page fully loaded to the end before executing data scraping procedure'''
    driver.get(url)
    driver.maximize_window() 
    scroll_to_current_endheight(driver)
    
    # click button to show more :
    show_more_button = driver.find_element(By.XPATH, "//a[@id='load-button']") 
    show_more_button.click()   

    # Now we can fully load
    scroll_to_current_endheight(driver)


def create_csv(data_rows_list, csv_name : str) :
    df = pd.DataFrame(data_rows_list)
    df.to_csv(csv_name, index=False)

def main():
    webdriver_path = args.chromedriver_path
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    ''' "AI trend dataset" - dynamic scraping Module 1 :'''
    #fully load dynamic page first:
    url = f"https://topstartups.io/?industries=Artificial+Intelligence&sort=valuation"
    driver = webdriver.Chrome(webdriver_path, chrome_options=chrome_options)
    ready_page(driver, url)

    # Scraping: 
    ai_data = []

    startups = driver.find_elements(By.CSS_SELECTOR, 'div.col-12.col-md-6.col-xl-4.infinite-item') 

    for startup in startups:
        
        name_element = startup.find_element(By.CSS_SELECTOR, 'div.col-8.col-md-9').find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")
        name = name_element.text

        header_2 = startup.find_element(By.ID, 'item-card-filter').find_elements(By.TAG_NAME, "p")[0]
        categories = header_2.find_elements(By.TAG_NAME, "span")
        # finding category :
        for id, category in enumerate(categories):
            row = {}
            if len(category.text)==0 or ("Artificial Intelligence" in category.text): continue
            else:   
                row['Startup'] = name
                row['AI field'] = category.text
                print(row)
                ai_data.append( row )

    print(ai_data)

    driver.close()
    create_csv( ai_data, "AI_field_trend_dataset.csv")



    ''' "Top Startups dataset" dynamic scraping Module 2 :'''
    driver = webdriver.Chrome(webdriver_path, chrome_options=chrome_options)
    url = f"https://topstartups.io/?sort=valuation"
    ready_page(driver, url)

    #scraping:
    startup_data = []

    startups = driver.find_elements(By.CSS_SELECTOR, 'div.col-12.col-md-6.col-xl-4.infinite-item') 

    for id , startup in enumerate(startups):
        name_element = startup.find_element(By.CSS_SELECTOR, 'div.col-8.col-md-9').find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")
        name = name_element.text
        print(id,'### ',name)


        '''# scraping employees, founded year:'''
        card_header_2 = startup.find_element(By.ID, 'item-card-filter').find_elements(By.TAG_NAME, "p")[1]
        
        employees = card_header_2.find_elements(By.TAG_NAME, "span")[0].text.split()[0].split("-")
        #print(employees)
        if len(employees)==2 : 
            employees = employees[1]  
        else: 
            employees = employees[0]

        founded = card_header_2.find_elements(By.TAG_NAME, "span")[1].text.split(':')[1]
        print("employees, founded serially: ",employees, "," ,founded)



        '''# scraping value worth information  :'''
        card_header_3 = startup.find_element(By.ID, 'item-card-filter').find_elements(By.TAG_NAME, "p")[2]
        funding_elements = card_header_3.find_elements(By.TAG_NAME, "span")

        def process_currency(value):
            '''if billion(B) or in thousand(K), convert to million for better scaling. 
            otherwise data already is in million. processed accordingly'''
            
            if 'B' in value:
                value = value.strip('$B')
                value = int( float(value) * 1000.0 )
            elif 'K' in value:
                value = value.strip('$K')
                value = float(value) / 1000.0  
            else: value = value.strip('$M')

            return value

        value = 0
        for element in funding_elements: #capture valuation worth
            if("valuation" in element.text):
                value = element.text.split()[0]
                value = process_currency(value)
                print("valuation: M",value)

        if(value==0): #if valuation worth not provided, then capture funding round capital
            for element in funding_elements:
                if '$' in element.text:
                    value = element.text
                    value = value[value.find('$'):].split()[0]
                    value = process_currency(value)
                    print("funding round: M",value)
        

        '''# scrap locations :'''
        location = card_header_2.text.replace("\n",'').split(':')[2]
        match = re.search(r"([0-9]+)", location) 
        location = location [1: match.start()]
        
        country = location.split(',')[-1]
        print(country[1:], "|" ,location)


        '''# scrap technologies: '''
        card_header_1 = startup.find_element(By.ID, 'item-card-filter').find_elements(By.TAG_NAME, "p")[0]
        categories = card_header_1.find_elements(By.TAG_NAME, "span")
        
        technologies = ""
        for category in categories:
            if len(category.text)==0 : continue
            else:   technologies = technologies + category.text + ", "
        technologies = technologies[:-2]
        print(technologies)
        
        '''# scraping URls : '''
        startup_url = startup.find_element(By.ID, 'startup-website-link').get_attribute('href')
        image_url =  startup.find_element(By.TAG_NAME, "img").get_attribute('src')

        print()

        #enter data to dictionary:
        row_data = {}
        row_data["Startup"]=name
        row_data["Valuation (in Millions)"]=value
        row_data["Employees(estimate)"]=employees
        row_data["Founded"]=founded
        row_data["Country"]=country
        row_data["HQ Location"]=location
        row_data["Technologies"]=technologies
        row_data["Website URL"]=startup_url
        row_data["image URL"]=image_url
        
        startup_data.append( row_data )

    driver.close()
    create_csv(startup_data, "top_startups_details.csv")



    ''' "Software Engineers in Startups dataset" dynamic scraping Module 3 :'''
    driver = webdriver.Chrome(webdriver_path, chrome_options=chrome_options)
    url = f"https://topstartups.io/startup-salary-equity-database/?title=software+engineer"
    ready_page(driver, url)
    driver.implicitly_wait(5)

    se_data = [] #software engineer row data collection 

    def fetch_table_data(driver):
        tr = driver.find_elements(By.TAG_NAME, "tr")
        tr.pop(0) # this tr doesn't contain relevant data 
        
        for record in tr: 
            td =  record.find_elements(By.TAG_NAME, "td")
            row = {}
            row['Position title'] = td[0].get_attribute('innerHTML')
            row['Salary($)'] = td[1].find_element(By.TAG_NAME, "span").get_attribute('innerHTML').strip('$').replace(',', '')
            row['Years in Startup'] = td[6].get_attribute('innerHTML')
            row['Total Experience( Year)'] = td[5].get_attribute('innerHTML')

            print(row)
            se_data.append(row)


    def button_click(xpath_string) : 
        button = driver.find_element(By.XPATH, xpath_string)
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)

    # 1 click sorts low years to high. click again to sort high to low 
    # sort according to year in startup : 
    button_click('//*[@id="mydatatable"]/thead/tr/th[7]') 
    button_click('//*[@id="mydatatable"]/thead/tr/th[7]')

    fetch_table_data(driver)

    # click next button and scraping data
    for i in range(2,51):  
        button_click('//*[@id="mydatatable_next"]')
        fetch_table_data(driver)

    driver.close()
    create_csv(se_data, 'SE_in_startups_dataset.csv')



    ''' # Data processing : '''
    # import numpy as np
    # from datetime import datetime, date

    df = pd.read_csv("Top_startups_details_dataset.csv")

    df.info()

    df['Year in Business'] = df['Founded'].apply(lambda year: (date.today().year - year) )

    display(df)

    df.to_csv('Top_startups_details_dataset_complete.csv', index = False)

    return



if __name__ == "__main__":
    main()