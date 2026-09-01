from fastapi import FastAPI

from BackEnd.routes.weather import router as weather_router


app = FastAPI(
    title="Smart Weather Dashboard API",
    description="Backend API for the Smart Weather Dashboard",
    version="1.0.0"
)


app.include_router(weather_router)


@app.get("/")
def root():

    return {
        "message": "Smart Weather Dashboard API is running!"
    }
