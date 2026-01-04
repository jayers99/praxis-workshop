"""Slug generation utilities."""

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug.

    - Converts to lowercase
    - Replaces spaces and underscores with hyphens
    - Removes non-alphanumeric characters (except hyphens)
    - Collapses multiple hyphens
    - Strips leading/trailing hyphens

    Args:
        text: Text to slugify.

    Returns:
        URL-safe slug.
    """
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    text = text.lower()

    # Remove file extension if present
    if "." in text:
        text = text.rsplit(".", 1)[0]

    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)

    # Remove non-alphanumeric characters (except hyphens)
    text = re.sub(r"[^a-z0-9-]", "", text)

    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    return text
