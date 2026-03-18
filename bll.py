from datetime import datetime
from models import Owner, Apartment, Photo, Booking, Review
from dal import IRepository, IFileLoader

class SyncService:
    def __init__(self, repo: IRepository, loader: IFileLoader):
        self.repo = repo
        self.loader = loader

    def process_data(self, file_path):
        rows = self.loader.load_csv(file_path)
        owners_map = {}

        for r in rows:
            email = r['owner_email']
            if email not in owners_map:
                o = Owner(firstName=r['owner_fn'], lastName=r['owner_ln'], email=email)
                owners_map[email] = o
                self.repo.add(o)
            
            apt = Apartment(
                address=r['apt_addr'], pricePerNight=float(r['apt_price']),
                description=r['apt_desc'], isAvailable=r['apt_avail'] == 'True',
                owner=owners_map[email]
            )
            self.repo.add(apt)
            self.repo.add(Photo(imageURL=r['photo_url'], caption=r['photo_caption'], apartment=apt))
            # ... аналогічно для Booking та Review
            
        self.repo.commit()