from dataclasses import dataclass, asdict
from datetime import datetime, time
from typing import Optional


@dataclass
class Job:
    number: int
    duration: str
    status: str
    campaign_id: str
    company_id: str
    created_at: str
    type: Optional[str]
    frequency: Optional[str]
    last_run_time: Optional[str]
    cloud_task_id: Optional[str]
    time_of_day: Optional[str]
    count: int = 0
    completed_at: Optional[str] = None
    id: Optional[str] = None
    tag: Optional[str] = None
    edited_at: Optional[str] = None
    next_run_time: Optional[str] = None

    def to_json(self):
        # remove id
        data = asdict(self)
        data.pop("id")
        return data
