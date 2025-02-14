import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from src.config import Config
from src.tool.apis import router as tools_router
from src.agent.apis import router as agents_router
from src.task.apis import router as tasks_router
from src.user.apis import router as user_attributes_router
from src.chat.apis import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from langtrace_python_sdk import langtrace

langtrace.init(api_key=Config.LANGTRACE_API_KEY)

if not os.path.exists("static"):
    os.mkdir("static")

origins = ["*"]
app = FastAPI(
    title="Colabi",
    # Disable OpenAPI docs in production to reduce startup time
    # openapi_url=False,
    # docs_url=False,
    # redoc_url=False,
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def root():
    return JSONResponse(content={"status": "Healthy"}, status_code=200)


app.include_router(tools_router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(agents_router, prefix="/api/v1/agent", tags=["agents"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(
    user_attributes_router, prefix="/api/v1/user_attributes", tags=["user_attributes"]
)
app.mount("/static", StaticFiles(directory="static"), name="static")

