from flask import Flask, jsonify, send_file
import requests
from datetime import datetime

app = Flask(__name__)

BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa"

def download_file(year):
    url = f"{BASE_URL}/{year}"
    filename = f"orcamento_{year}.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename, "seus arquivos já estão disponíveis"
    else:
        return None, "Portal da Transparência com instabilidades, tente novamente mais tarde"

@app.route('/download_last', methods=['GET'])
def download_orcamento():
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    
    filename, message = download_file(year)
    
    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": message}), 500

if __name__ == '__main__':
    app.run(debug=True)
