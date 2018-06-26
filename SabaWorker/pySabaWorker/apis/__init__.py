from flask_restplus import Api

from pySabaWorker.apis.admin_api import api as admin_ns
from pySabaWorker.apis.blob_api import api as blob_ns
from pySabaWorker.apis.job_api import api as job_ns

api = Api(
    title="Saba Worker API Documentation",
    version="1.0",
    description="Saba Worker is one module of RyuGoo",
    doc="/doc/"
)

api.add_namespace(admin_ns)
api.add_namespace(blob_ns)
api.add_namespace(job_ns)