from ninja import Router
from django.http import HttpRequest

from .schema import (
    LessonIn,
    LessonCreateSchema,
    LessonSchema,
    QuizIn,
    QuizSaveSchema,
    QuestionSaveSchema,
    ChoiceSaveSchema,
    QuizDetailSchema,
    QuizPublicDetailSchema,
    QuizSubmitSchema,
    ResultSchema,
    QuizAnswerListSchema,
)
from typing import List
from .models import Lesson, LessonElement, Quiz, Question, Choice, QuizAnswer, QuizAnswerItem
from slugify import slugify
from valearnis.auth.authentication import AuthBearer
from .utils import get_total
from valearnis.auth.permissions import permission_decorator, IsAdmin

lessons_router = Router(auth=AuthBearer())


@lessons_router.get("/", response={200: List[LessonSchema]})
def get_lessons(request):
    return Lesson.objects.all()


@lessons_router.post("/", response={200: LessonSchema})
@permission_decorator(IsAdmin)
def create_lesson(request, data: LessonIn):
    data.slug = slugify(data.name)
    lesson_data = LessonCreateSchema(**data.dict())
    lesson = Lesson.objects.create(**lesson_data.dict())

    for element in data.lesson_elements or []:
        LessonElement.objects.create(lesson=lesson, **element.dict())

    return lesson


@lessons_router.get("{slug}/", response={200: LessonSchema})
def get_lesson(request, slug: str):
    return Lesson.objects.filter(slug=slug).first()


@lessons_router.put("{slug}/", response={200: LessonSchema})
@permission_decorator(IsAdmin)
def update_lesson(request, slug: str, data: LessonIn):
    lesson_data = LessonCreateSchema(**data.dict())
    lesson_data.slug = slugify(data.name)
    lesson = Lesson.objects.filter(slug=slug).first()
    for field, value in lesson_data.dict().items():
        setattr(lesson, field, value)
    lesson.save()

    lesson_elements_ids_to_retain = []
    for lesson_element in data.lesson_elements or []:
        # IF LESSON ELEMENT EXISTS, UPDATE
        if lesson_element.id:
            _lesson_element = LessonElement.objects.get(id=lesson_element.id)
            for field, value in lesson_element.dict().items():
                setattr(_lesson_element, field, value)
            _lesson_element.save()
            lesson_elements_ids_to_retain.append(_lesson_element.id)
        # IF NOT, CREATE A NEW LESSON ELEMENT
        else:
            _lesson_element = LessonElement.objects.create(lesson=lesson, **lesson_element.dict())
            lesson_elements_ids_to_retain.append(_lesson_element.id)
    # THEN DELETE REMAINING LESSON ELEMENTS
    lesson_elements_to_delete = lesson.lessonelement_set.exclude(id__in=lesson_elements_ids_to_retain)
    lesson_elements_to_delete.delete()
    return lesson


@lessons_router.post("{slug}/quizzes/", response={200: QuizDetailSchema})
@permission_decorator(IsAdmin)
def create_quiz(request, slug: str, data: QuizIn):
    lesson = Lesson.objects.get(slug=slug)
    quiz_data = QuizSaveSchema(**data.dict())
    quiz = Quiz.objects.create(lesson=lesson, **quiz_data.dict())

    for question_data in data.questions:
        question = QuestionSaveSchema(**question_data.dict())
        _question = Question.objects.create(quiz=quiz, **question.dict())

        for choice_data in question_data.choices:
            choice = ChoiceSaveSchema(**choice_data.dict())
            Choice.objects.create(question=_question, **choice.dict())

    return quiz


@lessons_router.get("{slug}/quizzes/", response={200: List[QuizDetailSchema]})
@permission_decorator(IsAdmin)
def quiz_list(request, slug: str):
    lesson = Lesson.objects.get(slug=slug)
    return Quiz.objects.filter(lesson__id=lesson.id)


@lessons_router.get("{slug}/quizzes/{quiz_id}/", response={200: QuizDetailSchema})
def get_quiz(request, slug: str, quiz_id: int):
    return Quiz.objects.get(id=quiz_id)


