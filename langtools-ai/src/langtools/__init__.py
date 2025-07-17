"""Langtools package namespace."""

from __future__ import annotations

from typing import cast

import pkgutil

__path__ = cast(list[str], pkgutil.extend_path(__path__, __name__))
