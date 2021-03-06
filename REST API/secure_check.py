from user import User

users = [User(1,'Bob', 'mypassword1'),
        User(2, 'Tim', 'mypassword2')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):






