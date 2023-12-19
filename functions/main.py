# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
import firebase_functions
from firebase_functions import scheduler_fn
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
from models import Resort, Report, ForecastPoint, Forecast
import requests
import datetime 
firebase_functions.options.set_global_options(max_instances=10)
import logging

logger = logging.getLogger('cloudfunctions.googleapis.com%2Fcloud-functions')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = initialize_app()
NOAA_BASE_URL = "https://forecast.weather.gov/MapClick.php"
SNOWTEL_BASE_URL="https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data"

@scheduler_fn.on_schedule(schedule="every 1 hours")
def obtain_snow_data(event: scheduler_fn.ScheduledEvent) -> None:
    """Obtain snow data from snotel and noaa and store in firestore"""
    firestore_client = firestore.client()
    resorts = firestore_client.collection("resorts").stream()
    for resort_doc in resorts:
        resort = Resort.from_dict(resort_doc.to_dict())
        obtain_resort_data(resort, firestore_client)

def obtain_resort_data(resort: Resort, firestore_client: google.cloud.firestore.Client) -> None:
    """Obtain snow data for a single resort and store in firestore"""
    forecast_data = get_forecast_data(resort)
    snow_depth, wind_speed = get_snow_data(resort)
    report = Report(resort.name, snow_depth, wind_speed, forecast_data, datetime.datetime.now())
    firestore_client.collection("reports").add(report.to_dict())
     
def get_forecast_data(resort: Resort) -> Forecast:
    """Obtain forecast data for a single resort"""
    response = requests.get(NOAA_BASE_URL, params={"lat": resort.latitude, "lon": resort.longitude, "FcstType": "json"})
    if response.status_code != 200:
        raise Exception("Error obtaining forecast data")
    forecast_json = response.json()
    forecast = Forecast(resort.longitude, resort.latitude, 0)
    forecast.points = []
    for idx, time in enumerate(forecast_json["time"]["startPeriodName"]):
        forecast.add_point(ForecastPoint(
            time,
            forecast_json["data"]["temperature"][idx],
            forecast_json["time"]["tempLabel"][idx],
            forecast_json["data"]["pop"][idx],
            forecast_json["data"]["weather"][idx],
            forecast_json["data"]["text"][idx],
            forecast_json["data"]["iconLink"][idx],
        ))
    return forecast

def get_snow_data(resort: Resort) -> Report:
    """Obtain snow data for a single resort"""
    now = datetime.datetime.now() - datetime.timedelta(hours=6)#cause this is deployed with utc
    begin_date = (now - datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
    end_date = now.strftime("%Y-%m-%d %H:%M")
    response = requests.get(SNOWTEL_BASE_URL, params={"stationTriplets": resort.snowtel_id,"elements": "SNWD,WSPDV", "beginDate": begin_date,"endDate": end_date, "duration": "HOURLY","periodRef": "END","returnFlags": "false","returnOriginalValues": "false","returnSuspectData": "false",})
    logger.info(response.request.url)
    if response.status_code != 200:
        raise Exception("Error obtaining snow data")
    snow_json = response.json()
    snow_depth, wind_speed = None, None
    for snow_point in snow_json[0]['data']:
        if snow_point['stationElement']['elementCode'] == 'SNWD':
            snow_depth = snow_point['values'][-1]['value']
        elif snow_point['stationElement']['elementCode'] == 'WSPDV':
            wind_speed = snow_point['values'][-1]['value']
    return snow_depth, wind_speed

