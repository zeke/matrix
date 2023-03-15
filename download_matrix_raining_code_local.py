import os
import requests
from bs4 import BeautifulSoup
import youtube_dl
import re

YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="

def youtube_search(query):
    search_url = YOUTUBE_SEARCH_URL + query.replace(" ", "+")
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    video_id = None
    for link in soup.find_all("a", href=True):
        href = link['href']
        match = re.search(r'/watch\?v=([\w-]+)', href)
        if match:
            video_id = match.group(1)
            break
    return video_id

def download_video(video_id):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': f'{video_id}.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

def create_html(video_id):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                overflow: hidden;
            }}
            video {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <video src="{video_id}.mp4" autoplay loop></video>
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    # query = "matrix raining code"
    # video_id = youtube_search(query)
    # video_id = "kqUR3KtWbTk"
    # download_video(video_id)
    create_html("matrix")
