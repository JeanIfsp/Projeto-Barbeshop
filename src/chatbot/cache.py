from django.core.cache import cache
import json

class RedisManager:
    
    def __init__(self, timeout=60*15):
        """Inicializa com um tempo de expiração padrão para os valores em cache."""
        self.timeout = timeout

    def set_key(self, key, data):
        """Escreve ou atualiza uma chave no Redis."""
        json_data = json.dumps(data)  # Serializa o dicionário para JSON
        cache.set(key, json_data)


    def get_key(self, key):
        """Recupera o valor de uma chave do Redis."""
        json_data = cache.get(key)
        if json_data is not None:
            data = json.loads(json_data.encode('utf-8'))  # Deserializa o JSON para um dicionário
            return data
        return None

    def delete_key(self, key):
        """Deleta uma chave do Redis."""
        result = cache.delete(key)
        if result == 1:
            return True
        return False
