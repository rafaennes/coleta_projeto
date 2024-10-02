from flask import Flask, jsonify, send_file
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/despesas-execucao"

# Function to generate URL and download file for a given year and month
def download_file(year_month):
    url = f"{BASE_URL}/{year_month}"
    filename = f"despesas_execucao_{year_month}.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename, "seus arquivos já estão disponíveis"
    else:
        return None, "Portal da Transparência com instabilidades, tente novamente mais tarde"

# Route to download file for the current month
@app.route('/download_last', methods=['GET'])
def download_last():
    current_date = datetime.now()
    year_month = current_date.strftime("%Y%m")
    
    filename, message = download_file(year_month)
    
    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": message}), 500

# Route to download files for the last 'n' months
@app.route('/download_last_n_months/<int:n>', methods=['GET'])
def download_last_n_months(n):
    current_date = datetime.now()
    files = []
    
    for i in range(n):
        target_date = current_date - timedelta(days=i*30)  # Approximation for month intervals
        year_month = target_date.strftime("%Y%m")
        filename, message = download_file(year_month)
        
        if filename:
            files.append(filename)
        else:
            return jsonify({"message": message}), 500
    
    return jsonify({"files": files, "message": "seus arquivos já estão disponíveis"})

# Route to download files from January until the current month (Year-To-Date)
@app.route('/download_ytd', methods=['GET'])
def download_ytd():
    current_date = datetime.now()
    files = []
    
    # Loop from January until the current month
    for month in range(1, current_date.month + 1):
        year_month = f"{current_date.year}{month:02d}"
        filename, message = download_file(year_month)
        
        if filename:
            files.append(filename)
        else:
            return jsonify({"message": message}), 500
    
    return jsonify({"files": files, "message": "seus arquivos já estão disponíveis"})

# Clean up the downloaded files after sending them
@app.after_request
def cleanup(response):
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error deleting file {file}: {e}")
    return response

if __name__ == '__main__':
    app.run(debug=True)
