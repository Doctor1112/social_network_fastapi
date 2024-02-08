


from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    entity: str

    def __init__(self, id):
        detail = f"A {self.entity} with id {id} doesn't exist"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserNotFoundException(NotFoundException):
    entity = "user"


class FriendRequestNotFoundException(NotFoundException):
    entity = "request"

    def __init__(self, sender_id, receiver_id):
        id = f"sender_id: {sender_id} and receiver_id: {receiver_id}"
        super().__init__(id)
