from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

ELASTICSEARCH_URL = "https://search-projetopln-axxqpsiqh2rdzthlp5asxoelwi.us-east-2.es.amazonaws.com/"

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
                text="Sorry, I couldn't understand what you meant")
            return []
        
        responses = requests.get(
            ELASTICSEARCH_URL + f"movies/_search?q={entity}")
        responses = responses.json()["hits"]["hits"]

        for response in responses:
            response_intent = response["_source"]["intent"].strip('\n')
            if response_intent == last_intent:
                dispatcher.utter_message(text=response["_source"]["response"])
                return []
        
        dispatcher.utter_message(text="Sorry, I couldn't find the information you wanted in my database")
        
        return []

