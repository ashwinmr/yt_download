# Youtube playlist downloader
Program for downloading public playlists from youtube

# Description
This program takes the url of a youtube playlist
It then scrapes the url for video links
It then downloades all the audio and converts to mp3 format.
Make sure the playlist is public

Since the youtube playlist page uses javascript, selenium and a webdriver are required to scrape the page.
The chrome driver can be downloaded here:
https://chromedriver.chromium.org/downloads
Place chromedriver.exe in the chromedriver folder

ffmpeg is required for converting audio files to mp3
It can be downloaded here:
https://ffmpeg.org/download.html
Place ffmpeg.exe in the ffmpeg folder

# Usage
```
python main.py <playlist_url>
```
The following flags are supported:
- -d : Output directory (default is temp/)
- -w : Path to webdriver used for scraping
- -c : Path to ffmpeg directory

## Examples
Example 1: Pop playlist
```
python main.py 'https://www.youtube.com/playlist?list=PLN_NC6nxffm4a3TOIHwpYkRK-4Kl6XODW'
```
