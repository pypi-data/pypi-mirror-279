import logging
from pathlib import Path

import user_agents
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from duckdb.typing import BLOB
from duckdb.typing import UUID as DuckDBUUID

from . import uuid_utils

logger = logging.getLogger(__name__)


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
