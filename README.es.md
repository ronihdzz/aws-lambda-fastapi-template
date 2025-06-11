# AWS Lambda FastAPI Template

[![English](https://img.shields.io/badge/🇺🇸-English-blue)](README.md) [![Español](https://img.shields.io/badge/🇪🇸-Español-red)](README.es.md)

| Ambiente | Cobertura |
|-----------|----------|
| main | ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/main/latest/coverage.svg) |
| development | ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/development/latest/coverage.svg) |

## 📋 Descripción del Template

Este es un template completo para el desarrollo de APIs REST con **FastAPI** diseñado para ser deployado en **AWS Lambda** usando **Mangum** como proxy inverso. El template implementa un enfoque **serverless** completo, proporcionando una arquitectura modular, manejo de errores estandarizado, testing automatizado contra bases de datos reales, y un stack integral de CI/CD con Docker.

### 🚀 **Contexto Serverless y AWS Lambda**

El template está optimizado para **arquitecturas serverless** usando AWS Lambda:
- **Mangum** actúa como adaptador/proxy inverso que permite que FastAPI funcione como una función Lambda
- **Serverless Computing**: Sin gestión de servidores, escalado automático, pago por uso
- **API Gateway Integration**: Compatible con AWS API Gateway para routing y autenticación
- **Cold Start Optimization**: Estructura optimizada para minimizar el tiempo de arranque en frío

## 🏗️ Arquitectura y Estructura del Proyecto

### Estructura de Directorios

```
aws-lambda-fastapi/
├── src/                          # Código fuente principal
│   ├── api/                      # Capa de API - Routers y endpoints
│   │   ├── v1/                   # Versioning de API
│   │   ├── routers.py            # Registro de routers principales
│   │   └── endpoints.py          # Endpoints base (health check, etc.)
│   ├── core/                     # Configuración central
│   │   ├── settings/             # Configuraciones por ambiente
│   │   ├── exceptions.py         # Excepciones específicas del dominio
│   │   └── internal_codes.py     # Códigos internos del dominio
│   ├── shared/                   # Utilidades compartidas
│   │   ├── middlewares/          # Middlewares personalizados
│   │   ├── base_responses.py     # Respuestas estandarizadas
│   │   ├── base_internal_codes.py # Códigos internos base
│   │   ├── base_exceptions.py    # Excepciones base
│   │   └── utils_dates.py        # Utilidades de fechas
│   ├── db/                       # Capa de base de datos
│   │   ├── postgresql/           # Configuración PostgreSQL
│   │   └── mongo/                # Configuración MongoDB
│   ├── tests/                    # Suite de pruebas
│   └── main.py                   # Punto de entrada de la aplicación
├── docker_images/                # Imágenes Docker personalizadas
│   └── testing/                  # Configuración para testing
├── .github/workflows/            # Pipelines CI/CD
└── docs/                         # Documentación del proyecto
```

## 🔧 Componentes Principales

### 1. **Sistema de Respuestas Estandarizadas** (`@/shared/base_responses.py`)

El template implementa un sistema de respuestas consistente usando un patrón **Envelope Response**:

```python
class EnvelopeResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] | list | None = None
    trace_id: str | None = None
```

**Convenciones:**
- Todas las respuestas siguen el mismo formato
- Manejo automático de serialización de Pydantic models
- Inclusión de trace_id para debugging
- Respuestas de error estructuradas con códigos internos

### 2. **Sistema de Códigos Internos** (`@/shared/base_internal_codes.py`)

Sistema de códigos de error estandarizado para tracking y debugging:

```python
class CommonInternalCode(InternalCodeBase):
    UNKNOWN = 100, "Unknown error"
    PYDANTIC_VALIDATIONS_REQUEST = 8001, "Failed Pydantic validations on request"
```

**Convenciones:**
- Códigos numéricos únicos para cada tipo de error
- Descripción clara del error
- Extensible para códigos específicos del dominio en `@/core/internal_codes.py`

### 3. **Middleware de Manejo de Errores** (`@/shared/middlewares/`)

#### CatcherExceptions
Middleware principal que captura todas las excepciones:
- Manejo de HTTPException de FastAPI
- Manejo de NoResultFound de SQLAlchemy
- Manejo de excepciones personalizadas
- Conversión automática a formato de respuesta estandarizado

#### CatcherExceptionsPydantic
Middleware específico para errores de validación de Pydantic:
- Captura errores de validación de request body
- Formato consistente de errores de validación

