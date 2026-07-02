# # Settings
# from __future__ import annotations

# import os
# from dataclasses import dataclass
# from dotenv import load_dotenv

# load_dotenv()


# @dataclass(frozen=True)
# class Settings:
#     """
#     Central application settings.

#     This file is the single source of truth for:
#     - model provider config
#     - tool API keys
#     - app environment
#     - logging level

#     Later, every module will import settings from here instead of reading env vars directly.
#     """

#     app_env: str = os.getenv("APP_ENV", "development")
#     log_level: str = os.getenv("LOG_LEVEL", "INFO")

#     gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
#     gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

#     virustotal_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "")
#     abuseipdb_api_key: str = os.getenv("ABUSEIPDB_API_KEY", "")
#     urlscan_api_key: str = os.getenv("URLSCAN_API_KEY", "")
#     nvd_api_key: str = os.getenv("NVD_API_KEY", "")
#     misp_url: str = os.getenv("MISP_URL", "")
#     misp_api_key: str = os.getenv("MISP_API_KEY", "")

#     def has_gemini(self) -> bool:
#         return bool(self.gemini_api_key)

#     def has_virustotal(self) -> bool:
#         return bool(self.virustotal_api_key)

#     def has_abuseipdb(self) -> bool:
#         return bool(self.abuseipdb_api_key)

#     def has_urlscan(self) -> bool:
#         return bool(self.urlscan_api_key)

#     def has_nvd(self) -> bool:
#         return bool(self.nvd_api_key)

#     def has_misp(self) -> bool:
#         return bool(self.misp_url and self.misp_api_key)


# settings = Settings()


from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the whole project.

    This file is the single source of truth for:
    - model keys
    - model names
    - storage locations
    - future security tool keys

    Every module should import settings from here instead of reading env vars directly.
    """

    # Project root and storage paths
    project_root: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    storage_dir: Path = Path(__file__).resolve().parents[2] / "storage"
    uploads_dir: Path = Path(__file__).resolve().parents[2] / "data" / "uploads"
    vectorstore_dir: Path = Path(__file__).resolve().parents[2] / "storage" / "vectorstore"
    checkpoints_dir: Path = Path(__file__).resolve().parents[2] / "storage" / "checkpoints"
    cache_dir: Path = Path(__file__).resolve().parents[2] / "storage" / "cache"

    # App behavior
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Gemini / Google API
    google_api_key: str = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Future cybersecurity tools
    virustotal_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "")
    abuseipdb_api_key: str = os.getenv("ABUSEIPDB_API_KEY", "")
    urlscan_api_key: str = os.getenv("URLSCAN_API_KEY", "")
    nvd_api_key: str = os.getenv("NVD_API_KEY", "")
    misp_url: str = os.getenv("MISP_URL", "")
    misp_api_key: str = os.getenv("MISP_API_KEY", "")

    def has_google_api_key(self) -> bool:
        return bool(self.google_api_key)

    def has_virustotal(self) -> bool:
        return bool(self.virustotal_api_key)

    def has_abuseipdb(self) -> bool:
        return bool(self.abuseipdb_api_key)

    def has_urlscan(self) -> bool:
        return bool(self.urlscan_api_key)

    def has_nvd(self) -> bool:
        return bool(self.nvd_api_key)

    def has_misp(self) -> bool:
        return bool(self.misp_url and self.misp_api_key)


settings = Settings()