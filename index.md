# Analyzing the Spread of YouTube Misinformation Through Twitter

## Background
Millions of people use platforms such as YouTube, Facebook, Twitter, and other social media networks. While these platforms grew popular for their social aspects of connecting people, they have also become popular ways to share and consume news. Since these platforms are so accessible, information spreads rapidly and virally. One key issue is that social media can be a core source of misinformation as these platforms are often used to establish a narrative and conduct propaganda without verification or fact-checking. Over the past decade, the proliferation of misinformation has created concern in terms of social progress, politics, education, and national unification. Reports from the Pew Research Center show that 64% of Americans are confused about current events because of the rampant presence of fake news on social media and 23% have passed on misinformation to their contacts both intentionally and unintentionally [1]. Thus, it's clear that misinformation spreads very easily on social media platforms compared to other avenues of communication. 

People are increasingly engaging with content that is often flashy and spreading misinformation (i.e conspiracy theories) but not engaging in fact-checking with the same fervor. Fact-checking and verification of online information is also a complicated task. Many accounts do not represent real people, posts can be sponsored, some users may be bots, and political affiliations are usually not disclosed. Sometimes it is impossible to differentiate between genuine content and content that is intended to manipulate opinions. This makes it difficult to validate information with the large volume of content churned out daily even for the most diligent and fact-checking individuals. As a result, many platforms have begun implementing more fact-checking to combat misinformation at a wider scale but the effectiveness of these initiatives is unknown. 

Misinformation has been shown to mobilize people in dangerous ways and distract people from truthful cases of wrongdoing or public safety. We hope that with our project, we are able to dissect the spread of misinformation regarding public health over a time period in which the nation experienced major public health and safety issues such as the COVID-19 pandemic, mask mandates, uncertainties regarding medical treatments and development of new vaccines. We hope to understand how Twitter and YouTube’s platforms interacted and aided the spread of misinformation. This will allow us to then determine how we can reduce the spread of misinformation by understanding effective policies against misinformation and creating better misinformation detection pipelines.

### What We Hope to Learn
Beyond gaining a general understanding of the spread of misinformation on YouTube, we want to answer the following questions:  
1. How much public health misinformation spread on Twitter is from Youtube?
2. How effectively does YouTube’s platform detect public health misinformation?
3. How do YouTube comments aid in spreading public health misinformation?

## Our Methods
### Data Gathering and Cleaning 
We first **gathered tweets using the Twitter API**. Using datasets of all tweet ids released on the Twitter platform from January 1, 2021 to December 31, 2021, we rehydrated tweet ids into full tweet objects using the Twarc python library. From there, we selected any tweets with hashtags and text that include health related keywords and a link to YouTube. We be extracted the YouTube links and added them to a dataset. 

From our dataset of selected tweets, we will be **extracting the YouTube links and using the YouTube API** to get data regarding the videos. We will be **collecting the video captions, comments, comment metadata like user, likes, replies, and video metadata such as channel, views, likes, dislikes, date posted, video description**. Since the focus of our project is to use NLP to determine misinformation in a video, we will not include any videos that do not have captions available in our final dataset. 

### Missingness
We also have to **account for any broken links or links to YouTube for videos that are no longer on the platform**. YouTube might remove videos for several reasons, including copyright violation, inappropriate content, harassment, hate speech, or misinformation. Additionally, a user might remove their own video. Thus, we cannot claim that all broken links lead to misinformation. However, to create a clear picture of why a video was removed, we will be recording the reason YouTube gave for the video’s removal. From there, we will be using the Wayback Machine API to view the view counts, channel subscriber counts, full descriptions of the videos, and the video's creation date. Note, that not all the videos will be archived on the Wayback Machine since more popular and widely shared videos are more likely to be collected and saved in the archive thus we will have to account for that bias. 

We also tracked how many tweet ids we could not rehydrate into complete Tweet objects. This means that the Tweets had been removed from Twitter either because they were deleted by the user or removed by the platform for violating policies. We wanted to take into consideration how this missingness could affect our analysis and final results. 

### Analysis
After we’ve collected the video caption texts from the YouTube videos, we will be **using NLP on the video captions to detect if the video propagates misinformation or not**. We will then pre-process the texts by removing any special characters and removing texts with fewer than 500 characters to reduce noise in the dataset. From there, we will generate numerical representation vectors to represent the texts from the GloVe Wikipedia embedding [9].  We will then build a Support Vector Classifier to determine if video is misinformation based on its captions. 

We will also be **considering the comments assocaiated with a video to check the spread of misinformation**. We want to determine if the comments are engaging in further misinformation, fact-checking or neither. To accomplish this, we will be building a network of commenters to see if the same users comment on multiple videos and conduct sentiment analysis on the text of the comment. This will help us determine if comments come from bot-like or spam accounts. Additionally, this will help us understand if comments can also manipulate users and promote disinformation. 

## Results
This section will include our final results. 

### Statistics
We will be including important statistics we found in our analysis such as the proportion of YouTube videos that were removed, proportion that contained misinformation, and the various types of YouTube content linked in tweets. 

### Graphs
We will also be adding all of our charts and graphs in this section. 

### Examples 
Additionally, we want to include examples of specific YouTube videos to show the process of how we extracted the text data using the YouTube API and how we detected misinformation using NLP in the captions and comments.

## Future Work
We will be discussing future avenues of exploration in this section. We will also cover any weakness that our methods had and how we could improve them.
