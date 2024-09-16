from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

import helpers

api = NinjaExtraAPI()

api.add_router("", "authentication.api.router")



# api.register_controllers(NinjaJWTDefaultController)