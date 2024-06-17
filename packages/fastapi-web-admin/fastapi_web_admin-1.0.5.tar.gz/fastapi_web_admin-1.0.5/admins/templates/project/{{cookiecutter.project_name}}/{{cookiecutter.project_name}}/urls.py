from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse


async def index():
    html_str = open("templates/index.html", 'r').read()
    return HTMLResponse(html_str)


router = APIRouter()
router.add_api_route("/", endpoint=index, name="index")
