import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Manual .env loader
def load_env_file(file_path=".env"):
    """Manually load environment variables from a .env file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):  # Skip empty lines and comments
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Load environment variables
load_env_file()

# Read API key from the environment variables
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found in .env file.")

# YouTube API configuration
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def fetch_channel_videos(channel_url):
    """Fetch videos from a YouTube channel using its handle."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    handle = channel_url.split("/")[-1]
    videos = []

    try:
        # Get channel details
        channel_response = youtube.search().list(
            part="snippet",
            type="channel",
            q=handle,
            maxResults=1
        ).execute()

        if not channel_response["items"]:
            print(f"Channel with handle {handle} not found.")
            return None, None

        channel_id = channel_response["items"][0]["id"]["channelId"]

        # Fetch videos with pagination
        next_page_token = None
        total_videos_fetched = 0
        while True:
            video_response = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=10,
                pageToken=next_page_token
            ).execute()

            for item in video_response["items"]:
                videos.append({
                    "Video ID": item["id"]["videoId"],
                    "Title": item["snippet"]["title"],
                    "Description": item["snippet"]["description"],
                    "Published Date": item["snippet"]["publishedAt"],
                    "Thumbnail URL": item["snippet"]["thumbnails"]["high"]["url"]
                })
                total_videos_fetched += 1

            # Log progress
            print(f"Fetched {len(videos)} videos so far.")

            # Check if the user wants to continue after the first batch
            if len(videos) >= 10:
                print(f"Progress: {len(videos)} videos fetched. Do you want to fetch more? (y/n)")
                user_input = input().strip().lower()
                if user_input != "y":
                    return channel_id, videos

            # Continue fetching if the user agrees
            next_page_token = video_response.get("nextPageToken")
            if not next_page_token:
                break

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")

    return channel_id, videos

def fetch_video_statistics(video_id):
    """Fetch statistics for a given video."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    try:
        video_response = youtube.videos().list(
            part="statistics,contentDetails",
            id=video_id
        ).execute()

        if video_response["items"]:
            stats = video_response["items"][0]["statistics"]
            details = video_response["items"][0]["contentDetails"]
            return {
                "View Count": stats.get("viewCount", 0),
                "Like Count": stats.get("likeCount", 0),
                "Comment Count": stats.get("commentCount", 0),
                "Duration": details["duration"]
            }
    except HttpError as e:
        print(f"An HTTP error occurred while fetching stats for video {video_id}: {e}")
    return {}

def fetch_comments(video_id, max_comments=100):
    """Fetch the latest comments and their replies for a video."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    try:
        next_page_token = None
        while len(comments) < max_comments:
            comment_response = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=20,
                pageToken=next_page_token
            ).execute()

            for item in comment_response["items"]:
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "Video ID": video_id,
                    "Comment ID": item["id"],
                    "Comment Text": top_comment["textOriginal"],
                    "Author Name": top_comment["authorDisplayName"],
                    "Published Date": top_comment["publishedAt"],
                    "Like Count": top_comment["likeCount"],
                    "Reply To": None
                })
                # Fetch replies
                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        reply_snippet = reply["snippet"]
                        comments.append({
                            "Video ID": video_id,
                            "Comment ID": reply["id"],
                            "Comment Text": reply_snippet["textOriginal"],
                            "Author Name": reply_snippet["authorDisplayName"],
                            "Published Date": reply_snippet["publishedAt"],
                            "Like Count": reply_snippet["likeCount"],
                            "Reply To": item["id"]
                        })

            next_page_token = comment_response.get("nextPageToken")
            if not next_page_token:
                break
    except HttpError as e:
        print(f"An HTTP error occurred while fetching comments for video {video_id}: {e}")
    return comments

def main(channel_url):
    channel_id, videos = fetch_channel_videos(channel_url)
    if not videos:
        print("No videos found for the provided channel.")
        return

    # Fetch video statistics and comments
    video_data = []
    comments_data = []
    for video in videos:
        stats = fetch_video_statistics(video["Video ID"])
        video.update(stats)
        video_data.append(video)

        comments = fetch_comments(video["Video ID"])
        comments_data.extend(comments)

        # Log progress
        percentage = (len(video_data) / len(videos)) * 100
        print(f"Progress: {percentage:.2f}% completed.")

    # Save data to Excel
    with pd.ExcelWriter("YouTube_Channel_Data.xlsx", engine="openpyxl") as writer:
        pd.DataFrame(video_data).to_excel(writer, sheet_name="Video Data", index=False)
        pd.DataFrame(comments_data).to_excel(writer, sheet_name="Comments Data", index=False)

    print("Data saved to YouTube_Channel_Data.xlsx.")

if __name__ == "__main__":
    channel_url = input("Enter the YouTube channel URL with handle: ")
    main(channel_url)