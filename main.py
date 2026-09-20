
from fastapi import FastAPI, Depends
from app.api.v1.endpoints import auth, admin, posts
from app.db.dbsession import async_get_db, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

import logging
from app.core.init_db import init_roles_and_permissions
from app.db.dbsession import async_engine



logging.basicConfig(level=logging.DEBUG)


app = FastAPI(debug = True,)


@app.on_event("startup")
async def startup():
    async with AsyncSession(async_engine) as session:
        await init_roles_and_permissions(session)



app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(posts.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8085, reload=True)


