from .models import QuizAnswer


def get_total(quiz_answer: QuizAnswer):
    total = 0
    for quiz_item in quiz_answer.quizansweritem_set.all():
        answer_ids = [x.id for x in quiz_item.answers.all()]
        for choice in quiz_item.question.choice_set.all():
            if choice.is_answer and choice.id not in answer_ids:
                break
            elif not choice.is_answer and choice.id in answer_ids:
                break
        else:
            total += 1
    return total
