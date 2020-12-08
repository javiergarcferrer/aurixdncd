from flask import Flask
app = Flask(__name__)
app.config["DEBUG"] = True

import pandas as pd

@app.route('/')
def main():
    return 'Hello World!'