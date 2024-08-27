# /api


### auth/sign-up/anon
response ok body:
```json
{
    "ok": 1,
    "jwt_access": "xxx.yyy.zzz"
}
```
additional response ok set-cookie:
```refresh=REFRESH_TOKEN```

response error {INSERT HTTP CODE} body:
```json
{
    "ok": 0,
    "code": "TODO:",
    "info": {}
}
```

### auth/sign-up/user
request body:
```json
{
    "username": "string",
    "nickname": "string",
    "email": "string",
    "email-code": "string"
}
```

optional additional request cookie:
```refresh=REFRESH_TOKEN```

response ok body:
```json
{
    "ok": 1,
    "some access JWT": "TODO:..."
}
```

additional response ok set-cookie:
```refresh=REFRESH_TOKEN```

response error {INSERT HTTP CODE HERE} body:
```json
{
    "ok": 0,
    "code": "TODO:",
    "info": {}
}
```

### auth/sign-in/via/reissue-access
required request cookie:
```refresh=REFRESH_TOKEN```

response ok body:
```json
{
    "ok": 1,
    "some access JWT": "TODO:..."
}
```

response error {INSERT HTTP CODE HERE} body:
```json
{
    "ok": 0,
    "code": "TODO:",
    "info": {}
}
```

### auth/sign-in/via/email-code TODO: limit
request body:
```json
{
    "email": "string",
    "email-code": "string",
}
```

response ok body:
```json
{
    "ok": 1,
    "some access JWT": "TODO:..."
}
```
response ok cookie:
```refresh=REFRESH_TOKEN```

response error {INSERT HTTP CODE HERE} body:
```json
{
    "ok": 0,
    "code": "TODO:...",
    "info": {}
}
```
### /verify/email/already-used TODO: websockets + limit
ws request body:
```json
{
    "email": "string",
}
```

ws response ok body:
```json
{
    "ok": 1,
    "{received-email}": "bool",
}
```

ws response error body:
```json
{
    "ok": 0,
    "code": "LIMIT_REACHED",
    "info": {
        "wait": 30,
    }
}
```

### /verify/email/send-code TODO: limit
request body:
```json
{
    "email": "string"
}
```

response ok body:
```json
{
    "ok": 1
}
```

response error {INSERT HTTP CODE HERE} body:
```json
{
    "ok": 0,
    "code": "OCCUPIED",
    "info": {}
}
```

response error {INSERT HTTP CODE HERE} body:
```json
{
    "ok": 0,
    "code": "LIMIT_REACHED",
    "info": {
        "wait": 30,
    }
}
```


### game/create
### game/join
### game/watch
### game/random

Пример цепочки вызовов для полноценной регистрации [Этап 2]:
http /auth/sign-up/anon Допустим пользователь начал игру с кем-то [опционально]
ws /verify/email/already-used Начал регистрацию, пишет email для привязки аккаунта
http /verify/email/send-code Отправляет код на свободную почту
http /auth/sign-up/user Регистрируется, получает ACCESS и REFRESH для полноценного аккаунта

