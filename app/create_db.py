from database import engine
from models import Base  # Certifique-se de importar a Base e não SQLModel

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    

    
if __name__ == "__main__":
    create_db_and_tables()