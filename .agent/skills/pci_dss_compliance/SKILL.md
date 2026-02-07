---
name: PCI-DSS Compliance
description: Payment card security, requirements, and audit preparation
---

# PCI-DSS Compliance Skill

## 12 Requirements

| # | Requirement |
|---|-------------|
| 1 | Install and maintain firewall |
| 2 | No vendor-supplied defaults |
| 3 | Protect stored cardholder data |
| 4 | Encrypt transmission over networks |
| 5 | Use and update anti-virus |
| 6 | Develop secure systems |
| 7 | Restrict access by need-to-know |
| 8 | Assign unique IDs |
| 9 | Restrict physical access |
| 10 | Track and monitor access |
| 11 | Test security systems |
| 12 | Maintain security policy |

## Cardholder Data

| Data Element | Storage Allowed | Protection |
|--------------|-----------------|------------|
| PAN (Card Number) | Yes | Encrypt or truncate |
| Cardholder Name | Yes | Protect per policy |
| Expiration | Yes | Protect per policy |
| CVV/CVC | **Never** | N/A |
| PIN | **Never** | N/A |

## PAN Display Rules

- Mask when displayed: `****-****-****-1234`
- Full PAN only for business need
- Never display CVV

## Encryption Requirements

| Data State | Requirement |
|------------|-------------|
| At rest | AES-256 or equivalent |
| In transit | TLS 1.2+ |
| Key management | Separate from data |

## Compliance Levels

| Level | Transactions/Year | Audit |
|-------|-------------------|-------|
| 1 | 6M+ | On-site QSA |
| 2 | 1M - 6M | SAQ + scan |
| 3 | 20K - 1M | SAQ + scan |
| 4 | < 20K | SAQ |

## Quick Wins

- Use Stripe/PayPal (reduces scope)
- Tokenization over storage
- Segment card environment
- Quarterly vulnerability scans
- Annual penetration test

## When to Apply
Use when handling payment cards, building checkout flows, or preparing for PCI audit.
