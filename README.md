# Introduction
This tools can help you make lottery in groups' post easily.

# Installation
1.  Clone it
    ```
    $ git clone https://github.com/colman423/fb-lottery-helper.git
    $ cd fb-lottery-helper
    ```
2. Install package
    ```
    $ pip install -r requirement.txt
    ```
    Mac users may also need to add `sudo` at front.
    ```
    $ sudo pip3 install -r requirement.txt
    ```   
3. Install web driver

	[Chrome web driver](http://chromedriver.chromium.org/downloads)
    
4. Locate web driver

	config/config.py
	```
    driver_path = "/Somewhere/your/webdriver/store"
    ```

5. Register a Google Sheets API

    [Register a Google Sheets API](https://developers.google.com/sheets/api/quickstart/js)

6. Add api key into config

	config/config.py
	```
    google_key = {
        'apiKey': 'yourapikey',
        'clientId': 'yourclientid',
        'discoveryDocs': ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
        'scope': "https://www.googleapis.com/auth/spreadsheets.readonly",
    }
    ```

7. Start and open "http://localhost:3000/" with browser
    ```
    $ python run.py
    ```

# Usage


#


# Warning!
- **DO NOT** share .cookie file to others!
(Others can enter your Facebook by .cookie file.)
- Facebook frequently update their HTML class rules, 
so this tool might broken in the near future QAQ.

# Built Using
- Selenium - Dynamic web scrapying.
- PyQuery - Easier to query HTML element in python.
- Google sheet API - To parse google sheet.
- Flask - A lightweight web server.
- Bootstrap - great UI template.
- JQuery - nice tool for coding js for HTML.
