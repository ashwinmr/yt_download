from __future__ import unicode_literals
import os.path
import sys
import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import time
import youtube_dl

def parse_args():
  """ Parse arguments for program
  """
  parser = argparse.ArgumentParser(description="Program for downloading youtube playlist")
  parser.add_argument('url', help='Url for youtube playlist')
  parser.add_argument('-d','--output_dir', default='temp', help='Path to output directory')
  parser.add_argument('-w','--web_driver_path', default='chromedriver/chromedriver.exe', help='Path to chrome web driver')
  parser.add_argument('-c','--ffmpeg_dir', default='ffmpeg/', help='Path to ffmpeg directory for converting audio')
  parser.add_argument('-s','--start', type=int, default=1, help='Starting song number in playlist')
  parser.add_argument('-e','--end', type=int, help='Ending song number in playlist')

  return parser.parse_args()

def get_html_no_js(url):
    """ Get html from url that does not require Javascript
    """
    r = requests.get(url)

    # with open('res.html','w',encoding=r.encoding) as f:
    #     f.write(r.text)

    return r.text

def get_html_with_js(url, web_driver_path):
    """ Get html from url that uses Javascript to load
    """
    driver = Chrome(web_driver_path)
    driver.get(url)

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    # Get all html and close
    html = driver.page_source
    driver.close()

    # with open('res.html','w',encoding='utf-8') as f:
    #     f.write(html)

    return html

def get_video_links(html):
    """ Get list of video links from html
    """
    soup = BeautifulSoup(html, 'lxml')

    video_links = []
    video_titles = []
    playlist_items = soup.find_all('ytd-playlist-video-renderer')
    for playlist_item in playlist_items:

        # Get video link
        href = playlist_item.find('a')['href']
        video_link = 'https://www.youtube.com' + href.split('&')[0]
        video_links.append(video_link)

        # Get video title
        video_title = playlist_item.find('a').get('title')
        video_titles.append(video_title)

    # Print list
    print('\nLinks:')
    res = '\n'.join("{} \t {}".format(x, y) for x, y in zip(video_titles, video_links))
    print(res)

    return video_links, video_titles

def download_audio(url,output_dir,ffmpeg_dir):
    """ Download audio file from youtube url
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_dir,
        'outtmpl': output_dir + '/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
            }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    args = parse_args()

    url = args.url
    web_driver_path = args.web_driver_path
    ffmpeg_dir = args.ffmpeg_dir
    output_dir = args.output_dir
    start = args.start
    end = args.end

    # Check for webdriver
    if not os.path.exists(web_driver_path):
        print('Please download the crome driver from https://chromedriver.chromium.org/downloads and place chromedriver.exe in the chromedriver folder')
        sys.exit()

    # Check for ffmpeg
    ffmpeg_path = os.path.join(ffmpeg_dir,'ffmpeg.exe')
    if not os.path.exists(ffmpeg_path):
        print('Please download ffmpeg from https://ffmpeg.org/download.html and place ffmpeg.exe in the ffmpeg folder')
        sys.exit()

    html = get_html_with_js(url,web_driver_path)
    video_links, video_titles = get_video_links(html)

    # Check if output dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get subset of songs
    if start < 1:
        start = 1
    if end is None or end > len(video_links):
        end = len(video_links)
    video_links = video_links[start-1:end]
    video_titles = video_titles[start-1:end]

    print('\nDownloading:')
    for video_link, video_title in zip(video_links,video_titles):
        try:
            download_audio(video_link,output_dir = output_dir, ffmpeg_dir = ffmpeg_dir)
        except:
            print('\tWarning: Unable to download {video_title}'.format(video_title=video_title))
