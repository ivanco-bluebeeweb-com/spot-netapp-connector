# Spot by NetApp Connector — Connector Discovery

**Vendor API Baseline:** https://spot.io

## Архитектура API
- **Базовый адрес:** `https://api.spotinst.io`
- **Протокол:** REST / HTTPS (JSON)
- **Аутентификация:** Personal Access Token (Authorization: Bearer <token>)
- **Ключевые эндпоинты:**
  - эласигруппы (/aws/ec2/elastigroup)
  - кластеры Ocean (/ocean/aws/k8s/cluster)
  - расчет экономии (/cost/analysis)
- **Тестовая точка проверки подключения:** `GET /aws/ec2/elastigroup`.
