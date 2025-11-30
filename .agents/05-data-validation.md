# 5. Data Models and Validation (Pydantic v2)

## 5.1 Pydantic Models

* Pydantic v2 MUST be used for data validation and serialization where structured validation is needed (e.g. API payloads, configuration, external data).

```python
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr


class Product(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0, decimal_places=2)
    created_at: datetime
    is_active: bool = True
    email: EmailStr | None = None
```

## 5.2 External Data Validation

* All external inputs (HTTP bodies, query params, environment variables, message payloads) MUST be validated.
* Plain dicts from untrusted sources MUST NOT be used directly without validation.
