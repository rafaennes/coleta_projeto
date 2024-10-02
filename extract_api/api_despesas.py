from flask import Flask, jsonify
import requests
import io
from datetime import datetime

app = Flask(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/despesas-execucao/{}"


def download_file(year_month):
    """Downloads the CSV file for the given YYYYMM and saves it."""
    url = BASE_URL.format(year_month)
    print(f"Attempting to download from URL: {url}")  # Debugging statement
    response = requests.get(url)

    if response.status_code == 200:
        file_name = f"despesas_orcamento_{year_month}.csv"

        # Decode response content to a string using ISO-8859-1
        content = response.content.decode('ISO-8859-1')

        # Use StringIO to manage string content
        with io.StringIO(content) as csvfile:
            with open(file_name, 'w', encoding='ISO-8859-1', newline='') as output_file:
                output_file.write(csvfile.getvalue())

        print(f"File saved as: {file_name}")  # Debugging statement
        return file_name
    else:
        print(f"Failed to download file. Status code: {response.status_code}")  # Debugging statement
        return None


@app.route('/download_last', methods=['GET'])
def download_last():
    """Downloads the CSV for the last month."""
    now = datetime.now()
    last_month = now.month - 1 if now.month > 1 else 12
    last_year = now.year if now.month > 1 else now.year - 1
    last_month_year_month = f"{last_year}{last_month:02d}"
    
    file_name = download_file(last_month_year_month)
    if file_name:
        return jsonify({"message": f"File {file_name} downloaded successfully."}), 200
    else:
        return jsonify({"error": "Failed to download file."}), 404


@app.route('/download_last_n_months/<int:n>', methods=['GET'])
def download_last_n_months(n):
    """Downloads CSV files for the last n months."""
    now = datetime.now()
    files_downloaded = []

    for i in range(n):
        month_to_download = now.month - i
        year_to_download = now.year

        if month_to_download <= 0:
            month_to_download += 12
            year_to_download -= 1

        year_month = f"{year_to_download}{month_to_download:02d}"
        file_name = download_file(year_month)
        
        if file_name:
            files_downloaded.append(file_name)

    return jsonify({"files_downloaded": files_downloaded}), 200


@app.route('/download_ytd', methods=['GET'])
def download_ytd():
    """Downloads CSV files from January to the current month of the current year."""
    now = datetime.now()
    files_downloaded = []

    for month in range(1, now.month + 1):
        year_month = f"{now.year}{month:02d}"
        file_name = download_file(year_month)
        
        if file_name:
            files_downloaded.append(file_name)

    return jsonify({"files_downloaded": files_downloaded}), 200


if __name__ == '__main__':
    app.run(debug=True)