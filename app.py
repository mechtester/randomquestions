from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import zlib

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_sheet')
def select_sheet():
    return render_template('select_sheet.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith(('xls', 'xlsx')):
        file.save('uploaded_file.xlsx')
        sheet_names = pd.ExcelFile('uploaded_file.xlsx').sheet_names
        return render_template('select_sheet.html', sheet_names=sheet_names)
    else:
        return "Please upload a valid Excel file."

@app.route('/practice', methods=['POST'])
def shuffle_questions():
    sheet_name = request.form['sheet']
    df = pd.read_excel('uploaded_file.xlsx', sheet_name=sheet_name)
    shuffled_questions = df.sample(frac=1).to_dict(orient='records')
    session['shuffled_questions'] = shuffled_questions
    session['question_index'] = 0
    return redirect(url_for('view_question'))

@app.route('/question')
def view_question():
    shuffled_questions = session.get('shuffled_questions')
    question_index = session.get('question_index', 0)
    total_questions = len(shuffled_questions) if shuffled_questions else 0
    if shuffled_questions is None or question_index >= len(shuffled_questions):
        return "No questions available. Please upload an Excel file and start practicing."
    question = shuffled_questions[question_index]
    return render_template('question.html', question=question, question_index=question_index, total_questions=total_questions)

@app.route('/next_question', methods=['POST'])
def next_question():
    question_index = session.get('question_index', 0)
    question_index += 1
    session['question_index'] = question_index
    return redirect(url_for('view_question'))

@app.route('/show_answer', methods=['POST'])
def show_answer():
    question_index = int(request.form['question_index'])
    shuffled_questions = session.get('shuffled_questions')
    if shuffled_questions is None or question_index >= len(shuffled_questions):
        return "No answers available."
    answer = shuffled_questions[question_index]['ANSWERS']
    return render_template('question.html', question=shuffled_questions[question_index], question_index=question_index, answer=answer, total_questions=len(shuffled_questions))

@app.route('/store_data', methods=['POST'])
def store_data():
    data_to_store = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}  # Example data
    compressed_data = zlib.compress(str(data_to_store).encode('utf-8'))
    session['compressed_data'] = compressed_data
    return 'Data stored successfully.'

@app.route('/retrieve_data')
def retrieve_data():
    compressed_data = session.get('compressed_data')
    if compressed_data:
        decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
        return f'Retrieved Data: {decompressed_data}'
    else:
        return 'No data available.'

if __name__ == '__main__':
    app.run(debug=True)
