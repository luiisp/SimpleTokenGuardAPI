# leia README.md https://github.com/luiisp/SimpleTokenGuardAPI
from fastapi import FastAPI, Depends, HTTPException, status, Header
from itsdangerous import URLSafeSerializer
from tortoise import Tortoise, fields
from tortoise.models import Model
import secrets

app = FastAPI()
KEY = "key" 
serializer = URLSafeSerializer(KEY)

db_config = { # configs db
    "connections": {
        "default": ""
    },
    "apps": {
        "models": {
            "models": ["main"], 
            "default_connection": "default",
        }
    }
}

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=64)
    token = fields.CharField(max_length=256, null=True)

    class Meta:
        table = "users" 
        connection = "default"


async def init():
    await Tortoise.init(
        config=db_config,
    )
    await Tortoise.generate_schemas()

@app.on_event("startup")
async def startup_event():
    await init()

def generate_token(username):
    brute = f'{username}:{secrets.token_urlsafe(32)}'
    signed = serializer.dumps(brute)
    return signed

async def create_user(username, password, token):
    user = await User.create(username=username, password=password, token=token)
    return user.username

async def refresh_token(token, username):
    new_token = generate_token(username)
    await User.filter(token=token).update(token=new_token)
    print(new_token)
    return new_token

async def get_user(username, password):
    user = await User.get_or_none(username=username, password=password)
    return user

@app.post("/login")
async def login(request_data: dict):
    username = request_data.get('username')
    password = request_data.get('password')

    user = await get_user(username, password)

    if user is None:
        token = generate_token(username)
        created_user = await create_user(username, password, token)
        if created_user is None:
            raise HTTPException(status_code=401, detail="invalid credentials")
        return {"token": token, "username": username, "password": password}

    new_token = await refresh_token(user.token, user.username)
    return {"token": new_token, "username": user.username, "password": user.password}

async def authenticator(token: str = Header(...)):
    if not await User.filter(token=token).exists():
        raise HTTPException(status_code=401, detail="invalid token!")
    return token

@app.get("/security", dependencies=[Depends(authenticator)]) # rota que so pode ser acessada com token
async def security():
    return {"msg": "bem vindo a rota mais segura de todas!"}