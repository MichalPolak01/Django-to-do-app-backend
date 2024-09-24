from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from ninja import Router
import json
from ninja.errors import HttpError

from .schemas import UserEntryCreateSchema, UserEntryDetailsSchema, ErrorUserEntryCreateSchema, SignInSchema, UserEntryUpdateSchema, MessageSchema, PasswordChangeSchema, ErrorPasswordChangeSchema
from .forms import UserCreateForm, UserUpdateForm, PasswordChangeForm
import helpers
from core.api import api


router = Router()


@router.post("/register", response = { 201: UserEntryDetailsSchema, 400: ErrorUserEntryCreateSchema }, auth=helpers.api_auth_not_required, tags=["Authentication"])
def register(request, payload: UserEntryCreateSchema):
    form = UserCreateForm(payload.dict())

    if not form.is_valid():
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors
    
    obj = form.save()

    return 201, obj


@router.post("/login", auth=helpers.api_auth_not_required, tags=["Authentication"])
def login(request, payload: SignInSchema):
    user = authenticate(request, email=payload.email, password=payload.password)

    if user is None:
        raise HttpError(401, "Invalid email or password")
    
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "username": user.first_name,
    }


@router.get("/user", response=UserEntryDetailsSchema, auth=helpers.api_auth_required, tags=["Authentication"])
def get_user(request):
    return request.user


@api.put("/user/edit", response={200: UserEntryDetailsSchema, 400: ErrorUserEntryCreateSchema}, auth=helpers.api_auth_required, tags=["Authentication"])
def edit_user(request, payload: UserEntryUpdateSchema):
    user = request.user
    form = UserUpdateForm(payload.dict(), instance=user)

    if not form.is_valid():
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors
    
    obj = form.save()

    return 200, obj


@api.put("/user/change_password", response={200: MessageSchema, 400: ErrorPasswordChangeSchema}, auth=helpers.api_auth_required, tags=["Authentication"])
def change_password(request, payload: PasswordChangeSchema):
    user = request.user
    form = PasswordChangeForm(user, data=payload.dict())

    if not form.is_valid():
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors
    
    form.save()

    return 200, {"message": "Password changed successfully"}