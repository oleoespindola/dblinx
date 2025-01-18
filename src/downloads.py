import time

import os

from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

from .telegram import Telegram

LINX_USER = os.getenv('linx_user')
LINX_PASSWORD = os.getenv('linx_password')

SAV_USER = os.getenv('sav_user')
SAV_PASSWORD = os.getenv('sav_password')

LINX_URL = 'http://erp.microvix.com.br/'

class BaseDownload():
    def __init__(self, timeout: int, download_time: int, url: str, login_selector: dict, report_selector: dict, user: str, password: str, system: str):
        self.timeout = timeout
        self.download_time = download_time

        self.url = url

        self.login_selector = login_selector
        self.user = user
        self.password = password

        self.report_selector = report_selector
        self.system = system
        self.browser = webdriver.Firefox()

    def login(self):
        try:
            # Access the login page
            self.browser.get(self.url)

            self.browser.find_element(By.XPATH, self.login_selector['user']).send_keys(self.user)
            self.browser.find_element(By.XPATH, self.login_selector['password']).send_keys(self.password)

            self.browser.find_element(By.XPATH, self.login_selector['submit']).click()

            print(f'Login with susscess in {self.system} page')
        except WebDriverException:
            self.handle_error(f'Element not found {self.system} page')
        except Exception:
            self.handle_error(f'General error in {self.system} page')

    def navigate(self):
        try:
            time.sleep(self.timeout)

            for action in self.report_selector['actions']:
                if 'click' in action:
                    element = self.browser.find_element(By.XPATH, action['xpath'])
                    element.click()

                elif 'iframe' in action:
                    iframe = self.browser.find_element(By.XPATH, action['xpath'])
                    self.browser.switch_to.frame(iframe)

                elif 'input_date' in action:
                    fist_date = date.today() - timedelta(days=30)
                    element = self.browser.find_element(By.ID, action['xpath'])
                    element.clear()
                    element.send_keys(fist_date.strftime(f'%d-%m-%Y'))

                elif 'hover' in action:
                    hover_element = self.browser.find_element(By.CSS_SELECTOR, self.report_selector['export_button'])
                    action = ActionChains(self.browser)
                    action.move_to_element(hover_element).perform()

                else:
                    raise self.handle_error(f'key not valid for actions dict of {self.system}')
                
                time.sleep(self.timeout)
            
            print(f'Navigate with susscess in {self.system} page')
        except WebDriverException:
            self.handle_error(f'Element not found {self.system} page')
        except Exception:
            self.handle_error(f'General error in {self.system} page')
        
    def hendle_error(self, message: str):
        Telegram().send_message(message)

    def close_browser(self):
        self.browser.quit()
        print(f'Browser closed with susscess')

class EmployeeDownload(BaseDownload):
    def __init__(self, timeout: int, download_time: int):
        url = LINX_URL
        system = 'linx'
        login_selector = {
            'user': '//*[@id="f_login"]',
            'password': '//*[@id="f_senha"]',
        }
        user = LINX_USER
        password = LINX_PASSWORD
        actions = [
                {'element': '/html/body/div/div[3]/div/form/div/div/button/div'},
                {'element': '/html/body/div/div[3]/div/form/div/div/div/div[2]/ul/li[1]/a'},
                {'element': '//*[@id="btnselecionar_empresa"]'},
                {'element': '//*[@id="liModulo_0"]'},
                {'element': '/html/body/div[1]/aside/div/section/ul/li[2]/ul/li[5]/a'},
                {'iframe': '//*[@id="main"]'},
                {'element': '/html/body/div/section[1]/div[2]/div[2]/div[36]'},
                {'element': '/html/body/div/section[1]/div/div[3]/div[2]/div[2]/div[2]/button[2]'},
                {'element': '/html/body/div/div[1]/div[2]/div/div[1]/div'},
                {'element': '/html/body/div/div[1]/div[2]/div/div[1]/div/div[3]/ul/li[2]'},
                {'element': '/html/body/div/div[1]/div[1]/div[2]/div/button[4]'},
                {'hover': '#fm-tab-export > a:nth-child(1) > div:nth-child(1) > svg:nth-child(1)'},
                {'element': '#fm-tab-export-csv > a:nth-child(1) > div:nth-child(1) > svg:nth-child(1)'}
            ]
        super().__init__(timeout, download_time, url, login_selector, actions, user, password, system)
        self.download()

    def download(self):
        try:
            self.login()
            self.navigate()
        except WebDriverException as e:
            print(f'Element not found: {e}')
        except Exception as e:
            print(f'General error: {e}')
        finally:
            self.close_browser()

