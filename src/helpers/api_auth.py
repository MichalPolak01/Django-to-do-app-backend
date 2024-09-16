from ninja_jwt.authentication import JWTAuth


def allow_anonymous(request):
    return not request.user.is_authenticated
    

api_auth_required = [JWTAuth()]
api_auth_not_required = [JWTAuth(), allow_anonymous]