
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test.client import Client

from .models import Account, AskLike, AnswerLike, Answer, Ask
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from taggit.models import Tag
# Create your tests here.
User = get_user_model()

class AskMeTestCases(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='testuser', email='email@mail.ru', password='password')
        self.user2 = User.objects.create_user(username='testuser2', email='email2@mail.ru', password='password2')
        avatar = SimpleUploadedFile('avatar.jpg', content=b'', content_type='image/jpg')
        avatar2 = SimpleUploadedFile('noavatar.jpg', content=b'', content_type='image/jpg')
        self.account = Account.objects.create(user=self.user1, user_avatar=avatar)
        self.account2 = Account.objects.create(user=self.user2, user_avatar=avatar2)
        self.tag = Tag.objects.create(name='testTag')
        self.ask = Ask.objects.create(
            ask_title='TestAsk',
            ask_explane='TestAskExplane',
            asker_name=self.user1,
            ask_tags=self.tag
        )
        self.answer = Answer.objects.create(
            ask=self.ask,
            answerer_name=self.user2,
            answer_text='TestAnswer'
        )

    def test_user_signup_real(self):
        c = Client()
        data = {'username': 'newuser',
                'email': 'new@mail.ru',
                'password': 'newpassword',
                'password2': 'newpassword',
        }
        c.post('/signup/', data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Account.objects.filter(user=User.objects.get(username='newuser')).exists())

    def test_user_signup_email_exists(self):
        c = Client()
        data = {'username': 'newuser',
                'email': 'email@mail.ru',
                'password': 'newpassword',
                'password2': 'newpassword',
        }
        c.post('/signup/', data)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_signup_badpass(self):
        c = Client()
        data = {'username': 'newuser',
                'email': 'new@mail.ru',
                'password': 'newpassword',
                'password2': 'newpasswor',
        }
        c.post('/signup/', data)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_login_real(self):
        c = Client()
        response = c.login(username='testuser', password='password')
        self.assertTrue(response)

    def test_user_login_unreal(self):
        c = Client()
        response = c.login(username='testuser3', password='password3')
        self.assertFalse(response)

    def test_user_settings(self):
        c = Client()
        c.login(username='testuser', password='password')
        response = c.get('/settings/')
        self.assertEqual(response.context['user'], User.objects.get(username='testuser'))
        self.assertEqual(response.status_code, 200)

    def test_ask_add(self):
        c = Client()
        c.login(username='testuser', password='password')
        data = {'ask_title': 'TestQuest',
                'ask_explane': 'TestQuestion',
                'ask_tags': 'testing, question',
        }
        c.post('/ask/', data)
        self.assertTrue(Ask.objects.filter(ask_title='TestQuest').exists())

