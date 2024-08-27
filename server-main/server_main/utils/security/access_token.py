from __future__ import annotations
import jwt
import uuid
from pydantic import BaseModel
from result import Ok, Err, Result
from datetime import datetime, timedelta, timezone
from server_main.settings import settings


class AccessToken(BaseModel):
    iat: int
    exp: int
    usrid: uuid.UUID
    usrcat: int

    @staticmethod
    def new(user_id: uuid.UUID, user_created_at: datetime) -> AccessToken:
        dt_now: datetime = datetime.now(timezone.utc)
        iat: int = int(dt_now.timestamp())
        exp: int = int(
            (dt_now + timedelta(seconds=settings.access_token_expire)).timestamp()
        )

        return AccessToken(
            iat=iat,
            exp=exp,
            usrid=user_id,
            usrcat=int(user_created_at.timestamp()),
        )

    @staticmethod
    def decode(token: str) -> Result[AccessToken, str]:
        try:
            payload: dict = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            try:
                iat = int(payload["iat"])
                exp = int(payload["exp"])
                usrid = uuid.UUID(payload["usrid"])
                usrcat = int(payload["usrcat"])
                return Ok(AccessToken(iat=iat, exp=exp, usrid=usrid, usrcat=usrcat))
            except KeyError:
                return Err("INVALID_TOKEN")
            except ValueError:
                return Err("INVALID_TOKEN")
        except jwt.exceptions.PyJWTError:
            return Err("INVALID_TOKEN")

    def encode(self) -> str:
        return jwt.encode(
            {
                "iat": self.iat,
                "exp": self.exp,
                "usrid": str(self.usrid),
                "usrcat": self.usrcat,
            },
            settings.secret_key,
            algorithm="HS256",
        )
