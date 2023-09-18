# Path: main.py
import json
import logging
from typing import Optional, Tuple
import functions_framework
from datetime import datetime
from supacrud import Supabase, ResponseType
from flask import jsonify, Response, Request
from typing import Any, Dict, List, Tuple, Union
from src.models.job import Job

from src.services.campaign_service import CampaignService
from src.utils.create_job_number import create_job_number
from src.utils.get_env_vars import get_env_vars
from src.utils.get_secret_payload import get_secret_payload
from src.utils.campaign_duration import calculate_duration_time, is_over_29_days
from src.utils.next_runtime_calc import calculate_next_run_time
from src.services.helpers.campaign_job_helpers import start_campaign_job
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env_vars = get_env_vars()

service_key = get_secret_payload(
    project_id=env_vars["PROJECT_ID"],
    secret_id=env_vars["SUPABASE_SERVICE_ROLE_SECRET_ID"],
    version_id=env_vars["VERSION_ID"],
)

if not service_key:
    raise Exception("Service key not found")

supabase_client = Supabase(
    base_url=env_vars["SUPABASE_URL"],
    anon_key=env_vars["SUPABASE_ANON_KEY"],
    service_role_key=service_key,
)

campaign_service = CampaignService(supabase_client=supabase_client)


@functions_framework.http
def main(request: Request) -> Union[Response, Tuple[Response, int]]:
    """
    This function is the entry point for the campaign job.
    """
    print("Request method: ", request.method)
    print("Request data: ", request.get_data())
    print("Request headers: ", request.headers)
    print("Request args: ", request.args)
    if request.method != "POST":
        return jsonify({"message": "Method not allowed"}), 405
    if not request.data:
        return jsonify({"message": "No data in the request"}), 400
    campaign_id = json.loads(request.data)["id"]
    if not campaign_id:
        return jsonify({"message": "campaign_id is required"}), 400
    campaign_job = start_campaign_job(
        campaign_id=campaign_id,
        campaign_service=campaign_service,
        supabase_client=supabase_client,
        env_vars=env_vars,
        )
    if not campaign_job:
        return jsonify({"message": "Failed to start campaign job"}), 500

    return ("", 200)
