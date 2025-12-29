import time
import uvicorn
from pymongo import MongoClient
from fastapi import FastAPI, Query
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from data_extraction import scrape_location_data


def log_to_mongodb(log):
    required_fields = {
        "endpoint": str,
        "request_url": str,
        "status_code": int,
        "request_time": datetime,
        "elapsed": (int, float),
        "params": dict,
        "payload": dict,
        "data": dict,
        "response_path": str
    }

    for field, field_type in required_fields.items():
        if field not in log or not isinstance(log[field], field_type):
            raise ValueError(f"Missing or invalid field: {field}")

    optional_fields = {
        "error_message": (str, type(None)),
        "proxy": (str, type(None)),
        "cost": str
    }

    for field, field_type in optional_fields.items():
        if field in log and not isinstance(log[field], field_type):
            raise ValueError(f"Invalid type for optional field: {field}")

    try:
        client = MongoClient("mongodb://localhost:27017/") #< --- change connection string .....
        db = client["parcel_delivery_api"]
        collection = db["parcel_delivery_api_logs"]
        result = collection.insert_one(log)
        print(f"Log inserted with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting log into MongoDB: {e}")
        return None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

VALID_API_KEYS = ["D74018526N", "D74018526NTT"]

@app.get("/parcel_delivery_list/data")
async def get_data(
    pickup_add: str = Query(..., description="please enter your pickup_add in feild ..."),
    pickup_city: str = Query(..., description="please enter your pickup_city in feild ..."),
    dropoff_add: str = Query(..., description="please enter your dropoff_add in feild ..."),
    dropoff_city: str = Query(..., description="please enter your dropoff_pin in feild ..."),
    apikey: str = Query(..., description="Your API key")
):
    start_time = time.time()
    log_base = {
        "endpoint": "http://51.222.244.92:8723/parcel_delivery_list/data",
        "request_url": f"/parcel_delivery_list/data?&apikey={apikey}&pickup_add={pickup_add}&dropoff_add={dropoff_add}",
        "request_time": datetime.now(timezone.utc),
        "elapsed": 0,
        "params": {"key": apikey, "pickup_add" : pickup_add, "dropoff_add" : dropoff_add},
        "payload": {},
        "data": {},
        "response_path": "",
        "error_message": None,
    }
    # Validate API key
    if apikey not in VALID_API_KEYS:
        log_base["status_code"] = 401
        log_base["elapsed"] = time.time() - start_time
        log_base["error_message"] = "Invalid API Key"
        log_to_mongodb(log_base)
        return JSONResponse(status_code=401, content={"status": 401, "message": "Invalid API Key"})

    # Validate platform
    try:
        result = scrape_location_data(pickup_add, pickup_city, dropoff_add, dropoff_city)
        if result == "Something missing.." or result == "No Matches Available" or result == []:
            log_base["status_code"] = 400 if result == "Something missing.." else 404
            log_base["elapsed"] = time.time() - start_time
            log_base["error_message"] = result if result != [] else "No Matches Available"
            log_to_mongodb(log_base)
            return JSONResponse(status_code=log_base["status_code"], content={"status": log_base["status_code"], "pickup_add" : pickup_add, "dropoff_add" : dropoff_add, 'time_taken':time.time() - start_time, "data": log_base["error_message"]})
        log_base["status_code"] = 200
        log_base["elapsed"] = time.time() - start_time
        log_to_mongodb(log_base)
        return JSONResponse(status_code=200, content={"status": 200, "pickup_add" : pickup_add, "dropoff_add" : dropoff_add, 'time_taken':time.time() - start_time, "data": result})
    except Exception as e:
        log_base["status_code"] = 500
        log_base["error_message"] = str(e)
        log_base["elapsed"] = time.time() - start_time
        log_to_mongodb(log_base)
        return JSONResponse(status_code=500, content={"status": 500, "message": f"Server Error: {str(e)}"})

@app.get("/")
async def root():
    return JSONResponse(content={"status": 200, "message": "API is running!"})

if __name__ == "__main__":
    uvicorn.run("lambda:app", host="127.0.0.1", port=8723, reload=True, workers=8)
    # uvicorn.run("lambda:app", host="51.222.244.92", port=8723, reload=True, workers=8)