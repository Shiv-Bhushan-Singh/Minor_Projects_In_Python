from fastapi import APIRouter, HTTPException

from BackEnd.services.weather_services import (
    get_weather,
    get_forecast
)


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get("/")
def weather(city: str):

    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty."
        )

    try:

        weather_data = get_weather(city)

        return weather_data

    except ValueError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except PermissionError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

    except LookupError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except ConnectionError as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=429,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )
        
        
        


@router.get("/forecast")
def forecast(city: str):

    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty."
        )

    try:

        forecast_data = get_forecast(city)

        return forecast_data

    except ValueError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except PermissionError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

    except LookupError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except ConnectionError as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=429,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )