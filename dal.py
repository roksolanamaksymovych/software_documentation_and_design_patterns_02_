import csv
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class IRepository(ABC):
    @abstractmethod
    def add(self, entity): pass
    @abstractmethod
    def commit(self): pass
    @abstractmethod
    def delete(self, entity): pass

class CsvLoader:
    def load_csv(self, path: str):
        with open(path, mode='r', encoding='utf-8-sig', newline='') as f:
            sample = f.read(4096)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=";,")
                delim = dialect.delimiter
            except:
                delim = ";"
            return list(csv.DictReader(f, delimiter=delim))

class SqlAlchemyRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session
    def add(self, entity): self.session.add(entity)
    def commit(self): self.session.commit()
    def delete(self, entity): self.session.delete(entity)
    def get_all(self, model): return self.session.query(model).all()
    def get_by_id(self, model, id): return self.session.query(model).filter(model.id == id).first()