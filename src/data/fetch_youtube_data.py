import sys 
sys.path.insert(0, '../../secrets')


from googleapiclient.discovery import build
from youtubekeys import api_key
import csv


def youtube_data(video_ids_fn, outfolder="data/"):
    data_fields = ["video_title", "user", "date_posted", "like_count", "comment_count", "view_count", "description", "topic_details",
                  "video_tags", "category"]
    with open(outfolder+"youtube_metadata.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_fields)
  
    with open(video_ids_fn) as fn:
        for video_id in fn:
            try:
                metadata = fetch_metadata(video_id)
                with open(outfolder+"youtube_metadata.csv", 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(metadata)
            except Exception as e:
                pass  
    return

def fetch_metadata(video_id):
    
    # creating youtube resource object
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    categories_response = youtube.videoCategories().list(part='id,snippet', regionCode='us').execute()
    categories = {item['id']: item['snippet']['title'] for item in categories_response['items']}
  
    # retrieve youtube video results
    video_response=youtube.videos().list(part='snippet,statistics,status,topicDetails', id=video_id).execute()
    
    
    try:
        video_title = video_response['items'][0]['snippet']['title']
    except:
        video_title = None
    try:
        user = video_response['items'][0]['snippet']['channelId']
    except:
        user = None
    try:
        date_posted = video_response['items'][0]['snippet']['publishedAt']
    except:
        date_posted = None
    try:
        like_count = video_response['items'][0]['statistics']['likeCount']
    except:
        like_count = None
    try:
        comment_count = video_response['items'][0]['statistics']['commentCount']
    except:
        comment_count = None
    try:
        view_count = video_response['items'][0]['statistics']['viewCount']
    except:
        view_count = None
    try:    
        description = video_response['items'][0]['snippet']['description']
    except: 
        description = None
    try:
        topic_details = video_response['items'][0]['topicDetails']['topicCategories']
    except:
        topic_details = None
    try:
        video_tags = video_response['items'][0]['snippet']['tags']
    except:
        video_tags = None
    try:
        category = categories[video_response['items'][0]['snippet']['categoryId']]
    except:
        category = None
    
    data = [video_title, user, date_posted, like_count, comment_count, view_count, description, topic_details, video_tags, category]
    
    
    return data
    