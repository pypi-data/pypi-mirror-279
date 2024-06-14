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

from __future__ import print_function

import calendar
import getpass
import io
import json
import logging
import os
import os.path
import platform
import random
import re
import string
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile
from datetime import datetime
from typing import AnyStr, Callable, TextIO, Union

from ._jupyter import _in_ipython_environment

if sys.version_info[:2] >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

from urllib.parse import urljoin, urlparse, urlunparse

from requests.models import PreparedRequest

from ._typing import IO, Any, Dict, Generator, List, Optional, Set, Tuple
from .json_encoder import NestedEncoder
from .logging_messages import MISSING_PANDAS_OR_YDATA_PROFILING

LOGGER = logging.getLogger(__name__)
LOG_ONCE_CACHE: Set[str] = set()

AWS_LAMBDA_ENVIRONMENT_MARKER_KEY = "LAMBDA_TASK_ROOT"

if hasattr(time, "monotonic"):
    get_time_monotonic = time.monotonic
else:
    # Python2 just won't have accurate time durations
    # during clock adjustments, like leap year, etc.
    get_time_monotonic = time.time


def log_once_at_level(
    logging_level: int, message: str, *args: Any, **kwargs: Any
) -> None:
    """
    Log the given message once at the given level then at the DEBUG
    level on further calls.

    This is a global log-once-per-session, as opposed to the
    log-once-per-experiment.
    """
    global LOG_ONCE_CACHE

    if message not in LOG_ONCE_CACHE:
        LOG_ONCE_CACHE.add(message)
        LOGGER.log(logging_level, message, *args, **kwargs)
    else:
        LOGGER.debug(message, *args, **kwargs)


def merge_url(url: str, params: Dict[Any, Any]) -> str:
    """
    Given an URL that might have query strings,
    combine with additional query strings.

    Args:
        url - a url string (perhaps with a query string)
        params - a dict of additional query key/values

    Returns: a string
    """
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def url_join(base: str, *parts: Any, **kwargs: Any) -> str:
    """Given a base and url parts (for example [workspace, project, id]) returns a full URL"""
    # TODO: Enforce base to have a scheme and netloc?
    result = base

    for part in parts[:-1]:
        if not part.endswith("/"):
            raise ValueError("Intermediary part not ending with /")

        result = urljoin(result, part)

    result = urljoin(result, parts[-1])

    if kwargs:
        # merge the url with additional query args:
        result = merge_url(result, kwargs)

    return result


def is_iterable(value: Any) -> bool:
    try:
        iter(value)
        return True

    except (TypeError, AttributeError):
        return False


def is_list_like(value: Any) -> bool:
    """Check if the value is a list-like"""
    if is_iterable(value) and not isinstance(value, str):
        return True

    else:
        return False


def to_utf8(str_or_bytes: AnyStr) -> AnyStr:
    if hasattr(str_or_bytes, "decode"):
        return str_or_bytes.decode("utf-8", errors="replace")

    return str_or_bytes


def local_timestamp() -> int:
    """Return a timestamp in a format expected by the backend (milliseconds)"""
    now = datetime.utcnow()
    timestamp_in_seconds = calendar.timegm(now.timetuple()) + (now.microsecond / 1e6)
    return timestamp_milliseconds(timestamp_in_seconds)


def timestamp_milliseconds(timestamp_in_seconds: float) -> int:
    return int(timestamp_in_seconds * 1000)


def wait_for_done(
    check_function: Callable,
    timeout: float,
    progress_callback: Optional[Callable] = None,
    sleep_time: float = 1,
) -> None:
    """Wait up to TIMEOUT seconds for the check function to return True"""
    end_time = time.time() + timeout
    while check_function() is False and time.time() < end_time:
        if progress_callback is not None:
            progress_callback()
        # Wait a max of sleep_time, but keep checking to see if
        # check_function is done. Allows wait_for_empty to end
        # before sleep_time has elapsed:
        end_sleep_time = time.time() + sleep_time
        while check_function() is False and time.time() < end_sleep_time:
            time.sleep(sleep_time / 20.0)


