# Simple Log Service

A serverless application for storing and retrieving log entries using AWS Lambda, API Gateway, and DynamoDB.

## Overview

Simple Log Service provides a straightforward API for:
- Saving log entries with severity levels and messages
- Retrieving the most recent logs (up to 100 entries)

The application is built using AWS Serverless Application Model (SAM) and consists of:
- Two Lambda functions (Python 3.11)
- A DynamoDB table for log storage
- API Gateway endpoints

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  API POST   │     │  Save Log   │     │             │
│   /log      │────▶│   Lambda    │────▶│  DynamoDB   │
└─────────────┘     └─────────────┘     │  LogTable   │
                                        │             │
┌─────────────┐     ┌─────────────┐     │             │
│  API GET    │     │  Get Logs   │     │             │
│   /logs     │────▶│   Lambda    │◀────│             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## API Endpoints

### POST /log
Saves a new log entry to the database.

**Request Body:**
```json
{
  "Severity": "info",
  "Message": "This is a log message"
}
```

**Response:**
```json
{
  "message": "Log saved successfully."
}
```

### GET /logs
Retrieves the 100 most recent log entries, sorted by timestamp (newest first).

**Response:**
```json
[
  {
    "ID": "uuid-string",
    "DateTime": "2023-04-01T12:34:56.789",
    "Severity": "info",
    "Message": "This is a log message"
  },
  ...
]
```

## Deployment

### Prerequisites
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3.11](https://www.python.org/downloads/)
- [Docker](https://hub.docker.com/search/?type=edition&offering=community) (for local testing)
- AWS Account and configured credentials

### Deploy to AWS

```bash
# Build the application
sam build --use-container

# Deploy with guided prompts
sam deploy --guided
```

### Local Testing

```bash
# Start API locally
sam local start-api

# Test saving a log
curl -X POST http://localhost:3000/log \
  -H "Content-Type: application/json" \
  -d '{"Severity": "info", "Message": "Test log message"}'

# Get logs
curl http://localhost:3000/logs
```

You can also use the provided event files to test individual functions:

```bash
# Test save_log function
sam local invoke SaveLogFunction --event events/save_log_event.json

# Test get_logs function
sam local invoke GetLogsFunction --event events/get_logs_event.json
```

## Load Testing

The project includes a load testing script in the `test` directory:

```bash
# Install requirements
pip install -r test/requirements.txt

# Run load test (replace with your API endpoint)
python test/load_test.py --url https://your-api-id.execute-api.region.amazonaws.com/Prod/
```

## CI/CD

The project includes a GitHub Actions workflow in `.github/workflows/sam-pipeline.yml` for continuous integration and deployment.

## Cleanup

To delete all resources created by this application:

```bash
sam delete
```