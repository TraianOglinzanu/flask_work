class User():

    def __init__(self, id, username, password):

        self.id = id
        self.username = username

        #not hashing password for protection this time
        self.password = password

    def __str__(self):

        return f"User Id: {self.id}"