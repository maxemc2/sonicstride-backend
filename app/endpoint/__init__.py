from fastapi import APIRouter
# Local Application Imports
from endpoint import experiment_music

ROUTER = APIRouter()
ROUTER.include_router(experiment_music.router)