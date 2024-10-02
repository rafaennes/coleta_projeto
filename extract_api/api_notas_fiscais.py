import os
import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta
from zipfile import ZipFile
from io import BytesIO

app = Flask(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/notas-fiscais/"


def download_file_from_url(url, save_path):
    """Downloads a zip file from the provided URL and saves it to the given path."""
    response = requests.get(url)
    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(save_path)
        return True, "Files downloaded successfully."
    else:
        return False, "Error downloading file."


def get_year_month_str(months_ago=0):
    """Returns the date in YYYYMM format for a given number of months ago."""
    date = datetime.now() - timedelta(days=months_ago * 30)
    return date.strftime("%Y%m")


@app.route('/api/notas/download_last', methods=['GET'])
def download_last():
    """Downloads the file for the last available month (current system date)."""
    current_ym = get_year_month_str()
    url = f"{BASE_URL}{current_ym}"
    
    # Create the data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download the file
    success, message = download_file_from_url(url, "data")
    if success:
        return jsonify({"message": "seus arquivos já estão disponíveis"}), 200
    else:
        return jsonify({"message": "portal da transparencia com instabilidades, tente novamente mais tarde"}), 500


@app.route('/api/notas/download_last_n_months/<int:n>', methods=['GET'])
def download_last_n_months(n):
    """Downloads the files for the last 'n' months."""
    if n <= 0:
        return jsonify({"message": "Número de meses inválido. Deve ser maior que zero."}), 400
    
    if not os.path.exists('data'):
        os.makedirs('data')

    messages = []
    for i in range(n):
        ym = get_year_month_str(i)
        url = f"{BASE_URL}{ym}"
        success, message = download_file_from_url(url, "data")
        if success:
            messages.append(f"Arquivo de {ym} baixado com sucesso.")
        else:
            messages.append(f"Erro ao baixar o arquivo de {ym}.")

    return jsonify({"messages": messages}), 200


@app.route('/api/notas/download_ytd', methods=['GET'])
def download_ytd():
    """Downloads the files from January to the current month of the current year."""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    if not os.path.exists('data'):
        os.makedirs('data')

    messages = []
    for month in range(1, current_month + 1):
        ym = f"{current_year}{str(month).zfill(2)}"  # Format as YYYYMM
        url = f"{BASE_URL}{ym}"
        success, message = download_file_from_url(url, "data")
        if success:
            messages.append(f"Arquivo de {ym} baixado com sucesso.")
        else:
            messages.append(f"Erro ao baixar o arquivo de {ym}.")

    return jsonify({"messages": messages}), 200


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
