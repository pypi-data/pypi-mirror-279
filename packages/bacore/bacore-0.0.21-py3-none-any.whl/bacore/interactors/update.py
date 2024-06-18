
"""Set functionality module."""
import keyring
import subprocess as sup
from bacore.domain import settings
from pathlib import Path
from pydantic import SecretStr, validate_call


@validate_call
def git_repository(repo: Path, remote: str, commit_msg: str, branch: str = "main", rebase: bool = False) -> None:
    """Push latest changes in repository to remote.

    All the current edits are added and committed with the specified commit message.

    Args:
      repo: Path to the repository
      remote: Remote repository
      commit_msg: The commit message for the commit.
      branch: Branch to commit. Defaults to "master".
      rebase: If rebasing should be done when pulling. Default is False.
    """
    sup.run(["git", "-C", repo, "add", "-A"])
    sup.run(["git", "-C", repo, "commit", "-m", commit_msg])
    if rebase:
        sup.run(["git", "-C", repo, "pull", "--rebase"])
    sup.run(["git", "-C", repo, "push", remote, branch])


def secret_from_keyring(key: settings.Keyring) -> SecretStr:
    if key.secret is not None:
        try:
            keyring.set_password(service_name=key.service_name, username=key.secret_name, password=key.secret.get_secret_value())
        except Exception as e:
            raise Exception("Unable to set secret") from e
    else:
        raise ValueError("Value must be provided for secret.")
    return key.secret

