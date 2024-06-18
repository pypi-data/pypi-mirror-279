# Allows you to use _tdxlwings.reports instead of _tdxlwings.pro.reports

from .pro.reports import *  # noqa: F401,F403

__all__ = (  # noqa: F405
    "render_template",
    "create_report",
    "Image",
    "Markdown",
    "MarkdownStyle",
    "formatter",
)
