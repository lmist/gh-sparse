"""Define Types required by this script."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from result import Err, Ok
from pydantic import SecretStr, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


# these are cli cmds atgs
class GitHubSettings:
    # gh info
    user: str = 'whoislou'
    repo: str = 'full-stack-api-template'
    tree: str = 'tree'
    branch: str = 'master'
    directory: str = 'backend'
    files: str


# Define the type of the path to the configuration file
ConfigFilePath = Annotated[Path, Field(exists=True, readable=True, writable=False)]


class GlobalSettings(BaseSettings):
    """
    Describes the global settings of the application.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # when no default value is assigned in the constructor, this value is read from env file
    github_secret: SecretStr

    gh: GitHubSettings = GitHubSettings()


@lru_cache
def get_settings(envfile: Path):
    if not envfile.exists():
        raise FileNotFoundError(f'Could not find the file {envfile}')
    try:
        config_candidate = GlobalSettings(_env_file=envfile, _env_file_encoding='utf-8')
        return Ok(config_candidate)
    # Please don't raise from internal funcs, return the error instead, like this:
    except ValidationError as exc:
        return Err(exc)
