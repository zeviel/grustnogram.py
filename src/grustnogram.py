import requests


class GrustnoGram:
    def __init__(self):
        self.api = "https://api.grustnogram.ru"
        self.media_api = "https://media.grustnogram.ru"
        self.access_token = None
        self.headers = {
            "user-agent": "Dart/2.16 (dart:io)"
        }

    def upload_media(self, file: bytes):
        data = {"file": ("image.jpg", file, "image/jpg")}
        return requests.post(
            f"{self.media_api}/cors.php",
            files=data,
            headers=self.headers).json()

    def login(self, email: str, password: str):
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(
            f"{self.api}/sessions",
            json=data,
            headers=self.headers).json()
        self.access_token = response["data"]["access_token"]
        self.headers["access-token"] = self.access_token
        self.user_id = self.get_current_session()["data"]["id"]
        return response

    def logout(self):
        response = requests.delete(
            f"{self.api}/sessions/current",
            headers=self.headers)
        self.headers = response.headers
        self.access_token = None
        self.user_id = None
        return response.json()

    def get_current_session(self):
        return requests.get(
            f"{self.api}/users/self",
            headers=self.headers).json()

    def register(self, nickname: str, email: str, password: str):
        data = {
            "nickname": nickname,
            "email": email,
            "password": password
        }
        return requests.post(
            f"{self.api}/users",
            json=data,
            headers=self.headers).json()

    def get_phone_activation_code(self, phone_key: str, phone_number: str):
        data = {
            "phone_key": phone_key,
            "phone": phone_number
        }
        return requests.post(
            f"{self.api}/callme",
            json=data,
            headers=self.headers).json()

    def activate_phone(self, phone_number: str, activation_code: int):
        data = {
            "phone": phone_number,
            "code": activation_code
        }
        return requests.post(
            f"{self.api}/phoneactivate",
            json=data,
            headers=self.headers).json()

    def reset_password(self, email: str):
        data = {"email": email}
        return requests.post(
            f"{self.api}/respsswd",
            json=data,
            headers=self.headers).json()

    def like_post(self, post_id: int):
        data = {}
        return requests.post(
            f"{self.api}/posts/{post_id}/like",
            json=data,
            headers=self.headers).json()

    def unlike_post(self, post_id: int):
        return requests.delete(
            f"{self.api}/posts/{post_id}/like",
            headers=self.headers).json()

    def get_post_comments(self, post_id: int, offset: int = 0):
        return requests.get(
            f"{self.api}/posts/{post_id}/comments?offset={offset}",
            headers=self.headers).json()

    def get_post_likes(self, post_id: int, offset: int = 0):
        return requests.get(
            f"{self.api}/posts/{post_id}/likes?offset={offset}",
            headers=self.headers).json()

    def get_status(self):
        return requests.get(f"{self.api}/status", headers=self.headers).json()

    def get_posts_list(self, type: str = None):
        url = f"{self.api}/posts"
        if type:
            url += f"?{type}=1"
        return requests.get(url, headers=self.headers).json()

    def get_user_posts(self, user_id: int, limit: int = 15, offset: int = 0):
        return requests.get(
            f"{self.api}/posts?id_user={user_id}&limit={15}&offset={offset}",
            headers=self.headers).json()

    def comment_post(self, post_id: int, comment: str, reply_to: int = -1):
        data = {
            "comment": comment,
            "reply-to": reply_to
        }
        return requests.post(
            f"{self.api}/posts/{post_id}/comments",
            json=data,
            headers=self.headers).json()

    def delete_comment(self, comment_id: int):
        return requests.delete(
            f"{self.api}/posts/comments/{comment_id}",
            headers=self.headers).json()

    def follow_user(self, user_id: int):
        data = {}
        return requests.post(
            f"{self.api}/users/{user_id}/follow",
            json=data,
            headers=self.headers).json()

    def unfollow_user(self, user_id: int):
        return requests.delete(
            f"{self.api}/users/{user_id}/follow",
            headers=self.headers).json()

    def get_user_followers(self, user_id: int):
        return requests.get(
            f"{self.api}/followers/{user_id}",
            headers=self.headers).json()

    def get_user_followings(self, user_id: int):
        return requests.get(
            f"{self.api}/follow/{user_id}",
            headers=self.headers).json()

    def edit_profile(
            self,
            nickname: str = None,
            name: str = None,
            about: str = None,
            avatar: bytes = None):
        data = {}
        if nickname:
            data["nickname"] = nickname
        elif name:
            data["name"] = name
        elif about:
            data["about"] = about
        elif avatar:
            data["avatar"] = self.upload_media(avatar)["data"]
        return requests.put(
            f"{self.api}/users/self",
            json=data,
            headers=self.headers).json()

    def create_post(self, text: str, image: bytes, filter: int = 0):
        data = {
            "media": [self.upload_media(image)["data"]],
            "text": text,
            "filter": filter
        }
        return requests.post(
            f"{self.api}/posts",
            json=data,
            headers=self.headers).json()

    def get_user_info(self, nickname: str):
        return requests.get(
            f"{self.api}/users/{nickname}",
            headers=self.headers).json()

    def block_user(self, user_id: int):
        data = {}
        return requests.post(
            f"{self.api}/users/{user_id}/block",
            json=data,
            headers=self.headers).json()

    def unblock_user(self, user_id: int):
        return requests.delete(
            f"{self.api}/users/{user_id}/block",
            headers=self.headers).json()

    def report_user(self, user_id: int, type: int = 1):
        data = {"type": type}
        return requests.post(
            f"{self.api}/users/{user_id}/complaint",
            json=data,
            headers=self.headers).json()

    def report_comment(self, comment_id: int):
        data = {}
        return requests.post(
            f"{self.api}/posts/comments/{comment_id}/complaint",
            json=data,
            headers=self.headers).json()

    def report_post(self, post_id: int, type: int = 1):
        data = {"type": type}
        return requests.post(
            f"{self.api}/posts/{post_id}/complaint",
            json=data,
            headers=self.headers).json()

    def like_comment(self, comment_id: int):
        data = {}
        return requests.post(
            f"{self.api}/comments/{comment_id}/like",
            json=data,
            headers=self.headers).json()

    def unlike_comment(self, comment_id: int):
        return requests.delete(
            f"{self.api}/comments/{comment_id}/like",
            headers=self.headers).json()

    def get_notifications(self):
        return requests.get(
            f"{self.api}/notifications",
            headers=self.headers).json()

    def search_user(self, query: str):
        return requests.get(
            f"{self.api}/users?q={query}",
            headers=self.headers).json()

    def search_post(self, query: str):
        return requests.get(
            f"{self.api}/posts?q={query}",
            headers=self.headers).json()

    def get_users_list(self, top: int = 1):
        return requests.get(
            f"{self.api}/users?top={top}",
            headers=self.headers).json()

    def change_password(self, old_password: str, new_password: str):
        data = {
            "old_password": old_password,
            "new_password": new_password
        }
        return requests.put(
            f"{self.api}/users/self",
            json=data,
            headers=self.headers).json()

    def edit_post(self, post_id: int, text: str):
        data = {"text": text}
        return requests.put(
            f"{self.api}/posts/{post_id}",
            json=data,
            headers=self.headers).json()

    def delete_post(self, post_id: int):
        return requests.delete(
            f"{self.api}/posts/{post_id}",
            headers=self.headers).json()
