# PRD - WhatsApp MVP Telediario CDMX

## 🎯 MVP Scope (6-8 weeks)
**One Goal**: Replace current WhatsApp Web with a system that supports 8+ concurrent users without Meta blocks.

## 🚨 Critical Problems to Solve

| Problem | Current Impact | MVP Solution |
|---------|---------------|-------------|
| **4 user limit** | 50% of team can't access | 8+ concurrent users |
| **Meta blocks** | Complete service outage | WhatsApp Business API compliance |
| **Multimedia download fails** | Can't share content with production | Direct download to local storage |
| **Lost message history** | Can't follow up on stories | Persistent conversation storage |
| **No message forwarding** | Manual copy/paste to production chats | One-click forward to internal groups |

## 📋 MVP Requirements

### MUST HAVE (Non-negotiable)
```yaml
Concurrent Users:
  minimum: 8 active agents
  target: 12 agents
  test_criteria: All agents online simultaneously for 2+ hours

Message Management:
  receive: All WhatsApp message types (text, media, voice, location)
  send: Text responses + media forwarding
  history: 90+ days persistent storage
  search: By keyword, date, phone number

Multimedia Handling:
  download: Images, videos, voice notes, documents
  max_size: 16MB per file (WhatsApp limit)
  format_support: jpg, png, mp4, mp3, pdf, docx
  storage: Local download + cloud backup

Message Forwarding:
  target: Internal chat groups (Slack, Teams, or WhatsApp groups)
  one_click: Select message → forward to production
  batch_forward: Multiple messages at once

Reliability:
  uptime: 99.5% during business hours (5:30 AM - 11 PM)
  response_time: < 3 seconds message delivery
  zero_blocks: No Meta API violations for 30+ days
```

### NICE TO HAVE (Phase 2)
- Auto-categorization of messages
- Spam filtering
- Analytics dashboard
- Advanced search filters

### NOT IN MVP
- Chatbot responses
- AI message classification
- Custom workflows
- Video calling
- Voice messages playback

## 🏗️ Technical Architecture

### Core Stack Decision: Amazon Connect + AWS Amplify
```yaml
Contact Center: Amazon Connect (managed WhatsApp integration)
Frontend: React app hosted on AWS Amplify
WhatsApp Integration: AWS End User Messaging Social (WhatsApp Business API)
Database: DynamoDB (managed NoSQL)
File Storage: S3 for multimedia + CloudFront CDN
Authentication: Amazon Connect user management
Real-time: Amazon Connect Streams API
```

**Why Amazon Connect for MVP:**
- ✅ Managed WhatsApp Business API integration (no custom webhook handling)
- ✅ Built-in support for 100+ concurrent agents
- ✅ Contact Center Panel (CCP) handles message routing automatically
- ✅ AWS End User Messaging handles Meta API compliance
- ✅ Zero infrastructure management - focus on business logic
- ✅ 10-day implementation timeline proven

### Integration Points
```yaml
Input: 
  - WhatsApp messages via AWS End User Messaging
  - Amazon Connect Contact Flow routing
  
Output: 
  - Amazon Connect CCP (Contact Control Panel) 
  - Custom React interface via Connect Streams API
  - Forward API to internal chat systems
  - S3 direct download for multimedia files

Authentication: Amazon Connect agent authentication
Authorization: Connect Security Profiles (all agents same permissions for MVP)
```

## 🧪 Acceptance Criteria

### Test Scenarios
```yaml
Load Test:
  - 8 agents logged in simultaneously
  - 50+ messages received in 5 minutes
  - All multimedia downloads successful
  - No system degradation

Operational Test:
  - Agent receives WhatsApp with image
  - Agent downloads image in < 5 seconds
  - Agent forwards message to production chat
  - Agent searches previous messages by keyword
  - All actions complete successfully

Reliability Test:
  - System runs 24 hours without restart
  - No message loss during peak traffic
  - Meta API remains unblocked
```

### Success Metrics
```yaml
Technical:
  concurrent_users: 8+ without issues
  message_latency: < 3 seconds
  multimedia_download: < 5 seconds
  search_response: < 2 seconds
  uptime: 99.5%

Business:
  zero_meta_blocks: 30 consecutive days
  agent_satisfaction: > 8/10
  daily_operations: No manual workarounds needed
```

## 📱 User Stories (MVP Only)

```yaml
As an Agent:
  - I can log in and see all incoming WhatsApp messages
  - I can respond to messages with text
  - I can download any media file in one click
  - I can forward messages to production chat groups
  - I can search previous conversations by keyword
  - I can see who else is online (basic presence)

As a Coordinator:
  - I can see all active conversations across agents
  - I can reassign conversations between agents
  - I can access message history for story follow-ups
```

## 🚀 Implementation Phases

