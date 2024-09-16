from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from ninja import Router
import json
from ninja.errors import HttpError

from .schemas import UserEntryCreateSchema, UserEntryDetailsSchema, ErrorUserEntryCreateSchema, SignInSchema
from .forms import UserCreateForm
import helpers


router = Router()


@router.post("/register", response = { 201: UserEntryDetailsSchema, 400: ErrorUserEntryCreateSchema }, auth=helpers.api_auth_not_required)
def register(request, payload: UserEntryCreateSchema):
    form = UserCreateForm(payload.dict())

    if not form.is_valid():
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors
    
    obj = form.save()

    return 201, obj


@router.post("/login", auth=helpers.api_auth_not_required)
def login(request, payload: SignInSchema):
    user = authenticate(request, email=payload.email, password=payload.password)

    if user is None:
        raise HttpError(401, "Invalid email or password")
    
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }