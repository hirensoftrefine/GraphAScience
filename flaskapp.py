## Main python file you need tu run with 
## Command python flaskapp.py

from flask import Flask, request, jsonify
from flask import render_template
import json,sys, argparse
from waitress import serve

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='My Input')


app.config['UPLOAD_FOLDER'] = "uploads/"


from views import *


if __name__ == "__main__":
        #app.run(host='0.0.0.0', port=5000, debug=True)
        serve(app, host='0.0.0.0', port=5000)

