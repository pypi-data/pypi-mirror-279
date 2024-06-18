"""Retrieve Functionality Module (the "get" word feels overloaded)."""
import keyring
import platform
from bacore.domain import settings
from pydantic import SecretStr
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsRetrieveDict(Protocol):
    """Protocol for retrieval of file content as dict."""

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        ...


def file_as_dict(file: SupportsRetrieveDict) -> dict:
    """Content as dictionary."""
    return file.data_to_dict()


def secret_from_keyring(key: settings.Keyring) -> SecretStr:
    """Retrieve secret from keyring."""
    try:
        secret = keyring.get_password(service_name=key.service_name, username=key.secret_name)
    except Exception as e:
        raise Exception("Unable to get secret") from e
    if secret is None:
        raise Exception(f"Secret for service '{key.service_name}' and secret '{key.secret_name}' is None")
    return SecretStr(secret)


def system_information_os(func_os: callable = platform.system()) -> settings.System:
    """Retrieve system information."""
    information = settings.System(os=func_os)
    return information


