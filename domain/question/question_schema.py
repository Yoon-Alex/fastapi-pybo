import datetime
from pydantic import BaseModel, validator
from domain.answer.answer_schema import Answer

'''
스키마 모델은, pydantic의 BaseModel을 상속받아 사용. 
* 출력 항목을 정의, 타입 지정. 
정해진 타입이 아닌 다른 타입이 지정되면 오류. 
보여주고 싶지 않은 컬럼, 정보인 경우 스키마에서 간단히 제외하면 -> 편리 
'''


class Question(BaseModel):
    id: int
    # None 가질 수 있고 default 값(None) 지정. 
    subject: str | None = None 
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []  # backref="answers"

    class Config:
        orm_mode = True  # DataBase model 과 pydantic model 매핑


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')  # 값에 빈값을 허용하지 않는다는 뜻.
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []