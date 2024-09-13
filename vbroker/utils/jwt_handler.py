import jwt
import time


class JWTHandler:
    def is_expired(self, bearer_token: str) -> bool:
        if bearer_token is None:
            return True
        decoded = jwt.decode(bearer_token.replace("Bearer ", ""), options={"verify_signature": False})
        return int(time.time()) > (decoded.get("exp") - 1)


jwt_handler = JWTHandler()
