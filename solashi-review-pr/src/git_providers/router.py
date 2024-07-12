from fastapi import APIRouter


router = APIRouter(prefix="/git", tags=["gits"])

@router.get("/review-pr")
def review_pr_with_url(pr_url:str = ""):
    return pr_url

@router.get("/github_webhook")
def review_pr_with_github_webhook():
    return "aaaa"