"""Collection of Vault API endpoint classes."""
from hvac_ikame.api.auth_methods import AuthMethods
from hvac_ikame.api.secrets_engines import SecretsEngines
from hvac_ikame.api.system_backend import SystemBackend
from hvac_ikame.api.vault_api_base import VaultApiBase
from hvac_ikame.api.vault_api_category import VaultApiCategory

__all__ = (
    "AuthMethods",
    "SecretsEngines",
    "SystemBackend",
    "VaultApiBase",
    "VaultApiCategory",
)
