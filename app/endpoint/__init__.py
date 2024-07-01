from fastapi import APIRouter
# Local Application Imports
from endpoint import configs, audios, tracks, events, actions, others

ROUTER = APIRouter()
ROUTER.include_router(configs.router)
ROUTER.include_router(audios.router)
ROUTER.include_router(tracks.router)
ROUTER.include_router(events.router)
ROUTER.include_router(actions.router)
ROUTER.include_router(others.router)