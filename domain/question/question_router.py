from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
from starlette import status


# 라우터 파일 핵심. 
router = APIRouter(
    prefix="/api/question",
)


# 보호(protected) 인스턴스 속성 : _leading_underscore
# get_db 제너레이터에 의해 생성된 세션 객체 자동으로 함수에 contextmanager가 적용
# (Depends에서 contextmanager를 적용하게끔 설계되어 있다.)

# @router.get("/list", response_model=list[question_schema.Question])
# def question_list(db: Session = Depends(get_db)): 
#     # Question 모델 값의 list 형태로 return -> orm_mode 설정으로 Question 스키마와 매핑
#     _question_list = question_crud.get_question_list(db)
#     # _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     return _question_list

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    return {
        'total': total,
        'question_list': _question_list
    }


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question_crud.create_question(db=db, question_create=_question_create)


# 같은 작용
# 보호(protected) 인스턴스 속성 : _leading_underscore
# @router.get("/list")
# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     return _question_list
