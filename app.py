from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import pandas as pd
import joblib
from radon.raw import analyze
from radon.metrics import h_visit
import ast
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'py'}
app.secret_key = 'your_secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_file_group(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()

    if first_line.startswith("class "):
        return "large_class"
    elif first_line.startswith("def "):
        return "long_method"
    else:
        return None

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    large_class_files = [file for file in files if get_file_group(os.path.join(app.config['UPLOAD_FOLDER'], file)) == 'large_class']
    long_method_files = [file for file in files if get_file_group(os.path.join(app.config['UPLOAD_FOLDER'], file)) == 'long_method']
    return render_template('index.html', large_class_files=large_class_files, long_method_files=long_method_files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return redirect(request.url)

    uploaded_files = request.files.getlist('files[]')

    for file in uploaded_files:
        if file.filename == '':
            continue

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash(f'File "{file.filename}" uploaded successfully!', 'success')
        else:
            flash(f'Invalid file "{file.filename}". Please upload a .py file.', 'error')

    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(file_path, 'r') as file:
        code = file.read()

    highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())

    return render_template('view.html', code=highlighted_code, filename=filename)

@app.route('/delete/<filename>')
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'File "{filename}" deleted successfully!', 'success')
    else:
        flash(f'File "{filename}" not found.', 'error')

    return redirect(url_for('index'))

@app.route('/detect_large_class/<filename>')
def detect_large_class(filename):
    type = "large_class"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metrics, halstead_metrics = extract_metrics(file_path)
    row_data = {
        'difficulty': halstead_metrics.total.difficulty,
        'scloc': metrics.sloc,
        'loc': metrics.loc,
        'effort': halstead_metrics.total.effort,
        'time': halstead_metrics.total.time,
        'volume': halstead_metrics.total.volume,
        'bugs': halstead_metrics.total.bugs,
        'lloc': metrics.lloc,
        'comments': metrics.comments,
        'blanks': metrics.blank,
        'single_comments': metrics.single_comments,
        'calculated_length': halstead_metrics.total.calculated_length,
    }
    
    df = pd.DataFrame([row_data])
    normalized_data = normalize_dataframe(df, type)
    model_path = 'model/dt_large_class_model.pkl'  # Adjust the path to your large class model
    model = load_model(model_path)

    prediction, confidence_score = predict_data(model, normalized_data, type)
    
    return jsonify({
        'filename': filename,
        'code_smell': 'large_class' if prediction[0] else 'none',
        'confidence_score': confidence_score[0],
    })


@app.route('/detect_long_method/<filename>')
def detect_long_method(filename):
    type = "long_method"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metrics, halstead_metrics = extract_metrics(file_path)
    row_data = {
        'difficulty': halstead_metrics.total.difficulty,
        'scloc': metrics.sloc,
        'effort': halstead_metrics.total.effort,
        'time': halstead_metrics.total.time,
        'volume': halstead_metrics.total.volume,
        'bugs': halstead_metrics.total.bugs,
        'lloc': metrics.lloc,
        'calculated_length': halstead_metrics.total.calculated_length,
    }

    df = pd.DataFrame([row_data])
    normalized_data = normalize_dataframe(df, type)
    model_path = 'model/xgboost_long_method_model.pkl'  # Adjust the path to your long method model
    model = load_model(model_path)

    prediction, confidence_score = predict_data(model, normalized_data, type)

    return jsonify({
        'filename': filename,
        'code_smell': 'long_method' if prediction[0] else 'none',
        'confidence_score': float(confidence_score[0]),
    })
    
@app.route('/detection_result', methods=['POST'])
def detection_result():
    data = request.json
    # Process the detection result data as needed
    print(data)
    return jsonify({'message': 'Result received successfully!'})


def extract_metrics(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    metrics = analyze(source_code)
    
    # Use the ast module from the Python standard library
    ast_node = ast.parse(source_code)
    
    halstead_metrics = h_visit(ast_node)
    
    return metrics, halstead_metrics    

def normalize_dataframe(df, type):
    if type == 'large_class':
        loaded_scaler = joblib.load('model/large_class_scale.joblib')
    elif type == 'long_method':
        loaded_scaler = joblib.load('model/long_method_scale.joblib')
        
    normalized_df = pd.DataFrame(loaded_scaler.transform(df), columns=df.columns)
    return normalized_df

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = joblib.load(file)
    return model

def predict_data(model, data, type):
    if type == 'large_class':
        predictions = model.predict(data)
        probabilities = model.decision_function(data)
    
    elif type == 'long_method':
        raw_scores = model.predict(data, output_margin=True)  # Output raw decision scores
        probabilities = 1 / (1 + np.exp(-raw_scores))  # Sigmoid function to convert scores to probabilities
        
        predictions = (probabilities >= 0.5).astype(int)  # Convert probabilities to binary predictions
        
    return predictions, probabilities


if __name__ == '__main__':
    app.run(debug=True)
