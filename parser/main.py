import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.handlers import parser_router
import utilites
import sys

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

def main():
    func_name = sys.argv[1:]
    
    if func_name == "start_parsing":
        print("Parsing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        utilites.parser.main()
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
    


# python main.py start_parsing
# def start_parsing():
#     """Triger for start parser"""
#     name = sys.argv[1]
#     f = globals().get(name)
#     print(f)
#     if f:
#         utilites.parser.main()