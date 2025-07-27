"""ID generation utilities."""

import uuid6


def generate_uuidv7() -> str:
    """Generate a UUIDv7 string."""
    return str(uuid6.uuid7())


generate_pg_uuid = generate_uuidv7