def read_unix_packages(
    package_status_file: str = "/var/lib/dpkg/status",
) -> Optional[List[str]]:
    if os.path.isfile(package_status_file):
        package = None
        os_packages = []
        with open(package_status_file, "rb") as fp:
            for binary_line in fp:
                line = binary_line.decode("utf-8", errors="ignore").strip()
                if line.startswith("Package: "):
                    package = line[9:]
                if line.startswith("Version: "):
                    version = line[9:]
                    if package is not None:
                        os_packages.append((package, version))
                    package = None
        os_packages_list = sorted(
            [("%s=%s" % (package, version)) for (package, version) in os_packages]
        )
        return os_packages_list
    else:
        return None


def write_file_like_to_tmp_file(file_like_object: Union[IO, str], tmpdir) -> str:
    # Copy of `shutil.copyfileobj` with binary / text detection

    buf = file_like_object.read(1)

    tmp_file = tempfile.NamedTemporaryFile(mode="w+b", dir=tmpdir, delete=False)

    encode = False

    # Detect binary/text
    if not isinstance(buf, bytes):
        encode = True
        buf = buf.encode("utf-8")

    tmp_file.write(buf)

    # Main copy loop
    while True:
        buf = file_like_object.read(16 * 1024)

        if not buf:
            break

        if encode:
            buf = buf.encode("utf-8")

        tmp_file.write(buf)

    tmp_file.close()

    return tmp_file.name


ONE_KBYTE = float(1024)
ONE_MBYTE = float(1024 * 1024)
ONE_GBYTE = float(1024 * 1024 * 1024)


def format_bytes(size: float) -> str:
    """
    Given a size in bytes, return a sort string representation.
    """
    if size >= ONE_GBYTE:
        return "%.2f %s" % (size / ONE_GBYTE, "GB")
    elif size >= ONE_MBYTE:
        return "%.2f %s" % (size / ONE_MBYTE, "MB")
    elif size >= ONE_KBYTE:
        return "%.2f %s" % (size / ONE_KBYTE, "KB")
    else:
        return "%d %s" % (size, "bytes")


def get_file_extension(file_path: AnyStr) -> Optional[str]:
    if file_path is None:
        return None

    ext = os.path.splitext(file_path)[1]
    if not ext:
        return None

    # Get rid of the leading "."
    return ext[1::]


def encode_metadata(metadata: Optional[Dict[Any, Any]]) -> Optional[str]:
    if metadata is None:
        return None

    if type(metadata) is not dict:
        LOGGER.info("invalid metadata, expecting dict type", exc_info=True)
        return None

    if metadata == {}:
        return None

    try:
        json_encoded = json.dumps(
            metadata, separators=(",", ":"), sort_keys=True, cls=NestedEncoder
        )
        return json_encoded
    except Exception:
        LOGGER.info("invalid metadata, expecting JSON-encodable object", exc_info=True)
        return None


def get_comet_version() -> str:
    try:
        return importlib_metadata.version("comet_ml")
    except importlib_metadata.PackageNotFoundError:
        return "Please install comet with `pip install comet_ml`"


def get_user() -> str:
    try:
        return getpass.getuser()
    except KeyError:
        # We are in a system with no user, like Docker container with custom UID
        return "unknown"
    except Exception:
        LOGGER.debug(
            "Unknown exception getting the user from the system", exc_info=True
        )
        return "unknown"


