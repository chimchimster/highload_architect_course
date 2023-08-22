from aiohttp import web
from .controllers import index

account_routes = [
    web.get('/', index),
]