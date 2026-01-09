from flask import Flask, render_template, request, jsonify
from ml_utils import NLPProcessor, LogAnalyzer
import os

app = Flask(__name__)

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# API for Sentiment Analysis
@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get('text', '')
    result = NLPProcessor.analyze_sentiment(text)
    return jsonify(result)

# API for Text Mining
@app.route('/api/mine-text', methods=['POST'])
def mine_text():
    data = request.json
    text = data.get('text', '')
    result = NLPProcessor.mine_text(text)
    return jsonify(result)

# API for Log Analysis
@app.route('/api/analyze-logs', methods=['POST'])
def analyze_logs():
    data = request.json
    log_text = data.get('log', '')
    # Support analyzing multiple lines if sent as a block
    lines = log_text.split('\n')
    results = []
    
    for line in lines:
        if line.strip():
            analysis = LogAnalyzer.analyze_log(line)
            # Only return interesting logs to avoid clutter, or return all with status
            results.append({
                "log_content": line,
                "analysis": analysis
            })
            
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
