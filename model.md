---
title: Misinformation Model
---

| [Introduction](https://anaaamika.github.io/DSC180B-Misinformation/)| [Data](https://anaaamika.github.io/DSC180B-Misinformation/data) |[Misinformation Model](https://anaaamika.github.io/DSC180B-Misinformation/model)| [Topic Modeling](https://anaaamika.github.io/DSC180B-Misinformation/topic-model) | [Sentiment Analysis](https://anaaamika.github.io/DSC180B-Misinformation/sentiment-analysis) | [References](https://anaaamika.github.io/DSC180B-Misinformation/references) |

# Building a Misinformation Detection Model
<p>The focus of this research is to detect misinformation on YouTube which was accomplished by building a NLP model to categorize whether the text of YouTube video captions contained false and misleading information or not. Since our dataset of YouTube videos were not labeled, our model was trained on a pre-labeled dataset containing the text of articles with real and fake news from Kaggle. We also created a text processing pipeline to prepare the caption texts for analysis. This included normalizing the case of the text, removing punctuation, removing stop words, tokenization, and lemmatization. Stop words are the most common words in language like “a”, “the”, “is”, “are”, etc. which do not add any context or information so removing them is important to ensuring the model focuses on the relevant terms. Tokenization is the process of splitting the text into individual words or sentences so that the model can work with smaller pieces of data that are still coherent and relevant to the context outside of the text. Lastly, lemmatization is the process of converting a word to its lemma, or returning an inflected word to its root word, in contrast to stemming which simply removes the suffix of a word.</p>
<p>Before this cleaned text data can easily be used to build a misinformation detection model, it has to be first transformed into a feature vector. For this investigation, we created a TF-IDF vector. TF-IDF stands for term-frequency inverse-document-frequency and it calculates how much a token appears in a specific document as compared to the entire text corpus. As a result of this calculation, TF-IDF is able to identify how important a word is, so in the vector the weight assigned to each token not only depends on its frequency in a document but also how recurrent that term is in the entire corpora.</p> 
<p>After vectorization, we build the final model. We tried multiple classifiers including Logistic Regression, Naive Bayes, Decision Tree and finally found that sklearn’s Passive Aggressive Classifier had the best performance based on accuracy on the training dataset which was then used to detect misinformation from the YouTube videos. This was the expected result as the Passive Aggressive Classifier is suited for online learning that deals with large sets of data and their loss function is passive when dealing with an outcome that has been correctly classified, and aggressive when a miscalculation takes place, thus the model is constantly self-updating and adjusting. Running this model on our dataset of YouTube captions resulted in 23% of the video captions being classified as misinformation. </p> 

### Model Evaluation 
| Model| Accuracy Score |

| ----------- | ----------- |

| Logistic Regression| 0.704|
| Naive Bayes| 0.634|
| Decision Tree| 0.787|
| Passive Agressive Classifier| 0.790|

