import time
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .routes import transportFileEndpoints, activityEndpoints, \
    goodsEndpoints, addressEndpoints, \
    clientEndpoints, contactEndpoints, \
    departmentEndpoints, employeeEndpoints, \
    jsonEndpoints, userEndpoints
from fastapi.middleware.cors import CORSMiddleware
from .services import userService
from sqlalchemy.orm import Session
from app.database.database import get_db
from datetime import datetime, timedelta
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from pydantic import BaseModel






# Declaring main FAST API app
app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")
origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Adding middleware for checking process time of each endpoint call
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to Logichainge"}

@app.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
	user = userService.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	# subject identifier for who this token is for example id or username from database
	expires = timedelta(days=1)
	access_token = Authorize.create_access_token(subject=user.username, expires_time=expires)
	expires = timedelta(days=30)
	refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=expires)
	return {"access_token": access_token, "refresh_token": refresh_token}

@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

""" Declaring all routes as part of the main FAST API app """

app.include_router(transportFileEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(clientEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(contactEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(departmentEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(employeeEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(activityEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(addressEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(goodsEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(jsonEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(userEndpoints.router)  # ,dependencies=[Depends(verify_token)])