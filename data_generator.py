import csv
import random

def generate_csv(filename="data.csv", num_rows=1050):
    # 1. СПОЧАТКУ створюємо список назв колонок (fieldnames)
    fieldnames = [
        'owner_first_name', 
        'owner_last_name', 
        'owner_email', 
        'apartment_address', 
        'price_per_night', 
        'is_available'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        # 2. Тепер передаємо цей список у DictWriter
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        
        writer.writeheader()  # Записуємо заголовок
        
        for i in range(num_rows):
            writer.writerow({
                'owner_first_name': f'Name_{i}',
                'owner_last_name': f'Surname_{i}',
                'owner_email': f'owner_{i}@example.com',
                'apartment_address': f'Street {i}, Apt {random.randint(1, 100)}',
                'price_per_night': round(random.uniform(500, 5000), 2),
                'is_available': random.choice([True, False])
            })
    
    print(f"✅ Файл {filename} успішно створено з {num_rows} рядками.")

if __name__ == "__main__":
    generate_csv()