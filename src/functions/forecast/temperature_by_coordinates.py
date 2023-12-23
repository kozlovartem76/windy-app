
from fastapi import FastAPI
import uvicorn
from src.services.temperature.forecast import predict_temperature
    

app = FastAPI()

@app.get("/getForecast")
async def get_forecast(
    from_ts: int,
    to_ts: int,
    lat: float,
    lon: float,
):

    
    forecast_result = await predict_temperature(
        from_ts=from_ts,
        to_ts=to_ts,
        lat=lat,
        lon=lon
    )
    return forecast_result



