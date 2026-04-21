from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dal import SqlAlchemyRepository, CsvLoader
from bll import SyncService

def main():
    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Впровадження залежностей
    repo = SqlAlchemyRepository(session)
    loader = CsvLoader()
    service = SyncService(repo, loader)

    print("🚀 Починаємо імпорт...")
    service.process_data("data.csv")
    print("✅ Готово!")

if __name__ == "__main__":
    main()