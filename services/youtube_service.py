import requests
from config import YOUTUBE_API_KEY
import asyncio

class YouTubeService:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key=YOUTUBE_API_KEY):
        self.api_key = api_key

    async def search_video(self, query, max_results=1):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._search_sync, query, max_results)

    def _search_sync(self, query, max_results):
        params = {
            "part": "snippet",
            "q": query,
            "key": self.api_key,
            "maxResults": max_results,
            "type": "video"
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"Error en YouTube API: {response.text}")

        data = response.json()
        items = data.get("items", [])
        if not items:
            return None

        results = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            results.append({"title": title, "url": url})
        return results
