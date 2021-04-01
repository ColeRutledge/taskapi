import os
import uvicorn
from logging.config import dictConfig

from sqlalchemy.orm import Session

from app import db, models, config
from migrations.seed import seed_db


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    dictConfig(config.LOGGING_CONFIG)

    engine = db.create_database_engine()
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
    session = Session(autocommit=False, autoflush=False, bind=engine)
    seed_db(session)
    session.close()

    uvicorn.run(
        'app.main:app',
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=['app'],
        use_colors=True)
