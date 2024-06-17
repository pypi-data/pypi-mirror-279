from fastapi.routing import APIRouter


async def index():
    return {"message": "Hello World"}


router = APIRouter()
router.add_api_route("/", endpoint=index, name="index")