def log_asset_folder(
    folder: str, recursive: bool = False, extension_filter: Optional[List[str]] = None
) -> Generator[Tuple[str, str], None, None]:
    extension_filter_set = None

    if extension_filter is not None:
        extension_filter_set = set(extension_filter)

    if recursive:
        for dirpath, _, file_names in os.walk(folder):
            for file_name in file_names:

                if extension_filter_set:
                    file_extension = os.path.splitext(file_name)[1]

                    if file_extension not in extension_filter_set:
                        continue

                file_path = os.path.join(dirpath, file_name)
                yield file_name, file_path
    else:
        file_names = sorted(os.listdir(folder))
        for file_name in file_names:
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):

                if extension_filter_set:
                    file_extension = os.path.splitext(file_name)[1]
                    if file_extension not in extension_filter_set:
                        continue

                yield file_name, file_path


def valid_ui_tabs(
    tab: Optional[str] = None, preferred: bool = False
) -> Union[str, List[str]]:
    """
    List of valid UI tabs in browser.
    """
    mappings = {
        "artifacts": "artifacts",
        "assets": "assets",
        "audio": "audio",
        "charts": "chart",
        "code": "code",
        "confusion-matrices": "confusionMatrix",
        "graphics": "images",
        "histograms": "histograms",
        "installed-packages": "installedPackages",
        "metrics": "metrics",
        "notes": "notes",
        "parameters": "params",
        "system-metrics": "systemMetrics",
        "text": "text",
        "output": "stdout",
        "panels": "panels",
        "graph": "graph",
        "other": "other",
        "html": "html",
    }
    preferred_names = list(mappings.keys())
    # Additional keys:
    mappings.update(
        {
            "assetStorage": "assets",
            "chart": "chart",
            "confusion-matrix": "confusionMatrix",
            "confusionMatrix": "confusionMatrix",
            "images": "images",
            "installedPackages": "installedPackages",
            "params": "params",
            "systemMetrics": "systemMetrics",
            "graph-def": "graph",
            "graph-definition": "graph",
            "stdout": "stdout",
        }
    )
    if preferred:
        return preferred_names
    elif tab is None:
        return list(mappings.keys())
    elif tab in mappings:
        return mappings[tab]
    else:
        raise ValueError("invalid tab name; tab should be in %r" % preferred_names)


def shape(data: Any) -> List[int]:
    """
    Given a nested list or a numpy array,
    return the shape.
    """
    if hasattr(data, "shape"):
        return list(data.shape)
    else:
        try:
            length = len(data)
            return [length] + shape(data[0])
        except TypeError:
            return []


def tensor_length(data: Any) -> int:
    """
    Get the length of a tensor/list.
    """
    if hasattr(data, "shape"):
        return data.shape[0]
    else:
        try:
            length = len(data)
        except TypeError:
            length = 0
    return length


def clean_and_check_root_relative_path(root: str, relative_path: str) -> str:
    """
    Given a root and a relative path, resolve the relative path to get an
    absolute path and make sure the resolved path is a child to root. Cases
    where it could not be the case would be if the `relative_path` contains `..`
    or if one part of the relative path is a symlink going above the root.

    Return the absolute resolved path and raises a ValueError if the root path
    is not absolute or if the resolved relative path goes above the root.
    """
    if not os.path.isabs(root):
        raise ValueError("Root parameter %r should an absolute path" % root)

    if not root.endswith(os.sep):
        root = root + os.sep

    real_root = os.path.realpath(root)

    joined_path = os.path.join(real_root, relative_path)
    resolved_path = os.path.realpath(joined_path)

    if not resolved_path.startswith(real_root):
        raise ValueError("Final path %r is outside of %r" % (resolved_path, real_root))

    return resolved_path


def check_if_path_relative_to_root(root: str, absolute_path: str) -> bool:
    if not os.path.isabs(root):
        raise ValueError("Root parameter %r should an absolute path" % root)

    root_full_path = os.path.realpath(root) + os.sep
    full_path = os.path.realpath(absolute_path)

    return full_path.startswith(root_full_path)


def proper_registry_model_name(name: str) -> str:
    """
    A proper registry model name is:
        * lowercase
        * replaces all non-alphanumeric with dashes
        * removes leading and trailing dashes
        * limited to 1 dash in a row
    """
    name = "".join([(char if char.isalnum() else "-") for char in name])
    while name.startswith("-"):
        name = name[1:]
    while name.endswith("-"):
        name = name[:-1]
    name = name.lower()
    while "--" in name:
        name = name.replace("--", "-")
    return name


