# Cursor Context - WhatsApp Telediario CDMX

## 🎯 Proyecto MVP (6-8 semanas)

**Cliente**: Telediario CDMX (Newsroom - Canal de TV)  
**Problema crítico**: WhatsApp actual soporta 4 usuarios, necesitan 8+ concurrentes  
**Operación**: 24/7, manejo de denuncias ciudadanas y contenido multimedia  

## 🏗️ Arquitectura MVP Recomendada

**RECHAZADA**: Amazon Connect (over-engineering para este MVP)  
**APROBADA**: WhatsApp Business API + AWS Serverless Simple Stack

```
WhatsApp Business API
    ↓
API Gateway (webhook receiver)
    ↓ 
Lambda Functions (message processing)
    ↓
DynamoDB (conversations + metadata)
    ↓
S3 (multimedia storage)
    ↓
React Frontend (newsroom interface)
```

**Justificación**: La solución más simple que resuelve todos los problemas MVP.

## 📋 Requerimientos MVP ÚNICAMENTE

### MUST HAVE (Sprint 1-6)
- ✅ 8+ usuarios concurrentes sin bloqueos Meta
- ✅ Descarga/upload multimedia eficiente (fotos/videos)
- ✅ Historial completo de conversaciones (sin límite temporal)
- ✅ Reenvío de mensajes/media a otros grupos WhatsApp
- ✅ Búsqueda básica por keyword/fecha/ubicación

### PROHIBIDO EN MVP
- ❌ Chatbots/AI responses (equipo rechaza explícitamente)
- ❌ Analytics complejos 
- ❌ Microservices
- ❌ Workspaces avanzados
- ❌ Machine learning
- ❌ Real-time dashboards

## 🛠️ Stack Técnico MVP

### Backend
```yaml
API: WhatsApp Business API (oficial Meta)
Compute: AWS Lambda (Node.js 18+)
Database: DynamoDB 
Storage: S3 (multimedia)
API Gateway: AWS API Gateway REST
Auth: AWS Cognito (simple)
```

### Frontend  
```yaml
Framework: React 18 + TypeScript
Styling: Tailwind CSS
State: React Query + Zustand
Build: Vite
Deploy: AWS Amplify
```

### Integraciones Críticas
- WhatsApp Business API (webhook + send message)
- S3 pre-signed URLs (multimedia)
- DynamoDB streams (real-time updates)

## 📐 Principios de Desarrollo

1. **MVP ONLY**: Solo código que resuelve problemas documentados
2. **Zero Abstractions**: No frameworks custom, usar managed services
3. **Performance**: Sub-2s response times, manejar picos de tráfico
4. **Meta Compliance**: Seguir políticas WhatsApp al pie de la letra

## 🗂️ Estructura de Proyecto

```
whatsapp-telediario/
├── backend/
│   ├── functions/
│   │   ├── webhook-handler/     # Recibe msgs WhatsApp
│   │   ├── message-sender/      # Envía msgs/media
│   │   ├── media-processor/     # S3 upload/download
│   │   └── search-service/      # Búsqueda mensajes
│   ├── lib/
│   │   ├── whatsapp-client.js   # WhatsApp Business API
│   │   ├── dynamodb-utils.js    # DB operations
│   │   └── s3-utils.js          # Media handling
│   └── infrastructure/          # CDK/Terraform
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MessageList/     # Lista conversaciones
│   │   │   ├── MediaViewer/     # Preview fotos/videos  
│   │   │   ├── SearchBar/       # Búsqueda mensajes
│   │   │   └── ForwardModal/    # Reenvío a grupos
│   │   ├── hooks/
│   │   │   ├── useMessages.js   # React Query msgs
│   │   │   ├── useMediaUpload.js # S3 upload
│   │   │   └── useSearch.js     # Búsqueda real-time
│   │   └── utils/
│   │       ├── whatsapp-api.js  # API client
│   │       └── media-utils.js   # File handling
└── docs/
    └── api-specs.md             # WhatsApp webhook format
```

## 🎯 Features MVP por Sprint

### Sprint 1-2: Base Infrastructure
- WhatsApp Business API setup + webhook
- DynamoDB schema (conversations, messages, media)
- Basic Lambda functions (receive/send)
- S3 bucket + pre-signed URLs

### Sprint 3-4: Core Functionality  
- Frontend message interface
- Media download/upload
- Multi-user concurrent access
- Basic search (keyword)

### Sprint 5-6: Production Ready
- Message forwarding to groups
- Performance optimization
- Meta compliance validation
- Production deployment

## 🔧 Configuraciones Críticas

### WhatsApp Business API
```javascript
// Webhook verification (requerido por Meta)
const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN;
const ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN;
const PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID;
```

### DynamoDB Schema
```javascript
// conversations table
{
  PK: "CONVERSATION#{phone_number}",
  SK: "METADATA",
  phoneNumber: string,
  contactName: string,
  lastMessage: timestamp,
  messageCount: number,
  tags: [string], // "denuncia", "promocion", etc
}

// messages table  
{
  PK: "CONVERSATION#{phone_number}",
  SK: "MESSAGE#{timestamp}",
  messageId: string,
  type: "text|image|video|audio",
  content: string,
  mediaUrl?: string,
  direction: "inbound|outbound",
  timestamp: number,
  processed: boolean
}
```

## 🚫 Anti-Patterns para este MVP

- No usar Redux (Zustand es suficiente)
- No hacer real-time con WebSockets (polling es OK)
- No optimizar prematuramente (DynamoDB scan está OK para MVP)
- No agregar autenticación compleja (Cognito básico)

## ✅ Definition of Done MVP

**Technical**:
- 8 users concurrent sin degradación
- Multimedia download < 5 segundos  
- Zero bloqueos Meta por 30 días
- Search results < 2 segundos

**Business**:
- Equipo puede procesar denuncias sin interrupciones
- Reducción 40% tiempo de procesamiento vs sistema actual

## 📞 Casos de Uso Críticos

1. **Recepción Denuncia**: Usuario envía foto + texto → Sistema categoriza → Newsroom ve en interface
2. **Búsqueda Rápida**: Productor busca "Iztacalco choque" → Ve todos mensajes relacionados
3. **Reenvío Contenido**: Editor selecciona foto → Reenvía a grupo de producción
4. **Multi-usuario**: 8 personas acceden simultáneamente sin conflictos

---

**Mantra MVP**: "La mejor arquitectura es la que permite al equipo hacer su trabajo sin pensar en la tecnología"

Cursor: Enfócate solo en resolver estos problemas MVP con la máxima simplicidad. Cualquier código que no resuelva directamente estos casos de uso está fuera de scope.