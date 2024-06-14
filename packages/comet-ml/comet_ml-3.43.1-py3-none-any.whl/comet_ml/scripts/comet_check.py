#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import argparse
import importlib
import logging
import os
import sys
from urllib import request

from comet_ml._typing import Any, List, Optional
from comet_ml.config import (
    COMET_URL_OVERRIDE_CONFIG_KEY,
    Config,
    ConfigDictEnv,
    ConfigEnvFileEnv,
    ConfigIniEnv,
    ConfigOSEnv,
    get_check_tls_certificate,
    get_comet_url_override,
    get_config,
)
from comet_ml.connection import (
    _comet_version,
    _debug_proxy_for_http,
    get_optimizer_address,
    get_root_url,
    sanitize_url,
)
from comet_ml.connection_helpers import get_http_session
from comet_ml.connection_url_helpers import get_run_id_url
from comet_ml.utils import local_timestamp, url_join

LOGGER = logging.getLogger("comet_ml")
ADDITIONAL_ARGS = False

DELIMITERS_LENGTH = 80

REQUESTS_CA_BUNDLE = "REQUESTS_CA_BUNDLE"
CURL_CA_BUNDLE = "CURL_CA_BUNDLE"
WEBSOCKET_CLIENT_CA_BUNDLE = "WEBSOCKET_CLIENT_CA_BUNDLE"


def activate_debug():
    # activate debug logging
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.root.setLevel(logging.DEBUG)
    for h in LOGGER.handlers:
        if isinstance(h, logging.StreamHandler):
            if hasattr(h.formatter, "hide_traceback"):
                h.formatter.hide_traceback = False
            h.setLevel(logging.DEBUG)

    # Activate requests low-level request logging
    import http.client as http_client

    http_client.HTTPConnection.debuglevel = 5


def check_server_connection(server_address, verify_tls):
    url = get_run_id_url(server_address)
    try:
        with get_http_session(verify_tls=verify_tls) as session:
            payload = {
                "apiKey": "XXX",
                "local_timestamp": local_timestamp(),
                "experimentKey": "YYY",
                "offline": False,
                "projectName": None,
                "teamName": None,
                "libVersion": _comet_version(),
            }
            headers = {"Content-Type": "application/json;charset=utf-8"}
            session.post(url, data=payload, headers=headers)
            return True
    except Exception:
        LOGGER.error("Error checking server connectivity", exc_info=True)
        return False


def check_rest_api_connection(rest_api_url, verify_tls):
    url = url_join(rest_api_url, "account-details")
    try:
        with get_http_session(verify_tls=verify_tls) as session:
            session.get(url)
            return True
    except Exception:
        LOGGER.error("Error checking rest api connectivity", exc_info=True)
        return False


def check_optimizer_connection(optimizer_url, verify_tls):
    url = url_join(optimizer_url, "spec")
    try:
        with get_http_session(verify_tls=verify_tls) as session:
            params = {"algorithmName": "bayes"}
            session.get(url, params=params)
            return True
    except Exception:
        LOGGER.error("Error checking optimizer connectivity", exc_info=True)
        return False


def config_source(env):
    # type: (Any) -> Optional[str]
    if isinstance(env, ConfigOSEnv):
        return "environment variable"
    elif isinstance(env, ConfigEnvFileEnv):
        return "environment file %r" % env.path
    elif isinstance(env, ConfigIniEnv):
        return "INI file %r" % env.path
    elif isinstance(env, ConfigDictEnv):
        return "backend overriden values"
    else:
        LOGGER.debug("Unknown env class %r", env)
        return None


def check(args):
    # Called via `comet upload EXP.zip`
    if args.debug:
        activate_debug()

    config = get_config()
    verify_tls = get_check_tls_certificate(config)

    LOGGER.info("Comet Check")
    LOGGER.info("=" * DELIMITERS_LENGTH)
    print("")

    LOGGER.info("Checking connectivity to server...")
    print("")

    # Clientlib
    server_address = sanitize_url(get_comet_url_override(config))
    server_address_config_origin = config_source(
        config.get_config_origin(COMET_URL_OVERRIDE_CONFIG_KEY)
    )
    LOGGER.info("Configured server address %r", server_address)
    if server_address_config_origin and config.comet_url_override is None:
        LOGGER.info("Server address was configured in %s", server_address_config_origin)
    else:
        LOGGER.info("Server address is the default one")
    print("")
    server_connected = check_server_connection(server_address, verify_tls)
    print("")
    if server_connected:
        LOGGER.info("Server connection is ok")
    else:
        LOGGER.warning("Server connection is not ok")

    print("")

    # Rest API
    LOGGER.info("=" * DELIMITERS_LENGTH)
    LOGGER.info("Checking connectivity to Rest API...")
    LOGGER.info("=" * DELIMITERS_LENGTH)

    root_url = sanitize_url(get_root_url(get_comet_url_override(config)))
    rest_api_url = url_join(root_url, *["api/rest/", "v2" + "/"])
    LOGGER.info("Configured Rest API address %r", rest_api_url)
    if server_address_config_origin:
        LOGGER.info(
            "Rest API address was configured in %s", server_address_config_origin
        )
    else:
        LOGGER.info("Rest API address is the default one")
    print("")
    rest_api_connected = check_rest_api_connection(rest_api_url, verify_tls)
    print("")
    if rest_api_connected:
        LOGGER.info("REST API connection is ok")
    else:
        LOGGER.warning("REST API connection is not ok")

    print("")

    # Optimizer
    LOGGER.info("=" * DELIMITERS_LENGTH)
    LOGGER.info("Checking connectivity to Optimizer Server")
    LOGGER.info("=" * DELIMITERS_LENGTH)

    optimizer_url = get_optimizer_address(config)
    optimizer_url_config_origin = config_source(
        config.get_config_origin("comet.optimizer_url")
    )
    LOGGER.info(
        "Configured Optimizer address %r",
        optimizer_url,
    )
    if optimizer_url_config_origin:
        LOGGER.info(
            "Optimizer address was configured in %s", optimizer_url_config_origin
        )
    else:
        LOGGER.info("Optimizer address is the default one")
    print("")
    optimizer_connected = check_optimizer_connection(optimizer_url, verify_tls)
    print("")
    if optimizer_connected:
        LOGGER.info("Optimizer connection is ok")
    else:
        LOGGER.warning("Optimizer connection is not ok")

    print("")

    log_system_info()
    log_modules_info(["requests", "urllib3"])
    log_system_proxies_info()
    log_proxies_info_for_urls(http_urls=[server_address, rest_api_url])
    log_tls_verification(config)
    log_ca_bundles_paths()

    print("")
    print("")

    LOGGER.info("Summary")
    LOGGER.info("-" * DELIMITERS_LENGTH)
    LOGGER.info("Server connectivity\t\t\t%s", server_connected)
    LOGGER.info("Rest API connectivity\t\t%r", rest_api_connected)
    LOGGER.info("Optimizer server connectivity\t%r", optimizer_connected)


