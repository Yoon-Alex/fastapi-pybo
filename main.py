from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router

app = FastAPI()

origins = [  # frontend url
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)

# @app.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}

# @app.get("/what")
# def what():
#     return {"message": "FASTAPI를 배우는 중임다."}