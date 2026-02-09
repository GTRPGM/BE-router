# BE-router

GTRPGM 프로젝트를 위한 백엔드 라우터 서비스입니다. 사용자 인증, 게임 데이터 관리, 미니게임 로직 등을 포함하는 다양한 API 엔드포인트를 제공합니다.

## 주요 기능

- 사용자 인증 및 권한 관리 (`src/auth`)
- 게임 마스터(GM) 도구 및 관리 기능 (`src/gm`)
- 아이템, NPC, 월드 정보 등 게임 데이터 조회 (`src/info`)
- 미니게임 관련 로직 처리 (`src/minigame`)
- 게임 상태 관리 (`src/state`)

## 주요 기술 스택

- **언어**: Python 3.10+
- **웹 프레임워크**: FastAPI
- **패키지 관리**: `uv` (pip 호환)
- **컨테이너**: Docker, Docker Compose
- **데이터베이스**: PostgreSQL (예상)
- **캐싱**: Redis (예상)

## 프로젝트 구조

```
C:\projects\GTRPGM\BE-router\
├───.dockerignore
├───.gitignore
├───.markdownlint.yaml
├───.pre-commit-config.yaml
├───.python-version
├───docker-compose.yml
├───Dockerfile
├───Dockerfile-dev
├───pyproject.toml
├───README.md
├───uv.lock
├───.git\...
├───.github\
│   ├───pull_request_template.md
│   ├───ISSUE_TEMPLATE\
│   │   ├───Chore.yml
│   │   ├───Docs.yml
│   │   ├───Feat.yml
│   │   ├───Fix.yml
│   │   ├───Ops.yml
│   │   ├───Ref.yml
│   │   └───Test.yml
│   └───workflows\
│       ├───ci-dev.yml
│       └───deploy.yaml
├───.idea\
│   └───inspectionProfiles\...
├───.venv\
│   ├───Lib\...
│   └───Scripts\...
├───bin\
│   ├───project
│   └───readme.md
├───src\
│   ├───exceptions.py
│   ├───main.py
│   ├───__pycache__\...
│   ├───app\
│   │   └───__init__.py
│   ├───app.egg-info\
│   │   ├───dependency_links.txt
│   │   ├───PKG-INFO
│   │   ├───requires.txt
│   │   ├───SOURCES.txt
│   │   └───top_level.txt
│   ├───auth\
│   │   ├───__init__.py
│   │   ├───auth_router.py
│   │   ├───auth_service.py
│   │   ├───__pycache__\...
│   │   ├───dtos\
│   │   │   ├───__init__.py
│   │   │   ├───login_dtos.py
│   │   │   └───__pycache__\...
│   │   ├───queries\
│   │   │   ├───__init__.py
│   │   │   ├───create_user.sql
│   │   │   ├───get_user_by_id.sql
│   │   │   ├───get_user_by_username.sql
│   │   │   └───get_user_for_auth.sql
│   │   └───utils\
│   │       ├───__init__.py
│   │       ├───crypt_utils.py
│   │       ├───test_crypt.py
│   │       ├───token_utils.py
│   │       └───__pycache__\...
│   ├───common\
│   │   ├───__init__.py
│   │   ├───__pycache__\...
│   │   ├───dtos\
│   │   │   ├───__init__.py
│   │   │   ├───common_response.py
│   │   │   ├───custom.py
│   │   │   ├───pagination_meta.py
│   │   │   ├───wrapped_response.py
│   │   │   └───__pycache__\...
│   │   └───utils\
│   │       ├───__init__.py
│   │       ├───get_services.py
│   │       └───__pycache__\...
│   ├───configs\
│   │   ├───__init__.py
│   │   ├───api_routers.py
│   │   ├───color_hint_formatter.py
│   │   ├───database.py
│   │   ├───http_client.py
│   │   ├───logging_config.py
│   │   ├───origins.py
│   │   ├───redis_conn_rule.py
│   │   ├───redis_conn.py
│   │   ├───setting.py
│   │   └───__pycache__\...
│   ├───gm\
│   │   ├───__init__.py
│   │   ├───gm_routers.py
│   │   ├───__pycache__\...
│   │   └───dtos\
│   │       ├───gm_dtos.py
│   │       └───__pycache__\...
│   ├───info\
│   │   ├───__init__.py
│   │   ├───info_router.py
│   │   ├───item_service.py
│   │   ├───__pycache__\...
│   │   ├───dtos\
│   │   │   ├───__init__.py
│   │   │   ├───enemy_dtos.py
│   │   │   ├───item_dtos.py
│   │   │   ├───npc_dtos.py
│   │   │   ├───personality_dtos.py
│   │   │   ├───world_dtos.py
│   │   │   └───__pycache__\...
│   │   └───queries\
│   │       ├───__init__.py
│   │       ├───count_items.sql
│   │       └───get_items.sql
│   ├───minigame\
│   │   ├───__init__.py
│   │   ├───minigame_router.py
│   │   ├───__pycache__\...
│   │   └───dtos\
│   │       ├───__init__.py
│   │       ├───minigame_dtos.py
│   │       └───__pycache__\...
│   ├───state\
│   │   ├───__init__.py
│   │   ├───state_router.py
│   │   ├───__pycache__\...
│   │   └───dtos\
│   │       ├───__init__.py
│   │       ├───state_dtos.py
│   │       └───__pycache__\...
│   └───utils\
│       ├───__init__.py
│       ├───lifespan_handlers.py
│       ├───load_sql.py
│       ├───logger.py
│       ├───parse_json.py
│       ├───proxy_request.py
│       ├───proxy_stream.py
│       └───__pycache__\...
└───tests\
    └───conftest.py
```

