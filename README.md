# Intelligent Cloud Cost Governance – Phase 2

An internal AWS cost monitoring and optimization dashboard built using Python, Flask, and AWS SDK (boto3).

This project analyzes AWS resource usage (EC2, S3, RDS), collects real-time cost data using AWS Cost Explorer and CloudWatch APIs, applies rule-based optimization logic, and provides actionable recommendations via a web dashboard.

---

## 🚀 Project Objective

To build an intelligent cloud cost monitoring system that:

- Discovers active AWS resources
- Collects usage metrics
- Retrieves cost data
- Applies optimization logic
- Displays recommendations through a web dashboard
- Stores historical data in Amazon S3

This is Phase 2 of the Cloud Cost Governance project, extending Phase 1 with multi-resource support and automation.

---

## 🏗 Architecture Overview

User → Flask Dashboard → Backend Pipeline → AWS APIs  
→ CloudWatch (metrics)  
→ Cost Explorer (billing)  
→ Optimization Engine  
→ S3 (historical storage)

---

## 🧠 Core Features

- Multi-resource discovery (EC2, S3, RDS)
- Cost analysis for:
  - 1 Day
  - 7 Days
  - 30 Days
- Rule-based optimization engine
- Historical cost storage in S3
- Interactive dashboard UI
- Automated pipeline execution
- Cron-based scheduling support

---

## ⚙️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core backend logic |
| Flask | Web dashboard |
| boto3 | AWS SDK integration |
| AWS EC2 | Compute resource |
| AWS S3 | Historical data storage |
| AWS Cost Explorer | Cost retrieval |
| AWS CloudWatch | Metrics collection |
| Git | Version control |
| GitHub | Code hosting |

---

## 📂 Project Structure

---

## 🔄 Pipeline Flow

1. Discover AWS resources
2. Collect CloudWatch metrics
3. Fetch cost from AWS Cost Explorer
4. Apply optimization rules
5. Detect anomalies
6. Store processed data in S3
7. Display results on dashboard

---

## 📊 Optimization Logic (Current)

This version uses **Rule-Based Optimization**, such as:

- If EC2 CPU utilization is very low → Suggest stop/downsize
- If S3 cost is detected → Suggest lifecycle policy
- If RDS is underutilized → Suggest instance resizing

⚠️ Note: This is not a full machine learning prediction model yet.

---

## 🔮 Future Enhancement (Planned)

- Real Machine Learning cost prediction model
- Time-series forecasting (ARIMA / Prophet)
- Dynamic multi-account support
- SaaS deployment
- Real-time cost trend charts

---

## 🛠 Setup Instructions

### 1️⃣ Launch EC2 Instance
- Amazon Linux 2023
- Attach IAM role with:
  - Cost Explorer access
  - CloudWatch read access
  - S3 access

### 2️⃣ Connect via SSH

```bash
ssh -i key.pem ec2-user@<public-ip>


