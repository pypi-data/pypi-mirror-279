import uuid
from datetime import datetime, timezone
from typing import List

def generate_hash() -> str:
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()

def make_instance_id(machine_id: str, service_id: str) -> str:
    return f"{machine_id}:{service_id}"

# def flatten_target_list(targets: List[TargetProps]) -> List[TargetProps]:
#     flattened = []
#     for target in targets:
#         flattened.append(target)
#         flattened.extend(flatten_target_list(target.subtargets))
#     return flattened