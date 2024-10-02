# **Documentação da API de Download de Dados do Portal da Transparência - Emendas Parlamentares**

## **Descrição**
Esta API foi criada para baixar arquivos CSV do Portal da Transparência utilizando URLs que seguem o formato `https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares/YYYYMM`. A API possui três endpoints principais que permitem baixar o arquivo mais recente, arquivos de meses anteriores e os arquivos do ano corrente até o mês atual.

---

## Base URL

O URL base da API é fornecido pelo ngrok e será exibido no console quando você iniciar o servidor. Ele terá o formato:
> https://[código-aleatório].ngrok.io  

## Endpoints

### 1. Download do Último Mês

Baixa os dados de emendas parlamentares do mês atual.

- **URL:** `/download_last`
- **Método:** GET
- **Resposta de Sucesso:**
  - **Código:** 200
  - **Conteúdo:** `{ "message": "Baixado: emendas_parlamentares_YYYYMM.csv" }`

### 2. Download dos Últimos N Meses

Baixa os dados de emendas parlamentares dos últimos N meses.

- **URL:** `/download_last_n_months/<n>`
- **Método:** GET
- **Parâmetros do URL:**
  - `n`: Número de meses para baixar
- **Resposta de Sucesso:**
  - **Código:** 200
  - **Conteúdo:** `{ "messages": ["Baixado: emendas_parlamentares_YYYYMM.csv", ...] }`

### 3. Download do Ano Até a Data Atual (YTD)

Baixa os dados de emendas parlamentares desde janeiro do ano corrente até o mês atual.

- **URL:** `/download_ytd`
- **Método:** GET
- **Resposta de Sucesso:**
  - **Código:** 200
  - **Conteúdo:** `{ "messages": ["Baixado: emendas_parlamentares_YYYYMM.csv", ...] }`

## Uso

Para usar a API, faça requisições GET para os endpoints acima usando o URL base fornecido pelo ngrok. Os arquivos CSV serão salvos no diretório onde o servidor está sendo executado.

## Notas

- Esta API assume que os dados estão sempre disponíveis para todos os meses no Portal da Transparência.
- Os arquivos são baixados e salvos no servidor onde a API está rodando.
- Em caso de falha no download, uma mensagem de erro será retornada.

## Requisitos

- Python 3.6+
- Flask
- Requests
- pyngrok

## Configuração

1. Instale as dependências: