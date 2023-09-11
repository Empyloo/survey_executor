# Path: src/models/campaign.py
import datetime as dt
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class Campaign:
    id: Optional[str]
    name: str
    count: int
    threshold: int
    status: str
    company_id: str
    created_by: str
    duration: str
    next_run_time: dt.datetime
    created_at: Optional[dt.datetime]
    last_run_time: Optional[dt.datetime]
    updated_at: Optional[dt.datetime] = None
    type: Optional[str] = None
    end_date: Optional[dt.datetime] = None
    frequency: Optional[str] = None
    time_of_day: Optional[dt.time] = None
    description: Optional[str] = None
    audience_ids: Optional[List[str]] = None
    questionnaire_ids: Optional[List[str]] = None
    cloud_task_id: Optional[str] = None
