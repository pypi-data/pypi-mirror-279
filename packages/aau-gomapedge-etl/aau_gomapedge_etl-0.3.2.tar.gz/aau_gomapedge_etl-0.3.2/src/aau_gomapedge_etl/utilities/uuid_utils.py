from uuid import UUID


def parse_uuid(uuid: str) -> UUID | None:
    try:
        uuid_obj = UUID(uuid)
    except ValueError:
        return None
    return uuid_obj if uuid_obj.hex == uuid else None


def to_uuid(value: bytes) -> UUID:
    return UUID(bytes=value)
