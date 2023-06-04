from fastapi import APIRouter

router = APIRouter(
    prefix="", tags=[""]
)

@router.post("/login")
def login()