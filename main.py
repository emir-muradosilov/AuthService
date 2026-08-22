
from fastapi import FastAPI, Depends
from app.api.v1.endpoints import auth, admin
from app.db.dbsession import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

import logging


logging.basicConfig(level=logging.DEBUG)

app = FastAPI(debug = True,)


app.include_router(auth.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8085, reload=True)

