import os.path
import sys
import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import time

def parse_args():
  """ Parse arguments for program
  """
  parser = argparse.ArgumentParser(description="Program for downloading youtube playlist")
  parser.add_argument('url', help='Url for youtube playlist')
  parser.add_argument('-s','--save_file', default='temp/links.csv', help='File to save video links')
  parser.add_argument('-d','--web_driver_path', default='chromedriver.exe', help='Path to chrome web driver')

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
        video_title = playlist_item.find('span',id='video-title')['title']
        video_titles.append(video_title)

    return video_links, video_titles

if __name__ == "__main__":
    args = parse_args()

    url = args.url
    save_file = args.save_file

    # Check for webdriver
    if not os.path.exists(args.web_driver_path):
        print('Please downlaod the crome driver from https://chromedriver.chromium.org/ and place chromedriver.exe in the current folder')
        sys.exit()

    html = get_html_with_js(url, args.web_driver_path)

    video_links, video_titles = get_video_links(html)

    # Save to csv
    df = pd.DataFrame({'title' : video_titles, 'links' : video_links})
    df.to_csv(save_file, index=False)
