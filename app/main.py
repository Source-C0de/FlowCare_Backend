
from fastapi import FastAPI



def project_init() -> FastAPI:

    app = FastAPI()    
    return app

app = project_init()