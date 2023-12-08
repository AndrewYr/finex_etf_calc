import uvicorn
from fastapi import FastAPI
from finex_etf_calc.app.fastapi import create_app

app: FastAPI = create_app()


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
