# SIAK WARRRRRRGGGGHHHHHHH!!!!!!!!!!!!

## Requirements

- **Python**
- **Selenium**
- **python-dotenv**
- **beautifulsoup4**
- **lxml**
- **Chromedriver**

## Installation Instructions

1. **Install Python**  
   Ensure Python is installed. Download from [python.org](https://www.python.org/downloads/).

2. **Install Dependencies**  
   Navigate to the project directory and install required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**  
   Download the version matching your Chrome browser from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads). Extract it to a known location.

## Script Configuration

1. **Clone the Repository**  
   Clone the repository and navigate to the project directory:
   ```sh
   git clone https://github.com/mhmmdmadhanip/Bot-Bismillah.git
   cd Bot-Bismillah
   ```

2. **Setup Environment Variables**  
   Create a `.env` file in the project root and add your credentials:
   ```env
   USER=siak_username
   PASSW=siak_password
   DISPLAY_NAME=display_name_on_homepage
   ```

3. **Update Course List**  
   Ensure `matkul.json` is formatted like this:
   ```json
   {
       "Struktur Data & Algoritma": "749641-4",
       "Statistika & Probabilitas": "749738-3",
       "Analisis dan Perancangan Sistem Informasi": "749565-3"
   }
   ```
   "Course Name": "Course Code-SKS"

   You can write anything in course name, but the course code must be the same as in Siak page.

4. **Adjust Parallel Processes**  
   Modify `num_processes` to set the number of bots running simultaneously:
   ```python
   if __name__ == "__main__":
       alhamdulillah_event = multiprocessing.Event()  # Shared event

       num_processes = 5  # Set the number of parallel processes
       processes = []

       for i in range(num_processes):
           p = multiprocessing.Process(target=run_script, args=(alhamdulillah_event, i + 1))
           p.start()
           processes.append(p)

       for p in processes:
           p.join()  # Wait for all processes to finish
   ```

## Running the Script

To start the script, navigate to the directory containing `bismillah.py` and run:
```sh
python bismillah.py
```

## Notes

- The script uses Selenium to automate the login and course registration process. Ensure ChromeDriver matches your Chrome browser version.
- Update the script to match the structure and elements of the target website.