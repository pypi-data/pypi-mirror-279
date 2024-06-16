import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiosql
import aiosqlite
from dotenv import load_dotenv
from litestar import Controller
from litestar import get
from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.response import Template
from litestar_vite import ViteConfig
from litestar_vite import VitePlugin

load_dotenv()


class WebController(Controller):
    # opt = {"exclude_from_auth": True}
    include_in_schema = False

    @get("/favicon.ico", media_type="image/svg+xml")
    async def favicon(self) -> str:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<text y=".9em" font-size="90">🚀</text>'
            "</svg>"
        )

    @get("/")
    async def index(self) -> Template:
        return Template(template_name="index.html.j2", context={})


debug = os.getenv("DEBUG", False) in ("True", "true", "1")
vite = VitePlugin(
    config=ViteConfig(
        template_dir="templates/",
        use_server_lifespan=True,
        dev_mode=debug,
        resource_dir="../resources",
    )
)
cors_config = CORSConfig(allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","))
csrf_config = CSRFConfig(secret=os.getenv("SECRET_KEY"))
compression_config = CompressionConfig(backend="gzip", gzip_compress_level=9)


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    conn = getattr(app.state, "conn", None)
    if conn is None:
        app.state.conn = await aiosqlite.connect("mygists.sqlite3")
        # https://litestream.io/tips/
        await app.state.conn.execute("PRAGMA journal_mode = WAL")
        await app.state.conn.execute("PRAGMA busy_timeout = 5000")
        await app.state.conn.execute("PRAGMA synchronous = NORMAL")  # seems to have no effect I'm not sure why
        app.state.queries = aiosql.from_path("gists.sql", "aiosqlite")
        await app.state.queries.create_schema(app.state.conn)
    try:
        yield
    finally:
        del app.state.queries
        await app.state.conn.close()


app = Litestar(
    route_handlers=[WebController],
    plugins=[vite],
    pdb_on_exception=True,
    debug=debug,
    cors_config=cors_config,
    csrf_config=csrf_config,
    compression_config=compression_config,
    lifespan=[db_connection],
)
