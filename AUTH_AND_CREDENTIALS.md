# Spot by NetApp Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** Personal Access Token (Authorization: Bearer <token>)
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /aws/ec2/elastigroup`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
