---

# SIAK WARRRRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!!

## Requirements

- Python
- Selenium

## Installation Instructions

1. **Install Python 3.x**  
   Ensure that you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Selenium**  
   Open your terminal and run the following command to install Selenium:
   ```sh
   pip install selenium
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
   Open `bismillah.py` in your preferred text editor. Update the following lines with your credentials and other necessary details:
   ```python
   # Update these lines with your credentials
   username = "your_username"
   password = "your_password"
   display_name = "Display name in home page" 
   ```

3. **Update the Course List**  
   Ensure that the `matkul.txt` file is in the following format:
   ```
   kode_matkul-banyak_sks nama_matkul
   ```
   Example:
   ```
   749641-4 SDA
   749738-3 Statprob
   749565-3 Anaper
   ```

## Running the Script

To run the script, open your terminal and navigate to the directory containing `bismillah.py`, then execute the following command:
```sh
python bismillah.py
```

## Notes

- This script uses Selenium to automate the login process and course registration on a specified website. Ensure that you have the correct version of ChromeDriver matching your current Chrome browser version.
- Adjust the script according to the actual structure and elements of the login page and course registration page you are automating.

---