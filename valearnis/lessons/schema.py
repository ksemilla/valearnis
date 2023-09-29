from ninja import Schema, Field
from pydantic import validator
from .models import Lesson
from slugify import slugify
from typing import List
from enum import Enum


class LessonElementType(str, Enum):
    TEXT = "text"
    IMAGE = "image"


class LessonElementIn(Schema):
    id: int = None
    display_order: int
    text: str = None
    img_url: str = None
    type: LessonElementType


class LessonIn(Schema):
    id: int = None
    name: str
    subtitle: str = None
    description: str = None
    slug: str = None
    lesson_elements: List[LessonElementIn] | None
    img_url: str = None

    @validator("name")
    def validate_name(cls, value, values):
        lesson = Lesson.objects.filter(slug=slugify(value)).first()
        if lesson and ((values["id"] and lesson.id != values["id"]) or not values["id"]):
            raise ValueError("Conflicting name")
        return value


class LessonElementSchema(Schema):
    id: int = None
    display_order: int
    text: str = None
    img_url: str = None
    type: LessonElementType


class LessonCreateSchema(Schema):
    slug: str
    name: str
    subtitle: str
    description: str
    img_url: str = None


class QuestionType(str, Enum):
    SINGLE_MUTIPLE_CHOICE = "smc"
    MULTI_MULTIPLE_CHOICE = "mmc"


class ChoiceIn(Schema):
    id: int = None
    text: str
    is_answer: bool = False


class QuestionIn(Schema):
    id: int = None
    text: str
    type: QuestionType
    choices: List[ChoiceIn]

    @validator("choices")
    def validate_choices(cls, value, values):
        if len(value) < 2:
            raise ValueError("There should be atleast 2 choices")
        elif values["type"] == QuestionType.SINGLE_MUTIPLE_CHOICE:
            answer_count = [x.is_answer for x in value].count(True)
            if answer_count != 1:
                raise ValueError("There should be one and only one answer from the choices")
            choices_set = set([x.text for x in value])
            if len(choices_set) != len(value):
                raise ValueError("All choices should be unique")
        elif values["type"] == QuestionType.MULTI_MULTIPLE_CHOICE:
            answer_count = [x.is_answer for x in value].count(True)
            if answer_count == 0:
                raise ValueError("There should be atleast one answer from the choices")
            choices_set = set([x.text for x in value])
            if len(choices_set) != len(value):
                raise ValueError("All choices should be unique")
        return value


class QuizIn(Schema):
    id: int = None
    name: str
    questions: List[QuestionIn]

    @validator("questions")
    def validate_questions(cls, value):
        if len(value) == 0:
            raise ValueError("No questions were provided")
        return value


class QuizSaveSchema(Schema):
    id: int = None
    name: str


class QuestionSaveSchema(Schema):
    id: int = None
    text: str
    type: QuestionType


class ChoiceSaveSchema(Schema):
    id: int = None
    text: str
    is_answer: bool = False


class QuestionDetailSchema(QuestionSaveSchema):
    choices: List[ChoiceSaveSchema] = Field(..., alias="choice_set")


class QuizDetailSchema(QuizSaveSchema):
    questions: List[QuestionDetailSchema] = Field(..., alias="question_set")


class ChoicePublicDetailSchema(Schema):
    id: int = None
    text: str


class QuestionPublicDetailSchema(QuestionSaveSchema):
    choices: List[ChoicePublicDetailSchema] = Field(..., alias="choice_set")


class QuizPublicDetailSchema(QuizSaveSchema):
    questions: List[QuestionPublicDetailSchema] = Field(..., alias="question_set")


class LessonSchema(Schema):
    id: int
    slug: str
    name: str
    subtitle: str
    description: str
    img_url: str = None
    lesson_elements: List[LessonElementSchema] = Field(..., alias="lessonelement_set")
    quizzes: List[QuizPublicDetailSchema] = Field(..., alias="quiz_set")


class QuestionSubmitSchema(Schema):
    id: int
    text: str
    type: QuestionType


class QuizAnswerItemSubmitSchema(Schema):
    question: QuestionSubmitSchema
    answers: List[ChoiceIn]

    @validator("answers")
    def validate_questions(cls, value, values):
        answer_count = len(value)
        if len(value) == 0:
            raise ValueError("No answers selected")
        elif answer_count == 0:
            raise ValueError("There should be atleast one answer from the choices")
        elif values["question"].type == QuestionType.SINGLE_MUTIPLE_CHOICE and answer_count != 1:
            raise ValueError("There should be one and only one answer from the choices")
        return value


class QuizAnswerItemDetailSchema(Schema):
    question: QuestionDetailSchema
    answers: List[ChoiceIn]


class QuizSubmitSchema(Schema):
    quiz_items: List[QuizAnswerItemSubmitSchema]


class ResultSchema(Schema):
    quiz_answer_id: int
    quiz: QuizDetailSchema
    total_items: int
    total: int
    quiz_items: List[QuizAnswerItemSubmitSchema]


class QuizAnswerListSchema(Schema):
    id: int
    quiz: QuizDetailSchema
    total: int
    total_items: int
    percentage: float
