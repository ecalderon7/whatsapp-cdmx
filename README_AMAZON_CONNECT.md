# Amazon Connect Configuration Review Tool

Script en Python para conectarse a tu instancia de Amazon Connect y revisar toda la configuración actual.

## 🚀 Instalación Rápida

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar credenciales AWS** (elige una opción):
   
   **Opción A - AWS CLI (Recomendado):**
   ```bash
   aws configure
   ```
   
   **Opción B - Variables de entorno:**
   ```bash
   export AWS_ACCESS_KEY_ID=tu_access_key
   export AWS_SECRET_ACCESS_KEY=tu_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```
   
   **Opción C - IAM Role** (si ejecutas en EC2/Lambda)

3. **Ejecutar el script:**
   ```bash
   python amazon_connect_review.py
   ```

## 📋 Uso del Script

### Comandos Básicos

```bash
# Revisión básica en región us-east-1
python amazon_connect_review.py

# Especificar región diferente
python amazon_connect_review.py --region us-west-2

# Usar un perfil AWS específico
python amazon_connect_review.py --profile mi-perfil-aws

# Exportar configuración a JSON
python amazon_connect_review.py --export-json

# Revisión completa con todas las opciones
python amazon_connect_review.py --region us-west-2 --profile production --export-json
```

### Opciones Disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--region` | Región AWS donde está tu instancia | `--region us-west-2` |
| `--profile` | Perfil AWS a usar | `--profile production` |
| `--export-json` | Exporta la configuración a archivo JSON | `--export-json` |

## 🔍 Qué Información Muestra

El script revisa y muestra:

### 📋 **Instancias**
- ID y ARN de la instancia
- Alias y estado
- URLs de acceso
- Configuración de llamadas entrantes/salientes
- Tipo de gestión de identidades

### 📞 **Colas (Queues)**
- Lista de todas las colas
- IDs y ARNs
- Tipos de colas

### 👥 **Usuarios/Agentes**
- Lista de usuarios configurados
- IDs y nombres de usuario
- ARNs de usuarios

### 🔄 **Flujos de Contacto**
- Todos los contact flows configurados
- Estados (activos/inactivos)
- Tipos de flujos agrupados

### 📱 **Números de Teléfono**
- Números asociados a la instancia
- Tipos de números
- Códigos de país

### 🕐 **Horarios de Operación**
- Horarios configurados
- IDs y nombres

## 📁 Archivos de Salida

### Exportación JSON
Cuando usas `--export-json`, el script genera:

```
amazon_connect_config_YYYYMMDD_HHMMSS.json
```

**Estructura del archivo:**
```json
{
  "review_timestamp": "2024-01-15T10:30:45Z",
  "region": "us-east-1",
  "instances": [
    {
      "summary": {...},
      "details": {...},
      "queues": [...],
      "users": [...],
      "contact_flows": [...],
      "phone_numbers": [...],
      "hours_of_operations": [...]
    }
  ]
}
```

## 🔐 Permisos AWS Requeridos

Tu usuario/rol AWS necesita estos permisos mínimos:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "connect:ListInstances",
                "connect:DescribeInstance",
                "connect:ListQueues",
                "connect:ListUsers",
                "connect:ListContactFlows",
                "connect:ListPhoneNumbers",
                "connect:ListHoursOfOperations"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🚨 Solución de Problemas

### Error: No se encontraron credenciales AWS
```bash
❌ Error: No se encontraron credenciales AWS.
```
**Solución:**
1. Ejecuta `aws configure`
2. O configura variables de entorno
3. O asigna un IAM role si estás en EC2

### Error: AccessDenied
```bash
❌ Error obteniendo instancias: An error occurred (AccessDenied)
```
**Solución:**
- Verifica que tu usuario tiene los permisos de Amazon Connect listados arriba
- Verifica que estás en la región correcta

### Error: No se encontraron instancias
```bash
❌ No se encontraron instancias de Amazon Connect
```
**Posibles causas:**
- No tienes instancias de Amazon Connect en esa región
- Estás en la región incorrecta (usa `--region`)
- No tienes permisos para listar instancias

## 💡 Casos de Uso

### 1. Auditoría de Configuración
```bash
python amazon_connect_review.py --export-json
```
Genera un snapshot completo de tu configuración actual.

### 2. Revisión Multi-Región
```bash
python amazon_connect_review.py --region us-east-1
python amazon_connect_review.py --region us-west-2
```
Revisa instancias en múltiples regiones.

### 3. Revisión de Producción
```bash
python amazon_connect_review.py --profile production --region us-east-1 --export-json
```
Revisa el entorno de producción usando un perfil específico.

## 🔗 Recursos Adicionales

- [Amazon Connect Documentation](https://docs.aws.amazon.com/connect/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 📞 Contexto del Proyecto

> **Nota:** Este script fue creado para revisar Amazon Connect, aunque el proyecto WhatsApp CDMX rechazó esta solución por ser "over-engineering" para las necesidades del MVP. La solución recomendada para el proyecto es WhatsApp Business API + AWS Serverless.

Para más contexto del proyecto, consulta `context.md`.