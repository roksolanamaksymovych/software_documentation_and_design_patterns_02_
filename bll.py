import csv, random
from models import Owner, Apartment

class ApartmentService:
    def __init__(self, repository, loader=None):
        self.repo = repository
        self.loader = loader

    def get_all(self):
        return self.repo.get_all(Apartment)

    def create_apartment(self, address, price, is_available, f_name, l_name, email):
        owner = Owner(first_name=f_name, last_name=l_name, email=email)
        apt = Apartment(address=address, price_per_night=price, is_available=is_available, owner=owner)
        self.repo.add(owner)
        self.repo.add(apt)
        self.repo.commit()

    def update_apartment(self, apt_id, address, price, is_available):
        apt = self.repo.get_by_id(Apartment, apt_id)
        if apt:
            apt.address = address
            apt.price_per_night = price
            apt.is_available = is_available
            self.repo.commit()

    def delete_apt(self, apt_id):
        apt = self.repo.get_by_id(Apartment, apt_id)
        if apt:
            self.repo.delete(apt)
            self.repo.commit()

    def clear_database(self):
        for apt in self.repo.get_all(Apartment): self.repo.delete(apt)
        for owner in self.repo.get_all(Owner): self.repo.delete(owner)
        self.repo.commit()

    def import_from_csv(self, path):
        rows = self.loader.load_csv(path)
        for r in rows:
            self.create_apartment(r['owner_first_name'], float(r['price_per_night']), 
                                r['is_available'].lower() == 'true', r['owner_first_name'], 
                                r['owner_last_name'], r['owner_email'])

    def generate_data(self, path, rows, delim):
        fields = ['owner_first_name', 'owner_last_name', 'owner_email', 'apartment_address', 'price_per_night', 'is_available']
        with open(path, mode='w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=fields, delimiter=delim)
            w.writeheader()
            for i in range(rows):
                w.writerow({'owner_first_name': f'Name_{i}', 'owner_last_name': f'Surn_{i}', 'owner_email': f'm_{i}@ukr.net',
                            'apartment_address': f'St.{i}', 'price_per_night': random.randint(500, 5000), 'is_available': True})