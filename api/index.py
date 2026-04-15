from __future__ import annotations

"""Vercel entrypoint: expose the Flask `app` for the Python runtime.

This file is intentionally tiny — Vercel's Python builder will import
`app` from this module as the WSGI application.
"""

from main import app


if __name__ == "__main__":
    # Local run helper
    app.run(host="0.0.0.0", port=8000)
