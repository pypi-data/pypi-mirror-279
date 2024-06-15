#!/usr/bin/env python3
# This file is a part of marzer/check-symbols and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/check-symbols/blob/main/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

"""
Constants for various key paths.
"""

import tempfile
from pathlib import Path

PACKAGE = Path(Path(__file__).resolve().parent)
"""The root directory of the package installation."""

SRC = Path(PACKAGE, r'..').resolve()
"""The root directory of repository's package sources."""

REPOSITORY = Path(SRC, r'..').resolve()
"""The root directory of the repository."""

TEMP = Path(tempfile.gettempdir(), r'marzer', r'check-symbols')
"""A global temp directory shared by all instances of check-symbols."""

VERSION_TXT = PACKAGE / r'version.txt'
"""The version file, version.txt."""
