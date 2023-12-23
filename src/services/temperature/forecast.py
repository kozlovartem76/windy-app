import numpy as np
from pydantic import BaseModel
import os
from typing import List
import asyncio
import aiofiles
import struct
from src.services.common import polynomial_interpolation, round_to_nearest_and_get_index
from src.services.validation import validate_result
from async_lru import alru_cache

class Header(BaseModel):
    y1: int
    y2: int
    x1: int
    x2: int
    step_by_y: int
    step_by_x: int
    multiply: int
    
    

def validate_data(from_ts, to_ts, lat, lon):
    if from_ts > to_ts:
        raise Exception("from_ts bigger then to_ts")
    
    if lat > 180 or lon > 180:
        raise Exception("lat or lon cant be more than 180")
    
    
async def predict_temperature(
    from_ts: int,
    to_ts: int,
    lat: float,
    lon: float,
) -> dict:
    
    validate_data(from_ts, to_ts, lat, lon)
    
    path = 'data'
    list_of_files = choose_correct_files(path, from_ts, to_ts)
    
    tasks = [process_file(os.path.join(path, file), lat, lon) for file in list_of_files]
    results = await asyncio.gather(*tasks)
    
    res = {} 
    for result in results:
        res.update(result)
        
    validate_result(res)
    
    return res

def extract_header(header_data):
    header = struct.unpack(f'<7l1f', header_data)
    return serialize_header(header)
    
    

@alru_cache(maxsize=128)
async def process_file(file_path: str, lat: float, lon: float) -> dict:
    async with aiofiles.open(file_path, 'rb') as file:      
        res = {}
        
        header = extract_header(await file.read(8*4))
        
        lats, lons = calculate_lats_and_lons(header)
        lon_int = int(header.multiply*lon)
        lat_int = int(header.multiply*lat)
        
    
        chunk_size = len(lons)*4
        _, chunk_number = round_to_nearest_and_get_index(lat_int, header.step_by_y, lats)
        
        chunk_number_counter = 0
        
        while True:
            data = await file.read(chunk_size)
            if not data:
                break
            
            if chunk_number_counter == chunk_number:
                values = struct.unpack(f'<{chunk_size//4}f', data)
                interpolated_temperature = polynomial_interpolation(lon_int, lons, values, degree=2)

                res[int(os.path.basename(file.name[:-5]))] = {"temp": interpolated_temperature}
            chunk_number_counter +=1
            
    return res


def choose_correct_files(path: str, from_ts: int, to_ts: int) -> List[str]:
    list_of_files = []
    for file in os.listdir(path):
        if int(file[:-5]) >= from_ts and int(file[:-5]) <= to_ts:
            list_of_files.append(file)
    return list_of_files


def serialize_header(data: tuple) -> Header:
    return Header(
        **{          
            "y1": data[0],
            "y2": data[1],
            "x1": data[2],
            "x2": data[3],
            "step_by_y": data[4],
            "step_by_x": data[5],
            "multiply": data[6],
        }
    )
    

def calculate_lats_and_lons(header: Header):
    latitudes = np.arange(header.y1, header.y2 + header.step_by_y,  header.step_by_y)
    longitudes =  np.arange(header.x1, header.x2 + header.step_by_x, header.step_by_x)
    return latitudes, longitudes
    
    
