# Path: tests/test_start_campaign_job.py
from unittest.mock import Mock
import pytest
from src.services.helpers.campaign_job_helpers import fetch_campaign_and_emails

def test_fetch_campaign_and_emails():
    campaign_service = Mock()
    
    campaign_service.get_campaign.return_value = None
    campaign_service.get_campaign_emails.return_value = None
    
    campaign_id = "campaign_id"
    
    result = fetch_campaign_and_emails(
        campaign_service=campaign_service, campaign_id=campaign_id
    )
    
    assert result is None
 