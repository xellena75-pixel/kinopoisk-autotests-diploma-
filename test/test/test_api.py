import os
import sys
from typing import Dict, Any
import pytest
import requests
import allure
from config import (
    BASE_URL_API, API_KEY, MOVIE_ID, MOVIE_TITLE,
    MOVIE_YEAR_API, FILTER_YEAR, SEARCH_QUERY, SPECIAL_CHARS
)

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../')))


@pytest.fixture
def api_config() -> Dict[str, Any]:
    """Конфигурация API."""
    return {"base_url": BASE_URL_API, "headers": {"X-API-KEY": API_KEY}}


@allure.feature("API Тестирование")
class TestKinopoiskAPI:

    @pytest.mark.api
    @allure.title("1. Получение по ID")
    def test_api_movie_success(self, api_config: Dict[str, Any]) -> None:
        url = f"{api_config['base_url']}/{MOVIE_ID}"
        response = requests.get(url, headers=api_config['headers'])
        assert response.status_code == 200
        assert response.json()["nameRu"] == MOVIE_TITLE
        assert response.json()["year"] == MOVIE_YEAR_API

    @pytest.mark.api
    @allure.title(f"2. Фильтрация по году {FILTER_YEAR}")
    def test_api_filter_by_year(self, api_config: Dict[str, Any]) -> None:
        params = {"yearFrom": FILTER_YEAR, "yearTo": FILTER_YEAR}
        res = requests.get(
            api_config['base_url'],
            headers=api_config['headers'],
            params=params
        )
        assert res.status_code == 200
        assert len(res.json().get("items", [])) > 0

    @pytest.mark.api
    @allure.title(f"3. Поиск по слову {SEARCH_QUERY}")
    def test_api_search_by_name(self, api_config: Dict[str, Any]) -> None:
        params = {"keyword": SEARCH_QUERY}
        res = requests.get(
            api_config['base_url'],
            headers=api_config['headers'],
            params=params
        )
        assert res.status_code == 200
        assert res.json().get("total", 0) > 0

    @pytest.mark.api
    @allure.title("4. Некорректный токен")
    def test_api_invalid_token(self, api_config: Dict[str, Any]) -> None:
        headers = {"X-API-KEY": "invalid"}
        res = requests.get(
            api_config['base_url'],
            headers=headers
        )
        assert res.status_code == 401

    @pytest.mark.api
    @allure.title("5. Спецсимволы")
    def test_api_search_special_chars(
            self, api_config: Dict[str, Any]) -> None:
        params = {"keyword": SPECIAL_CHARS}
        res = requests.get(
            api_config['base_url'],
            headers=api_config['headers'],
            params=params
        )
        assert res.status_code == 200
        assert res.json().get("total") == 0
