import time
from decouple import config
from fastapi import Request
from src.databases.redis.redis_client import redis_client
from src.exceptions.too_many_requests_exception import TooManyRequestsException
from src.utils.client import get_client_ip

RATE_LIMIT_REQUESTS_PER_RESET_TIME = config("RATE_LIMIT_REQUESTS_PER_RESET_TIME", cast=int)
RATE_LIMIT_RESET_TIME_IN_SECONDS = config("RATE_LIMIT_RESET_TIME_IN_SECONDS", cast=int)
RATE_LIMIT_REQUEST_COUNT_KEY = config("RATE_LIMIT_REQUEST_COUNT_KEY")
RATE_LIMIT_FIRST_REQUEST_TIME_KEY = config("RATE_LIMIT_FIRST_REQUEST_TIME_KEY")

async def rate_limiter_middleware(request: Request, call_next):

    client_ip = get_client_ip(request)

    requests_per_client_key = get_request_per_client_key(client_ip)
    first_request_per_client_key = get_first_request_time_per_client_key(client_ip)
    

    requests_count = redis_client.get(requests_per_client_key)
    first_request_time = redis_client.get(first_request_per_client_key)
    

    if requests_count is None or first_request_time is None:
        requests_count = 0
        setFistRequestTime(client_ip)
    
    requests_count = int(requests_count)

    if requests_count >= RATE_LIMIT_REQUESTS_PER_RESET_TIME:
        raise TooManyRequestsException
    
    redis_client.set(requests_per_client_key, requests_count + 1)

    response = await call_next(request)
    return response

def setFistRequestTime(client_ip):
    first_request_time = time.time()
    redis_client.set(get_first_request_time_per_client_key(client_ip), first_request_time, ex=RATE_LIMIT_RESET_TIME_IN_SECONDS)

def get_request_per_client_key(client_ip):
    return f"{RATE_LIMIT_REQUEST_COUNT_KEY}:{client_ip}"

def get_first_request_time_per_client_key(client_ip):
    return f"{RATE_LIMIT_FIRST_REQUEST_TIME_KEY}:{client_ip}"