def is_interactive() -> bool:
    """
    Returns True if in interactive mode
    """
    return bool(getattr(sys, "ps1", sys.flags.interactive))


def safe_filename(filename: str) -> str:
    """
    Given a value, turn it into a valid filename.

    1. Remove the spaces
    2. Replace anything not alpha, '-', '_', or '.' with '_'
    3. Remove duplicate '_'
    """
    string = str(filename).strip().replace(" ", "_")
    string = re.sub(r"(?u)[^-\w.]", "_", string)
    return re.sub(r"_+", "_", string)


def get_dataframe_profile_html(
    dataframe: Any, minimal: Optional[bool]
) -> Optional[str]:
    """
    Log a pandas dataframe profile.
    """
    dataframe_profiling = _import_dataframe_profiling()

    if dataframe_profiling is None:
        return None

    if minimal:  # earlier versions of pandas_profiling did not support minimal
        profile = dataframe_profiling.ProfileReport(dataframe, minimal=minimal)
    else:
        profile = dataframe_profiling.ProfileReport(dataframe)
    html = profile.to_html()  # type: str
    html = html.replace("http:", "https:")
    return html


def _import_dataframe_profiling():
    """
    Pandas_profiling was deprecated by its creators in favor
    of the ydata_profiling. Comet still supports usage of the old package.
    """
    try:
        import ydata_profiling

        return ydata_profiling
    except ImportError:
        try:
            import pandas_profiling

            return pandas_profiling
        except ImportError:
            LOGGER.warning(MISSING_PANDAS_OR_YDATA_PROFILING, exc_info=True)
            return None


def clean_string(val: str) -> str:
    if val:
        return "".join([char for char in val if char not in ["'", '"', " "]])
    else:
        return ""


def get_api_key_from_user() -> str:
    """
    Get the Comet API key from the user.
    """
    from .config import get_comet_url_override, get_config

    settings = get_config()
    client_url = get_comet_url_override(settings)
    root_url = sanitize_url(get_root_url(client_url))

    print(
        "Please paste your Comet API key from {root_url}api/my/settings/".format(
            root_url=root_url
        )
    )
    print("(api key may not show as you type)")
    api_key = clean_string(getpass.getpass("Comet API key: "))
    return api_key


def parse_remote_uri(uri: Optional[str]) -> Optional[str]:
    if not uri:
        return None

    try:
        parsed = urlparse(uri)
        if parsed.path:
            # Split the path
            return parsed.path.split("/")[-1]
        else:
            return None
    except Exception:
        LOGGER.debug("Failure parsing URI %r", uri, exc_info=True)
        return None


def make_template_filename(group: Optional[str] = None) -> str:
    if group is None:
        group = random.randint(0, 10000000)

    return "template_projector_config-%s.json" % group


