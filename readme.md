# Order Fresh - Ejemplo con pyKDSAPI

Este proyecto contiene scripts de ejemplo para interactuar con la API de KDS utilizando la biblioteca `pyKDSAPI`.

## Prerrequisitos

Asegúrate de tener instalado lo siguiente antes de comenzar:

*   **Python 3:** Se recomienda la versión 3.8 o superior. Puedes descargarlo desde [python.org](https://www.python.org/).
*   **pip:** El gestor de paquetes de Python. Usualmente viene incluido con Python. Puedes verificar si lo tienes ejecutando `pip --version` en tu terminal.

## Instalación

1.  **Clona el repositorio (si aplica):** Si obtuviste este código desde un repositorio Git, clónalo:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```
    Si solo tienes los archivos localmente, puedes omitir este paso y asegurarte de estar en el directorio correcto en tu terminal.

2.  **Instala la dependencia `pyKDSAPI`:**
    El comando principal para instalar la biblioteca necesaria es:
    ```bash
    pip install pyKDSAPI
    ```

3.  ***(Opcional)*** **Instala desde `requirements.txt`:** Si en el futuro se añaden más dependencias y se crea un archivo `requirements.txt`, podrías instalarlas todas con:
    ```bash
    pip install -r requirements.txt
    ```
    *(Actualmente, solo `pyKDSAPI` es necesaria)*.

## Configuración

Antes de ejecutar los scripts, necesitas configurar tus credenciales y datos específicos directamente dentro de cada archivo `.py`:

*   Abre el script que deseas ejecutar (por ejemplo, `send_order_complete.py`).
*   Busca las siguientes variables cerca del inicio del archivo y **reemplaza los valores de ejemplo con tus datos reales**:
    *   `token`: Tu token de autenticación de la API.
    *   `location_id`: El ID de tu local/tienda.
    *   `device_id`: El ID del dispositivo desde el que se envía la orden.

**Ejemplo (dentro de `send_order_complete.py`):**

```python
# Datos reales (¡Reemplaza estos valores!)
token = 'TU_TOKEN_AQUI'
location_id = 'TU_LOCATION_ID_AQUI'
device_id = 'TU_DEVICE_ID_AQUI'
```

## Ejecución de los Scripts

Una vez que hayas instalado `pyKDSAPI` y configurado las credenciales en el script deseado, puedes ejecutarlo usando Python desde tu terminal. Asegúrate de estar en el directorio donde se encuentran los archivos `.py`.

**Comando general:**

```bash
python nombre_del_script.py
```

**Ejemplo específico para enviar una orden completa:**

```bash
python send_order_complete.py
```

El script se ejecutará y mostrará la salida en la terminal, indicando si la orden fue enviada y la respuesta recibida del servidor KDS.

# A simple API wrapper for the Fresh Technologies FreshKDS

## This package works great for sending order both minimal and 
## complex to your Fresh KDS screens via the KDS Cloud API


### If you find any issues, have any questions, or have a feature 
### feel free to create an issue 