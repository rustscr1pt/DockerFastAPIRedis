from controller.alchemy_controller.main import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()