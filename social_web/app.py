# TODO
# 1) Система аутентификации пользователей (база PostgreSQL)X


import jinja2
import aiohttp_jinja2

from aiohttp import web
from pathlib import Path
from account import account_routes


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            Path.cwd().joinpath(
                "templates",
            )
        ),
        enable_async=True,
    )
    app.add_routes(account_routes)
    web.run_app(app, host='127.0.0.1', port=5000)