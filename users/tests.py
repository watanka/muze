from django.test import TestCase
from .models import User, FriendRequest
from django.urls import reverse
# Create your tests here.
class UserTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            nickname="test-user1",
            username="test-user1",
            password="test-password"
        )
        self.friend = User.objects.create_user(
            nickname="test-user2",
            username="test-user2",
            password="test-password"
        )

        self.client.login(username="test-user1", password="test-password")

    def test_친구요청생성(self): 
        response = self.client.post(reverse('users:friend_request', args=[self.friend.id]),
                                    {'sender_id': self.user.id}
                                    )
        self.assertEqual(response.status_code, 200)
        friend_request = FriendRequest.objects.get(from_user = self.user.id, 
                                                   to_user = self.friend.id)
        self.assertIsNotNone(friend_request)

        self.user.friends.clear()
        self.friend.friends.clear()

    def test_친구요청을_상대방이_수락시에_친구가됨(self):
        # user가 friend에게 친구 요청
        response = self.client.post(reverse('users:friend_request', args=[self.friend.id]),
                                    {'sender_id': self.user.id}
                                    )
        # friend 계정으로 로그인
        self.client.login(username="test-user2", password="test-password")
        response = self.client.post(reverse('users:accept_friend_request'),
                            {'sender_id': self.user.id,
                             'receiver_id': self.friend.id,
                             }   
                         )
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.friend, self.user.friends.all())
        self.assertIn(self.user, self.friend.friends.all())

        self.user.friends.clear()
        self.friend.friends.clear()

    def test_친구요청을_거절할경우_친구가_아님(self):
        # user가 friend에게 친구 요청
        response = self.client.post(reverse('users:friend_request', args=[self.friend.id]),
                                    {'sender_id': self.user.id}
                                    )
        # friend 계정으로 로그인
        self.client.login(username="test-user2", password="test-password")
        response = self.client.post(reverse('users:reject_friend_request'),
                            {'sender_id': self.user.id,
                             'receiver_id': self.friend.id,
                             }   
                         )
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.friend, self.user.friends.all())
        self.assertNotIn(self.user, self.friend.friends.all())

    def test_이미_친구거나_친구요청을_보낸_상태라면_친구추가_실패(self):
        self.user

        
