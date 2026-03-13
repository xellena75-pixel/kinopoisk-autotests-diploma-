# Настройки окружения (Environment Settings)
BASE_URL_UI = "https://www.kinopoisk.ru"
BASE_URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films"

# Тестовые данные
API_KEY = "999a4483-7cf2-4845-8ffa-bcbaf4f5e034"
MOVIE_ID = 52812
MOVIE_TITLE = "Гладиатор 2000"

# Разделение данных для API и UI из-за различий в базе Кинопоиска
MOVIE_YEAR_API = 1999  # API возвращает 1999
MOVIE_STR_UI = "2000"  # На сайте отображается 2000

MOVIE_URL = f"{BASE_URL_UI}/film/474/"
SEARCH_QUERY = "Гладиатор"
FILTER_YEAR = 1999
SPECIAL_CHARS = "@@@"
