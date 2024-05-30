# SIAK WARRRRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!!

## Requirements

- Python
- Selenium

## Installation Instructions

1. **Install Python**  
   Ensure that you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install requirements.txt**  
   Open your terminal, navigate to the directory containing the `requirements.txt` file, and run the following command to install all the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**  
   Download the version of ChromeDriver that matches your current Chrome browser version from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads). Extract the downloaded file to a known location.

## Script Configuration

1. **Clone this repository**  
   Clone this repository to your local machine:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Update the Script**  
   Create a `.env` file in the root directory of your project. Open the `.env` file in a text editor and add the following lines, replacing the placeholders with your credentials:
   ```env
   USER=siak_username
   PASSW=siak_password
   DISPLAY_NAME=Display name in home page
   ```

3. **Update the Course List**  
   Ensure that the `matkul.json` file is in the following format:
   ```json
   {
       "nama_matkul": "kode_matkul-banyak_sks",
       "nama_matkul": "kode_matkul-banyak_sks",
       "nama_matkul": "kode_matkul-banyak_sks"
   }
   ```
   Example:
   ```json
   {
       "Struktur Data & Algoritma": "749641-4",
       "Statistika & Probabilitas": "749738-3",
       "Analisis dan Perancangan Sistem Informasi": "749565-3"
   }
   ```

   Update the `matkul.json` file with the course names and their corresponding codes.

## Running the Script

To run the script, open your terminal and navigate to the directory containing `bismillah.py`, then execute the following command:
```sh
python bismillah.py
```

## Notes

- This script uses Selenium to automate the login process and course registration on a specified website. Ensure that you have the correct version of ChromeDriver matching your current Chrome browser version.
- Adjust the script according to the actual structure and elements of the login page and course registration page you are automating.
