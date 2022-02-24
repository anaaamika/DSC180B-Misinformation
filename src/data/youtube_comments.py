import sys 
sys.path.insert(0, '../../secrets')

from googleapiclient.discovery import build
from youtubekeys import api_key

def comment_data(video_ids_fn, outfolder="data"):
    data_fields = ["video_id", "comment_id", "comment_text", "parent_comment", "reply_count", "like_count", "user"]
    with open(outfolder+"comment_data.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_fields)
  
    with open(video_ids_fn) as fn:
        for video_id in fn:
            try:
                comment_data = fetch_comment(video_id)
                with open(outfolder+"comment_data.csv", 'a') as f:
                    writer = csv.writer(f)
                    writer.writerows(comment_data)
            except:
                pass  
    return

def fetch_comments(video_id):
    
    comments = []
    
    # creating youtube resource object
    youtube = build('youtube', 'v3', developerKey=api_key)
  
    # retrieve youtube video results
    video_response=youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()
    
    # iterate video response
    while video_response:
        # extracting required info from each result object 
        for item in video_response['items']:
            parent_id = None
        
            # Extracting comments
            comment_id = item['snippet']['topLevelComment']['id']
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
    
              
            # counting number of reply of comment
            reply_count = item['snippet']['totalReplyCount']
            
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            user = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            
            data = [video_id, comment_id, comment_text, parent_id, reply_count, like_count, user]
            comments.append(data)
             
            # if reply is there
            if reply_count>0:
               
                # iterate through all reply
                for reply in item['replies']['comments']:
                    # Extract reply
                    parent_id = reply['snippet']['parentId']
                    comment_id = reply['id']
                    comment_text = reply['snippet']['textDisplay']

                    # counting number of reply of comment
                    try:
                        reply_count = reply['snippet']['totalReplyCount']
                    except:
                        reply_count = 0

                    like_count = reply['snippet']['likeCount']
                    user = reply['snippet']['authorChannelId']['value']
                      
                    data = [video_id, comment_id, comment_text, parent_id, reply_count, like_count, user]
                    comments.append(data)
                    
                    
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id
                ).execute()
        else:
            break
    return comments

# if __name__ == '__main__':
#     video_id = "OlWiPRWS-88"
#     fetch_comments(video_id)