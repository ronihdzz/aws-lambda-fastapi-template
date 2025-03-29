from fastapi import APIRouter


index_router = APIRouter(tags=["Index"])

@index_router.get("/")
async def index():
    return {"message": "Books API 📚"}