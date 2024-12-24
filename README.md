# ChromeDriver Automation Script

This repository contains a Python script for automating the process of downloading the correct version of ChromeDriver based on the installed version of Google Chrome. Additionally, the script provides functionality to automate login processes and scrape data from specific web pages.

## Features

1. **Automatic ChromeDriver Download**: 
   - Detects the installed Google Chrome version.
   - Downloads the appropriate ChromeDriver version.
   - Extracts and sets up the ChromeDriver executable.

2. **Web Automation with Selenium**:
   - Uses Selenium WebDriver for browser automation.
   - Supports headless browsing mode for background operations.

3. **Web Scraping**:
   - Scrapes specific data from web pages using BeautifulSoup.
   - Processes and organizes table data.

4. **Login Automation**:
   - Automates login to a specific Single Sign-On (SSO) portal.
   - Retrieves and uses session cookies for further navigation.

## Prerequisites

- Python 3.7 or higher
- Google Chrome installed
- Internet connection

### Python Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Required Packages
- `selenium`
- `beautifulsoup4`
- `requests`

## Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Run the Script**:
   ```bash
   python script.py
   ```

3. **Input Credentials**:
   - Enter your `id` and `password` when prompted.

## File Structure

```
.
├── script.py           # Main Python script
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Key Functions

### `download_file(url, dest_folder)`
Downloads a file from the specified URL and saves it to the destination folder.

### `get_chrome_version()`
Retrieves the installed version of Google Chrome from the system.

### `download_chromedriver(chrome_version, download_path)`
Downloads the correct version of ChromeDriver based on the detected Chrome version.

### `get_or_download_chromedriver()`
Checks if ChromeDriver is already set up; if not, it downloads and sets it up.

### Selenium Automation Workflow
- Opens the login page.
- Fills in the user credentials.
- Navigates to the target page after login.
- Scrapes and processes data from a table.

## Supported Platforms

- Windows
- Linux

## Notes
- Ensure Google Chrome is installed and accessible from the command line.
- Adjust the script's URLs and element locators to match your target website if necessary.

## Troubleshooting

- **`File download error`**: Check your internet connection and ensure the URL is correct.
- **`Failed to find Chrome version`**: Ensure Google Chrome is installed and properly configured in your system's PATH.
- **`PHPSESSID cookie not found`**: Verify that the login process is successful and the target page is accessible.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
