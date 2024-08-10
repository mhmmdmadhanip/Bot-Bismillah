import multiprocessing
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import datetime
import json

def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def logout_page(driver, process_number):
    logout_url = "https://academic.ui.ac.id/main/Authentication/Logout"
    driver.get(logout_url)
    time.sleep(0.5)
    print(f"Bot {process_number}: {get_current_time()} - logout bangg")

def login_page(driver, user, passw, process_number):
    username = driver.find_element(By.NAME, "u")
    username.clear()
    username.send_keys(user)
    time.sleep(0.1)

    password = driver.find_element(By.NAME, "p")
    password.clear()
    password.send_keys(passw)
    time.sleep(0.1)
    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    print(f"Bot {process_number}: {get_current_time()} - login bangg")

def war_page(driver, matkul_code, total_chosen, chosen_matkul, process_number):
    for name, kode in matkul_code.items():
        try:
            radio_input = driver.find_element(By.XPATH, f"//input[@value='{kode}']")
            total_chosen += 1
            if not radio_input.is_selected():
                radio_input.click()
                print(f"Bot {process_number}: {get_current_time()} - {name} dipilih! (kode: {kode})")
                chosen_matkul = True
                time.sleep(0.1)
            else:
                print(f"Bot {process_number}: {get_current_time()} - {name} sudah dipilih! (kode: {kode})")
        except:
            print(f"Bot {process_number}: {get_current_time()} - {name} tidak ada! (kode: {kode})")
            continue

    driver.find_element(By.XPATH, "//input[@value='Simpan IRS']").click()
    return chosen_matkul, total_chosen

def run_script(alhamdulillah_event, process_number):
    load_dotenv()
    driver = webdriver.Chrome()

    login_url = "https://academic.ui.ac.id/main/Authentication/"
    homepage_url = "https://academic.ui.ac.id/main/Welcome/"
    siak_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
    
    user = os.getenv("USER")
    passw = os.getenv("PASSW")
    display_name = os.getenv("DISPLAY_NAME")
    
    with open("matkul.json", "r") as json_file:
        matkul_code = json.load(json_file)

    total_matkul = len(matkul_code)
    chosen_matkul = False
    total_chosen = 0

    driver.get(login_url)
    time.sleep(0.5)

    while True:
        if alhamdulillah_event.is_set():
            print(f"Bot {process_number}: {get_current_time()} - Bot terminated due to another 'Alhamdulillah' event")
            break

        while display_name not in driver.page_source and "Fakultas Kedokteran" not in driver.page_source:
            driver.refresh()

        if "Fakultas Kedokteran" in driver.page_source:
            login_page(driver, user, passw, process_number)
            continue

        if "No role selected" in driver.page_source:
            logout_page(driver, process_number)
            continue

        if driver.current_url == homepage_url:
            driver.get(siak_url)
            time.sleep(0.5)
            continue

        if "CoursePlanEdit" in driver.current_url:
            if "Anda tidak dapat mengisi IRS" in driver.page_source:
                print(f"Bot {process_number}: {get_current_time()} - blom bisa bang T_T")
                logout_page(driver, process_number)
                continue

            print(f"Bot {process_number}: {get_current_time()} - milih dulu bang")
            time.sleep(1.5)

            print(f"Bot {process_number}: {get_current_time()} - bismillah menang")
            
            chosen_matkul, total_chosen = war_page(driver, matkul_code, total_chosen, chosen_matkul, process_number)

            if not chosen_matkul and total_chosen < total_matkul:
                print(f"Bot {process_number}: {get_current_time()} - ngulang isi T_T")
                driver.get(siak_url)
                continue
            
            while "CoursePlanSave" in driver.current_url:
                driver.refresh()

            while "CoursePlanDone" in driver.current_url and "IRS berhasil tersimpan!" not in driver.page_source:
                driver.refresh()

            print(f"Bot {process_number}: {get_current_time()} - alhamdulillah")
            
            if "IRS berhasil tersimpan!" in driver.page_source:
                alhamdulillah_event.set()  # Notify other processes
                try:
                    view_check_link = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[contains(.,'Lihat Pemeriksaan IRS')]"))
                    )
                    view_check_link.click()
                    print(f"Bot {process_number}: {get_current_time()} - 'Lihat Pemeriksaan IRS' Page")
                    
                    while "CoursePlanViewCheck" in driver.current_url and display_name not in driver.page_source:
                        driver.refresh()
                    
                    if "CoursePlanViewCheck" in driver.current_url:
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        rows = soup.find_all('tr')
                        for row in rows:
                            if " - " in row.text:
                                print(f"Bot {process_number}: {row.text.strip()}")
                            if "Kapasitas internal" in row.text:
                                print(f"Bot {process_number}: {row.text.strip()}")
                            if "Prasyarat" in row.text:
                                break

                except:
                    print(f"Bot {process_number}: {get_current_time()} - Gagal klik link 'Lihat Pemeriksaan IRS'")
            break

    driver.quit()

if __name__ == "__main__":
    alhamdulillah_event = multiprocessing.Event()  # Create the shared Event

    num_processes = 5  # Number of parallel processes 
    processes = []

    for i in range(num_processes):
        p = multiprocessing.Process(target=run_script, args=(alhamdulillah_event, i + 1))
        p.start()
        processes.append(p)

    for p in processes:
        p.join() 