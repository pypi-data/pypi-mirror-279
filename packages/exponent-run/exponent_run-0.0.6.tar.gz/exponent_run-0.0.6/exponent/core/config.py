import json
import logging
import os
from functools import lru_cache
from importlib.metadata import Distribution, PackageNotFoundError

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# If the package is editable, we want to use:
# base_url = localhost:3000
# base_api_url = localhost:8000


def is_editable_install() -> bool:
    if os.getenv("ENVIRONMENT") == "test":
        # We should explicitly set these variables
        # in test when needed
        return False

    try:
        dist = Distribution.from_name("exponent-run")
    except PackageNotFoundError:
        logger.info("No distribution info found for exponent-run")
        return False

    direct_url = dist.read_text("direct_url.json")
    if not direct_url:
        return False

    try:
        direct_url_json = json.loads(direct_url)
    except json.JSONDecodeError:
        logger.warning("Failed to decode distribution info for exponent-run")
        return False

    pkg_is_editable = direct_url_json.get("dir_info", {}).get("editable", False)
    return bool(pkg_is_editable)


class Settings(BaseSettings):
    base_url: str = "https://exponent.run"
    base_api_url: str = "https://api.exponent.run"
    api_key: str | None = None
    log_level: str = "WARNING"

    model_config = SettingsConfigDict(
        env_prefix="EXPONENT_",
        env_file=os.path.expanduser("~/.exponent"),
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings(use_prod: bool = False, use_staging: bool = False) -> Settings:
    if is_editable_install() and not (use_prod or use_staging):
        base_url = "http://localhost:3000"
        base_api_url = "http://localhost:8000"
    elif use_staging:
        # TODO: Change this to a real staging URL?
        base_url = "https://exponent.run"
        base_api_url = "https://staging-api.exponent.run"
    else:
        base_url = "https://exponent.run"
        base_api_url = "https://api.exponent.run"

    return Settings(base_url=base_url, base_api_url=base_api_url)
