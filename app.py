import sys
import os
import io

from flask import Flask, flash, redirect, request, render_template

app = Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Data Received")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
