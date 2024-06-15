from sqlmodel import Field, Session, create_engine, select

from systema.base import BaseModel, CreatedAtMixin, IdMixin, UpdatedAtMixin


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel, IdMixin):
    username: str = Field(..., unique=True)
    active: bool = True
    superuser: bool = False


class User(
    UserBase,
    CreatedAtMixin,
    UpdatedAtMixin,
    table=True,
):
    hashed_password: str

    @classmethod
    def get_superuser(cls):
        from systema.management import Settings

        engine = create_engine(Settings().db_address)
        with Session(engine) as session:
            statement = select(cls).where(cls.superuser)
            return session.exec(statement).one()
