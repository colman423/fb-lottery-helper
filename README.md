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
    
5. Start
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

# To do
- text cast from full to half
- get clean fb url