class ImmutableDict(dict):
    def _immutable(self, *args, **kws):
        raise TypeError("object is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class IterationProgressCallback(object):
    def __init__(self, iterable, callback, frequency):
        self._iterable = iterable
        self._callback = callback
        self._frequency = frequency

    def __iter__(self):
        last = get_time_monotonic()

        for obj in self._iterable:
            yield obj

            now = get_time_monotonic()
            diff = now - last
            if diff > self._frequency:
                last = now
                try:
                    self._callback()
                except Exception:
                    LOGGER.debug("Error calling the progress callback", exc_info=True)


def generate_guid() -> str:
    """Generate a GUID"""
    return uuid.uuid4().hex


def compact_json_dump(data: Any, fp: TextIO) -> None:
    json.dump(data, fp, sort_keys=True, separators=(",", ":"), cls=NestedEncoder)


def get_root_url(url: str) -> str:
    """Remove the path, params, query and fragment from a given URL"""
    parts = urlparse(url)
    scheme, netloc, path, params, query, fragment = parts

    return urlunparse((scheme, netloc, "", "", "", ""))


def sanitize_url(url: str, ending_slash: bool = True) -> str:
    """Sanitize URL, checking that it is a valid URL and ensure it contains an ending slash / or
    that it doesn't contain an ending slash depending on the value of ending_slash"""
    parts = urlparse(url)
    scheme, netloc, path, params, query, fragment = parts

    # TODO: Raise an exception if params, query and fragment are not empty?

    # Ensure the leading slash
    if ending_slash is True:
        if path and not path.endswith("/"):
            path = path + "/"
        elif not path and not netloc.endswith("/"):
            netloc = netloc + "/"
    else:
        if path and path.endswith("/"):
            path = path[:-1]

    return urlunparse((scheme, netloc, path, params, query, fragment))


def metric_name(name: str, prefix: Optional[str] = None) -> str:
    if prefix:
        return "%s.%s" % (prefix, name)
    else:
        return name


def subprocess_run_and_check(
    args: List[str],
    timeout: int,
    exception_warning_log_message: str,
    return_code_warning_log_message: str,
) -> Optional[bytes]:
    """Run the command passed as a List of string with the given timeout (ignored on Python 2.7).

    If the command ran but it's exit code is not 0, show the return_code_warning_log_message as a
    Warning log, logs the stdout/stderr in debug logs and return None.

    If any other error occurs, show the exception_warning_log_message as a Warning log and return
    None.
    """
    try:
        completed_process = subprocess.run(
            args,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except Exception:
        LOGGER.warning(exception_warning_log_message, exc_info=True)
        return None

    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as exception:
        LOGGER.warning(return_code_warning_log_message, exc_info=True)
        LOGGER.debug("Conda env export stdout: %r", exception.output)
        LOGGER.debug("Conda env export stderr: %r", exception.stderr)
        return None
    except Exception:
        LOGGER.warning(exception_warning_log_message, exc_info=True)
        return None

    return completed_process.stdout


def tag_experiment_with_commit_number(experiment):
    if sys.version_info.major == 3:
        commit = subprocess.check_output(
            "git rev-parse HEAD", shell=True, universal_newlines=True
        ).strip()
    else:
        commit = subprocess.check_output("git rev-parse HEAD", shell=True).strip()

    commit = commit[:8]
    experiment.add_tag(commit)


def tag_experiment_with_transport_layer_identifier(experiment):
    """Adds to the experiment TAG with transport layer identifier taken from environment"""
    experiment.add_tag("HTTP: %r" % True)


def is_aws_lambda_environment() -> bool:
    """Allows to check if we are executing in AWS lambda environment"""
    return AWS_LAMBDA_ENVIRONMENT_MARKER_KEY in os.environ


def find_logger_spec(logger_spec: str) -> str:
    if is_aws_lambda_environment():
        return "simple"

    if logger_spec == "default":
        if _in_ipython_environment():
            logger_spec = "simple"
        # MacOS default start mode is now spawn and fork is unsafe https://bugs.python.org/issue33725
        elif platform.system() == "Darwin":
            logger_spec = "simple"
        else:
            logger_spec = "native"
    else:
        logger_spec = logger_spec or None  # in case of ""

    return logger_spec


def optional_update(destination: Dict[str, Any], source: Dict[str, Any]) -> None:
    """
    the equivalent of destination.update(source),
    except that if a (key, value) pair in source is None,
    then this key is skipped.

    this essentially automates the pattern:
    if variable is not None:
        destination["variable"] = variable
    """
    for key, value in source.items():
        if value is not None:
            destination[key] = value


def read_git_patch_zip(patch_data: bytes) -> bytes:
    zip_patch = io.BytesIO(patch_data)
    archive = zipfile.ZipFile(zip_patch)
    return archive.read("git_diff.patch")


def random_ascii_string(length: int = 6) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))
