from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.text import MIMEText
import smtplib
import datetime
import time

class Browser:
    browser, service = None, None

    def __init__(self, driver: str) -> None:
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)

    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()

    def search_on_google(self, keywords: str):
        wait = WebDriverWait(self.browser, 10)  # Set the maximum wait time to 10 seconds
        search_bar = wait.until(EC.visibility_of_element_located((By.NAME, 'q')))  # Wait for the search bar element to be visible
        search_bar.clear()  # Clear any existing text in the search bar
        search_bar.send_keys(keywords)  # Enter the keywords
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))

        # Retrieve the search results
        search_results = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')

        # Analyze the search results and find the most relevant link
        most_relevant_link = None
        max_keyword_count = 0
        for result in search_results:
            link = result.find_element(By.CSS_SELECTOR, 'a') # finding a link
            link_text = link.text.lower()       # link text to lower case
            keyword_count = sum(keyword.lower() in link_text for keyword in keywords.split()) #compare how many words are similar to our text in link and sum to keywordcount
            if keyword_count > max_keyword_count: # we store the maxkeyword count in our variable and then compare links and store the link and keywords count for the link that has the most similarity to our text
                most_relevant_link = link
                max_keyword_count = keyword_count

        # Click on the most relevant link
        if most_relevant_link is not None:
            most_relevant_link.click()

    def close_popup(self):

        wait = WebDriverWait(self.browser, 10)

        wait.until(EC.visibility_of_element_located((By.ID, "country-modal-submit")))   # Close Popup

        button = self.browser.find_element(By.ID, "country-modal-submit")

        button.click()
        
       

        


    def check_title(self):
        product = "JAMIE LEATHER HARNESS CHELSEA BOOT"    # Check if title matches my keyword and return product availability

        wait = WebDriverWait(self.browser, 10)

      
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))

        title = self.browser.find_element(By.TAG_NAME, "h1")

        titleText = title.text

        if titleText == product:

            print("YEP Product is Found")
        else:
            print("Product Not Found")



    
    def check_size_exist(self):
       wait = WebDriverWait(self.browser, 10)
  
       wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-size")))
    
       button = self.browser.find_element(By.XPATH, "//button[@data-sku-code='190665474152']") #check size 8 by data-sku-code and check it's property purchasable. if it's true,
       is_purchasable = button.get_attribute("data-sku-purchasable")                           # It sends an email to me
    
       if is_purchasable == "true":
        print("Size 8 is purchasable.")
        self.sendEmail()

       else:
        print("Size 8 is not purchasable.")
      



    def sendEmail(self):
        message = MIMEText("The Doctor martens you want are available in Size 8")      # Send email using stmplib to start gmail server and send me an email 
        message['Subject'] = "PRODUCT AVAILABLE"
        message['From'] = "yagamikonooha@gmail.com"
        message['To'] = "achraf.layek1@gmail.com"


        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("yagamikonooha@gmail.com", "oqqwiyvuworhcjoc")
                server.sendmail("yagamikonooha@gmail.com", "achraf.layek1@gmail.com", message.as_string())
                print("Email Got sent")
        except smtplib.SMTPException as e:
            print("Error Sending Email", str(e))



    


        

        

        

# Example usage
if __name__ == "__main__":



    productName = "Doctor Martens JAMIE LEATHER HARNESS CHELSEA BOOTS " 

    browser = Browser('chromedriver.exe')

    browser.open_page("https://www.google.com")

    browser.search_on_google(productName)

    browser.close_popup()

    browser.check_title()

    browser.check_size_exist()



    # Continue with further actions on the clicked page

    browser.close_browser()

    file  = open(r'C:\Users\ACHRAF\Projects\Python Web Scraper')

    file.write(f'{datetime.datetime.now()} - Script Ran')
