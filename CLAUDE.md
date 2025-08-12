# WhatsApp CDMX - Claude Code Configuration

## Project Overview
WhatsApp CDMX - Starting with Amazon Connect + WABA proof of concept to validate core messaging functionality before full MVP implementation.

## Current Phase: Proof of Concept (PoC)
**Goal**: Test Amazon Connect's ability to receive and respond to WhatsApp messages via WABA using the Contact Control Panel (CCP).

**PoC Success Criteria**:
- ✅ Receive WhatsApp message in Amazon Connect
- ✅ Agent sees message in CCP interface  
- ✅ Agent responds via CCP
- ✅ Response delivered to WhatsApp user
- ✅ Conversation flow maintained

## Technology Stack

### PoC Phase (Minimal Setup)
- **Contact Center**: Amazon Connect (chat-only instance)
- **WhatsApp Integration**: AWS End User Messaging Social + WABA
- **Agent Interface**: Amazon Connect CCP (web-based)
- **Authentication**: Amazon Connect built-in user management

### Future MVP Stack
- **Frontend**: React + AWS Amplify
- **Database**: DynamoDB
- **Storage**: S3 + CloudFront
- **Real-time**: Connect Streams API

## Development Commands

### PoC Phase Commands
```bash
# AWS CLI Configuration
aws configure

# List Connect instances
aws connect list-instances

# Check Connect instance status
aws connect describe-instance --instance-id your-instance-id

# Test WABA webhook
curl -X POST https://your-webhook-url.amazonaws.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'

# Monitor Connect real-time metrics
aws connect get-current-metric-data --instance-id your-instance-id

# Check End User Messaging configuration
aws socialmessaging describe-whatsapp-channel-configuration
```

### Future MVP Commands
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Deploy to Amplify
amplify push

# Update Connect configuration
aws connect update-instance-attribute
```

## Project Structure
```
/
├── src/
│   ├── components/          # React components
│   ├── services/           # AWS service integrations
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   └── types/              # TypeScript definitions
├── amplify/                # AWS Amplify configuration
├── lambda/                 # Lambda function code
├── docs/                   # Project documentation
└── tests/                  # Test files
```

## Environment Variables

### PoC Phase (Required)
```bash
# AWS Configuration
AWS_REGION=us-east-1
CONNECT_INSTANCE_ID=your-poc-connect-instance-id
CONNECT_CONTACT_FLOW_ID=your-basic-contact-flow-id

# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_BUSINESS_ACCOUNT_ID=your-business-account-id
META_ACCESS_TOKEN=your-temporary-access-token

# End User Messaging
END_USER_MESSAGING_CONFIGURATION_ARN=your-configuration-arn
WEBHOOK_VERIFICATION_TOKEN=your-webhook-verification-token
```

### Future MVP Phase
```bash
# Database
DYNAMODB_TABLE_MESSAGES=whatsapp-messages
DYNAMODB_TABLE_AGENTS=whatsapp-agents

# Storage
S3_BUCKET_MEDIA=whatsapp-media-files
CLOUDFRONT_DOMAIN=your-cloudfront-domain
```

## Key Features Implementation

### Message Handling
- Receive all WhatsApp message types via AWS End User Messaging
- Route messages through Amazon Connect contact flows
- Store extended metadata in DynamoDB
- Real-time updates via Connect Streams API

### Multimedia Management
- Download images, videos, documents from S3
- CloudFront CDN for fast global delivery
- Automatic file processing and thumbnails
- Secure presigned URLs for access control

### Agent Operations
- Connect CCP embedded in React interface
- Multi-agent conversation management
- Message forwarding to production systems
- Search across conversation history

## Development Guidelines

### Code Quality
- TypeScript for type safety
- ESLint + Prettier for code formatting
- Jest for unit testing
- React Testing Library for component tests

### AWS Best Practices
- IAM roles with least privilege access
- CloudWatch monitoring and alerting
- Cost optimization with resource tagging
- Security compliance with encryption

### Performance Targets
- Message delivery: < 2 seconds
- File download: < 3 seconds
- Search response: < 1 second
- System uptime: 99.9%

## Troubleshooting

### Common Issues
1. **Connect CCP not loading**: Check CORS configuration
2. **Messages not routing**: Verify contact flow setup
3. **File downloads failing**: Check S3 permissions
4. **High latency**: Review CloudWatch metrics

### Support Contacts
- AWS Connect Support: Technical issues
- Meta Business Support: WhatsApp API issues
- Team Lead: Feature requirements and priorities

## Security Considerations
- All data encrypted in transit and at rest
- VPC configuration for network isolation
- Regular security audits and compliance checks
- Access logs for all user actions

## Monitoring and Alerts
- CloudWatch dashboards for real-time metrics
- SNS alerts for system issues
- Connect real-time metrics for agent performance
- Cost monitoring and budget alerts

## Backup and Recovery
- DynamoDB point-in-time recovery enabled
- S3 versioning for file protection
- Automated daily backups to secondary region
- Disaster recovery procedures documented