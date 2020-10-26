from selenium import webdriver 


class Screenshots:

    def __init__(self,file_path):
        
        option = webdriver.FirefoxOptions()
        option.add_argument("--headless")
        self.driver = webdriver.Firefox(options=option)
        self.driver.header_overrides = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }

        self.file_path = file_path
       
    def capture(self,domain):

        underscore_domain = domain.replace('.','_')

        img_path = f"{self.file_path}/{underscore_domain}.png"
        url = f"https://{domain}"

        print(f"SnapShoting  the domains ---->         {url}                                                   ",end="\r")

        try:
            self.driver.get(url)
            self.driver.get_screenshot_as_file(img_path)
        except:
            pass


    @property
    def end(self):
        self.driver.quit()



        