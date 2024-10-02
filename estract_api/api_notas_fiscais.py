import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/notas-fiscais/"

# Helper function to create the YYYYMM format
def get_yyyymm(date):
    return date.strftime('%Y%m')

# Helper function to download a CSV file from the given URL and save it locally
def download_csv(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return {"file": filename, "message": "seus arquivos já estão disponíveis"}
    else:
        return {"message": "Portal da Transparência com instabilidades, tente novamente mais tarde"}, 500

# Route to download the file for the current month (download_last)
@app.route('/download_last', methods=['GET'])
def download_last():
    current_date = datetime.now()
    yyyymm = get_yyyymm(current_date)
    url = f"{BASE_URL}{yyyymm}"
    filename = f"notas_fiscais_{yyyymm}.csv"
    return download_csv(url, filename)

# Route to download files for the last n months (download_last_n_months)
@app.route('/download_last_n_months/<int:n>', methods=['GET'])
def download_last_n_months(n):
    current_date = datetime.now()
    files = []
    
    for i in range(n):
        target_date = current_date - timedelta(days=i*30)
        yyyymm = get_yyyymm(target_date)
        url = f"{BASE_URL}{yyyymm}"
        filename = f"notas_fiscais_{yyyymm}.csv"
        response = download_csv(url, filename)
        
        if isinstance(response, tuple) and response[1] == 500:
            return response  # Return error if any download fails
        
        files.append(filename)

    return jsonify({"files": files, "message": "seus arquivos já estão disponíveis"})

# Route to download files from January to the current month of the current year (download_ytd)
@app.route('/download_ytd', methods=['GET'])
def download_ytd():
    current_date = datetime.now()
    files = []
    
    # Start from January of the current year
    for month in range(1, current_date.month + 1):
        target_date = datetime(current_date.year, month, 1)
        yyyymm = get_yyyymm(target_date)
        url = f"{BASE_URL}{yyyymm}"
        filename = f"notas_fiscais_{yyyymm}.csv"
        response = download_csv(url, filename)
        
        if isinstance(response, tuple) and response[1] == 500:
            return response  # Return error if any download fails
        
        files.append(filename)

    return jsonify({"files": files, "message": "seus arquivos já estão disponíveis"})

if __name__ == '__main__':
    app.run(debug=True)
