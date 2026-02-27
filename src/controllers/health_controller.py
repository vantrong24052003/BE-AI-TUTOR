from fastapi import APIRouter

router = APIRouter(prefix="/api/health")


@router.get("")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
