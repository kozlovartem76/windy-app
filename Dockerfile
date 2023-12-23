FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11



RUN pip3 install --upgrade pip

COPY data ./data
COPY src ./src

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.functions.forecast.temperature_by_coordinates:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

