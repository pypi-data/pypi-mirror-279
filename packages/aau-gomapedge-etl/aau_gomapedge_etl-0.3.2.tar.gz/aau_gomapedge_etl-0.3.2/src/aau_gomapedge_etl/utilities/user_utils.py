import logging
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import user_agents
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from duckdb.typing import BLOB
from duckdb.typing import UUID as DuckDBUUID

from . import uuid_utils

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class User:
    id: UUID
    data_dir: Path


def get_users_from_sqlite(con: DuckDBPyConnection, db: Path) -> DuckDBPyRelation:
    function_name = "to_uuid"
    con.create_function(function_name, uuid_utils.to_uuid, [BLOB], DuckDBUUID).execute(
        "set global sqlite_all_varchar = True"
    )
    user_tbl = con.query(
        """
SELECT to_uuid(encode(id)) AS id,
       epoch_ms(creation_time::BIGINT * 1000) AS creation_time,
       user_agent
FROM sqlite_scan($path, users);
""",
        params={"path": db.as_posix()},
    )
    con.remove_function(function_name)
    return user_tbl


def get_users_from_filesystem(root: Path, user_tbl: DuckDBPyRelation) -> list[User]:
    root.stat().st_atime

    user_ids: list[tuple[UUID]] = user_tbl.select("id").fetchall()
    user_lookup: set[UUID] = set(cols[0] for cols in user_ids)
    users: list[User] = []

    for directory in filter(lambda p: p.is_dir(), root.iterdir()):
        user_id = uuid_utils.parse_uuid(directory.name)
        if not user_id:
            continue

        if user_id not in user_lookup:
            logger.warning(
                f"User '{user_id}' found in filesystem but not in the user database"
            )
            continue
        users.append(User(user_id, directory))

    return users


def parse_user_agent(value: str) -> dict[str, str]:
    user_agent = user_agents.parse(value)
    return {
        "browser_family": user_agent.browser.family,
        "browser_version": user_agent.browser.version_string,
        "os_family": user_agent.os.family,
        "os_version": user_agent.os.version_string,
        "device_family": user_agent.device.family,
        "device_brand": user_agent.device.brand,
        "device_model": user_agent.device.model,
    }
