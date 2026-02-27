"""
Test Factories using factory-boy.

Factories generate test data consistently.
"""
from factory import Factory, Faker, Sequence, SubFactory, LazyAttribute
from factory.fuzzy import FuzzyChoice
from datetime import datetime

from src.models.user import User
from src.models.course import Course
from src.models.lesson import Lesson
from src.models.quiz import Quiz, Question, Answer


class UserFactory(Factory):
    """Factory for creating User test instances."""

    class Meta:
        model = User

    email = Faker("email")
    name = Faker("name")
    password = Faker("password", length=12)
    avatar = Faker("image_url")
    is_active = True
    created_at = datetime.utcnow()


class CourseFactory(Factory):
    """Factory for creating Course test instances."""

    class Meta:
        model = Course

    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    creator_id = 1  # Override in tests
    thumbnail = Faker("image_url")
    category = FuzzyChoice(["programming", "design", "business", "marketing"])
    level = FuzzyChoice(["beginner", "intermediate", "advanced"])
    duration_hours = FuzzyChoice([10, 20, 30, 40, 50])
    is_published = True
    created_at = datetime.utcnow()


class LessonFactory(Factory):
    """Factory for creating Lesson test instances."""

    class Meta:
        model = Lesson

    course_id = 1  # Override in tests
    title = Faker("sentence", nb_words=3)
    content = Faker("paragraph", nb_sentences=10)
    video_url = Faker("url")
    order = Sequence(lambda n: n + 1)
    duration_minutes = FuzzyChoice([15, 30, 45, 60])
    created_at = datetime.utcnow()


class QuizFactory(Factory):
    """Factory for creating Quiz test instances."""

    class Meta:
        model = Quiz

    lesson_id = 1  # Override in tests
    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    time_limit = FuzzyChoice([15, 30, 45, 60])
    passing_score = FuzzyChoice([50, 60, 70, 80])
    max_attempts = 3
    created_at = datetime.utcnow()


class QuestionFactory(Factory):
    """Factory for creating Question test instances."""

    class Meta:
        model = Question

    quiz_id = 1  # Override in tests
    content = Faker("sentence")
    type = FuzzyChoice(["single_choice", "multiple_choice", "true_false", "fill_blank"])
    points = FuzzyChoice([1, 2, 3, 5])
    order = Sequence(lambda n: n + 1)


class AnswerFactory(Factory):
    """Factory for creating Answer test instances."""

    class Meta:
        model = Answer

    question_id = 1  # Override in tests
    content = Faker("sentence")
    is_correct = Faker("boolean")
    order = Sequence(lambda n: n + 1)
