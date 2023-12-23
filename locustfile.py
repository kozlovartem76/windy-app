
import random
from locust import HttpUser, between, task

class AppUser(HttpUser):
    wait_time = between(2, 5)
    
    from_ts_values = [1688497200]
    to_ts_values = [1688504400, 1688500800]
    lat_values = [70.5000, 69.0000, 66.0000, 65.0000, 43.0000]
    lon_values = [62.5000, 43.5000, 47.5000]

    @task
    def forecast_world(self):
        from_ts = random.choice(self.from_ts_values)
        to_ts = random.choice(self.to_ts_values)
        lat = random.choice(self.lat_values)
        lon = random.choice(self.lon_values)

        self.client.get(f"/getForecast?from_ts={from_ts}&to_ts={to_ts}&lat={lat}&lon={lon}")

