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
![alt text](<test POST from postman.PNG>)

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
![alt text](<test GET from postman.PNG>)

## Deployment

### Prerequisites
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3.11](https://www.python.org/downloads/)
- [Docker](https://hub.docker.com/search/?type=edition&offering=community) (for local testing)
- AWS Account and configured credentials

### How to deploy to AWS

```bash
# Validate the SAM template
sam validate

# Build the application
sam build --use-container

# Deploy with guided prompts
sam deploy --guided
```

During the guided deployment, you'll be prompted for:
- Stack Name: Name for your CloudFormation stack (e.g., "simple-log-service")
- AWS Region: Region to deploy to (e.g., "us-east-1")
- Confirm changes before deploy: Recommended "yes" for first deployment
- Allow SAM CLI IAM role creation: Enter "yes" (required for Lambda permissions)
- Save arguments to samconfig.toml: Enter "yes" to save settings for future deployments

After deployment completes, the output will show your API Gateway endpoint URL.

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

## Load Testing

The project includes a load testing script in the `test` directory to send 100 test log entries:

```bash
# Install requirements
pip install -r test/requirements.txt

# Run load test (replace with your API endpoint)
python test/load_test.py --url https://your-api-id.execute-api.region.amazonaws.com/Prod/
```
![alt text](<100 POST test using python script.PNG>)

## CI/CD

The project includes a GitHub Actions workflow in `.github/workflows/sam-pipeline.yml` for continuous integration and deployment. This pipeline will automatically:

1. Build and deploy your application whenever you push changes to the main branch
2. Deploy to AWS using the SAM CLI

To use the CI/CD pipeline:

```bash
# Add your changes
git add .

# Commit your changes
git commit -m "Your commit message"

# Push to the main branch
git push origin main
```

After pushing, GitHub Actions will automatically trigger the workflow defined in the sam-pipeline.yml file, and your changes will be deployed to AWS without manual intervention.

## Cleanup

To delete all resources created by this application:

```bash
sam delete
```