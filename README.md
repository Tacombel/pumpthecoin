tacombel/pumpthecoin:v0.12.6c34-a

Instalacion en un nuevo ordenador con VS Code

Crear el entorno virtual: CTRL-SHIFT-P Python:crear ambiente

Descargar el proyecto: CTRL-SHIFT-P Git_clonar

Instalar modulos: pip install -r requirements.txt

Instalar gunicorn: pip install gunicorn

La db la crea gunicorn, así que hay que lanzarlo antes de nada ./gunicorn_test.sh

Cerramos gunicorn y lanzamos flask run para estar en el entorno debug de falsk

-----------------------------------------------

Donations welcome:

SCP: 795e003fd556513661fe450351985416facb6b77b92730ffa8c2b208a51c741f863990305924

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