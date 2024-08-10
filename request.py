import os
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv

# Create a session object to persist cookies and headers
load_dotenv()
session = requests.Session()

# Function to perform a POST request with retries
def post_with_retry(url, data, delay=2):
    while True:
        response = session.post(url, data=data, verify=False)
        if response.status_code == 200:
            return response
        else:
            print(f"POST request failed. Retrying...")
            time.sleep(delay)

# Function to perform a GET request with retries
def get_with_retry(url, delay=2):
    while True:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            return response
        else:
            print(f"GET request failed. Retrying...")
            time.sleep(delay)

# 1. POST Request to login
login_url = "https://academic.ui.ac.id/main/Authentication/Index"
login_data = {
    'u': os.getenv("USER"),
    'p': os.getenv("PASSW")
}

login_response = post_with_retry(login_url, login_data)

print("Login successful.")

# 2. GET Request to ChangeRole
change_role_url = "https://academic.ui.ac.id/main/Authentication/ChangeRole"
change_role_response = get_with_retry(change_role_url)

print("Role changed successfully.")

# 3. GET Request to CoursePlanEdit to retrieve the token
course_plan_edit_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
course_plan_edit_response = get_with_retry(course_plan_edit_url)

soup = BeautifulSoup(course_plan_edit_response.text, 'html.parser')
token_input = soup.find('input', {'name': 'tokens'})
if token_input:
    token = token_input['value']
    print(f"Token retrieved: {token}")
else:
    raise Exception("Token not found.")

# 4. POST Request to save the course plan
course_plan_save_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"
course_plan_save_data = {
    'tokens': token,
    # 'c[Kode MK_Kurikulum]': 'CourseCode-SKS' ex: 'c[MD04600304_04.00.01.01-2021]': '750730-1',
    'comment': None,
    'submit': 'Simpan IRS'
}

course_plan_save_response = post_with_retry(course_plan_save_url, course_plan_save_data)

print("Course plan saved successfully.")

# 5. GET Request to CoursePlanDone
course_plan_done_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanDone"
course_plan_done_response = get_with_retry(course_plan_done_url)

print("Course plan submission done.")

# 6. GET Request to CoursePlanViewCheck
course_plan_view_check_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanViewCheck"
course_plan_view_check_response = get_with_retry(course_plan_view_check_url)

print("Course plan view check successful.")