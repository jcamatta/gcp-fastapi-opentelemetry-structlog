# ACTUALIZACION DEL TEMPLATE

## COMPOSICION DE LA CARPETA

Esta dividida en 3 partes:
1. La carpeta src con el codigo y todos los elementos necesarios para ejecutar el modelo ML.
2. La carpeta test para, valga la redundancia, testear el codigo en src.
3. Los archivos por fuera de esta carpeta.

### SRC

Source es el codigo con la API encargada de ejecutar el modelo de ML. Compuesta por:
- main.py: es donde se encuentra la app que ejecuta el servidor para levantar la api.
- Carpeta core: donde se guardan archivos o configuraciones usadas en todo el codigo. Por ejemplo: constantes, logger, errores generales, configuraciones, etc.
- Carpeta models: dentro de models, cada carpeta es un modelo de ML. En el caso mas simple solo hay uno, pero puede haber una api con mas de un modelo a la vez.

En el main.py se agregan middlewares. Los middlewares son funciones que pueden acceder a la request y response de la API, por ejemplo para agregar nuevos headers, o hacer algun tipo de operacion previa o post-response. Por ultimo, en main.py se encuentra la "app". En esta app incluimos los routers. Los routers son mini-apis, que en este caso en particular, seria un router por modelo de machine learning.

#### CORE

- config.py: constantes, variables de entorno, etc.
- logger.py: configura el logger generado por structlog. Structlog es una libreria que permite generar logs de tipo json o estructurados.
- tracer.py: configura el objeto tracer que captura y genera trazas usando opentelemetry.
- utils.py: funciones extras.


### TEST

Esta carpeta esta formada por un archivo test_{archivo_a_testear}.py. 
Se testea la aplicacion con un simple `pytest`

### ARCHIVOS DE LA APP

1. Dockerfile: este docker se usa en produccion/cloud para levantar la cloud run.
2. dev.Dockerfile: este docker se usa en local para testear la aplicacion.
3. dev.requirements.txt: un requirements que se usa en desarrollo para levantar el virtual enviroment, contiene pytest y htmx, entre otros, usados para test.
4. requirements.txt: requirements asociado a Dockerfile para cloud o produccion.
5. entrypoint.sh: es el script que va ejecutar el dockerfile para iniciar la aplicacion. Es una alternativa por script a usar CMD [...] o ENTRYPOINT [...]
6. compose.yaml: archivo compose para levantar la aplicacion en local. Conectado con el run.sh.
7. run.sh: ejecuta el comando `docker compose up` para levantar la aplicacion, pero antes setea algunas variables de entorno necesarias o a usar por el docker compose.
8. .dockerignore: el docker ignore usado por el dockerfile que filtra que archivos se observan en el directorio.
