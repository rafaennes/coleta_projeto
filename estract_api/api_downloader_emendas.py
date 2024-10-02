import requests
from datetime import datetime, timedelta
import os
from flask import Flask, jsonify

app = Flask(__name__)

class EmendasParlamentaresAPI:
    BASE_URL = "https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares/"

    @staticmethod
    def _get_current_date():
        return datetime.now()

    @staticmethod
    def _format_date(date):
        return date.strftime("%Y%m")

    def _download_file(self, date):
        url = f"{self.BASE_URL}{self._format_date(date)}"
        response = requests.get(url)
        if response.status_code == 200:
            filename = f"emendas_parlamentares_{self._format_date(date)}.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            return f"Baixado: {filename}"
        else:
            return f"Falha ao baixar dados para {self._format_date(date)}"

    def download_last(self):
        current_date = self._get_current_date()
        return self._download_file(current_date)

    def download_last_n_months(self, n):
        current_date = self._get_current_date()
        results = []
        for i in range(n):
            date = current_date - timedelta(days=30*i)
            results.append(self._download_file(date))
        return results

    def download_ytd(self):
        current_date = self._get_current_date()
        start_date = datetime(current_date.year, 1, 1)
        results = []
        while start_date <= current_date:
            results.append(self._download_file(start_date))
            start_date += timedelta(days=30)
        return results

api = EmendasParlamentaresAPI()

@app.route('/download_last', methods=['GET'])
def download_last():
    result = api.download_last()
    return jsonify({"message": result})

@app.route('/download_last_n_months/<int:n>', methods=['GET'])
def download_last_n_months(n):
    results = api.download_last_n_months(n)
    return jsonify({"messages": results})

@app.route('/download_ytd', methods=['GET'])
def download_ytd():
    results = api.download_ytd()
    return jsonify({"messages": results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)