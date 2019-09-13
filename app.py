from flask import Flask, render_template, request, Response, jsonify, g
import os
from pharmaconer_runner import PharmaCoNERRunner
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
# DATABASE = "./logs.db"


def start(server=True):
    """Initialize config"""
    '''
    # Database
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("CREATE TABLE queries (original_text TEXT, timestamp INTEGER);")
        cur.execute("CREATE TABLE errors (message TEXT, timestamp INTEGER);")
        conn.commit()
        conn.close()
    '''
    # PharmaCoNER
    if server:
        pharmaconer_path = '/srv/PharmaCoNERTaggerDemo/PlanTL-PharmacoNER'
        output_path = '/srv/PharmaCoNERTaggerDemo/demos_output'
        parameters_path = '/srv/PharmaCoNERTaggerDemo/PharmaCoNERDemoBackend/pharmaconer_deploy_parameters.ini'
    else:
        pharmaconer_path = '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/src/CustomNeuroNER/'
        output_path = '/home/jordiae/Documents/PharmacoNERTask/FarmacoNER/task/deploy_test_output2'
        parameters_path = '/home/jordiae/PycharmProjects/PharmaCoNERDemoBackend/pharmaconer_deploy_parameters.ini'
    pharmaCoNERRunner = PharmaCoNERRunner(pharmaconer_path, output_path, parameters_path)
    global pharmaCoNERRunner


start()

'''
def get_db():
    """Helper to get database"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Helper to close database"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
'''

@app.route('/api/submit', methods=['POST'])
def api_submit():
    """Submit form with text to tag, returns JSON"""
    result = request.form
    output = pharmaCoNERRunner.run(result['inputText'])
    return jsonify(status=output['status'], data=output['data'])


'''
@app.route('/submit', methods=['POST'])
def submit():
    """Submit form with text to tag"""
    result = request.form
    output = pharmaCoNERRunner.run(result['inputText'])
    plain_text_res = str(output)
    return Response(plain_text_res, mimetype='text/utf-8')


@app.route('/')
def form():
    """Home page, form"""
    return render_template('form.html')
'''

if __name__ == '__main__':
    app.run()
