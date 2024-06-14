import dataclasses
import typing as t
import uuid

import jose.jwt

import mantik.authentication as authentication
import mantik.utils as utils
import mantik.utils.mantik_api.connection

UNICORE_USERNAME_ENV_VAR = "MANTIK_UNICORE_USERNAME"
UNICORE_PASSWORD_ENV_VAR = "MANTIK_UNICORE_PASSWORD"
FIRECREST_CLIENT_ID_ENV_VAR = "MANTIK_FIRECREST_CLIENT_ID"
FIRECREST_CLIENT_SECRET_ENV_VAR = "MANTIK_FIRECREST_CLIENT_SECRET"


@dataclasses.dataclass
class HpcRestApi:
    username: str
    password: str

    @classmethod
    def from_unicore_env_vars(
        cls,
        connection_id: t.Optional[uuid.UUID] = None,
    ) -> "HpcRestApi":
        if connection_id:
            return cls._credentials_from_api(connection_id=connection_id)
        return cls._credentials_from_env_vars(
            username_env_var=UNICORE_USERNAME_ENV_VAR,
            password_env_var=UNICORE_PASSWORD_ENV_VAR,
        )

    @classmethod
    def from_firecrest_env_vars(
        cls,
        connection_id: t.Optional[uuid.UUID] = None,
    ) -> "HpcRestApi":
        if connection_id:
            return cls._credentials_from_api(connection_id=connection_id)
        return cls._credentials_from_env_vars(
            username_env_var=FIRECREST_CLIENT_ID_ENV_VAR,
            password_env_var=FIRECREST_CLIENT_SECRET_ENV_VAR,
        )

    @classmethod
    def _credentials_from_api(
        cls,
        connection_id: uuid.UUID,
    ) -> "HpcRestApi":
        access_token = authentication.auth.get_valid_access_token()
        user_id = _get_sub_from_token(access_token)
        connection = mantik.utils.mantik_api.connection.get(
            user_id=uuid.UUID(user_id),
            connection_id=connection_id,
            token=access_token,
        )
        return cls(username=connection.login_name, password=connection.password)

    @classmethod
    def _credentials_from_env_vars(
        cls, username_env_var: str, password_env_var: str
    ) -> "HpcRestApi":
        username = utils.env.get_required_env_var(username_env_var)
        password = utils.env.get_required_env_var(password_env_var)
        return cls(username=username, password=password)


def _get_sub_from_token(token: str):
    # The `sub` field of the token claims contains the user UUID.
    return jose.jwt.get_unverified_claims(token)["sub"]
