import requests
from datetime import datetime, timedelta

tipo_cambio_cache = {
    'valor': None,
    'timestamp': None,
}

def obtener_tipo_cambio():
    if tipo_cambio_cache['valor'] and tipo_cambio_cache['timestamp'] > datetime.now() - timedelta(minutes=10):
        return tipo_cambio_cache['valor']
    
    url = 'https://mindicador.cl/api/dolar'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        tipo_cambio = data['serie'][0]['valor']
        
        tipo_cambio_cache['valor'] = tipo_cambio
        tipo_cambio_cache['timestamp'] = datetime.now()
        
        return tipo_cambio
    except (requests.RequestException, ValueError) as e:
        # Manejar errores o proporcionar un valor predeterminado
        return tipo_cambio_cache['valor'] if tipo_cambio_cache['valor'] else 1  # o algún valor predeterminado
