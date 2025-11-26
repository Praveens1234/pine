
import pytest
from unittest.mock import patch, MagicMock

# Patch the OpenAI client before importing the app
with patch('openai.OpenAI', MagicMock()):
    from app import app, generate

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>AI Pine Script Generator</h1>' in response.data

@pytest.mark.asyncio
async def test_generate_endpoint():
    # Use the app's test request context
    with app.test_request_context(method='POST', data={'description': 'a simple moving average'}):
        # Mock the async validation function
        with patch('app.validate_pine_script') as mock_validate:
            # Configure the mock to return a successful validation
            mock_validate.return_value = (True, "Mock validation successful.")
            
            # Since we're in a test request context, we can call the async view function directly
            response, status_code = await generate()
            
            assert status_code == 200
            assert '<h1>Generated Pine Script</h1>' in response
            assert 'Validation successful: Mock validation successful.' in response
