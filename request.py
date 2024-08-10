import os
import requests
from bs4 import BeautifulSoup
import datetime
import time
from dotenv import load_dotenv
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning from urllib3
urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to persist cookies and headers
load_dotenv()
session = requests.Session()

# Function to get current time formatted as HH-MM-SS
def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

# Function to perform a POST request with retries
def post_with_retry(url, data, delay=2):
    while True:
        response = session.post(url, data=data, verify=False)
        if response.status_code == 200:
            return response
        else:
            print(f"[{get_current_time()}] POST request failed. Retrying...")
            time.sleep(delay)

# Function to perform a GET request with retries
def get_with_retry(url, delay=2):
    while True:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            return response
        else:
            print(f"[{get_current_time()}] GET request failed. Retrying...")
            time.sleep(delay)

# Function to read and parse the local HTML file
def read_local_html_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

# Function to log out the user
def logout():
    logout_url = "https://academic.ui.ac.id/main/Authentication/Logout"
    get_with_retry(logout_url)
    print(f"[{get_current_time()}] Logged out.")

# Main function to encapsulate the process
def main():
    while True:
        try:
            # 1. POST Request to login
            login_url = "https://academic.ui.ac.id/main/Authentication/Index"
            login_data = {
                'u': os.getenv("USER"),
                'p': os.getenv("PASSW")
            }

            login_response = post_with_retry(login_url, login_data)
            print(f"[{get_current_time()}] Login successful.")

            # 2. GET Request to ChangeRole
            change_role_url = "https://academic.ui.ac.id/main/Authentication/ChangeRole"
            change_role_response = get_with_retry(change_role_url)
            print(f"[{get_current_time()}] Role changed successfully.")

            # 3. GET Request to CoursePlanEdit to retrieve the token
            course_plan_edit_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
            course_plan_edit_response = get_with_retry(course_plan_edit_url)

            soup = BeautifulSoup(course_plan_edit_response.text, 'html.parser')
            token_input = soup.find('input', {'name': 'tokens'})
            if token_input:
                token = token_input['value']
                print(f"[{get_current_time()}] Token retrieved: {token}")
                break  # Token found, exit the loop
            else:
                print(f"[{get_current_time()}] Token not found. Logging out and retrying...")
                logout()

        except Exception as e:
            print(f"[{get_current_time()}] Error occurred: {str(e)}. Retrying...")
            logout()

    # 4. POST Request to save the course plan
    course_plan_save_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"
    course_plan_save_data = {
        'tokens': token,
        # 'c[Kode MK_Kurikulum]': 'CourseCode-SKS' ex: 'c[MD04600304_04.00.01.01-2021]': '750730-1',
        'comment': None,
        'submit': 'Simpan IRS'
    }

    course_plan_save_response = post_with_retry(course_plan_save_url, course_plan_save_data)
    print(f"[{get_current_time()}] Course plan saved successfully.")

    # 5. GET Request to CoursePlanDone
    course_plan_done_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanDone"
    course_plan_done_response = get_with_retry(course_plan_done_url)
    print(f"[{get_current_time()}] Course plan submission done.")

    # 6. GET Request to CoursePlanViewCheck
    course_plan_view_check_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanViewCheck"
    course_plan_view_check_response = get_with_retry(course_plan_view_check_url)

    # Save the response content to an HTML file
    html_filename = "course_plan_view_check.html"

    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(course_plan_view_check_response.text)

    print(f"[{get_current_time()}] HTML preview saved as {html_filename}.")

    # Read and parse the saved HTML file
    soup = read_local_html_file(html_filename)

    # Extract and print the relevant data from the HTML
    rows = soup.find_all('tr')
    for row in rows:
        if " - " in row.text:
            print(f"{row.text.strip()}")
        if "Kapasitas internal" in row.text:
            print(f"{row.text.strip()}")
        if "Prasyarat" in row.text:
            break

    print(f"[{get_current_time()}] Course plan view check successful. HTML preview read from {html_filename}.")

# Start the main process
main()