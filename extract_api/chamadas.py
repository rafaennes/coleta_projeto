import requests
import asyncio

async def make_request(url):
    try:
        print(f"Chamando API: {url}...")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro ao chamar {url}: {e}")

async def main():
    # Primeira chamada: despesas-execucao
    await make_request('http://127.0.0.1:5000/download_last_n_months/despesas-execucao/3')

    # Aguardar 2 segundos antes de fazer a próxima requisição
    await asyncio.sleep(10)

    # Segunda chamada: notas-fiscais
    await make_request('http://127.0.0.1:5000/download_last_n_months/notas-fiscais/3')

    # Aguardar 2 segundos antes de fazer a próxima requisição
    await asyncio.sleep(10)
    # Terceira chamada: emendas-parlamentares
    await make_request('http://127.0.0.1:5000/download_last_n_months/emendas-parlamentares/3')

if __name__ == "__main__":
    asyncio.run(main())
    # Executa a função principal assíncrona