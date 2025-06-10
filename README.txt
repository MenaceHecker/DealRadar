# DealRadar – Serverless Scraping + Alert System

DealRadar is a fully serverless system designed to scrape websites, detect changes, and send real-time alerts based on defined conditions (Currently trying to scrape the big ones like Amazon and Walmart). Built on AWS services including Lambda, EventBridge, DynamoDB, and SNS.

## Architecture Overview

- Scheduled scraping jobs via AWS EventBridge
- Serverless execution using AWS Lambda
- Data storage in DynamoDB
- Alert system via SNS email notifications
- Monitoring via CloudWatch Logs

## Tech Stack

- Python (scraper scripts)
- AWS Lambda
- AWS EventBridge (for scheduling)
- AWS DynamoDB
- AWS SNS (notifications)
- AWS CloudWatch (logging)

## Goals

- Scalability with serverless architecture
- Fault tolerance and error recovery
- Real-time alerting on specific conditions (e.g., price drop, new listing)

## 📚 Setup Instructions (Only this for the time being)
Setup the environment using : 
1. For Windows: .\venv\Scripts\activate 
2. For MacOS/Linux: source venv/bin/activate
