
def fake_url(
    handler: str = "getForecast",
    from_ts: int = 1688497200,
    to_ts: int = 1688504400,
    lat: float = 70.5,
    lon: float = 62.5000,
) -> str:
    return build_s3_url(handler, from_ts, to_ts, lat, lon)


def build_s3_url(
    handler: str,
    from_ts: int,
    to_ts: int,
    lat: float,
    lon: float
) -> str:
    return f"https://127.0.0.1:8000/{handler}?from_ts={from_ts}&to_ts={to_ts}&lat={lat}&lon={lon}"

