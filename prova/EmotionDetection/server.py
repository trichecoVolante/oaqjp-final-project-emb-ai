"""
Server module for the Emotion Detection web application.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    """
    Process the input statement and return the emotion analysis.

    Retrieves the user's input from the form data, passes it to the
    emotion_detector function, and formats the response based on
    whether the input is valid or not.

    Returns:
        Response object: A JSON response containing either the emotion analysis or
        an error message with the appropriate HTTP status code.
    """
    # Get the input statement from the request
    statement = request.form.get('statement')

    # Process the statement using the emotion_detector function
    result, status_code = emotion_detector(statement)

    # Handle the case where the dominant emotion is None (invalid input)
    if status_code == 400 or result.get('dominant_emotion') is None:
        return jsonify({
            'response': 'Invalid text! Please try again.',
            'emotion_data': result
        }), 400

    # Format the response for displaying
    response_text = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, 'joy': {result['joy']} "
        f"and 'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )

    # Return the response as JSON
    return jsonify({
        'response': response_text,
        'emotion_data': result
    }), 200


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: The rendered 'index.html' template.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
