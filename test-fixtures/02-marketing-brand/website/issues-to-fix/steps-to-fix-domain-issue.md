---
title: Steps to Fix Domain Issue
tags: [website, troubleshooting, dns]
status: active
---

# Steps to Fix Domain Issue

## Problem Description

The symphonycore.com domain is not resolving correctly to our hosting provider.

## Root Cause

DNS records were not updated after migrating from old hosting provider.

## Solution Steps

1. Log into domain registrar (GoDaddy)
2. Navigate to DNS management
3. Update A record to point to: 192.168.1.100
4. Update CNAME for www to: symphonycore.com
5. Wait 24-48 hours for propagation

## Verification

Test DNS propagation:
- Use https://dnschecker.org
- Verify A record resolves correctly
- Test www and root domain

## Follow-up Actions

- Document new DNS configuration
- Set up monitoring alerts
- Update internal wiki
