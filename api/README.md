# PYTHON API



## Start server
```shell
export MONGO_URI="<mongo_uri>" && ./server.sh
```


## Make requests
```shell
curl "167.172.151.128:8000/api/v1/gastos_publicos"
curl "167.172.151.128:8000/api/v1/emendas"
curl "167.172.151.128:8000/api/v1/notas_fiscais"
curl "167.172.151.128:8000/api/v1/orcamento?page=2"
```
