# Guía de Onboarding Técnico — NovaTech S.A.

## 1. Tu primera semana

El primer día recibís tu laptop y tus cuentas (correo, Slack, GitHub y Bitwarden). A cada persona nueva se le asigna un buddy, que es un compañero con experiencia que responde dudas durante los primeros 60 días. Durante la primera semana tenés que completar la capacitación de seguridad y levantar el entorno local de desarrollo.

## 2. Stack tecnológico

Las aplicaciones de NovaTech se desarrollan con Python 3.11 y FastAPI. La base de datos principal es PostgreSQL 15. Todo servicio se empaqueta con Docker y se despliega con pipelines de GitHub Actions. La documentación técnica vive en NovaDocs, la wiki interna.

## 3. Convenciones de código

- Las ramas se nombran feature/ID-ticket-descripcion, por ejemplo feature/NT-142-login-mfa.
- Los mensajes de commit siguen la convención Conventional Commits (feat:, fix:, docs:).
- Todo Pull Request requiere 2 aprobaciones antes de hacer merge a main.
- La cobertura mínima de tests es del 80% para que el pipeline pase.
- El formato se controla con Black y el linting con Ruff; ambos corren automáticamente en el pipeline.

## 4. Entornos y despliegues

Existen tres entornos: dev, staging y prod. Los cambios deben pasar por staging antes de llegar a producción. Los despliegues a producción se realizan únicamente los martes y jueves entre las 10:00 y las 16:00 hs. Está prohibido desplegar a producción los viernes, salvo un hotfix aprobado por el líder técnico.

## 5. Guardia (on-call)

La guardia es rotativa y semanal: comienza los lunes a las 9:00 hs y termina el lunes siguiente a la misma hora. Quien está de guardia debe responder a las alertas críticas en un máximo de 15 minutos. Una persona nueva no entra en la rotación de guardia hasta cumplir 3 meses en la empresa. Cada guardia se compensa con 1 día libre dentro del mes siguiente.