### 4. **Sistema de Configuración** (`@/core/settings/`)

Configuración por ambientes usando Pydantic Settings:

```
settings/
├── base.py           # Configuración base
├── local.py          # Desarrollo local
├── development.py    # Ambiente de desarrollo
├── staging.py        # Ambiente de staging
├── production.py     # Ambiente de producción
└── testing.py        # Configuración para tests
```

**Convenciones:**
- Variables de entorno tipadas
- Validación automática de configuración
- Configuración específica por ambiente
- Soporte para múltiples bases de datos

### 5. **Sistema Multi-Base de Datos** (`@/db/`)

Template preparado para múltiples gestores de base de datos con **ejemplos funcionales**:

#### PostgreSQL (`@/db/postgresql/`)
```
postgresql/
├── base.py           # Clase base para modelos SQLAlchemy
├── connection.py     # Configuración de conexión
├── models/
│   └── public/       # Esquema 'public'
│       └── book.py   # Modelo de ejemplo
└── __init__.py       # Exports principales
```

- **SQLAlchemy 2.0**: ORM moderno con syntax moderna
- **Modelos tipados**: Full type hints y validación
- **Conexión singleton**: Reutilizable y eficiente

#### MongoDB (`@/db/mongo/`)
```
mongo/
├── base.py           # Clase base para documentos
├── connection.py     # Cliente MongoDB configurado
├── models/           # Modelos de documentos
└── __init__.py       # Exports principales
```

- **PyMongo**: Driver oficial de MongoDB
- **Pydantic Integration**: Modelos con validación automática
- **Async Ready**: Preparado para operaciones asíncronas

**Convenciones:**
- Modelos organizados por esquemas/colecciones
- Conexiones singleton pattern
- Configuración específica por ambiente
- **Extensible**: Fácil agregar Redis, DynamoDB, etc.

### 6. **Estructura de API Modular** (`@/api/`)

Sistema de versionado y organización modular por dominio:

```
api/
├── v1/                    # Versión 1 de la API
│   └── books/             # Módulo de dominio (ejemplo)
│       ├── endpoints.py   # Define los endpoints REST
│       ├── repositories.py # Acceso a la base de datos
│       ├── schema.py      # Modelos Pydantic (DTOs)
│       └── services.py    # Lógica de negocio
├── routers.py             # Registro de routers globales
└── endpoints.py           # Endpoints base (health, index)
```

**Convenciones del Módulo:**
- **endpoints.py**: Definición de rutas y validaciones de entrada
- **services.py**: Lógica de negocio, orquestación
- **repositories.py**: Acceso a datos, queries específicas
- **schema.py**: DTOs (Data Transfer Objects) con Pydantic

**Escalabilidad**: Puedes añadir más módulos (`users/`, `orders/`, etc.) siguiendo la misma estructura.

### 7. **Sistema de Testing** (`@/tests/`)

Suite completa de testing automatizado:

```
tests/
├── common/           # Utilities comunes para tests
├── utils/            # Utilidades de testing
├── v1/               # Tests específicos por versión
└── __init__.py       # Configuración de base de datos para tests
```

**Convenciones:**
- **Base de datos de testing separada**: Configuración automática via `environment_testing`
- **Fixtures reutilizables**: Utilities comunes en `tests/common/`
- **Cobertura automatizada**: Integrada en CI/CD con reportes detallados
- **Tests organizados por versión**: Estructura modular por versión de API
- **Setup automático**: El script `prepare_database()` crea esquemas y tablas necesarios cada vez que el runner arranca

### 8. **Stack Docker Integral** (`@/docker_images/`)

El proyecto organiza de forma integral las imágenes Docker para diferentes propósitos:

#### **Testing Docker** (`@/docker_images/testing/`)
Configuración especializada para testing contra **bases de datos reales** (no mocks):

- **`Dockerfile.testing`**: Imagen optimizada para ejecutar tests
- **`ci.env.sh`**: Script que configura variables de entorno para CI/CD
- **`entrypoint.sh`**: Orquesta la ejecución de tests y generación de reportes

**Selección de Bases de Datos en CI:**
```bash
# En ci.env.sh puedes seleccionar qué bases de datos levantar
export POSTGRESQL_URL="${GITHUB_DATABASE_POSTGRESQL:-$POSTGRESQL_URL}"
export MONGO_URL="${GITHUB_DATABASE_MONGODB:-$MONGO_URL}"
export REDIS_URL="${GITHUB_DATABASE_REDIS:-$REDIS_URL}"
```

