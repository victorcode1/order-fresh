import os
from pathlib import Path


ENV_PATH = Path(__file__).resolve().with_name(".env")


def load_env_file() -> None:
    if not ENV_PATH.exists():
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
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


def _get_required_env(name: str) -> str:
    load_env_file()
    value = os.getenv(name)
    if value:
        return value

    raise RuntimeError(f"No se encontro {name} en el entorno o en .env")


def get_location_id() -> str:
    return _get_required_env("FRESH_KDS_LOCATION_ID")


def get_device_id() -> str:
    return _get_required_env("FRESH_KDS_DEVICE_ID")


def set_env_values(values: dict[str, str]) -> None:
    load_env_file()
    existing_lines: list[str] = []
    if ENV_PATH.exists():
        existing_lines = ENV_PATH.read_text(encoding="utf-8").splitlines()

    remaining = dict(values)
    updated_lines: list[str] = []

    for line in existing_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            updated_lines.append(line)
            continue

        key, _ = line.split("=", 1)
        normalized_key = key.strip()
        if normalized_key in remaining:
            updated_lines.append(f"{normalized_key}={remaining.pop(normalized_key)}")
        else:
            updated_lines.append(line)

    if remaining:
        if updated_lines and updated_lines[-1].strip():
            updated_lines.append("")
        for key, value in remaining.items():
            updated_lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    for key, value in values.items():
        os.environ[key] = value