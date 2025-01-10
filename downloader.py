import requests
from bs4 import BeautifulSoup

def get_video_url(xhamster_url):
    try:
        response = requests.get(xhamster_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract video URL (may need adjustments if xHamster changes its structure)
        video_tag = soup.find('video')
        if video_tag:
            video_url = video_tag.get('src')
            return video_url
        else:
            return None
    except Exception as e:
        print(f"Error fetching video URL: {e}")
        return None

def download_video(video_url, output_path):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return output_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
        