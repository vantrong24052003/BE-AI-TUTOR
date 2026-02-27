# FastAPI Best Practices

## Async/Await

Always use async for database operations:

```python
# Good
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Bad - blocking
def get_users(db: Session):
    return db.query(User).all()
```

## Dependency Injection

Use FastAPI's dependency injection:

```python
from fastapi import Depends

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Decode token and return user
    pass

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Error Handling

Use HTTPException for API errors:

```python
from fastapi import HTTPException, status

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

## Pydantic Schemas

Separate schemas for different operations:

```python
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

## Database Sessions

Use dependency injection for database sessions:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

## Response Models

Always define response models:

```python
@router.post("", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate):
    ...
```

## Validation

Use Pydantic validators:

```python
from pydantic import field_validator

class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```
