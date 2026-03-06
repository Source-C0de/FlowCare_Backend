from uuid import UUID


class User:
    def __init__(self, id : UUID, name: str, email: str , hashed_password: str):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        
    def changed_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password