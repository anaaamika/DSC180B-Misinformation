#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    with open("youtube-v3-api-captions.json", "r") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))
    
# Call the API's captions.list method to list the existing caption tracks.
def list_captions(youtube, video_id):
    results = youtube.captions().list(
        part="snippet",
        videoId=video_id
      ).execute()

    for item in results["items"]:
        id = item["id"]
        name = item["snippet"]["name"]
        language = item["snippet"]["language"]
        print("Caption track '%s(%s)' in '%s' language." % (name, id, language))

    return results["items"]

# Call the API's captions.download method to download an existing caption track.
def download_caption(youtube, caption_id, tfmt):
    subtitle = youtube.captions().download(
        id=caption_id,
        tfmt=tfmt
        ).execute()

    print("First line of caption track: %s" % (subtitle))
    
if __name__ == "__main__":
    # The "videoid" option specifies the YouTube video ID that uniquely
    # identifies the video for which the caption track will be uploaded.
    argparser.add_argument("--videoid",
        help="Required; ID for video for which the caption track will be uploaded.")
    # The "name" option specifies the name of the caption trackto be used.
    argparser.add_argument("--name", help="Caption track name", default="YouTube for Developers")
    # The "file" option specifies the binary file to be uploaded as a caption track.
    argparser.add_argument("--file", help="Captions track file to upload")
    # The "language" option specifies the language of the caption track to be uploaded.
    argparser.add_argument("--language", help="Caption track language", default="en")
    # The "captionid" option specifies the ID of the caption track to be processed.
    argparser.add_argument("--captionid", help="Required; ID of the caption track to be processed")
    # The "action" option specifies the action to be processed.
    argparser.add_argument("--action", help="Action", default="all")
    
    args = argparser.parse_args()

    if (args.action in ('upload', 'list', 'all')):
        if not args.videoid:
            exit("Please specify videoid using the --videoid= parameter.")

    if (args.action in ('update', 'download', 'delete')):
        if not args.captionid:
            exit("Please specify captionid using the --captionid= parameter.")

    if (args.action in ('upload', 'all')):
        if not args.file:
            exit("Please specify a caption track file using the --file= parameter.")
        if not os.path.exists(args.file):
            exit("Please specify a valid file using the --file= parameter.")
            
    youtube = get_authenticated_service(args)
    
    try:
        
        if args.action == 'list':
            list_captions(youtube, args.videoid)
        elif args.action == 'download':
            download_caption(youtube, args.captionid, 'srt')
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    else:
        print("Created and managed caption tracks.")

