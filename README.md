# Youtube playlist downloader
Program for downloading public playlists from youtube

# Description
This program takes the url of a youtube playlist
It then scrapes the url for video links
Make sure the playlist is public

Since the youtube playlist page uses javascript, selenium and a webdriver are required to scrape the page.
The chrome driver can be downloaded here:
https://chromedriver.chromium.org/

# Usage
```
python main.py <playlist_url>
```
The following flags are supported:
- -s : Csv file to save video links
- -d : Path to webdriver used for scraping

## Examples
Example 1: Pop playlist
```
python main.py 'https://www.youtube.com/playlist?list=PLN_NC6nxffm4a3TOIHwpYkRK-4Kl6XODW'
```