def get_parser_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--debug",
        help="Activate the raw HTTP logs and be more verbose in general",
        action="store_const",
        const=True,
        default=False,
    )


def log_system_info() -> None:
    """Collects and logs the system information such as: Python version, platform, executable path"""
    LOGGER.info("=" * DELIMITERS_LENGTH)
    LOGGER.info("System Information")
    LOGGER.info("=" * DELIMITERS_LENGTH)
    LOGGER.info("Python %s on %s\n%s", sys.version, sys.platform, sys.executable)


def log_modules_info(mod_names: List[str]) -> None:
    """Collects and logs information about specific modules"""
    for mod_name in mod_names:
        try:
            mod = importlib.import_module(mod_name)
            LOGGER.info("%s\tv%s", mod_name, mod.__version__)
        except Exception:
            LOGGER.error("Module %s not found" % mod_name, exc_info=True)


def log_system_proxies_info() -> None:
    """Collects and logs information about registered system proxies"""
    proxies = request.getproxies()
    if proxies:
        LOGGER.info("-" * DELIMITERS_LENGTH)
        LOGGER.info("System Proxies Information")
        LOGGER.info("-" * DELIMITERS_LENGTH)
        for schema, server in proxies.items():
            LOGGER.info("%s: %s", schema, server)
    else:
        LOGGER.info("-" * DELIMITERS_LENGTH)
        LOGGER.info("No system proxies registered")

    LOGGER.info("-" * DELIMITERS_LENGTH)


def log_proxies_info_for_urls(http_urls: List[str]) -> None:
    # Log HTTP proxy info
    for url in http_urls:
        try:
            proxy = _debug_proxy_for_http(url)
            log_proxy_info_for_url(url, proxy)
        except Exception:
            LOGGER.error("Failed to check proxy for URL: %s", url, exc_info=True)


def log_proxy_info_for_url(url: str, proxy: Optional[str]) -> None:
    """Collects and logs information about proxies which proxy access to the specified list of URLs"""
    if proxy:
        LOGGER.info(
            "%s -> %s",
            url,
            proxy,
        )
    else:
        LOGGER.info("%s -> NO PROXY", url)


def log_tls_verification(config: Config) -> None:
    LOGGER.info("-" * DELIMITERS_LENGTH)
    tls_verification = get_check_tls_certificate(config)

    if tls_verification:
        LOGGER.info("TLS Certificate verification is ENABLED")
    else:
        LOGGER.info("TLS Certification verification is DISABLED")


def log_ca_bundles_paths() -> None:
    LOGGER.info("=" * DELIMITERS_LENGTH)
    LOGGER.info("HTTP CA bundle paths")
    LOGGER.info("-" * DELIMITERS_LENGTH)
    if os.environ.get(REQUESTS_CA_BUNDLE) or os.environ.get(CURL_CA_BUNDLE):
        LOGGER.info("%s: %s", REQUESTS_CA_BUNDLE, os.environ.get(REQUESTS_CA_BUNDLE))
        LOGGER.info("%s: %s", CURL_CA_BUNDLE, os.environ.get(CURL_CA_BUNDLE))
    else:
        LOGGER.info("requests is using the default CA bundle")

    if WEBSOCKET_CLIENT_CA_BUNDLE in os.environ:
        LOGGER.info("=" * DELIMITERS_LENGTH)
        LOGGER.info("WebSocket CA bundle paths")
        LOGGER.info("-" * DELIMITERS_LENGTH)
        LOGGER.info(os.environ[WEBSOCKET_CLIENT_CA_BUNDLE])


def main(args):
    # Called via `comet check`
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    get_parser_arguments(parser)
    parsed_args = parser.parse_args(args)

    check(parsed_args)


if __name__ == "__main__":
    # Called via python -m comet_ml.scripts.comet_check
    main(sys.argv[1:])
