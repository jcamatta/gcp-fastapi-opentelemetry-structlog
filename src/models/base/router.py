import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.base.pipeline import pipeline
from src.models.base.params import Params


ROUTE_BASE = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
router = APIRouter(prefix=f"/{ROUTE_BASE}", tags=[ROUTE_BASE])


@router.post("/controller", response_class=JSONResponse)
def controller(params: Params):
    """
        MAIN entry point para obtener una prediccion
    """

    prediction: dict = pipeline(params)
    return prediction


@router.get("/health-check", response_class=JSONResponse)
def health_check():
    """
        TEST si el modelo funciona correctamente
    """

    dummy_params = Params(bucket_name="test_bucket", blob_name="test_blob.txt")
    prediction: dict = pipeline(dummy_params)
    return prediction