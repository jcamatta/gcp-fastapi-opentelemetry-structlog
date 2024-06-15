from src.models.base.router import router as base_router
from src.models.base.params import Params
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

# TestClient para cada router. En este caso para base_router.
client = TestClient(app=base_router)

# Parametros o constantes que se re-utilizan con diferentes tests.
params = Params(bucket_name="some-bucket", blob_name="some-file.txt")
params_json = jsonable_encoder(params)

dummy_params = Params(bucket_name="test_bucket", blob_name="test_blob.txt")
dummy_params_json = jsonable_encoder(dummy_params)


# Recordar que cada router lleva un prefix igual a su nombre. En este caso /base
def test_base_controller():
    """
        Realiza un post al endpoint /base/controller y evalua el response
    """
    response = client.post("/base/controller", json=params_json)
    assert response.status_code == 200
    assert response.json() == {"prediction": str(params)}

def test_base_health_check():
    """
        Realiza un get al endpoint /base/controller y evalua el response
    """
    response = client.get("/base/health-check")
    assert response.status_code == 200
    assert response.json() == {"prediction": str(dummy_params)}

def test_base_params():
    """
        Testea el objeto Params
    """
    assert str == type(params.bucket_name)
    assert str == type(params.blob_name)
    assert str(params) == "Params(bucket_name(str)=some-bucket, blob_name(str)=some-file.txt)"
    assert params.__str__() == params.__repr__()