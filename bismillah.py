from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

driver = webdriver.Chrome()

login_url = "https://academic.ui.ac.id/main/Authentication/"
homepage_url = "https://academic.ui.ac.id/main/Welcome/"
logout_url = "https://academic.ui.ac.id/main/Authentication/Logout"
siak_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

down_string = "Universitas Indonesia"
matkul_code = {}

# with open("matkul.txt", "r") as file:
#     for line in file:
#         (kelas, nama) = line.split()
#         matkul_code[nama] = kelas
#         total_matkul += 1

with open("matkul.json", "r") as json_file:
    matkul_code = json.load(json_file)

print(matkul_code)
total_matkul = len(matkul_code)

#Isi ini sesuai akun
user = os.getenv("USER")
passw = os.getenv("PASSW")

#Nama yang ada di atas kiri homepage (( person MUHAMMAD MADHANI PUTRA – Mahasiswa S1 Reguler Sistem Informasi (06.00.12.01) ))
display_name = os.getenv("DISPLAY_NAME")

chosen_matkul = False
total_chosen = 0

def logout_page():
    driver.get(logout_url)
    time.sleep(0.5)

def login_page():

    username = driver.find_element(By.NAME, "u")
    username.clear()
    username.send_keys(user)
    time.sleep(0.1)

    password = driver.find_element(By.NAME, "p")
    password.clear()
    password.send_keys(passw)
    time.sleep(0.1)
    driver.find_element(By.XPATH, "//input[@value='Login']").click()

def war_page():
    for name, kode in matkul_code.items():
        try:
            radio_input = driver.find_element(By.XPATH, f"//input[@value='{kode}']")
            global total_chosen
            total_chosen += 1
            if(not radio_input.is_selected()): 
                radio_input.click()
                print(f"{name} dipilih! (kode: {kode})")
                global chosen_matkul
                chosen_matkul = True
                time.sleep(0.1)
            else :
                print(f"{name} sudah dipilih! (kode: {kode})")
        except:
            print(f"{name} tidak ada! (kode: {kode})")
            logout_page()
            return False

    driver.find_element(By.XPATH, "//input[@value='Simpan IRS']").click()
    return True

if __name__ == "__main__":
    #new_term = "Tahun Ajaran 2019/2020 Term 1"
    driver.get(login_url)
    time.sleep(0.5)

    while(True):

        while(display_name not in driver.page_source and 
              "Fakultas Kedokteran" not in driver.page_source):
            driver.refresh()
            

        if "Fakultas Kedokteran" in driver.page_source:
            login_page()
            continue

        print("login bangg")
        if driver.current_url == homepage_url:
            driver.get(siak_url)
            time.sleep(0.5)
            continue

        if "CoursePlanEdit" in driver.current_url:
            if "Anda tidak dapat mengisi IRS" in driver.page_source:
                print("blom bisa bang T_T")
                logout_page()
                continue

            print("milih dulu bang")
            time.sleep(1.5)

            print("bismillah menang")
            if(not war_page()):
                print("belom bisa bangT_T")
                logout_page()
                continue

            if (not chosen_matkul and total_chosen < total_matkul):
                print("ngulang isi T_T")
                driver.get(siak_url)
                continue
            
            print("alhamdulillah")
            break

    while True:
    	pass