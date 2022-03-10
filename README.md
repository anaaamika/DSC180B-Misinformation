# DSC180B Misinformation Project
Project Website: https://anaaamika.github.io/DSC180B-Misinformation/

## Build Instructions
Ensure that you have twarckeys.py and youtubekeys.py files in your secrets folder. The twarckeys.py file should contain the variables consumer_key, consumer_secret, access_token, access_token_secret populated from the project keys and tokens from [the Developer Portal for the Twitter API](https://developer.twitter.com/en/portal/dashboard). The youtubekeys.py file should contain the variable api_key populated with a API key for [the YouTube Data API v3](https://developers.google.com/youtube/v3). 

To build the project run the following commands: 
`python run.py data`

This will populate the *data* folder with tweet datasets, YouTube video ids dataset, and datasets with YouTube metadata. 

Then run `python run.py analysis` to view preliminary analysis on the YouTube captions and metadata.

Finally, run `python run.py model` to build a misinformation detection model based on the YouTube transcripts. 
