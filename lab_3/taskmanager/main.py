from fastapi import FastAPI
import uvicorn
from db.connection import init_db
from endpoints.case_endpoints import case_router
from endpoints.subcase_endpoint import subcase_router
from endpoints.message_endpoint import message_router
from endpoints.doing_endpoint import doing_router
from endpoints.user_endpoints import user_router

app = FastAPI()

app.include_router(case_router, prefix="/api/cases", tags=["cases"])
app.include_router(subcase_router, prefix="/api/subcases", tags=["subcases"])
app.include_router(message_router, prefix="/api/messages", tags=["messages"])
app.include_router(doing_router, prefix="/api/doing", tags=["doings"])
app.include_router(user_router, prefix="/api", tags=["users"])


@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)