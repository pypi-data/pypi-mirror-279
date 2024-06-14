class JwtUser:

    def __init__(self, user):
        self.user_id = user.get('sub')
        self.roles = user.get('roles')

    def contain(self, roles: list[str]) -> bool:
        return bool(len(set(self.roles) & set(roles)))

    def is_authenticated(self) -> bool:
        return bool(self.user_id)

