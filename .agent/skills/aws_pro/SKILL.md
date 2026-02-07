---
name: AWS Pro
description: EC2, S3, Lambda, IAM, and cloud architecture best practices
---

# AWS Pro Skill

## Core Services

| Service | Use For |
|---------|---------|
| EC2 | Virtual servers |
| S3 | Object storage |
| RDS | Managed databases |
| Lambda | Serverless functions |
| CloudFront | CDN |
| Route 53 | DNS |
| IAM | Access control |

## IAM Best Practices

- Use roles, not users for applications
- Least privilege principle
- Enable MFA for root and all users
- Use groups to assign permissions
- Rotate credentials regularly

## S3 Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

## Lambda Function

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello!'})
    }
```

## Cost Optimization

| Strategy | Savings |
|----------|---------|
| Reserved Instances | Up to 72% |
| Spot Instances | Up to 90% |
| Right-sizing | Variable |
| Auto-scaling | Pay for use |

## CLI Commands

```bash
# S3
aws s3 cp file.txt s3://bucket/
aws s3 sync ./folder s3://bucket/folder

# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-xxx

# Lambda
aws lambda invoke --function-name myFunc output.json
```

## When to Apply
Use when deploying to AWS, designing cloud architecture, or optimizing costs.
