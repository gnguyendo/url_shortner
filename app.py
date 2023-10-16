import sqlite3
from flask import Flask, request, make_response
import hashlib
import base64

app = Flask(__name__)


connection = sqlite3.connect('urls.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
connection.close()

#API that shortens URL
@app.post("/shorten_url")
def shortern_url():
    try:
        connection = sqlite3.connect('urls.db')
        cursor = connection.cursor()
        original_url = request.args['original_url']
        hash = md5_hash(original_url)
        shortened_url = url_from_hash(hash)
        cursor.execute("SELECT original_url FROM urls WHERE shortened_url = ?;", (shortened_url,))
        result = cursor.fetchone()
        if (result):
            response = make_response("URL Exists Already", 200)
        else:
            cursor.execute("INSERT INTO urls (original_url, shortened_url) VALUES (?, ?);",  (original_url, shortened_url))
            response = make_response(shortened_url, 200)
        connection.commit()
        cursor.close()
        response.mimetype = "text/plain"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

#API that returns original URL from a shortened URL
@app.get("/redirect_url")
def redirect_url():
    try:
        shortened_url = request.args['shortened_url']
        connection = sqlite3.connect('urls.db')
        cursor = connection.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE shortened_url = ?;", (shortened_url,))
        result = cursor.fetchone()
        connection.commit()
        cursor.close()

        response = make_response(result[0], 200)
        response.mimetype = "text/plain"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")


#API for Listings all URLS
@app.get("/list_urls")
def list_urls():
    try:
        connection = sqlite3.connect('urls.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM urls")
        result = cursor.fetchall()
        connection.commit()
        cursor.close()

        response = make_response(result, 200)
        response.mimetype = "text/plain"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

    
def md5_hash(url):
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return (m.hexdigest())

def url_from_hash(hash):
    return f"www.shortenedurl.com/{hash}"