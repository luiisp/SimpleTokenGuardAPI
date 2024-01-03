## SimpleTokenGuardAPI

#### ⚡SimpleTokenGuardAPI é um exemplo de API com rotas que requerem autententicação.

Toda vez que um usuario faz login com seu usuario e senha ele recebe um token unico assinado digitalmente com seu username.

## Examples
### /login
* #### Request
body

	{"username":"admin",
	"password":"admin"}
* #### Response
```
	{"token": "ImFkbWluOmswdG91RGZkOHM2UExzUzZpcGxKa2YyUlpxZmFkVWp1M2hOSUhoMnUyY1Ei.z3wtl8C6H5BUlSyex208os8BBUU",
	"username": "admin",
	"password": "admin"}
```
### Incluindo esse token unico no header da request o user pode entrar em rotas protegidas como /security sem problemas


### /security
header
* #### Request
```
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0
    Content-Type: application/json
    token: ImFkbWluOmswdG91RGZkOHM2UExzUzZpcGxKa2YyUlpxZmFkVWp1M2hOSUhoMnUyY1Ei.z3wtl8C6H5BUlSyex208os8BBUU}
```
* #### Response
```
    {"msg": "bem vindo a rota mais segura de todas!"}
```
## libs

* fastapi
* itsdangerous
* tortoise
* uvicorn

## Running

### Use `uvicorn main:app` para rodar a api (precisará da lib uvicorn)

