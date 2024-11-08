import random
from locust import HttpUser, task, between, events
from urllib.parse import quote
import logging
import time
import os, json

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_search_queries():
    """검색 쿼리 JSON 파일 로드"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'search_queries.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['queries']



class SearchUser(HttpUser):
    wait_time = between(0.1, 0.1)
    
    def on_start(self):
        """테스트 시작 시 실행되는 메소드"""
        self.search_query = {'keyword': 'KCM', 'category': 'artists'} # load_search_queries()
        self.csrf_token = 'arlWR9u85C4FYguE5Bf6HtFheQ0C6JfPF4N7ouB1SdJeTHhIajGERzFmywI0GZe6'
        # 응답 시간 통계를 위한 변수
        self.response_times = []

    @task
    def search_specific_artist(self):
        """특정 아티스트 반복 검색"""
        self._do_search()
    
    def _do_search(self):
        search_data = self.search_query

        encoded_query = quote(search_data['keyword'])
        start_time = time.time()
        
        with self.client.get(
            f"/musics/search?csrfmiddlewaretoken={self.csrf_token}&category={search_data['category']}&keyword={encoded_query}",
            name=f"Search {search_data['category']}: {search_data['keyword']}",
            catch_response=True
        ) as response:
            duration = time.time() - start_time
            if response.status_code == 200:
                logger.info(f"Successful search for {search_data['keyword']} ({duration:.2f}s)")
                response.success()
                self.response_times.append(duration)
            else:
                error_msg = f"Search failed for {search_data['keyword']}: {response.status_code}"
                logger.error(error_msg)
                response.failure(error_msg)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """테스트 시작 시 실행"""
    logger.info("Load test is starting")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """테스트 종료 시 실행"""
    logger.info("Load test is ending")
    
    # 테스트 결과 요약
    if hasattr(environment.runner, "stats"):
        stats = environment.runner.stats
        logger.info(f"""
        Test Summary:
        - Total Requests: {stats.total.num_requests}
        - Failed Requests: {stats.total.num_failures}
        - Average Response Time: {stats.total.avg_response_time:.2f}ms
        - Median Response Time: {stats.total.median_response_time}ms
        - 95th Percentile: {stats.total.get_response_time_percentile(0.95)}ms
        """)