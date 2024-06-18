#!/usr/bin/env python
import logging
from pathlib import Path

from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_model"
base_dir = Path(__file__).absolute().parent

project_settings = DefaultTestSettings(
    APP_NAME="edc_model",
    BASE_DIR=base_dir,
    ETC_DIR=str(base_dir / app_name / "tests" / "etc"),
    KEY_PATH=str(base_dir / app_name / "tests" / "etc"),
    ALLOWED_HOSTS=["localhost"],
    ROOT_URLCONF=f"{app_name}.tests.urls",
    STATIC_URL="/static/",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "multisite",
        "django_crypto_fields.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_model.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
).settings


def main():
    func_main(project_settings, *[f"{app_name}.tests"])


if __name__ == "__main__":
    logging.basicConfig()
    main()
