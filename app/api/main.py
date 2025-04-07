from fastapi import FastAPI

from app.api.services.router import router as router_tron

app = FastAPI()


app.include_router(router_tron)