## 로컬 환경 설정

### 공통 요구사항

프로젝트를 로컬에서 실행하기 위해서는 다음 도구들이 필요합니다:

-   **Python 3.10 이상**: [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드 및 설치.
-   **`uv` 패키지 관리자**: `pip`를 대체하는 빠른 Python 패키지 설치 도구입니다.
    ```bash
    pip install uv
    # 또는 pipx가 설치되어 있다면
    # pipx install uv
    ```
-   **Docker Desktop**: 컨테이너화된 서비스를 실행하기 위해 필요합니다. [Docker 공식 웹사이트](https://www.docker.com/products/docker-desktop/)에서 다운로드 및 설치.
-   **Git**: 소스 코드를 클론하기 위해 필요합니다.
    ```bash
    git clone [프로젝트-저장소-URL]
    cd BE-router
    ```

### 가상 환경 설정

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 가상 환경을 생성하고 필요한 의존성을 설치합니다.

```bash
uv venv
uv sync
```

### PyCharm 설정

1.  **프로젝트 열기**: PyCharm을 실행하고 "Open"을 클릭한 뒤, `BE-router` 프로젝트 폴더를 선택합니다.
2.  **Python 인터프리터 설정**:
    *   "File" > "Settings" (macOS: "PyCharm" > "Preferences")로 이동합니다.
    *   "Project: BE-router" > "Python Interpreter"를 선택합니다.
    *   오른쪽 상단의 톱니바퀴 아이콘을 클릭하고 "Add Interpreter" > "Virtualenv Environment"를 선택합니다.
    *   "Existing environment"를 선택하고, "Interpreter" 경로에 프로젝트 루트에 생성된 `.venv/Scripts/python.exe` (Windows) 또는 `.venv/bin/python` (macOS/Linux)을 찾아 지정합니다.
    *   "OK"를 클릭하여 설정을 완료합니다.

### VSCode 설정

1.  **프로젝트 열기**: VSCode를 실행하고 "File" > "Open Folder"를 클릭한 뒤, `BE-router` 프로젝트 폴더를 선택합니다.
2.  **Python 확장 설치**: VSCode 왼쪽 사이드바에서 Extensions 탭을 열고 "Python"을 검색하여 Microsoft에서 제공하는 Python 확장을 설치합니다.
3.  **Python 인터프리터 선택**:
    *   `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`)를 눌러 Command Palette를 엽니다.
    *   "Python: Select Interpreter"를 검색하여 선택합니다.
    *   프로젝트 루트에 생성된 `.venv` 환경을 선택합니다. (일반적으로 `Python 3.x.x ('.venv': venv)`)

## 프로젝트 실행 방법

### Docker Compose를 이용한 실행 (권장)

프로덕션 환경과 유사한 환경에서 프로젝트를 실행하려면 Docker Compose를 사용하는 것이 좋습니다.

1.  프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 서비스를 빌드하고 시작합니다.
    ```bash
    docker compose up --build
    ```
2.  백그라운드에서 실행하려면 `-d` 옵션을 추가합니다.
    ```bash
    docker compose up --build -d
    ```
3.  서비스 중지:
    ```bash
    docker compose down
    ```

### 로컬에서 직접 실행 (PyCharm/VSCode)

로컬 개발 환경에서 직접 FastAPI 애플리케이션을 실행하는 방법입니다.

1.  **터미널 열기**:
    *   **PyCharm**: 하단의 "Terminal" 탭을 클릭합니다.
    *   **VSCode**: "Terminal" > "New Terminal"을 선택합니다.

2.  **가상 환경 활성화**:
    *   **Windows (PowerShell)**:
        ```bash
        .\.venv\Scripts\Activate.ps1
        ```
    *   **macOS/Linux (Bash/Zsh)**:
        ```bash
        source ./.venv/bin/activate
        ```

3.  **FastAPI 애플리케이션 실행**:
    가상 환경이 활성화된 상태에서 다음 명령어를 실행합니다.
    ```bash
    uvicorn src.main:app --reload
    ```
    - 위 명령어는 `src/main.py` 파일의 `app` 객체를 사용하여 FastAPI 서버를 시작하고, 코드 변경 시 자동으로 서버를 재시작합니다.
    - 파이참에서는 main.py의 `if __name__ == "__main__":` 찾아 ▶ 아이콘 버튼을 눌러 직접 실행해도 됩니다. 첫 실행 이후에는 Shift + f10 조합키를 눌러 즉시 실행이 가능합니다.

### API 문서 확인

프로젝트가 성공적으로 실행되면, 웹 브라우저에서 다음 URL을 통해 API 문서를 확인할 수 있습니다:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`
