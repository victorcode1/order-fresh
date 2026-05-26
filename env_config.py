import os
from pathlib import Path


def load_env_file() -> None:
    env_path = Path(__file__).resolve().with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_integration_token() -> str:
    load_env_file()
    token = os.getenv("X_INTEGRATION_TOKEN") or os.getenv("FRESH_KDS_API_KEY")
    if token:
        return token

    raise RuntimeError(
        "No se encontro X_INTEGRATION_TOKEN ni FRESH_KDS_API_KEY en el entorno o en .env"
    )