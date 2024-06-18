#import os
#import sys
#import json
#import sklearn
import re
import requests
import numpy as np
import pandas as pd
from io import StringIO
from sklearn import svm
from nrclex import NRCLex
from datasets import load_dataset
#from textblob import TextBlob
from collections import Counter
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from googletrans import Translator
translator = Translator()

# Importing NLTK modules
import nltk
#nltk.download('punkt')
#nltk.download('vader_lexicon')
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
#from nltk.sentiment import SentimentIntensityAnalyzer


################ ANALYZER-1 START ############################

class EmotionAnalyzerLeXmo:
    def __init__(self, desired_emotions, desired_sentiments):
        self.desired_emotions = desired_emotions
        self.desired_sentiments = desired_sentiments
        
    
    def LeXmo(self, text):

        '''
          Takes text and adds if to a dictionary with 10 Keys  for each of the 10 emotions in the NRC Emotion Lexicon,
          each dictionay contains the value of the text in that emotions divided to the text word count
          INPUT: string
          OUTPUT: dictionary with the text and the value of 10 emotions
          '''

        response = requests.get('https://raw.github.com/dinbav/LeXmo/master/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
        nrc = StringIO(response.text)



        LeXmo_dict = {'text': text, 'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'negative': [],
                      'positive': [], 'sadness': [], 'surprise': [], 'trust': []}

        emolex_df = pd.read_csv(nrc,
                                names=["word", "emotion", "association"],
                                sep=r'\t', engine='python')

        emolex_words = emolex_df.pivot(index='word',
                                       columns='emotion',
                                       values='association').reset_index()
        emolex_words.drop(emolex_words.index[0])

        emotions = emolex_words.columns.drop('word')

        stemmer = SnowballStemmer("english")

        document = word_tokenize(text)

        word_count = len(document)
        rows_list = []
        for word in document:
            word = stemmer.stem(word.lower())

            emo_score = (emolex_words[emolex_words.word == word])
            rows_list.append(emo_score)

        df = pd.concat(rows_list)
        df.reset_index(drop=True)

        for emotion in list(emotions):
            LeXmo_dict[emotion] = df[emotion].sum() / word_count

        return LeXmo_dict


    def perform_analysis(self, text):
        try:
            emo = self.LeXmo(text)
            emo.pop('text', None)
            # Remove anticipation emotion
            emo.pop('anticipation', None)
            extracted_emotions = {emotion.lower(): round(float(emo.get(emotion.lower(), "0.0")) * 100, 2) for emotion in
                                  self.desired_emotions.keys()}
            extracted_sentiment = {sentiment.lower(): round(float(emo.get(sentiment.lower(), "0.0")) * 100, 2) for sentiment in
                                   self.desired_sentiments.keys()}

            return {
                "library": "lexmo",
                "result": extracted_emotions,
                "max_prediction": {
                    "label": max(extracted_emotions, key=extracted_emotions.get),
                    "percentage": max(extracted_emotions.values())
                }
            }

        except Exception as e:
            #print(f"Error during emotion analysis: {str(e)}")
            return {
                "library": "lexmo",
                "result": {},
                "max_prediction": {"label": "", "percentage": 0}
            }

    def analyze(self, new_text):
        desired_emotions = {"fear": "0.0", "anger": "0.0", "surprise": "0.0", "sadness": "0.0", "disgust": "0.0", "joy": "0.0",
                            "anticipation": "0.0"}
        desired_sentiments = {"positive": "0.0", "negative": "0.0", "neutral": "0.0"}

        analyzer = EmotionAnalyzerLeXmo(desired_emotions, desired_sentiments)

        extracted_emotions = analyzer.perform_analysis(new_text)

        if extracted_emotions["max_prediction"]["percentage"] == 0:
            # If all extracted emotions are 0, set results to None
            results = None
        else:
            results = extracted_emotions

        return results

################ ANALYZER-1 END ############################

################ ANALYZER-2 START ############################

class EmotionAnalyzerNRCLex:
    def __init__(self, desired_emotions):
        # Remove anticipation emotion from desired_emotions
        self.desired_emotions = [emotion for emotion in desired_emotions if emotion != 'anticipation']

    def get_emotions_for_text(self, text):
        # Analyze emotions in the text
        text_object = NRCLex(text)
        
        # Get overall emotion frequencies
        overall_emotion_frequencies = text_object.affect_frequencies

        # Extract desired emotion frequencies
        emotion_frequencies = {emotion: overall_emotion_frequencies.get(emotion, 0) for emotion in self.desired_emotions}

        # Calculate the percentage for each emotion
        total_words = len(text_object.words)
        emotion_percentages = {emotion: count * 100 if total_words > 0 else 0 for emotion, count in emotion_frequencies.items()}

        # Round the emotion percentages to two decimal places
        rounded_emotion_percentages = {emotion: round(percentage, 2) for emotion, percentage in emotion_percentages.items()}

        # Create the result dictionary
        max_emotion = max(emotion_percentages, key=emotion_percentages.get)
        max_prediction = {"label": max_emotion, "percentage": rounded_emotion_percentages[max_emotion]}
        # Check if all emotion frequencies are 0
        all_zero = all(value == 0 for value in emotion_frequencies.values())

        # Return {"result": null} if all emotions are 0
        return {
            "library": "nrclex",
            "result": rounded_emotion_percentages,
            "max_prediction": max_prediction
        } if not all_zero else None

    def analyze(self, new_text):
        # Define the desired emotions
        desired_emotions = ["fear", "anger", "surprise", "sadness", "disgust", "joy", "anticipation"]

        # Create an instance of the EmotionAnalyzer class
        emotion_analyzer = EmotionAnalyzerNRCLex(desired_emotions)
        # Get emotion analysis results
        results = emotion_analyzer.get_emotions_for_text(new_text)

        # Print the results in the specified format
        return results

################ ANALYZER-2 END ############################

################ ANALYZER-3 START ###########################

class EmotionAnalyzerWordNet:
    def __init__(self, target_emotions):
        # Remove anticipation emotion from target_emotions
        self.target_emotions = [emotion for emotion in target_emotions if emotion != 'anticipation']

    def get_emotions_for_text(self, text):
        total_words = 0
        emotion_count = {emotion: 0 for emotion in self.target_emotions}

        words = nltk.word_tokenize(text)
        total_words = len(words)

        for word in words:
            synsets = wordnet.synsets(word)
            for synset in synsets:
                for lemma in synset.lemmas():
                    for emotion in self.target_emotions:
                        if emotion in lemma.name():
                            emotion_count[emotion] += 1

        emotion_percentage = {emotion: min(max(round((count / total_words) * 100, 2), 0), 100) for emotion, count in emotion_count.items()}

        max_emotion = max(emotion_percentage, key=emotion_percentage.get)

        # Check if all emotion percentages are 0
        all_zero = all(value == 0 for value in emotion_percentage.values())

        # Set result to null if all emotion percentages are 0
        result = None if all_zero else {
            "library": "wordnet",
            "result": emotion_percentage,
            "max_prediction": {"label": max_emotion, "percentage": emotion_percentage[max_emotion]}
        }

        return result

    def analyze(self, new_text):
        # Specify the target emotions
        target_emotions = ["fear", "anger", "surprise", "sadness", "disgust", "joy"]

        # Create an instance of the EmotionAnalyzer class
        emotion_analyzer = EmotionAnalyzerWordNet(target_emotions)

        # Get emotion analysis results
        results = emotion_analyzer.get_emotions_for_text(new_text)

        # Print the results in the specified format
        return results

################ ANALYZER-3 END ############################

################ ANALYZER-4 START ##########################

class EmotionClassifierDatasets:
    def __init__(self):
        self.emotion_labels = {
            0: 'sadness',
            1: 'joy',
            2: 'disgust',
            3: 'anger',
            4: 'fear',
            5: 'surprise'
        }
        self.frequency_threshold = 5
        # Experiment with different values for min_df
        self.utterance_vec = CountVectorizer(min_df=self.frequency_threshold, tokenizer=nltk.word_tokenize, token_pattern=None)
        self.tfidf_transformer = TfidfTransformer()
        self.svm_linear_clf = svm.LinearSVC(max_iter=2000, dual=True)

    def load_emotion_dataset(self):
        dataset = load_dataset("emotion", trust_remote_code=True)
        train_data = dataset['train']
        validation_data = dataset['validation']
        return train_data, validation_data

    def preprocess_dataframe(self, dataframe):
        dataframe.rename(columns={'label': 'emotion'}, inplace=True)
        return dataframe['text'].tolist(), dataframe['emotion'].tolist()

    def train_classifier(self, training_tfidf_vectors, training_labels):
        self.svm_linear_clf.fit(training_tfidf_vectors, training_labels)

    def predict_sentiment(self, new_text):
        new_text_instances = [new_text]
        new_text_count_vectors = self.utterance_vec.transform(new_text_instances)
        new_text_tfidf_vectors = self.tfidf_transformer.fit_transform(new_text_count_vectors)

        # Use decision_function to get the signed distance of samples to the hyperplane
        decision_values = self.svm_linear_clf.decision_function(new_text_tfidf_vectors)

        # Apply the sigmoid function to convert decision values to probabilities
        probabilities = 1 / (1 + np.exp(-decision_values))

        # Convert probabilities to percentage format with two decimal places
        percentages = np.round(probabilities * 100, 2).tolist()[0]

        # Find the emotion with the maximum probability
        max_emotion_index = np.argmax(probabilities)
        max_emotion_label = self.emotion_labels[max_emotion_index]
        max_emotion_value = round(percentages[max_emotion_index], 2)
        max_emotion_score = round(max_emotion_value, 0)

        # Convert percentages to dictionary
        emotion_percentages = dict(zip(self.emotion_labels.values(), percentages))
        max_prediction = {"label": max_emotion_label, "percentage": max_emotion_score}
        res = {"library": "datasets", "result": emotion_percentages, "max_prediction": max_prediction}

        return res

    def analyze(self, new_text):
        emotion_classifier = EmotionClassifierDatasets()

        train_data, _ = emotion_classifier.load_emotion_dataset()

        dftrain = pd.DataFrame(train_data)
        training_instances, training_labels = emotion_classifier.preprocess_dataframe(dftrain)

        # Experiment with different values for min_df
        training_count_vectors = emotion_classifier.utterance_vec.fit_transform(training_instances)
        training_tfidf_vectors = emotion_classifier.tfidf_transformer.fit_transform(training_count_vectors)

        emotion_classifier.train_classifier(training_tfidf_vectors, training_labels)

        pred_percentages = emotion_classifier.predict_sentiment(new_text)

        return pred_percentages

################ ANALYZER-4 END ############################

################ SENTIMENT ANALYZER START ############################
class SentimentAnalyzerTransformers:
    def __init__(self):
        self.sentiment_pipeline = pipeline('sentiment-analysis')

    def analyze_sentiment(self, text):
        results = self.sentiment_pipeline(text)
        sentiment_label = results[0]['label']
        sentiment_score = results[0]['score']
            
        return sentiment_label.capitalize(), sentiment_score

def get_threshold(sentiment, score):
	#{"fear": 0.1, "anger": 0.2, "disgust": 0.3, "sadness": 0.4, "anger,sadness":0.5, "joy":0.6, "surprise":0.8 }
    if(sentiment=="Negative"):
        threshold = 0.4
        if(score < 0.998200000000000):
            threshold = 0.1
        elif(score < 0.999300000000000):
            threshold = 0.2
        elif(score < 0.999400000000000):
            threshold = 0.3
        elif(score > 0.999400000000000):
            threshold = 0.4
        elif(score > 0.999500000000000):
            threshold = 0.5
    if(sentiment=="Positive"):
        threshold = 0.6
        if(score > 0.9994000000000000):
            threshold = 0.8
        
    return threshold

def fix_string_issue(s):
    # Replace periods between words with a space
    fixed_s = re.sub(r'\.(?=\w)', ' ', s)
    return fixed_s

def main(config, new_text):
    # Check if a command-line argument is provided
    #if len(sys.argv) > 1:
        # Retrieve the text input from the command line
    #    new_text = sys.argv[1]
    #else:
        # Provide a default text if no command-line argument is provided
    #    new_text = "Empty Text"
    #sentiment_analyzer = SentimentAnalyzer(new_text)
    #sentiment, sentiment_score = sentiment_analyzer.analyze_sentiment()
    
    if len(new_text) == 0:
        new_text="Wow, I am so happy."
   
    new_text = new_text[:1500]
    new_text = fix_string_issue(new_text)
    
    #TRANSALTE TEXT INTO ENGLISH
    #APPLY GOOGLE TRANSLATE ONLY WHEN IT IS True
    if config.get('googleTranslate', True):
        translated = translator.translate(new_text, dest='en')
        new_text = translated.text
   
    
    sentiment_analyzer = SentimentAnalyzerTransformers()
    sentiment, sentiment_score = sentiment_analyzer.analyze_sentiment(new_text)
    threshold_value = get_threshold(sentiment, sentiment_score)
    #print(sentiment, sentiment_score)
    
    final_result = {
        "library": "esanalyzer",
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "threshold_value":threshold_value
    }

    #IF SENTIMENT IS ENABLED
    if config.get('emotions', True):
        # Define possible positive, negative, and neutral emotions with threshold values
        possible_positive_emotions = {"joy": 0.6, "surprise": 0.8}
        possible_negative_emotions = {"fear": 0.1, "anger": 0.2, "disgust": 0.3, "sadness": 0.4, "anger,sadness":0.5}
        possible_neutral_emotions = {"neutral": 0.0}

        analyzers = [
            (EmotionAnalyzerLeXmo, {"desired_emotions": possible_positive_emotions, "desired_sentiments": {}}),
            (EmotionAnalyzerNRCLex, {"desired_emotions": possible_positive_emotions}),
            (EmotionAnalyzerWordNet, {"target_emotions": ["fear", "anger", "surprise", "sadness", "disgust", "joy"]}),
            (EmotionClassifierDatasets, {}),
        ]
        
        found_valid_emotions = False
        all_analyzers_results = []
        for analyzer_cls, init_args in analyzers:
            # Create an instance of the analyzer
            analyzer_instance = analyzer_cls(**init_args)

            # Call the analyze method
            emotions = analyzer_instance.analyze(new_text)
            #print(analyzer_cls)
            #print(emotions)
            if emotions is not None:
                emotions.update({"sentiment": sentiment, "sentiment_score": sentiment_score})
                all_analyzers_results.append(emotions)
                max_prediction_label = emotions.get("max_prediction", {}).get("label", "")
                max_prediction_percentage = emotions.get("max_prediction", {}).get("percentage", 0)

                # Validate emotions based on sentiment and possible emotions
                if(sentiment == "Positive" and max_prediction_label in possible_positive_emotions):
                    found_valid_emotions = True
                    final_result = emotions
                    break  # Stop calling other analyzers if the emotions are valid
                elif(sentiment == "Negative" and max_prediction_label in possible_negative_emotions):
                    found_valid_emotions = True
                    final_result = emotions
                    break  # Stop calling other analyzers if the emotions are valid
                elif(sentiment == "Neutral" and max_prediction_label in possible_neutral_emotions):
                    found_valid_emotions = True
                    final_result = emotions
                    break  # Stop calling other analyzers if the emotions are valid
        #print("all_analyzers_results")
        #print(all_analyzers_results)
        all_analyzers_results = []
        if not found_valid_emotions:
            if not all_analyzers_results:
                if sentiment == "Positive":
                    # If sentiment is positive, choose max prediction label from possible_positive_emotions
                    max_prediction_label = max(possible_positive_emotions, key=possible_positive_emotions.get)
                    max_prediction_percentage = possible_positive_emotions[max_prediction_label]
                elif sentiment == "Negative":
                    # If sentiment is negative, choose max prediction label from possible_negative_emotions
                    max_prediction_label = max(possible_negative_emotions, key=possible_negative_emotions.get)
                    max_prediction_percentage = possible_negative_emotions[max_prediction_label]
                elif sentiment == "Neutral":
                    # If sentiment is neutral, choose max prediction label from possible_neutral_emotions
                    max_prediction_label = max(possible_neutral_emotions, key=possible_neutral_emotions.get)
                    max_prediction_percentage = possible_neutral_emotions[max_prediction_label]

                # No valid emotions found, generate default result for the max prediction label and percentage
                max_prediction_percentage = round(abs(max_prediction_percentage * 100))
                final_result["max_prediction"]["label"] = max_prediction_label
                final_result["max_prediction"]["percentage"] = max_prediction_percentage
                final_result["result"] = {max_prediction_label: max_prediction_percentage}
                
            else:
                max_prediction_labels = [result.get("max_prediction", {}).get("label", "") for result in all_analyzers_results]

                # Use Counter to find the most common label
                most_common_labels = Counter(max_prediction_labels).most_common()
                #print("most_common_labels")
                #print(most_common_labels)
                
                # After choosing the most common labels
                max_prediction_labels = [label for label, _ in most_common_labels]

                # Separate the labels based on emotion categories
                positive_labels = [label for label in max_prediction_labels if label in possible_positive_emotions]
                negative_labels = [label for label in max_prediction_labels if label in possible_negative_emotions]
                neutral_labels = [label for label in max_prediction_labels if label in possible_neutral_emotions]
                
                # Choose the label based on the emotion category with the highest score
                if positive_labels:
                    chosen_labels = positive_labels
                elif negative_labels:
                    chosen_labels = negative_labels
                elif neutral_labels:
                    chosen_labels = neutral_labels
                else:
                    # Handle the case where no valid emotion category is found
                    chosen_labels = []


                # Extract sentiment, sentiment_score, and percentage based on max_prediction_label
                if max_prediction_label in possible_positive_emotions:
                    sentiment = "Positive"
                    sentiment_score = possible_positive_emotions[max_prediction_label]
                elif max_prediction_label in possible_negative_emotions:
                    sentiment = "Negative"
                    sentiment_score = possible_negative_emotions[max_prediction_label]
                elif max_prediction_label in possible_neutral_emotions:
                    sentiment = "Neutral"
                    sentiment_score = possible_neutral_emotions[max_prediction_label]
                else:
                    # Handle the case where max_prediction_label is not found in any emotion dictionary
                    sentiment = "Unknown"
                    sentiment_score = 0.0

                # Use the chosen values to populate the final result
                max_prediction_percentage = round(abs(sentiment_score * 100))
                final_result["library"] = "voting"
                final_result["max_prediction"]["label"] = ", ".join(chosen_labels)
                final_result["max_prediction"]["percentage"] = max_prediction_percentage
                final_result["result"] = {label: max_prediction_percentage for label in chosen_labels}
                final_result["sentiment"] = sentiment
                final_result["sentiment_score"] = sentiment_score


        #IF PERCENTAGE IS LESS THAN 11
        #final_result["sentiment_score"] = round(final_result["sentiment_score"], 2)
        if final_result["max_prediction"]["percentage"] < 11:
            final_result["max_prediction"]["percentage"] *= 10
            final_result["max_prediction"]["percentage"] = round(final_result["max_prediction"]["percentage"], 2)
            
            if final_result["max_prediction"]["percentage"] > 100:
                final_result["max_prediction"]["percentage"] = 100
                
                    
    return  final_result
    #print(json.dumps(final_result))


#if __name__ == "__main__":
#    main()

class EmotionAnalyzer:
    def __init__(self, config):
        self.config = config
        #print(self.config)
    #@staticmethod
    def analyze(self, text):
        # Call the main function and pass the text
        result = main(self.config, text)
        return result
        
################ SENTIMENT ANALYZER END ############################