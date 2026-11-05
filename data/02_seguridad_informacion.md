# Política de Seguridad de la Información — NovaTech S.A.

## 1. Contraseñas y autenticación

Toda contraseña personal debe tener al menos 14 caracteres. Está prohibido reutilizar contraseñas entre sistemas. NovaTech provee un gestor de contraseñas corporativo (Bitwarden) y su uso es obligatorio para todo el personal.

La autenticación multifactor (MFA) es obligatoria en correo, VPN, repositorios de código y consola de la nube. Se recomienda usar una aplicación de autenticación; los códigos por SMS solo se aceptan como último recurso. Las contraseñas de las cuentas de servicio se rotan cada 180 días. Las cuentas personales no tienen rotación periódica forzada, salvo sospecha de compromiso.

## 2. Clasificación de la información

Los datos de NovaTech se clasifican en cuatro niveles:

- Pública: puede difundirse libremente (por ejemplo, contenido del sitio web).
- Interna: solo para personal de NovaTech (por ejemplo, procedimientos).
- Confidencial: datos de clientes y contratos; requiere acceso por necesidad.
- Restringida: credenciales, claves de cifrado y datos personales sensibles.

Los datos de nivel Restringida no pueden almacenarse ni abrirse en dispositivos personales (BYOD). Los datos Confidenciales solo pueden enviarse por canales aprobados por el equipo de Seguridad.

## 3. Dispositivos y redes

Todas las laptops corporativas deben tener el disco cifrado. Al conectarse desde redes públicas (cafés, aeropuertos, hoteles) el uso de la VPN corporativa es obligatorio. Está prohibido instalar software no incluido en el catálogo aprobado sin autorización del equipo de Seguridad.

## 4. Manejo de claves y secretos en código

Nunca se deben subir claves de API, tokens ni contraseñas a un repositorio, ni siquiera a uno privado. Los secretos locales se guardan en archivos .env incluidos en .gitignore, y en producción se usa el gestor de secretos de la nube. Si una clave se filtra por error, debe revocarse de inmediato y reportarse como incidente.

## 5. Reporte de incidentes

Cualquier incidente sospechoso (phishing, pérdida de un equipo, filtración de una clave) debe reportarse dentro de la primera hora de detectado, escribiendo a security@novatech.example y avisando en el canal de Slack #incidentes. Reportar a tiempo nunca es motivo de sanción; ocultar un incidente sí lo es.

## 6. Copias de seguridad y capacitación

Se realizan backups automáticos diarios de las bases de datos de producción, con una retención de 35 días. Cada trimestre el equipo de Seguridad ejecuta simulacros de phishing, y todo el personal debe completar una capacitación anual de concientización.
