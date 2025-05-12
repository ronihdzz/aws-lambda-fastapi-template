# aws-lambda-fastapi

| CI Environment | Coverage |
|-----------|----------|
| main| ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/main/latest/coverage.svg) |
| development| ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/development/latest/coverage.svg) |


## Run project

```
uvicorn main:app --reload --port=9595
```

Run pre-commit

```
pre-commit run --all-files
```

Run mympi:

```
mypy src 
```



Check docker deploy lambda

```
curl -Xcurl -X POST "http://localhost:9100/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "2.0",
    "routeKey": "GET /",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {},
    "requestContext": {
      "http": {
        "method": "GET",
        "path": "/",
        "sourceIp": "127.0.0.1"
      }
    },
    "isBase64Encoded": false
  }'
```
