import os
import platform
import requests
import zipfile
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.RequestException as e:
        raise RuntimeError(f"File download error: {e}")

    return local_filename

def get_chrome_version():
    platform_name = platform.system()
    if platform_name == "Windows":
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(reg_key, "version")
            return version
        except Exception as e:
            raise RuntimeError(f"Failed to find Chrome version: {e}")
    elif platform_name == "Darwin":
        try:
            result = os.popen("/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version").read()
            return result.split()[2]
        except Exception as e:
            raise RuntimeError(f"Failed to find Chrome version: {e}")
    elif platform_name == "Linux":
        try:
            result = os.popen("google-chrome --version || chromium-browser --version").read()
            return result.split()[2]
        except Exception as e:
            raise RuntimeError(f"Failed to find Chrome version: {e}")
    else:
        raise RuntimeError(f"Unsupported platform: {platform_name}")

def download_chromedriver(chrome_version, download_path):
    base_url = "https://storage.googleapis.com/chrome-for-testing-public/"
    system_map = {
        "Windows": "chromedriver-win64.zip",
        "Linux": "chromedriver-linux64.zip",
    }

    os_names = {
        "Windows": "win64",
        "Linux": "linux64",
    }

    platform_name = platform.system()

    if platform_name not in system_map:
        raise RuntimeError(f"Unsupported platform: {platform_name}")

    driver_filename = system_map[platform_name]
    os_name = os_names[platform_name]

    major_version = chrome_version  
    version_url = f"{base_url}{major_version}/{os_name}/{driver_filename}"
    try:
        zip_path = download_file(version_url, download_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(download_path)
        os.remove(zip_path)

        if platform_name=='Linux':
            chromedriver_path = os.path.join(download_path+'/'+driver_filename[:-4], "chromedriver")
        else: 
            chromedriver_path = os.path.join(download_path+'\\'+driver_filename[:-4], "chromedriver.exe")
        
        os.chmod(chromedriver_path, 0o755)

    except RuntimeError as e:
        raise RuntimeError(f"Failed to download ChromeDriver: {e}")

    return chromedriver_path

def get_or_download_chromedriver():
    """Ensure the proper ChromeDriver version is installed or download it."""
    current_path = os.getcwd()
    chrome_version = get_chrome_version()
    try:
        chromedriver_path = download_chromedriver(chrome_version, current_path)
    except RuntimeError as e:
        print(f"Error downloading ChromeDriver: {e}")
        raise
    return chromedriver_path

try:
    chromedriver_path = get_or_download_chromedriver()
    print(f"ChromeDriver downloaded and available at: {chromedriver_path}")
except RuntimeError:
    print("Failed to initialize ChromeDriver. Exiting...")
    exit(1)

print(chromedriver_path)

service = Service(chromedriver_path)
options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=options)

user_id = input('id: ')
password = input('password: ')

try:
    login_url = "https://sso.aztu.edu.az/"
    admin_url = "https://sso.aztu.edu.az/Admin"
    getdata_url = 'https://sap.aztu.edu.az/studies/lecture_attend.php?lec_open_idx=60461&lecture_code=4138&sem_code=20242&_pjax=%23secondary_content'

    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserId"))).send_keys(user_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password"))).send_keys(password)

    driver.find_element(By.NAME, "Password").send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.url_contains("/Admin"))

    current_url = driver.current_url
    if "/Admin" in current_url:
        print("Login success!")

        cookies = driver.get_cookies()
        username_cookie = next((cookie["value"] for cookie in cookies if cookie["name"] == "username"), None)

        if username_cookie:
            print(f"Username cookie found: {username_cookie}")

            driver.add_cookie({"name": "username", "value": username_cookie, "path": "/"})
            driver.get(admin_url)  

            page_source = driver.page_source
            print("The source code of the page has been obtained!")

            soup = BeautifulSoup(page_source, 'html.parser')

            link_elements = soup.find_all('a', class_='nav-link')

            if len(link_elements) >= 3:
                third_link = link_elements[2]
                target_url = third_link.get('href')

                driver.get(target_url)

                time.sleep(4)

                cookies = driver.get_cookies()
                session_cookie = next((cookie["value"] for cookie in cookies if cookie["name"] == "PHPSESSID"), None)

                if session_cookie:
                    print(f"PHPSESSID cookie found: {session_cookie}")

                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                    }
                    cookies = {
                        "PHPSESSID": session_cookie
                    }
                    driver.get(getdata_url)
                    time.sleep(10) 
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")

                    table = soup.find("table", {"id": "datatable-buttons"})

                    headers = []
                    for th in table.find_all("th"):
                        header_text = th.get_text(strip=True)
                        headers.append(header_text)

                    rows = []
                    for tr in table.find_all("tr")[1:]:  
                        cells = tr.find_all(["td", "th"]) 
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        rows.append(row_data)
                    
                    date,attendance=rows[2][1:],rows[-1][3:-2]
                    date = cleaned_list = list(filter(None, date))
                    attendance = cleaned_list = list(filter(None, attendance))

                    for i, j in zip(date, attendance):
                        if j == 'i/e':
                            print(f"{i} - {j} Status: Participated in the class. ")
                        elif j == 'q/b':
                            print(f"{i} - {j} Status: Did not participate in the class. ")
                else:
                    print("PHPSESSID cookie not found!")
        else:
            print("Username cookie not found!")
    else:
        print("Username ve ya password incorrect!")

except Exception as e:
    print(f"Error occured: {e}")
finally:
    driver.quit() 
