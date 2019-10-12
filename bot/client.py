import random
import logging

from faker import Faker
import requests


fake = Faker()

class BotClient():

    def __init__(self, number_of_users, max_posts_per_user, max_likes_per_user, url):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.url = url

    def register_users(self):
        user_psw_dict = {}
        for _ in range(self.number_of_users):
            profile = fake.simple_profile()
            username = profile.get('username')
            names = profile.get('name').split()
            password = fake.password()
            email = fake.email()
            firstname, lastname = names[0], names[1]

            parameters = {
                'username': username,
                'password': password,
                'email': email,
                'first_name': firstname,
                'last_name': lastname
            }

            response = requests.post(url=self.url + '/api/users/', data=parameters)
            if response.status_code == 201:
                logging.info(f"user created successfully {email} {password}")
                user_psw_dict[username] = password
            else:
                logging.info(f"Failed to create account.\n Email:{email}; Username {username}; First Name:{firstname}; Last Name: {lastname}")

        return user_psw_dict

    def auth_users(self, users):
        user_token_dict={}
        for username, password in users.items():
            parameters = {
                'username': username,
                'password': password
            }
            print(parameters)
            response = requests.post(url=self.url + '/api/auth/', data=parameters)
            if response.status_code == 200:
                logging.info(f"{username} successfully authenticated.")
                print(response)
                print(response.text + '\n')
                resp_json = response.json()
                if resp_json.get('token'):
                    token = resp_json.get('token')
                    user_token_dict[username] = token
            else:
                logging.info(f"Failed to  authenticate : {username}")

        return user_token_dict

    def create_posts(self, users):
        user_posts = {}
        posts = []
        for username, token in users.items():
            random_num_of_posts = random.randint(1, self.max_posts_per_user)
            print(username, token, random_num_of_posts)
            user_posts[username] = {'token': token, 'posts': []}
            for i in range(random_num_of_posts):
                headers = {'Authorization': 'Bearer {}'.format(token)}
                parameters = {
                    'text': fake.sentence(),
                }
                response = requests.post(url=self.url + '/api/posts/', data=parameters, headers=headers)
                if response.status_code == 201:
                    resp_json = response.json()
                    post_id = resp_json.get('id')
                    text = resp_json.get('text')
                    logging.info(f"new post from user {username}")
                    user_posts[username]['posts'].append(post_id)
                    posts.append(post_id)

        return user_posts, posts

    def like_posts(self, users, posts):
        for username, params in users.items():
            token, user_posts = params['token'], params['posts']
            likes_by_user = 0
            while likes_by_user < self.max_likes_per_user:
                other_users_posts = list(set(posts) - set(user_posts))
                if other_users_posts:
                    post_id = random.choice(other_users_posts)
                    headers = {'Authorization': 'Bearer {}'.format(token)}
                    response = requests.post(url=self.url + '/api/posts/{}/likes/'.format(post_id), headers=headers)
                    if response.status_code == 201:
                        logging.info(f"User {username} liked post {post_id}\n")
                        likes_by_user += 1
                        posts.remove(post_id)
                else:
                    break


    def start_activity(self):
        users_with_psw = self.register_users()
        print('registration finished \n')
        print(users_with_psw)
        users_with_token = self.auth_users(users_with_psw)
        print('authorization finished \n')
        user_posts, posts = self.create_posts(users_with_token)
        print('post creation finished \n')

        self.like_posts(user_posts, posts)
        print('users liked the posts \n')
        print('finish')


if __name__ == "__main__":
    from bot.config import BotConfig

    client = BotClient(BotConfig.number_of_users,
                       BotConfig.max_likes_per_user,
                       BotConfig.max_posts_per_user,
                       BotConfig.url)

    client.start_activity()

