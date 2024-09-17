from fastapi import APIRouter

from . import (
    github,
    gitlab
)

router = APIRouter()

router_dirs: list = [
    gitlab,
    github
]
for router_dir in router_dirs:
    router.include_router(router_dir.router)
