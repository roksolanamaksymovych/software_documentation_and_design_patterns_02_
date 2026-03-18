import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename="data.csv", rows=1050):
    headers = [
        "owner_fn", "owner_ln", "owner_email",
        "apt_addr", "apt_price", "apt_desc", "apt_avail",
        "photo_url", "photo_caption",
        "checkin", "checkout", "b_status", "b_cost",
        "rev_comment", "rev_rating", "rev_date"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in range(rows):
            writer.writerow([
                f"Owner_{i%50}", f"Surname_{i%50}", f"user{i%50}@mail.com",
                f"Street {i}, Apt {random.randint(1,100)}", round(random.uniform(50, 500), 2),
                "Comfortable place", random.choice([True, False]),
                f"http://img.com/{i}.jpg", "Interior view",
                (datetime.now() + timedelta(days=i)).date(), (datetime.now() + timedelta(days=i+2)).date(),
                "Confirmed", random.uniform(100, 1000),
                "Great experience!", random.randint(1, 5), datetime.now().date()
            ])
    print(f"✅ Файл {filename} створено ({rows} рядків).")

if __name__ == "__main__":
    generate_csv()