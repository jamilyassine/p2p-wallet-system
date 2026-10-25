# Deployment Documentation

## UAT Environment

- **Platform:** AWS
- **EC2 instance:** `wallet-uat-api`
- **Region:** `eu-north-1`
- **Frontend:** Next.js, port 3000
- **Backend:** FastAPI, port 8000
- **Database:** AWS RDS PostgreSQL
- **Docker Compose:** `docker-compose.uat.yml`

## Deployment Validation

Check	                                       Result
Docker Compose configuration	                 PASS
Backend health endpoint	                         PASS
Database connectivity	                         PASS
Frontend responds after restart	                 PASS
Login and dashboard	                             PASS
Transfer history	                             PASS
Sender and recipient balances	                 PASS
Successful transfer ledger entries	             PASS
Failed transfer handling	                     PASS
Recipient notifications	                         PASS
Container restart recovery	                     PASS

## Financial Validation

- Sender balance after testing: **$73.99**
- Recipient balance after testing: **$26.01**
- Successful incoming transfers: $25.00, $0.01 and $1.00.
- The failed $100.00 transfer did not reduce the sender's balance.
- Recipient balance matched successful incoming transfers.
- Verified ledger entries matched the successful transfers.

## Known Limitations and Follow-up

- UAT currently uses HTTP. HTTPS and domain configuration are planned for Day 4.
- Frontend validation has been performed manually. Automated frontend checks are planned for the CI/CD phase.
- Confirm the RDS security-group configuration follows the intended database access design.
- Frontend and backend ports are restricted by inbound security-group rules to a specific public IP.

## Security Notes

- Do not commit credentials or secrets to Git.
- The UAT database runs separately on AWS RDS.
- Repeat health, authentication, transfer, balance and ledger checks after significant deployment changes.