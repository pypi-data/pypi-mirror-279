from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.edge import service
from WMain.WRequests import WSession
from WMain.WUrl import WUrl
from typing import Union, List, Tuple
import time
import zipfile
import os
import time
VERSION = "__version__"
EDGE_DIR_NAME = "edge"
EDGE_FILE_NAME = "msedgedriver.exe"
edge_zip_url = f"https://msedgedriver.azureedge.net/{VERSION}/edgedriver_win64.zip"

def get_edge_driver_zip_url(version: str):
    return edge_zip_url.replace(VERSION, version)


def download_edge_driver(session: WSession, version: str, path: str, is_force: bool=False):
    os.makedirs(path, exist_ok=True)
    file = path.rstrip("/") + f"/{EDGE_DIR_NAME}_{version}.zip"
    if not is_force and os.path.exists(file):
        return
    with open(file, "wb+") as f:
        f.write(session.get(get_edge_driver_zip_url(version)).content)
    extract_edge_driver_zip(file)
    

def extract_edge_driver_zip(file: str):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(file))

class WEdgeDriver:
    driver: Edge = None
    
    def __init__(self, file: str):
        self.__srv = service.Service(file)
        self.__options = EdgeOptions()
    
    def start(self):
        self.__edge = Edge(options=self.__options, service=self.__srv)
    
    def option_headless(self):
        self.__options.add_argument('headless')

    def option_window_size(self, width, height):
        self.__options.add_argument(f'window-size={width}x{height}')

    def option_no_images(self):
        self.__options.add_argument('blink-settings=imagesEnabled=false')

    def option_no_gpu(self):
        self.__options.add_argument('disable-gpu')

    def option_no_music(self):
        self.__options.add_argument('--mute-audio')

    def option_maxsize(self):
        self.__options.add_argument('--start-maximized')
    
    def click_by_xpath(self, xpath: str):
        self.wait_for_element(xpath).click()

    def send_keys_by_xpath(self, xpath: str, keys: str):
        self.wait_for_element(xpath).send_keys(keys)
    
    def get_elements_by_xpath(self, xpath: str) -> List[WebElement]:
        return self.__edge.find_elements(By.XPATH, xpath)
    
    def get(self, url: str):
        self.__edge.get(str(url))
    
    def wait_for_element(self, xpath: str, timeout: float=10, step: float=0.2) -> Union[None, WebElement]:
        while timeout > 0:
            try:
                element = self.__edge.find_element(By.XPATH, xpath)
                self.js_scroll_to_element(element)
                return element
            except Exception:
                time.sleep(step)
                timeout -= step
        return None
    
    def js_scroll_to_element(self, element: WebElement):
        self.__edge.execute_script("arguments[0].scrollIntoView();", element)
    
    def switch_to_end_window(self):
        windows = self.__edge.window_handles
        self.__edge.switch_to.window(windows[-1])

    def js(self, js_path: str, func: str, args: list):
        start = f'return {func}({args})\n'
        with open(js_path, 'r') as f:
            return self.__edge.execute_script(start + f.read())
        
class WEdgeDownloader:

    def __init__(self, session: WSession=WSession(), path: str='./driver'):
        self.session = session
        self.path = path.strip() + "/" + EDGE_DIR_NAME

    def __download(self, version: str, is_force: bool=False):
        version = version.strip()
        download_edge_driver(self.session, version, self.path, is_force)
            
    
    def __call__(self, version: str, is_force: bool=False):
        self.__download(version, is_force)
        
    def start(self, version: str, is_force: bool=False):
        self.__download(version, is_force)
        
    def get_driver(self):
        for filename in os.listdir(self.path):
            if "driver" in filename:
                return WEdgeDriver(self.path + "/" + filename)
            
        return None
                
        

if __name__ == "__main__":
    s = WSession()
    s.ini.set_proxy(20000)
    dn = WEdgeDownloader(s)
    dn("126.0.2592.56 ")
    edge = dn.get_driver()
    edge.start()
    edge.get("https://iedu.jlu.edu.cn")
    while 1:
        time.sleep(1)