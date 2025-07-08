from sqlmodel import Session, SQLModel, create_engine

#db connection settings
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "crud"

#connecting to db
mysql_url = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)
engine = create_engine(mysql_url, echo=True)

#create tables into db from the model
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#dependencie for db operations 
def get_session():
    with Session(engine) as session:
        yield session
        