### Sprint 1-2: Amazon Connect Foundation (Weeks 1-2)
**Goal**: Basic WhatsApp message flow via Connect
```yaml
Amazon Connect Setup:
  - Create Connect instance with chat-only configuration
  - Configure 8+ agent accounts with WhatsApp permissions
  - Set up basic routing profiles and queues
  - Test agent login to Contact Control Panel (CCP)

AWS End User Messaging:
  - Register WhatsApp Business number
  - Configure event destinations to Connect
  - Test message routing from WhatsApp to Connect
  - Verify multimedia message handling

Basic Frontend (Amplify):
  - Create React app with Connect Streams SDK
  - Deploy to AWS Amplify for HTTPS hosting
  - Embed Connect CCP in custom interface
  - Test agent authentication and basic chat
```

### Sprint 3-4: Core Features Implementation (Weeks 3-4)
**Goal**: All MVP features working in Connect environment
```yaml
Enhanced Frontend:
  - Custom React components around Connect Streams API
  - Multimedia preview and download from S3
  - Message forwarding interface to production chats
  - Search functionality across Connect contact history
  - Agent presence and conversation management

Connect Customization:
  - Contact flows for WhatsApp message routing
  - Custom contact attributes for categorization
  - Lambda functions for message forwarding logic
  - DynamoDB tables for extended message history

Integration Layer:
  - Lambda functions for production chat forwarding
  - S3 event triggers for multimedia processing
  - CloudWatch monitoring and alerting
  - API Gateway for external integrations
```

### Sprint 5-6: Production Deployment (Weeks 5-6)
**Goal**: Stable production system with team onboarding
```yaml
Production Readiness:
  - Amplify production environment with custom domain
  - Connect production instance configuration
  - Load testing with 8+ concurrent agents
  - Performance optimization and caching

Migration & Training:
  - Gradual migration from WhatsApp Web
  - Team training on Connect CCP interface
  - Documentation and support procedures
  - 24/7 monitoring setup with CloudWatch

Operations:
  - Backup and disaster recovery procedures
  - Cost optimization and resource monitoring
  - Support escalation procedures
  - Performance baseline establishment
```

## 🔧 Development Guidelines

### Code Quality
```yaml
Keep it simple: Favor readable code over clever solutions
Single responsibility: Each function does one thing well
Error handling: Graceful degradation, never crash
Logging: All WhatsApp API interactions logged
Testing: Unit tests for core functions only
Documentation: README with setup and deployment steps
```

### API Design Principles
```yaml
RESTful: Standard HTTP methods and status codes
Consistent: Same patterns for all endpoints
Versioned: /api/v1/ prefix for future compatibility
Documented: OpenAPI/Swagger documentation
Secure: Authentication on all endpoints
```

### Database Design (DynamoDB)
```yaml
Connect Contact Records (Managed by Amazon Connect):
  - Contact ID, phone number, agent ID, timestamps
  - Built-in search and filtering capabilities
  - Automatic retention and compliance features

Extended Message Data (DynamoDB):
  - PK: contact_id, SK: timestamp
  - message_content, media_urls, forwarded_status
  - search_keywords, categories, agent_notes
  - GSI on phone_number for customer history

Agent Preferences (DynamoDB):
  - PK: agent_id
  - workspace_settings, notification_preferences
  - forwarding_destinations, quick_responses

Media Files (S3 + DynamoDB):
  - S3: Actual file storage with CloudFront CDN
  - DynamoDB: File metadata, access logs, sharing history
  - Lifecycle policies for automatic archival
```

### Amazon Connect Specific Configuration
```yaml
Instance Settings:
  identity_management: "Store users within Amazon Connect"
  telephony: Disabled (Chat/Messaging only)
  data_storage: Default S3 buckets for transcripts
  
Security Profiles:
  WhatsApp_Agent: CCP access, chat permissions, no voice
  WhatsApp_Supervisor: All agent permissions + reporting
  
Routing Profiles:
  WhatsApp_Basic: Chat concurrency 3, single queue
  Priority_Channels: [Chat: Priority 1]
  
Contact Flows:
  WhatsApp_Inbound: Route to available agent queue
  WhatsApp_Transfer: Enable agent-to-agent transfers
```

## 📞 Emergency Procedures

### System Down
1. **Immediate**: Switch to WhatsApp Web fallback
2. **Alert**: Notify development team via monitoring
3. **Investigate**: Check logs, database, API status
4. **Resolve**: Fix issue or roll back to last stable version
5. **Post-mortem**: Document cause and prevention

### Meta API Issues
1. **Identify**: Check Meta Business Manager for violations
2. **Review**: Analyze recent API calls in logs
3. **Mitigate**: Implement rate limiting if needed
4. **Contact**: Meta support if account suspended
5. **Prevent**: Update API usage patterns

