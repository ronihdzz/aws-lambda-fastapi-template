# aws-lambda-fastapi

| CI Environment | Coverage |
|-----------|----------|
| main| ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/tree/artifacts/main/latest/coverage.svg) |
| development| ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/tree/artifacts/development/latest/coverage.svg) |



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

