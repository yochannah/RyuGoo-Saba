from flask_restplus import Api

from pySabaMaster.apis.admin_api import api as admin_ns
from pySabaMaster.apis.azure_api import api as azure_ns
from pySabaMaster.apis.jobs_api import api as jobs_ns

api = Api(
    title="Saba Master API Documentation",
    version="1.0",
    description="Saba Master is one module of RyuGoo",
    doc="/doc/"
)

api.add_namespace(admin_ns)
api.add_namespace(azure_ns)
api.add_namespace(jobs_ns)
