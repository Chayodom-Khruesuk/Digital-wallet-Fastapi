from sqlmodel import SQLModel, create_engine, Session

connect_args = {}

engine = create_engine(
    "postgresql+pg8000://postgres:123456@localhost/digital_wallet",
    connect_args=connect_args,
)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def init_db():
    SQLModel.metadata.create_all(engine)
