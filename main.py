import csv
import json
import uuid
from abc import ABC, abstractmethod

# Бібліотеки для реальної роботи зі сховищами
import redis
from confluent_kafka import Producer

# ==========================================
# 1. ПАТЕРН СТРАТЕГІЯ (Рівень запису)
# ==========================================
class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data: dict):
        pass

class ConsoleStrategy(OutputStrategy):
    def write(self, data: dict):
        print(f"[CONSOLE] Виведено рядок: {data}")

class RedisStrategy(OutputStrategy):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, data: dict):
        # БЕРЕМО 'INCIDENT_KEY' З ТВОГО ДАТАСЕТУ ДЛЯ КЛЮЧА В REDIS
        key = f"record:{data.get('INCIDENT_KEY', uuid.uuid4())}"
        
        self.client.set(key, json.dumps(data))
        print(f"[REDIS] Записано ключ: {key}")

class KafkaStrategy(OutputStrategy):
    def __init__(self, broker: str, topic: str):
        self.producer = Producer({'bootstrap.servers': broker})
        self.topic = topic

    def write(self, data: dict):
        self.producer.produce(self.topic, value=json.dumps(data).encode('utf-8'))
        self.producer.flush()
        print(f"[KAFKA] Відправлено повідомлення в топік '{self.topic}'")

# ==========================================
# 2. РІВЕНЬ ЧИТАННЯ (Повністю відділений)
# ==========================================
class DataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_data(self):
        """Генератор, який вичитує файл по одному рядку"""
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row

# ==========================================
# 3. ТОЧКА ВХОДУ (Збірка та конфігурація)
# ==========================================
def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def get_strategy(config: dict) -> OutputStrategy:
    """Фабричний метод: обирає стратегію на основі конфігураційного файлу"""
    strategy_type = config.get("output_strategy", "console")
    
    if strategy_type == "redis":
        return RedisStrategy(config["redis_host"], config["redis_port"])
    elif strategy_type == "kafka":
        return KafkaStrategy(config["kafka_broker"], config["kafka_topic"])
    else:
        return ConsoleStrategy()

def main():
    # 1. Читаємо конфігурацію (без зміни коду!)
    config = load_config()
    
    # 2. Ініціалізуємо обрану стратегію
    strategy = get_strategy(config)
    
    # 3. Ініціалізуємо об'єкт для читання
    reader = DataReader("dataset.csv")
    
    # 4. Процес: Читаємо і передаємо стратегії
    print(f"--- Запуск з активною стратегією: {config.get('output_strategy').upper()} ---")
    for record in reader.read_data():
        strategy.write(record)
    print("--- Обробку завершено ---")

if __name__ == "__main__":
    main()