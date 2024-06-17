from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse


async def index():
    return HTMLResponse('templates/index.html')


router = APIRouter()
router.add_api_route("/", endpoint=index, name="index")
