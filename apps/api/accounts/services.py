from accounts.models import Profile, User
from core.services import BaseService


class CreateUserWithProfileService(BaseService):
    def __init__(
        self,
        *,
        username: str,
        email: str,
        password: str,
        display_name: str = "",
    ) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.display_name = display_name

    def execute(self) -> User:
        user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

        profile = Profile(
            user=user,
            display_name=self.display_name,
        )
        profile.save()

        return user
