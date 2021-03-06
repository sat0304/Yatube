import shutil
import tempfile

from django.core.cache import cache
from django.conf import settings
from django.test import TestCase, override_settings

from posts.models import Comment, Group, Follow, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='not_auth')
        cls.auth = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст',
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            text='Тестовый коментарий',
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.auth,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = self.post
        group = self.group
        comment = self.comment
        follow = self.follow
        field_object_names = {
            group.title: 'Тестовая группа',
            post.text: 'Тестовый_текст',
            comment.text: 'Тестовый коментарий',
            str(follow): 'Подписчик: not_auth, на автора: auth',
        }
        for field, expected_value in field_object_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    str(field),
                    expected_value
                )

    def test_model_Post_have_correct_verbose_name(self):
        """Проверяем, что у модели Post корректно работает verbose name."""
        post = self.post
        field_verbose_names = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_model_Post_have_correct_help_text(self):
        """Проверяем, что у модели Post корректно работает help text."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