class SalesDownload(BaseDownload):
    def __init__(self, timeout: int, download_time: int):
        url = LINX_URL
        system = 'linx'
        login_selector = {
            'user': '//*[@id="f_login"]',
            'password': '//*[@id="f_senha"]',
        }
        user = LINX_USER
        password = LINX_PASSWORD
        actions = [
                {'element': '/html/body/div/div[3]/div/form/div/div/button/div'},
                {'element': '/html/body/div/div[3]/div/form/div/div/div/div[2]/ul/li[1]/a'},
                {'element': '//*[@id="btnselecionar_empresa"]'},
                {'element': '//*[@id="liModulo_0"]'},
                {'element': '/html/body/div[1]/aside/div/section/ul/li[2]/ul/li[5]/a'},
                {'iframe': '//*[@id="main"]'},
                {'element': '/html/body/div/section[1]/div[2]/div[2]/div[10]'},
                {'element': '/html/body/div/section[1]/div/div[3]/div[3]/div[2]/div[2]/button[2]'},
                {'input_date': 'datePickerRelatorioReceb'},
                {'element': '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/span'},
                {'element': '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[3]/ul/li[1]'},
                {'element': '/html/body/div[1]/div[1]/div[1]/div[2]/div/button[4]'},
                {'hover': '#fm-tab-export > a:nth-child(1) > div:nth-child(1) > svg:nth-child(1)'},
                {'element': '#fm-tab-export-csv > a:nth-child(1) > div:nth-child(1) > svg:nth-child(1)'}
            ]
        super().__init__(timeout, download_time, url, login_selector, actions, user, password, system)
        self.download()

    def download(self):
        try:
            self.login()
            self.navigate_to_report()
        except WebDriverException as e:
            print(f'Element not found: {e}')
        except Exception as e:
            print(f'General error: {e}')
        finally:
            self.close_browser()


class MobilePlansDownload(BaseDownload):
    def __init__(self, timeout: int, download_time: int):
        url = 'https://sav.wooza.com.br/motorola/auth/login'
        system = 'linx'
        login_selector = {
            'user': '//*[@id="mat-input-2"]',
            'password': '//*[@id="mat-input-0"]'
        }
        user = SAV_USER
        password = SAV_PASSWORD
        actions = [
            {'xpath': '//*[@id="mat-select-0"]'},
            {'xpath': '/html/body/div[2]/div[4]/div/div/div/mat-option[1]/span'},
            {'xpath': '/html/body/div[2]/div[2]/div/mat-dialog-container/app-pdv-choice-modal/div[2]/button'},
            {'xpath': '/html/body/app-root/vertical-layout-1/div[1]/div/div/div/content/app-modules-dashboard/div/div/div/app-card-dashboard[2]/a'},
            {'xpath': '/html/body/app-root/vertical-layout-1/div[1]/div/div/div/content/app-dashboard-users/div/app-dash-reports-module/div/div/app-card-dashboard[1]/a'},
            {'xpath': '/html/body/app-root/vertical-layout-1/div[1]/div/div/div/content/app-reports-my-sales/div/div/div/div[2]/div[2]/button'},
        ]
        super().__init__(timeout, download_time, url, login_selector, actions, user, password, system)
        self.download()

    def download(self):
        try:
            self.login()
            self.navigate_to_report()
        except WebDriverException as e:
            print(f'Element not found: {e}')
        except Exception as e:
            print(f'General error: {e}')
        finally:
            self.close_browser()


class InsuranceDownload(BaseDownload):
    def __init__(self, timeout: int, download_time: int):
        url = LINX_URL
        system = 'linx'
        login_selector = {
            'user': '//*[@id="f_login"]',
            'password': '//*[@id="f_senha"]',
        }
        user = LINX_USER
        password = LINX_PASSWORD
        actions = [
                {'element': '/html/body/div/div[3]/div/form/div/div/button/div'},
                {'element': '/html/body/div/div[3]/div/form/div/div/div/div[2]/ul/li[1]/a'},
                {'element': '//*[@id="btnselecionar_empresa"]'},
                {'element': '//*[@id="liModulo_0"]'},
                {'element': '/html/body/div[1]/aside/div/section/ul/li[2]/ul/li[3]/a'},
                {'iframe': '//*[@id="main"]'}, 
                {'element': '/html/body/form/table[1]/tbody/tr[1]/td[1]/b/a'},
                {'input_date': 'dt_ne_ini'}, 
                {'element': '/html/body/form/input[17]'},
                {'element': '//*[@id="listar1"]'},
                {'element': '//*[@id="listar10"]'},
                {'element': '/html/body/form/input[20]'},
                {'element': 'botaoExportarXLS'},
            ]
        super().__init__(timeout, download_time, url, login_selector, actions, user, password, system)
        self.download()

    def download(self):
        try:
            self.login()
            self.navigate_to_report()
        except WebDriverException as e:
            print(f'Element not found: {e}')
        except Exception as e:
            print(f'General error: {e}')
        finally:
            self.close_browser()