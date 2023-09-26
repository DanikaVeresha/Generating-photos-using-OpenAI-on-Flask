from flask import Flask, request, render_template
from pymongo.mongo_client import MongoClient
import random
import datetime
import openai
from key_OpenAi import OPENAI_API_KEY

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def gener_photo():
    if request.method == 'POST':
        openai.api_key = OPENAI_API_KEY
        PROMPT = request.form['description']

        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="1024x1024",
        )
        document = response["data"][0]["url"]
        uri = "mongodb+srv://deshdesh288:Password4321@clustertest.zz1mki1.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client.db_photosGener
        collection = db.photos
        numbers_documents = random.randint(1, 1000000)
        data = [{
            "id": numbers_documents,
            "status": "The link is not active after 2 hours from the moment of generation",
            "prompt": PROMPT,
            "url": document,
            "time": datetime.datetime.now()}]
        collection.insert_many(data)
        return f'<h4>Well done! Your generated one photo!</h4> ' \
               f'<h4>id: {numbers_documents}</h4>'
    else:
        return render_template('gener_photo.html')


@app.route('/get', methods=['GET', 'POST'])
def get_photo():
    if request.method == 'POST':
        uri = "mongodb+srv://deshdesh288:Password4321@clustertest.zz1mki1.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client.db_photosGener
        collection = db.photos
        request_id = request.form['id_photo']
        url_document = collection.find_one({"id": int(request_id)})
        return f'<h4>id: {request_id}</h4> ' \
               f'<img src="{url_document["url"]}">'
    else:
        return render_template('get_photo.html')


@app.route('/show', methods=['GET', 'POST'])
def show_photo():
    if request.method == 'POST':
        uri = "mongodb+srv://deshdesh288:Password4321@clustertest.zz1mki1.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client.db_photosGener
        collection = db.photos
        documents = collection.find({})
        return render_template('show_photo.html',
                               documents=documents)
    else:
        return render_template('show_photo.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_photo():
    if request.method == 'POST':
        try:
            uri = "mongodb+srv://deshdesh288:Password4321" \
                  "@clustertest.zz1mki1.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(uri)
            db = client.db_photosGener
            collection = db.photos
            request_id = request.form['id_photo']
            collection.delete_one({"id": int(request_id)})
            return f'<h4>Well done! Your deleted one photo!</h4> ' \
                   f'<h4>id: {request_id}</h4> '
        except Exception as error:
            print(error)
            print('Not connected to MongoDB')
    else:
        return render_template('delete_photo.html')


if __name__ == '__main__':
    app.run()
