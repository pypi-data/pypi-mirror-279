import requests
from requests.auth import HTTPBasicAuth
import random

def getBoo(tags= str):
    # Definir las credenciales
    username = 'shinjielpajaslocas'  # Tu de usuario de Danbooru
    api_key = 'ULxv3hnJ3iMPoc15MmxDnv19'  # Tu API key obtenida de tu perfil

    # Definir la URL base de la API
    base_url = 'https://danbooru.donmai.us'

    # Definir los parámetros de la consulta
    params = {
        'tags': tags  # Etiquetas para buscar
    }

    try:
        # Hacer la solicitud GET a la API de Danbooru con autenticación
        response = requests.get(f'{base_url}/posts.json', params=params, auth=HTTPBasicAuth(username, api_key))

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            if data:
                return random.choice(data)['file_url']  # Obtener la URL de una imagen aleatoria
            else:
                raise Exception("No se encontraron imágenes con las etiquetas proporcionadas.")
        elif response.status_code == 422:
            raise Exception("Error 422: Los parámetros de la solicitud no son válidos.")
        else:
            raise Exception(f'Error al obtener la respuesta. Código de estado: {response.status_code}')

    except requests.exceptions.RequestException as e:
        raise Exception(f'Error de solicitud HTTP: {e}')