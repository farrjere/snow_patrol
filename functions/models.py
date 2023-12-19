import datetime
class Resort:
    def __init__(self, name, latitude, longitude, snowtel_id):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.snowtel_id = snowtel_id
    
    @staticmethod
    def from_dict(source):
        return Resort(
            source['name'],
            source['latitude'],
            source['longitude'],
            source['snowtel_id'],
        )
    
    def to_dict(self):
        return {
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'snowtel_id': self.snowtel_id,
        }
    
    def __repr__(self) -> str:
        return f"Resort(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"
    
class Report:
    def __init__(self, resort, snow_depth, wind_speed, forecast, report_time=datetime.datetime.now()):
        self.resort = resort
        self.snow_depth = snow_depth
        #self.snow_change = snow_change
        self.wind_speed = wind_speed
        self.forecast = forecast
        self.report_time = report_time
    
    @staticmethod
    def from_dict(source):
        return Report(
            source['resort'],
            source['snow_depth'],
            #source['snow_change'],
            source['wind_speed'],
            source['forecast'],
            source['report_time'],
        )
    
    def to_dict(self):
        return {
            'resort': self.resort,
            'snow_depth': self.snow_depth,
            #'snow_change': self.snow_change,
            'wind_speed': self.wind_speed,
            'forecast': self.forecast.to_dict(),
            'report_time': self.report_time,
        }
    
    def __repr__(self) -> str:
        return f"Report(resort={self.resort}, snow_depth={self.snow_depth}, wind_speed={self.wind_speed}, report_time={self.report_time})"

class ForecastPoint:
    def __init__(self, time, temp, temp_type, precipitation_probability, weather_type, forecast_desc, forecast_icon):
        self.time = time
        self.temperature = temp
        self.temperature_type = temp_type
        self.precipitation_probability = precipitation_probability
        self.weather_type = weather_type
        self.forecast_desc = forecast_desc
        self.forecast_icon = forecast_icon
    
    @staticmethod
    def from_dict(source):
        return ForecastPoint(
            source['time'],
            source['temperature'],
            source['temperature_type'],
            source['percipitation_probability'],
            source['weather_type'],
            source['forecast_desc'],
            source['forecast_icon'],
        )
    
    def to_dict(self):
        return {
            'time': self.time,
            'temperature': self.temperature,
            'temperature_type': self.temperature_type,
            'percipitation_probability': self.precipitation_probability,
            'weather_type': self.weather_type,
            'forecast_desc': self.forecast_desc,
            'forecast_icon': self.forecast_icon,
        }
    
    def __repr__(self) -> str:
        return f"ForecastPoint(time={self.time}, temperature={self.temperature}, temperature_type={self.temperature_type}, percipitation_probability={self.precipitation_probability}, weather_type={self.weather_type}, forecast_desc={self.forecast_desc}, forecast_icon={self.forecast_icon})"
        

class Forecast:
    def __init__(self, longitude, latitude, height):
        self.longitude = longitude
        self.latitude = latitude
        self.height = height
        self._points = []
    
    def add_point(self, point):
        self._points.append(point)
    
    def points(self):
        return self._points
    
    def to_dict(self):
        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'height': self.height,
            'points': [point.to_dict() for point in self._points],
        }