### High Load Scenarios
1. **Monitor**: Watch response times and error rates
2. **Scale**: Increase server resources if available
3. **Queue**: Implement message queuing for peak loads
4. **Communicate**: Inform team of any service degradation
5. **Optimize**: Post-incident performance improvements

## 🎯 Definition of Done

### MVP Release Criteria
**Technical Readiness:**
- [ ] 8 agents can work simultaneously for 12+ hours
- [ ] All multimedia types download in < 5 seconds
- [ ] Message forwarding works to all production systems
- [ ] Search returns results in < 2 seconds
- [ ] Zero Meta API violations for 14 consecutive days
- [ ] System uptime > 99.5% for 1 week

**Business Readiness:**
- [ ] Team trained on new system
- [ ] All daily workflows tested and documented
- [ ] Fallback procedures established
- [ ] Support procedures documented
- [ ] Performance baselines established

**Success Definition:**
> "The newsroom team operates for one full week without mentioning WhatsApp problems or requesting WhatsApp Web access."

## 📊 Key Performance Indicators

### Technical KPIs
```yaml
Availability: 99.9% (Amazon Connect SLA + Amplify SLA)
Performance: 
  - Message delivery: < 2 seconds (Connect Streams real-time)
  - File download: < 3 seconds (S3 + CloudFront CDN)  
  - Search response: < 1 second (DynamoDB + Connect search)
Capacity: 12+ concurrent users (Connect scales automatically)
Reliability: Zero unplanned downtime per week
```

### Business KPIs
```yaml
Operational Efficiency:
  - 50% reduction in message processing time vs WhatsApp Web
  - 100% multimedia accessibility and download success
  - Zero production delays due to WhatsApp system issues

User Satisfaction:
  - Agent satisfaction score: > 8/10
  - Zero requests to return to WhatsApp Web after 2 weeks
  - < 1 support ticket per week after training period

Content Flow:
  - 100% message forwarding success rate
  - < 30 seconds from WhatsApp to production chat
  - Zero lost breaking news due to Connect system issues
```

## 🏗️ AWS Architecture Overview

### Core Services
```yaml
Amazon Connect:
  - Purpose: Contact center platform with WhatsApp integration
  - Config: Chat-only instance, 12 agent licenses
  - Features: CCP interface, automatic routing, real-time analytics

AWS Amplify:
  - Purpose: Frontend hosting with CI/CD
  - Config: React app with Connect Streams SDK
  - Features: HTTPS, custom domain, auto-scaling, CDN

AWS End User Messaging Social:
  - Purpose: WhatsApp Business API integration
  - Config: Event destinations to Connect
  - Features: Managed Meta compliance, automatic scaling

DynamoDB:
  - Purpose: Extended message metadata and agent preferences
  - Config: On-demand billing, point-in-time recovery
  - Features: Fast search, automatic scaling, Connect integration

S3 + CloudFront:
  - Purpose: Multimedia file storage and delivery
  - Config: Versioning enabled, lifecycle policies
  - Features: Global CDN, automatic compression, HTTPS
```

### Development Workflow
```yaml
Code Repository: AWS CodeCommit (or GitHub)
CI/CD Pipeline: AWS Amplify Console
Frontend Deployment: Amplify (automatic on git push)
Backend Functions: Lambda (triggered by Connect events)
Monitoring: CloudWatch (Connect + Amplify + Lambda metrics)
```

## 🔄 Post-MVP Roadmap

### Phase 2: Intelligence (Weeks 9-12)
- Message categorization (denuncias/promociones/otros)
- Basic spam filtering
- Trending topics dashboard
- Agent workload balancing

### Phase 3: Automation (Weeks 13-16)
- Smart message routing
- Automated data collection for news stories
- Integration with newsroom management systems
- Advanced analytics and reporting

### Phase 4: Scale (Weeks 17-20)
- Multi-location support
- Advanced workflow automation
- AI-powered content insights
- Full newsroom integration

---

## 📝 Development Notes

### Critical Dependencies
- WhatsApp Business API approval (can take 1-2 weeks)
- Meta Business Manager setup
- Production chat system APIs (Slack/Teams)
- Cloud infrastructure provisioning

### Risk Mitigation
- **Meta API Changes**: Monitor Meta developer updates weekly
- **Peak Load**: Implement auto-scaling from day one
- **Team Adoption**: Gradual migration with parallel systems
- **Data Loss**: Real-time backups and replication

### Architecture Decisions
- **Monolith vs Microservices**: Monolith for MVP simplicity
- **Database**: PostgreSQL for ACID compliance and search
- **Real-time**: WebSockets for instant message delivery
- **Files**: S3-compatible storage with CDN for media
- **Auth**: Simple session-based, OAuth2 for Phase 2

---

*This PRD is a living document. Update as requirements evolve, but maintain MVP focus until successful deployment.*