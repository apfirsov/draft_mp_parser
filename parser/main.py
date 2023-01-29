import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.handlers import parser_router

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="parser_marketplace")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(
    parser_router,
    prefix="/parser",
    tags=["parser"]
)
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
