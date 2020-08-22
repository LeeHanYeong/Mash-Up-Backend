import importlib
import os

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
SETTINGS_MODULE_CASES = [
    {
        "keys": [
            None,
            "config.settings",
            "config.settings.local",
            "config.settings.dev",
        ],
        "module": "config.wsgi.dev",
    },
    {"keys": ["config.settings.production"], "module": "config.wsgi.production",},
]

for case in SETTINGS_MODULE_CASES:
    if SETTINGS_MODULE in case["keys"]:
        globals().update(importlib.import_module(case["module"]).__dict__)