Los tests se ejecutan contra **instanciones reales** de PostgreSQL, MongoDB y Redis en el runner de GitHub Actions.

#### **Build y Deploy Docker**
- **`docker_images/build/`**: Imagen para construcción optimizada
- **`docker_images/deploy/`**: Imagen final para deployment en AWS Lambda

## 🚀 Pipelines CI/CD Completos

### **Flujo Principal de GitHub Actions**

El pipeline ejecuta una secuencia completa y robusta:

#### **1. 🔍 Linting (Pre-commit)**
```yaml
- Ejecuta pre-commit para linting (configurado en .pre-commit-config.yaml)
- Formateo de código con Black
- Linting con Flake8  
- Type checking con MyPy
- Validación de imports y estructura
```

#### **2. 🧪 Testing con Bases de Datos Reales**
```yaml
services:
  postgres: # PostgreSQL 13 en puerto 5432
  mongodb:  # MongoDB 4.4 en puerto 27017  
  redis:    # Redis 6 en puerto 6379
```
- Levanta servicios reales de bases de datos
- Ejecuta tests contra instancias reales (no mocks)
- Genera reportes de cobertura detallados

#### **3. 📊 Cobertura y Badges**
- **Generación**: `coverage run`, `coverage xml`, `coverage-badge`
- **Archivado**: Usa `ronihdzz/git-archive-action@v3` para guardar artefactos
- **Storage**: Los reportes se almacenan en rama dedicada `artifacts`
- **Badges**: Se generan badges dinámicos de % de cobertura mostrados en README

#### **4. 🏗️ Build y Deploy**
- Construcción de imagen Docker optimizada para Lambda
- Push a Amazon ECR (Elastic Container Registry)
- Deploy automático a AWS Lambda
- Versionado automático por ambiente (dev/staging/prod)

### **Configuración de Ambientes**

```yaml
BRANCH_ENV_MAP: 
  "main": "prod"
  "development": "dev" 
  "staging": "stg"
```

Cada rama mapea automáticamente a su ambiente correspondiente.

## 📦 Dependencias y Tecnologías

### Core Dependencies
- **FastAPI**: Framework web moderno y rápido
- **Mangum**: Adaptador para AWS Lambda
- **Pydantic**: Validación de datos y settings
- **SQLAlchemy**: ORM para bases de datos relacionales
- **PyMongo**: Driver para MongoDB
- **Loguru**: Logging avanzado

### Development Dependencies
- **Pytest**: Framework de testing
- **Coverage**: Cobertura de código
- **MyPy**: Type checking
- **Pre-commit**: Hooks de pre-commit

## 🛠️ Comandos de Desarrollo

### Ejecutar el proyecto localmente
```bash
uvicorn main:app --reload --port=9595
```

### Ejecutar tests
```bash
pytest src/tests/ -v --cov=src
```

### Ejecutar pre-commit hooks
```bash
pre-commit run --all-files
```

### Type checking
```bash
mypy src/
```

### Testing con Docker
```bash
docker-compose -f docker-compose.yml up testing
```

## 🔍 Testing de Lambda Localmente

Para probar la función Lambda localmente:

```bash
curl -X POST "http://localhost:9100/2015-03-31/functions/function/invocations" \
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


## 🎯 **Ventajas del Template**

### **Para Desarrollo**
- **Serverless Ready**: Optimizado para AWS Lambda con Mangum
- **Multi-Database**: Soporte nativo para PostgreSQL, MongoDB, Redis
- **Type Safety**: Full TypeScript-like experience con MyPy
- **Error Handling**: Sistema robusto de manejo de errores con códigos internos

### **Para Testing**
- **Real Databases**: Tests contra bases de datos reales, no mocks
- **Automated Setup**: Creación automática de esquemas y datos de prueba
- **Coverage Tracking**: Reportes detallados con badges automáticos
- **Docker Isolated**: Ambiente de testing completamente aislado

### **Para CI/CD**
- **Full Pipeline**: Linting → Testing → Coverage → Build → Deploy
- **Multi-Environment**: Soporte automático para dev/staging/prod
- **Quality Gates**: Pre-commit hooks y validaciones automáticas
- **Artifact Management**: Storage automático de reportes y badges

### **Para Producción**
- **AWS Optimized**: Configurado para AWS Lambda + API Gateway
- **Environment Config**: Configuración tipada por ambiente
- **Monitoring Ready**: Logging estructurado con Loguru + Sentry
- **Scalable Architecture**: Estructura modular fácil de escalar
