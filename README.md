# aws-lambda-fastapi

## Run project

```
uvicorn main:app --reload --port=9595
```




En github ir a la seccion de 'settings' en 'secrets' y crear 
las siguientes variables:



* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_DEFAULT_REGION

* AWS_S3_BUCKET
* AWS_LAMBDA_FUNCTION_NAME


Run mympi:

```
mypy src 
```

Run pre-commit

```
pre-commit run --all-files
```