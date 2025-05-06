from db.database import Base, engine

# Drop and recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
