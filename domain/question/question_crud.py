from datetime import datetime

from models import Question, User
from sqlalchemy.orm import Session
from domain.question.question_schema import QuestionCreate


'''
데이터를 조회하는 부분을 따로 분리하여 작성 
-> 서로 다른 라우터에서 데이터를 처리하는 부분이 동일하여 중복될 수 있기 때문. 
* 반복 작업 -> 모듈 구성으로 효율적 사용

tip. 
1. db 세션은 라우터에서 받아서 매개변수로 입력. -> but type 지정위해 라이브러리 설정 필요.

'''


def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()
