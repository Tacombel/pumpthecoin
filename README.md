v 0.11.3

Copy LICENSE, pumpthecoin.py and requirements.txt in you system. Ignore all other files.

Create and launch the .venv. Install dependencies.

Then python pumpthecoin.py x

where x is the target coin price, in dollars.

-----------------------------------------------

Donations welcome:

SCP: 29397f5ac09162c48aeea537c4950d90a6b370899a2c8054a71e82ab4954228bb63e59c56464

Para obtener el query, en el panel de grafana que está la información buscada, ir a Inspect>Panel JSON

Buscar la linea "rawSql"

Los datos que necesitamos son "format", "rawSql" y "refId". El "datasourceId":2 no se de donde sale.

Mas abajo en el JSON sale
 "datasource": {

        "uid": "nJPYpy2Gk",

        "type": "postgres"

      }

Supongo que tiene alguna relacion.
