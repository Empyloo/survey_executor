# Path: src/services/campaign_service.py
import logging
import json
import datetime as dt
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from google.cloud import tasks_v2
from supacrud import Supabase
from src.models.campaign import Campaign
from src.models.job import Job
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)


class CampaignService:
    def __init__(self, supabase_client: Supabase):
        self.supabase_client = supabase_client

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Fetch a campaign based on its id."""
        response = self.supabase_client.read(
            url=f"rest/v1/campaigns?id=eq.{campaign_id}"
        )
        if response:
            return Campaign(**response[0])
        else:
            logger.error(f"No campaign found with id {campaign_id}")
            return None

    def get_campaign_emails(self, campaign_id: str) -> Optional[List[str]]:
        """Fetch the emails for a campaign based on the campaign id."""
        response = self.supabase_client.rpc(
            url="rest/v1/rpc/get_campaign_emails",
            params={"campaign_id_param": campaign_id},
        )
        if response:
            emails = [email["email"] for email in response]
            return emails
        else:
            logger.error(f"No emails found for campaign id {campaign_id}")
            return None

    def create_job(self, job_data: Job) -> Optional[Job]:
        """Create a new job."""
        data = job_data.to_json()
        response = self.supabase_client.create("rest/v1/jobs", data)
        print(response)
        if response:
            return Job(**response[0])
        else:
            logger.error(f"Failed to create job with data {job_data}")
            return None

    def send_emails(self, job_id: str, emails: List[str]) -> bool:
        """Send emails for a given job."""
        failed_emails = []
        for email in emails:
            data = {
                "email": email,
            }
            redirect_to = f"https://app.empylo.com/#/survey?surveyId={job_id}"
            redirect_to_encoded = quote(redirect_to, safe="")
            try:
                self.supabase_client.create(
                    f"auth/v1/magiclink?redirect_to={redirect_to_encoded}",
                    data=data,
                )
            except Exception as e:
                logger.error(f"Failed to send email to {email}")
                failed_emails.append(email)
        if failed_emails:
            logger.error(f"Failed to send emails to {failed_emails}")
            if len(failed_emails) == len(emails):
                return False
        return True

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=3))
    def create_survey_analytics_task(
        self,
        env: Dict,
        payload: Dict,
        task_name: str,
        schedule_time: Optional[dt.datetime] = None,
        queue_name: Optional[str] = None,
    ) -> tasks_v2.types.task.Task:
        """Create a survey analytics task for a given job."""
        try:
            client = tasks_v2.CloudTasksClient()
            parent = client.queue_path(env["PROJECT_ID"], env["REGION"], queue_name)
            task = {
                "http_request": {
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": env["SURVEY_ANALYSER_FUNCTION_URL"],
                    "oidc_token": {
                        "service_account_email": env["SERVICE_ACCOUNT_EMAIL"],
                        "audience": env["SERVICE_ACCOUNT_EMAIL"],
                    },
                },
                "name": f"projects/{env['PROJECT_ID']}/locations/{env['REGION']}/queues/{queue_name}/tasks/{task_name}",
            }
            if schedule_time:
                task["schedule_time"] = schedule_time

            payload_str = json.dumps(payload)
            converted_payload = payload_str.encode()
            task["http_request"]["body"] = converted_payload

            response = client.create_task(request={"parent": parent, "task": task})

            logger.info("Created task %s", response.name)
            return response
        except Exception as error:
            logger.error(
                f"Error creating task for queue '{queue_name}' with payload '{payload}' and schedule time '{schedule_time}': {error}"
            )
            raise
