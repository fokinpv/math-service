from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from . import statistics

templates = Jinja2Templates(directory="templates")
router = APIRouter()


def get_statistics():
    """Statistics injector"""
    return statistics.Statistics


@router.get('/', include_in_schema=False)
def index(
        request: Request,
        statistics: statistics.Statistics = Depends(get_statistics)
):
    return templates.TemplateResponse(
        'index.html', context={'request': request, 'statistics': statistics.data}
    )
