import datetime
from polls.models import Question, Choice
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

# Create your tests here.

def put_choices_to_question(question: Question, choice_text: str):
    return Choice.objects.create(question=question, choice_text=choice_text)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionModelTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        past_question = create_question(question_text = "Past Question", days = -5)
        put_choices_to_question(past_question, "Choice to Past Question")
        url = reverse("polls:detail", args = (past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        future_question = create_question(question_text="Future question.", days=30)
        url = reverse("polls:detail", args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        put_choices_to_question(question, 'choice to future question')
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_was_published_recently_with_old_question(self):
        someday_in_past = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date = someday_in_past)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_future_question(self):
        someday_in_future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = someday_in_future)
        self.assertIs(future_question.was_published_recently(), False)

    def test_questions_without_choices_are_excluded(self):
        question_without_choice = create_question("Questions with No Choice", days = -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])