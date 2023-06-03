tacombel/pumpthecoin:v0.12.6c18
experimental version for bagbuilder contest

-----------------------------------------------

Donations welcome:

SCP: 29397f5ac09162c48aeea537c4950d90a6b370899a2c8054a71e82ab4954228bb63e59c56464

-----------------------------------------------

Para obtener el query, en el panel de grafana que está la información buscada, ir a Inspect>Panel JSON

Buscar la linea "rawSql"

Los datos que necesitamos son "format", "rawSql" y "refId". El "datasourceId":2 no se de donde sale.

Mas abajo en el JSON sale
 "datasource": {

        "uid": "nJPYpy2Gk",

        "type": "postgres"

      }

Supongo que tiene alguna relacion.

-----------------------------------------------

Estructura

Uso .env para poner todas las environment

Para que los módulos cargen las variables es necesario añadir load_dotenv()

Para que las cargue cuando lanzo flask run lanzo la funcion en __init__.py

Para probar con gunicorn está el gunicorn_test.sh

La configuracion por defecto de gunicorn esta en gunicorn.conf.py junto con sus funciones. Aqui se ponen las funciones que no quiero que se ejecuten en cada worker.

gunicorn no lee el dotenv, así que si se quiere cambiar el nivel de logging hacer export LOGINLEVEL=DEBUG

Usar el directorio contest para guardar ficheros. El server hace copia de seguridad de todo lo que se ponga ahí

Al lanzar el contenedor añadir como environment todas las de .env, excepto las tres de FLASK, La primera se declara al build el contenedor.