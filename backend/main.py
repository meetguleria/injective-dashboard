import uvicorn
from fastapi import FastAPI
from routers import orderbook_router
from config import settings

app = FastAPI(title="Injective Real-Time Dashboard Backend")

# Mount the routers
app.include_router(orderbook_router.router, prefix="/orderbook", tags=["Orderbook"])

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.reload)