import os

from dotenv import load_dotenv

load_dotenv(override=False)

# DB 설정
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
# REDIS
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
# 원격 서버
REMOTE_HOST = os.getenv("REMOTE_HOST")
APP_HOST = os.getenv("APP_HOST")  # 운영 환경에서는 '0.0.0.0' 주입
APP_PORT = int(os.getenv("APP_PORT"))
RULE_ENGINE_PORT = int(os.getenv("RULE_ENGINE_PORT"))
APP_ENV = os.getenv("APP_ENV")  # local, dev, prod 등

# 프론트엔드
WEB_PORT = os.getenv("WEB_PORT")

# 인증 - JWT 인증 관련 설정
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7일 동안 유효
REFRESH_TOKEN_EXPIRE_SECONDS = (
    REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
)  # 7일 만료 (초단위)

# 타 서비스(마이크로서비스) 기본 URL
REMOTE_SERVICE_URL = f"http://{REMOTE_HOST}:{RULE_ENGINE_PORT}/info"
