# 6. Configuration Management

## 6.1 Centralized Settings

* Configuration MUST be loaded via a single settings module using `pydantic_settings`.

```python
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    max_connections: int = 100

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

* Code MUST NOT read `os.environ` directly across the codebase; environment access MUST go through the settings module.

```python
# ❌ Forbidden
os.getenv("DATABASE_URL")

# ✅ Required
from project.config import get_settings

settings = get_settings()
settings.database_url
```
