import pytest
import responses.matchers
from responses import RequestsMock
from tatry.exceptions import TatryAPIError
from tatry.models.utils import UsageResponse
from tatry.client import API_URL

@pytest.fixture
def mock_responses():
    with RequestsMock() as rsps:
        yield rsps

def test_get_usage_default(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/usage",
        json={
            "status": "success",
            "data": {
                "time_range": {
                    "month": "2024-02"
                },
                "usage": {
                    "queries": {
                        "total": 1000,
                        "by_source": {
                            "wikipedia": 500,
                            "academic_journals": 500
                        }
                    },
                    "documents": {
                        "total": 5000,
                        "by_source": {
                            "wikipedia": 2500,
                            "academic_journals": 2500
                        }
                    }
                }
            }
        },
        status=200,
    )
    
    response = client.utils.get_usage()
    assert isinstance(response, UsageResponse)
    assert response.status == "success"
    assert response.data.usage.queries.total == 1000
    assert response.data.usage.documents.total == 5000

def test_get_usage_specific_month(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/usage",
        match=[RequestsMock.matchers.query_param_matcher({"month": "2024-01"})],
        json={
            "status": "success",
            "data": {
                "time_range": {
                    "month": "2024-01"
                },
                "usage": {
                    "queries": {
                        "total": 500,
                        "by_source": {
                            "wikipedia": 250,
                            "academic_journals": 250
                        }
                    },
                    "documents": {
                        "total": 2500,
                        "by_source": {
                            "wikipedia": 1250,
                            "academic_journals": 1250
                        }
                    }
                }
            }
        },
        status=200,
    )
    
    response = client.utils.get_usage(month="2024-01")
    assert response.status == "success"
    assert response.data.time_range.month == "2024-01"
    assert response.data.usage.queries.total == 500

def test_submit_feedback_with_metadata(client, mock_responses):
    feedback_id = "fb_20240218120000"
    metadata = {
        "browser": "Chrome",
        "version": "120.0",
        "os": "Windows"
    }
    
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/feedback",
        match=[
            responses.matchers.json_params_matcher({
                "type": "bug",
                "description": "Test feedback",
                "metadata": metadata
            })
        ],
        json={
            "status": "success",
            "data": {
                "id": feedback_id,
                "received_at": "2024-02-18T12:00:00Z",
                "message": "Thank you for your feedback"
            }
        },
        status=200,
    )
    
    response = client.utils.submit_feedback(
        feedback_type="bug",
        description="Test feedback",
        metadata=metadata
    )
    
    assert response.status == "success"
    assert response.data.id == feedback_id
    assert response.data.message == "Thank you for your feedback"

def test_submit_feedback_validation_error(client, mock_responses):
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/feedback",
        json={
            "error": "Validation error",
            "details": "Invalid feedback type"
        },
        status=400,
    )
    
    with pytest.raises(TatryAPIError) as exc:
        client.utils.submit_feedback(
            feedback_type="invalid",
            description=""
        )
    assert exc.value.status_code == 400

def test_check_health(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/health",
        json={'status': 'success', 'data': {'status': 'healthy', 'version': '1.0.0', 'timestamp': '2025-02-18T15:59:27Z'}},
        status=200,
    )
    
    response = client.utils.check_health()
    assert response.status == "success"