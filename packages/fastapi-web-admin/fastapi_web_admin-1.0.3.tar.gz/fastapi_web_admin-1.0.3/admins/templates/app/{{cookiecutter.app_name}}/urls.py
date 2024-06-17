from fastapi.routing import APIRouter


router = APIRouter("/{{cookiecutter.app_name}}", tags=["{{cookiecutter.app_name}} 模块"])

# router.add_api_route()