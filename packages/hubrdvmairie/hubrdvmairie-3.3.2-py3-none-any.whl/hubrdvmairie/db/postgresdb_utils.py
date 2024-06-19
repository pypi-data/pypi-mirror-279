from .postgresdb import session


def create_tables():
    # check_database()
    # Base.metadata.drop_all(bind=engine)
    # print("created tables...")
    # Base.metadata.create_all(bind=engine)
    # print(Base.metadata.tables.keys())
    pass


def get_database():
    db = session()
    try:
        yield db
    finally:
        db.close()
