# Path: src/services/helpers/campaign_job_helpers.py
from datetime import datetime
from typing import Optional
from supacrud import Supabase
from src.models.job import Job
from src.models.campaign import Campaign
from src.services.campaign_service import CampaignService
from src.utils.campaign_duration import calculate_duration_time
from src.utils.create_job_number import create_job_number
from src.utils.next_runtime_calc import calculate_next_run_time


def fetch_campaign_and_emails(campaign_service, campaign_id: str) -> Optional[Campaign]:
    campaign = campaign_service.get_campaign(campaign_id=campaign_id)
    if not campaign:
        return None
    emails = campaign_service.get_campaign_emails(campaign_id=campaign_id)
    if not emails:
        return None
    return campaign, emails


def calculate_next_runtime(campaign: Campaign) -> Optional[str]:
    next_run_time = None
    if campaign.type != "instant":
        next_run_time = calculate_next_run_time(
            frequency=campaign.frequency,
            time_of_day=campaign.time_of_day,
        )
    return next_run_time.isoformat() if next_run_time else None


def create_job_data(
    campaign: Campaign, next_run_time: Optional[str], supabase_client
) -> Job:
    job_number = create_job_number(campaign_id=campaign.id, supabase=supabase_client)
    return Job(
        number=job_number,
        campaign_id=campaign.id,
        status="active",
        company_id=campaign.company_id,
        next_run_time=next_run_time,
        created_at=datetime.now().isoformat(),
        edited_at=datetime.now().isoformat(),
        last_run_time=campaign.last_run_time.isoformat()
        if campaign.last_run_time
        else None,
        type=campaign.type,
        duration=campaign.duration,
        frequency=campaign.frequency,
        time_of_day=campaign.time_of_day.isoformat() if campaign.time_of_day else None,
        cloud_task_id=campaign.cloud_task_id,
    )


def schedule_survey_analytics(
    campaign: Campaign, job: Job, campaign_service, env_vars: dict
):
    survey_job_execution_time = calculate_duration_time(
        type=campaign.type,
        duration=campaign.duration,
        time_of_day=campaign.time_of_day,
    )
    campaign_service.create_survey_analytics_task(
        env=env_vars,
        payload={"job_id": job.id},
        task_name=f"survey-analytics-{job.id}",
        schedule_time=survey_job_execution_time,
        queue_name="survey-analytics",
    )


def start_campaign_job(
    campaign_id: str,
    campaign_service: CampaignService,
    supabase_client: Supabase,
    env_vars: dict,
) -> Optional[Job]:
    campaign, emails = fetch_campaign_and_emails(campaign_service, campaign_id)
    if campaign is None or emails is None:
        return None

    next_run_time = calculate_next_runtime(campaign)
    job_data = create_job_data(campaign, next_run_time, supabase_client)
    job = campaign_service.create_job(job_data=job_data)
    if not job:
        return None

    if emails:
        campaign_service.send_emails(job_id=job.id, emails=emails)
        schedule_survey_analytics(campaign, job, campaign_service, env_vars)

    return job