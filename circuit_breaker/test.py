import pytest
from unittest.mock  import Mock
from datetime import timedelta
from circuit_breaker import CircuitBreaker

@pytest.fixture
def mock_api():
    return Mock()

@pytest.fixture
def circuit_breaker(mock_api):
    def fallback_func():
        return "1차 api 실패할 경우 호출"

    return CircuitBreaker(
        main_func=mock_api,
        sub_func=fallback_func,
        max_failures=3,
        delay=timedelta(seconds=10)
    )

def test_circuit_breaker_success(mock_api, circuit_breaker):
    # API가 성공하는 경우를 시뮬레이션
    mock_api.return_value = "success"
    
    result = circuit_breaker.execute(Exception)
    assert result == "success"
    assert circuit_breaker.status.value == "closed"

def test_circuit_breaker_failure(mock_api, circuit_breaker):
    # API가 실패하는 경우를 시뮬레이션
    mock_api.side_effect = Exception("API Error")
    
    # 연속 실패로 서킷이 열리는지 테스트
    for _ in range(4):
        result = circuit_breaker.execute(Exception)
    
    assert circuit_breaker.status.value == "open"
    assert result == "1차 api 실패할 경우 호출"