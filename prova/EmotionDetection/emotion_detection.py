import requests
import json

def emotion_detector(text_to_analyze):
    # API URL and headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }

    # Input JSON format
    input_data = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        # Make the POST request to the Watson API
        response = requests.post(url, headers=headers, json=input_data)

        # Access the status_code attribute of the response
        if response.status_code == 400:
            # Return dictionary with None values for all keys
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }, 400

        # Raise exception for bad requests (status codes >= 400)
        response.raise_for_status()

        # Parse the JSON response into a dictionary
        response_data = response.json()

        # Extract the relevant emotions from the response
        emotion_predictions = response_data.get('emotionPredictions', [])
        if emotion_predictions:
            emotions = emotion_predictions[0].get('emotion', {})
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)

            # Create a dictionary of emotions and their scores
            emotion_dict = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness
            }

            # Find the dominant emotion (emotion with the highest score)
            dominant_emotion = max(emotion_dict, key=emotion_dict.get)

            # Add the dominant emotion to the dictionary
            emotion_dict['dominant_emotion'] = dominant_emotion

            # Return the formatted result and status code 200 (success)
            return emotion_dict, 200

        else:
            # If no emotion predictions are found, return None values
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }, 400

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            # Return dictionary with None values for all keys
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }, 400
        else:
            # For other HTTP errors, return an error message and the status code
            return {"error": f"HTTP error occurred: {http_err}"}, response.status_code
    except Exception as err:
        # For any other exceptions, return an error message and status code 500
        return {"error": f"An error occurred: {err}"}, 500

# Example usage
if __name__ == "__main__":
    sample_text = "I am glad this happened"
    result, status_code = emotion_detector(sample_text)
    print(result)
    print(f"Status Code: {status_code}")
