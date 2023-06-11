import datetime
from pydantic import BaseModel, validator


class AnswerCreate(BaseModel): # 입력 받는
    content: str

    # content의 값이 없거나 또는 빈 값인 경우 "빈 값은 허용되지 않습니다." 라는 오류가 발생
    @validator('content')  # "" 처럼 빈 문자열이 입력될 수 있다는 점
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Answer(BaseModel): 
    id: int
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True