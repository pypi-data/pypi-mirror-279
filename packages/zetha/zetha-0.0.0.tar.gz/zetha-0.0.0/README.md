# Zetha
<img src="images/zetha_icon.webp" alt="zetha_icon" width="400">

### O que é?
Zetha é um pacote Python voltado a auxiliar desenvolvedores em manutenções de dados dos sistemas Betha.
Este pacote usa o ORM do SQLAlchemy para permitir que dados sejam persistidos e manipulados de forma
simples e intuitiva.


### Requerimentos
Zetha foi programado com um database PostgreSQL em mente. Então acesso de administrado a um servidor PostgreSQL
é necessário para seu uso.


### Como usar?
Primeiro instale o pacote usando pip.
```sh
pip install zetha
```

Então você pode começar a utiliza-lo em scripts Python.

Exemplo de uso para inserir dados em database:
```python
from request import get
from zetha import Tokens, Connect, folha as f

tokens = Tokens() # Usado para coletar tokens de API de variaveis de ambiente, mais detalhes em zetha.cloud_api
conn = Connect('MeuDatabase') # Efetua conexão com database 'MeuDatabase' em servidor, mais detalhes em zetha.connect
headers = {"Authorization": f"Bearer {tokens.ENTIDADE}"}

conn.persist_tables() # Cria tabelas em servidor

url_cargos = f.Cargo.url_api() # Obtem url de endpoint
schema_cargo = f.Cargo.__schema__() # Obtem schema para conversão de objeto para json e vice-versa

response = get(url_cargos, headers=headers)
response_json = response.json()

with conn.session as session: # Abre conexão com database
    # Abaixo Json é convertido em lista de objetos e inserido em database
    cargo_objs: list[f.Cargo] = schema_cargo.load(response_json['content'], many=True)
    session.add_all(cargo_objs)
    session.commit() # Salva insert / alteracões em database
```

Exemplo de uso para manipular dados em database:
```python
from sqlalchemy import select
from zetha import Connect, folha as f

conn = Connect('MeuDatabase')

with conn.session as session:
    # Query de cargos de origem
    query = select(f.Cargo).where(f.Cargo.origem_id == None)

    for cargo in session.scalars(query): # Itera por resultados de query
        codigo_correto = cargo.codigo_e_social # Obtem dado de cargo de origem

        for historico in cargo.historicos: # Itera por historicos de cargo
            historico.codigo_e_social = codigo_correto # Altera valor de historico

    session.commit()
```

Exemplo de uso para subir dados para sistema:
```python
from requests import post, get
from sqlalchemy import select
from zetha import Tokens, Connect, folha as f, migrator as m

tokens = Tokens()
conn = Connect('MeuDatabase')
headers = {"Authorization": f"Bearer {tokens.ENTIDADE}"}

url_cargos = f.Cargo.url_api().replace('cargo', 'historico-cargo')
# Schema abaixo tras apenas dados de id cloud e codigo esocial para json.
schema_cargo = f.Cargo.__schema__(only=('cloud_id', 'codigo_e_social'))

url_lotes = 'https://pessoal.betha.cloud/service-layer/v1/api/lotes/lotes/{id}'

with conn.session as session:
    # Query de historicos de cargos
    query = select(f.Cargo).where(f.Cargo.origem_id != None)
    historicos = session.scalars(query) # Obtem lista de historicos

    for historico in historicos:
        # Cria objeto de identificador para historicos
        m.Identifier.identify(historico)

    identifiers = [historico.identifier for historico in historicos] # Coleta identificadores
    lotes = m.Lote.make_lotes(identifiers) # Usa identificadores para criar novos lotes
    session.add_all(lotes)
    session.commit()

    for lote in lotes:
        lote_json = lote.json(schema_cargo) # Usa schema para converter lote em json

        response = post(url_cargo, headers=headers) # Envia lotes ao cloud
        response_json = response.json() # Coleta id de lote

        lote_json.api_id = response_json['id'] # Adiciona id cloud de lote ao objeto
        session.commit()

    # Itera por lotes apos envio ao cloud
    for lote in lotes:
        # Obtem lote e salva dados de resposta ao lote
        response = lote.get_lote(url_lotes, headers=headers)
        lote.read_response(response)
        lote.update() # Atualiza status de lote baseado em resposta de servidor
        session.commit()
```
