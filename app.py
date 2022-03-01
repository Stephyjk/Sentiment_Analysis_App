from flask import Flask, render_template, request
import numpy as np
import re
import os
from numpy import array
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import load_model


IMAGE_FOLDER = os.path.join('static', 'img_pool')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


def init():
    global model, graph
    # load the pre-trained Keras model
    model = load_model('sentiment_analysis_model_new.h5')
    # graph = tf.get_default_graph()

# Code for Sentiment Analysis


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("index.html")


@app.route('/sentiment_analysis_prediction', methods=['POST', "GET"])
def sent_anly_prediction():
    if request.method == 'POST':
        text = request.form['text']
        Sentiment = ''
        max_review_length = 500
        word_to_id = imdb.get_word_index()
        strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
        text = text.lower().replace("<br />", " ")
        text = re.sub(strip_special_chars, "", text.lower())

        words = text.split()  # split string into a list
        x_test = [[word_to_id[word] if (
            word in word_to_id and word_to_id[word] <= 20000) else 0 for word in words]]
        # Should be same which you used for training data
        x_test = sequence.pad_sequences(x_test, maxlen=500)
        vector = np.array([x_test.flatten()])
        # with graph.as_default():
        probability = model.predict(array([vector][0]))[0][0]
        # class1 = model.predict_classes(array([vector][0]))[0][0]
        class1 = (model.predict(array([vector][0]))[
                  0][0] > 0.5).astype("int32")

        if class1 == 0:
            sentiment = 'Negative'
            img_filename = os.path.join(
                app.config['UPLOAD_FOLDER'], 'sad_face.jpg')
            response = 'We are sorry to hear that'
        else:
            sentiment = 'Positive'
            img_filename = os.path.join(
                app.config['UPLOAD_FOLDER'], 'smiley_face.jpg')
            response = 'We are happy to hear that'
    return render_template('index.html', text=text, sentiment=sentiment, probability=probability, image=img_filename, response=response)
# Code for Sentiment Analysis


if __name__ == "__main__":
    init()
    app.run()
