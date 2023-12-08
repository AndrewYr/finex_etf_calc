from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from finex_etf_calc.api.views import routes, admin_routes
healthcheck_route = APIRouter()


@healthcheck_route.get('/v1/health')
async def health_check():
    return {'status': 'ok'}


async def redirect_to_swagger():
    return RedirectResponse('/docs', status_code=301)


def create_app():
    app = FastAPI(title='finex-etf-calc')

    app.add_api_route('/', redirect_to_swagger, methods=['GET'])

    app.include_router(healthcheck_route)
    app.include_router(routes, prefix='/v1', tags=['v1'])
    app.include_router(admin_routes, prefix='/admin/v1', tags=['admin'])

    return app
