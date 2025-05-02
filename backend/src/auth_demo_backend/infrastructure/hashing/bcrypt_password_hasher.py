import bcrypt

from auth_demo_backend.domain.ports import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):

    def hash(self, password: str) -> str:

        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).hex()

    def verify(self, password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(password.encode("utf-8"), bytes.fromhex(hashed_password))
