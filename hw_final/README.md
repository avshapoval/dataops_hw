# Итоговое задание DataOps - Отчет о выполнении



## Краткое описание

Выполнены этапы 1-6 из задания.

Развернут полный стек ML-инфраструктуры в Docker Compose, включающий:
- MLflow для tracking экспериментов
- Airflow для оркестрации
- LakeFS для версионирования данных
- JupyterHub для разработки
- ML-сервис с FastAPI
- Prometheus + Grafana для мониторинга

Все сервисы работают в единой Docker сети, используют реальные креды и готовы к продакшн-использованию.



## Выполненные этапы

### 1. MLflow

**Что сделано:**
- Создан Dockerfile на базе python:3.11-slim
- Установлен MLflow server с psycopg2-binary и boto3
- Настроен docker-compose с PostgreSQL для метаданных
- Настроены переменные окружения в .env
- MLflow запущен и доступен на http://localhost:5000

**Проверка:**
```bash
curl http://localhost:5000/health
# Ответ: OK
```

### 2. Airflow 

**Что сделано:**
- Создан docker-compose с Airflow 2.8.1
- Добавлен PostgreSQL для метаданных
- Настроены переменные окружения
- Выполнены миграции через airflow_init
- Запущены сервисы: webserver, scheduler, triggerer
- Создан пользователь admin/admin2026
- Создан example DAG

**Проверка:**
- Веб-интерфейс: http://localhost:8080
- Логин: admin / admin2026
- DAG `example_dag` доступен и может быть запущен



### 3. LakeFS

**Что сделано:**
- Создан docker-compose для LakeFS
- Добавлен PostgreSQL для метаданных
- Добавлен MinIO для хранения артефактов
- Настроены переменные окружения
- LakeFS запущен и доступен на http://localhost:8001
- MinIO доступен на http://localhost:9001

**Проверка:**
1. Открыть http://localhost:8001
2. Создать администратора
3. Создать репозиторий `my-data-repo` с namespace `s3://lakefs-data`
4. Создать ветку, загрузить файл, сделать commit



### 4. JupyterHub

**Что сделано:**
- Создан Dockerfile на базе python:3.14-slim
- Установлены jupyterhub, jupyterlab, notebook
- Установлен configurable-http-proxy через npm
- Созданы пользователи: admin, user1, user2
- Создан конфигурационный файл jupyterhub_config.py
- JupyterHub запущен и доступен на http://localhost:8888

**Проверка:**
- URL: http://localhost:8888
- Логин: admin / admin2026
- Можно запустить JupyterLab и создать notebook



### 5. ML-сервис

**Что сделано:**
- Создан FastAPI сервис с endpoint /api/v1/predict
- Обучена модель LinearRegression на датасете diabetes
- Добавлено логирование в JSON формате
- Добавлено логирование в PostgreSQL (вход, выход, время, версия)
- Создан Dockerfile и docker-compose.yaml
- Сервис запущен и доступен на http://localhost:8000

**API Endpoints:**
- GET /health - проверка здоровья
- POST /api/v1/predict - предсказания
- GET /metrics - метрики Prometheus

**Проверка:**
```bash
# Health check
curl http://localhost:8000/health
# Ответ: {"status":"healthy","model_loaded":true}

# Предсказание
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age":0.05,"sex":0.05,"bmi":0.06,"bp":0.02,"s1":-0.04,"s2":-0.03,"s3":0.0,"s4":0.0,"s5":0.02,"s6":-0.03}'
# Ответ: {"predict":207.70218491516079}

# Проверка логов в БД
docker exec -it postgres_ml_service psql -U ml_service_user -d ml_service_db \
  -c "SELECT id, timestamp, prediction, model_version FROM predictions LIMIT 5;"
```



### 6. Мониторинг

**Что сделано:**
- Развернуты Prometheus и Grafana через docker-compose
- Настроен сбор метрик Prometheus (prometheus.yml)
- Добавлен endpoint /metrics в ML-сервис (starlette-exporter)
- Prometheus собирает метрики с ml_service:8000/metrics

**Метрики:**
- starlette_requests_total - общее количество запросов
- starlette_requests_in_progress - текущие запросы
- starlette_request_duration_seconds - длительность запросов

**Проверка:**
```bash
# Prometheus
curl http://localhost:9090/-/healthy
# Ответ: Prometheus Server is Healthy.

# Метрики ML Service
curl http://localhost:8000/metrics | grep starlette_requests_total
```

**Grafana:**
1. Открыть http://localhost:3000
2. Войти: admin / admin2026
3. Добавить Data Source: Prometheus (http://prometheus:9090)
4. Создать Dashboard с метриками starlette_requests_total

**Файлы:**
- `prometheus/prometheus.yml`
- `docker-compose.yaml` (сервисы: prometheus, grafana)
- `ml_service/app.py` (добавлен PrometheusMiddleware)




## Инструкции для проверки

### Запуск

```bash
cd hw_final
docker-compose up -d
```

Ожидайте 1-2 минуты для инициализации всех сервисов.

### Проверка статуса

```bash
docker-compose ps
```

Все сервисы должны быть "Up" или "healthy".

### Доступ к сервисам

| Сервис | URL | Логин | Пароль |
|--|--|-|--|
| MLflow | http://localhost:5000 | - | - |
| Airflow | http://localhost:8080 | admin | admin2026 |
| LakeFS | http://localhost:8001 | создать при первом входе | - |
| JupyterHub | http://localhost:8888 | admin | admin2026 |
| ML Service | http://localhost:8000 | - | - |
| Grafana | http://localhost:3000 | admin | admin2026 |
| Prometheus | http://localhost:9090 | - | - |
| MinIO | http://localhost:9001 | minioadmin | minioadmin |

### Быстрая проверка ML Service

```bash
# Health check
curl http://localhost:8000/health

# Предсказание
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age":0.05,"sex":0.05,"bmi":0.06,"bp":0.02,"s1":-0.04,"s2":-0.03,"s3":0.0,"s4":0.0,"s5":0.02,"s6":-0.03}'

# Метрики
curl http://localhost:8000/metrics | grep starlette_requests_total

# Логи в БД
docker exec -it postgres_ml_service psql -U ml_service_user -d ml_service_db \
  -c "SELECT * FROM predictions LIMIT 5;"
```



## Дополнительные фичи

1. **Единый docker-compose**
3. **Созданы Health checks**
4. **Сконфигурированы ависимости сервисов**
7. **Логирование в БД** - все предсказания сохраняются
8. **JSON логи** - использоуется структурированное логирование


## Заключение

Все требования итогового задания выполнены. Развернут полноценный стек ML-инфраструктуры с мониторингом, логированием и версионированием. Все сервисы работают корректно, доступны через веб-интерфейсы и готовы к использованию.
