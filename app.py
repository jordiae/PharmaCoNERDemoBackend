from flask import Flask, render_template, request, Response
from run_pharmaconer import run_pharmaconer

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    result = request.form
    return Response(run_pharmaconer(result['Text']), mimetype='text/utf-8')


@app.route('/')
def form():
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
