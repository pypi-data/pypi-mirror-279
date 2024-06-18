"""Tests for interactors.retrieve module."""
from bacore.domain import settings
from bacore.interactors import retrieve, update


def test_secret_from_keyring():
    """Test update keyring secret."""
    key = settings.Keyring(service_name="test_bacore", secret_name="bacore_user", secret=settings.SecretStr("bacore_pass"))
    secret = update.secret_from_keyring(key=key)
    assert secret.get_secret_value() == retrieve.secret_from_keyring(key=key).get_secret_value()

