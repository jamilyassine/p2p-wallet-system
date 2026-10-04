# Environment Strategy

## DEV
- Local development
- Docker Compose
- Local `.env`
- Local PostgreSQL

## UAT
- Deployed environment
- Separate database
- Environment variables managed by the deployment platform
- No production secrets

## PROD
- Production deployment
- Separate database
- Production secrets managed securely
- No secrets committed to Git