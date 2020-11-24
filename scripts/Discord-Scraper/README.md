# Discord Scraper

## Table of Contents
* [Configuring Discord application for PC](#desktop-application)
* [Configuring Discord website for PC](#website)
* [Notes](#notes)
* [Changelog](#changelog)

## Configuring

### Desktop Application:

Step 1:
Open your Discord app and click the settings wheel.
![Step 1](images/Step1.png "Step 1")

Step 2:
Find and Click 'Appearance' and enable Developer Mode.

![Step 2](images/Step2.png "Step 2")

Developer Mode is located at the very bottom of the appearance page, within the "Advanced" catagory.

![Step 3](images/Step3.png "Step 3")

### Website:

Step 3:
Close the settings menu and press CTRL + SHIFT + I to open the Developer panel (similiar to your browser).

Step 4:
Click on the server you want to scrape, then click the channel you plan to scrape.
Go to the Network tab, click 'messages?limit=50' (or something similar) within the name list.
Click the header tab, and copy the value of "authorization" into the config.json file.
![Step 4](images/Step4.png "Step 4")
![Step 5](images/Step5.png "Step 5")

Step 5:
Close the Developer panel and right-click on the server icon and copy ID.

![Step 6](images/Step6.png "Step 6")

Paste the server ID into the config.json file.
![Step 7](images/Step7.png "Step 7")

Step 6:
Right-click on the channel name and copy ID.
Paste the channel ID into the config.json file.

![Step 8](images/Step8.png "Step 8")

Step 7:
Run the script to start the downloading process.

## Notes

* You can copy in multiple channels on multiple servers if you want to.
* You must make modifications to the JSON file before running the script (otherwise you'll end up with errors).
