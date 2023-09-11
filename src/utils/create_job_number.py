import logging
from supacrud import Supabase

logger = logging.getLogger(__name__)


def create_job_number(campaign_id: str, supabase: Supabase) -> int:
    """
    Job number is the the number of jobs for that campaign.
    Get all the jobs with the given campaign id and then get the count of the
    jobs and add 1 to it to get the job name
    """
    try:
        response = supabase.read(url=f"rest/v1/jobs?campaign_id=eq.{campaign_id}")
        if response:
            return len(response) + 1
        else:
            return 1
    except Exception as e:
        logger.error(f"Failed to create job name for campaign id {campaign_id}")
        logger.error(e)
        return None
