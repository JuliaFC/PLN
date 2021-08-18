from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import random
ELASTICSEARCH_URL = "https://search-projetopln-axxqpsiqh2rdzthlp5asxoelwi.us-east-2.es.amazonaws.com/"

responsesTexts = {'director_to_movie': [' directed ', ' was the director of ', ' was the responsable of '],
 'movie_to_director': [' was directed by ', ' was conducted by ', ' was headed by '],
 'actor_to_movie': [' starred in ', ' acted in ', ' has been actor of '],
 'movie_to_actor': [' had a cast of ', ' was starred by ', ' was acted by '],
 'writer_to_movie': [' wrote ', ' is the author of ', ' is responsible for '],
 'movie_to_writer': [' was written by ', ' has been written by ', ' had as writer '],
 'movie_to_genre': [' is classified as ', ' has been classified as ', ' is classified as '],
 'movie_to_tags': [' is tagged as ', ' can be described as ', ' is about '],
 'tag_to_movie': [' is the main tag to ', ' is the tag of ', ' tags the movie '],
 'movie_to_imdb_votes': [' has the number of votes ', ' has the number of votes ', ' has the number of votes '],
 'movie_to_language': [' is played in ', '\'s language is ', ' original language is '],
 'movie_to_imdb_rating': [' has the IMDB rating of ', ' is rated ' , ' has the IMDB rating of '],
 'movie_to_year': [' has been released in ', ' has been published in ', ' was first seen in ']
 }


class ActionAnswerObject(Action):

    def name(self) -> Text:
        return "action_answer_object"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # print(tracker.latest_message)
        last_intent = tracker.get_intent_of_latest_message()
        if not last_intent:
            dispatcher.utter_message(text="Sorry, I did not understand. Could repeat in other words?")
            return []
        print(last_intent)

        entity = " ".join(entity_object['value'] for entity_object in tracker.latest_message['entities'])

        print(entity)
        # print(type(entity))
        if not entity:
            dispatcher.utter_message(
                text="Sorry, I couldn't understand what you meant. Do you mind saying it with other words?")
            return []
        random_number = random.randint(0,2)
        responses = requests.get(
            ELASTICSEARCH_URL + f"movies/_search?q={entity}")
        responses = responses.json()["hits"]["hits"]
        for response in responses:
            response_intent = response["_source"]["intent"].strip('\n')
            if response_intent == last_intent:
                dispatcher.utter_message(text=entity + responsesTexts[last_intent][random_number] + response["_source"]["response"])
                dispatcher.utter_message(text="Well, what would you like to ask next?")
                return []
        
        dispatcher.utter_message(text="Sorry, I couldn't find the information you wanted in my database. Why don't you try another question?")
        
        return []