@lessons_router.put("{slug}/quizzes/{quiz_id}/", response={200: QuizDetailSchema})
@permission_decorator(IsAdmin)
def get_quiz(request, slug: str, quiz_id: int, data: QuizIn):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_data = QuizSaveSchema(**data.dict())
    for field, value in quiz_data.dict().items():
        setattr(quiz, field, value)
    quiz.save()

    questions_id_to_retain = []
    for question_data in data.questions:
        _question_data = QuestionSaveSchema(**question_data.dict())
        # IF QUESTION EXISTS, UPDATE
        if question_data.id:
            _question = Question.objects.get(id=question_data.id)
            for field, value in _question_data.dict().items():
                setattr(_question, field, value)
            _question.save()
            questions_id_to_retain.append(_question.id)
        # IF NOT, CREATE A NEW QUESTION
        else:
            _question = Question.objects.create(quiz=quiz, **_question_data.dict())
            questions_id_to_retain.append(_question.id)

        choice_ids_to_retain = []
        for choice_data in question_data.choices:
            _choice_data = ChoiceSaveSchema(**choice_data.dict())
            # IF CHOICE EXISTS, UPDATE CHOICE
            if choice_data.id:
                _choice = Choice.objects.get(id=choice_data.id)
                for field, value in _choice_data.dict().items():
                    setattr(_choice, field, value)
                _choice.save()
                choice_ids_to_retain.append(_choice.id)
            # IF NOT, CREATE A NEW QUESTION
            else:
                _choice = Choice.objects.create(question=_question, **_choice_data.dict())
                choice_ids_to_retain.append(_choice.id)

        # DELETE UNRELATED CHOICES
        choice_ids_to_delete = _question.choice_set.exclude(id__in=choice_ids_to_retain)
        choice_ids_to_delete.delete()

    # DELETE UNRELATED QUESTIONS
    question_ids_to_delete = quiz.question_set.exclude(id__in=questions_id_to_retain)
    question_ids_to_delete.delete()

    return quiz


@lessons_router.get("{slug}/quizzes/{quiz_id}/take/", response={200: QuizPublicDetailSchema})
def get_quiz(request, slug: str, quiz_id: int):
    return Quiz.objects.get(id=quiz_id)


@lessons_router.post("{slug}/quizzes/{quiz_id}/submit/", response={200: ResultSchema})
def get_quiz(request: HttpRequest, slug: str, quiz_id: int, data: QuizSubmitSchema):
    quiz = Quiz.objects.get(id=quiz_id)
    user = request.user

    quiz_answer = QuizAnswer.objects.create(user=user, quiz=quiz)

    total = 0
    for quiz_item in data.quiz_items:
        question = Question(**quiz_item.question.dict())
        quiz_answer_item = QuizAnswerItem.objects.create(
            quiz_answer=quiz_answer,
            question=question,
        )
        answer_ids = [x.id for x in quiz_item.answers]
        choices = Choice.objects.filter(id__in=answer_ids)
        quiz_answer_item.answers.add(*choices)
        quiz_answer_item.save()

        for choice in question.choice_set.all():
            if choice.is_answer and choice.id not in answer_ids:
                break
            elif not choice.is_answer and choice.id in answer_ids:
                break
        else:
            total += 1

    result = ResultSchema(
        quiz_answer_id=quiz_answer.id,
        quiz=quiz,
        total_items=len(data.quiz_items),
        total=total,
        quiz_items=data.quiz_items,
    )

    quiz_answer.total = total
    quiz_answer.total_items = len(data.quiz_items)
    quiz_answer.percentage = (quiz_answer.total / quiz_answer.total_items) * 100
    quiz_answer.save()

    return result


quizz_answers_router = Router(auth=AuthBearer())


@quizz_answers_router.get("{id}/", response={200: ResultSchema})
def get_quiz(request, id: int):
    quiz_answer = QuizAnswer.objects.get(id=id)
    result = ResultSchema(
        quiz_answer_id=quiz_answer.id,
        quiz=quiz_answer.quiz,
        total_items=quiz_answer.quiz.question_set.count(),
        total=get_total(quiz_answer),
        quiz_items=list(quiz_answer.quizansweritem_set.all()),
    )
    return result
