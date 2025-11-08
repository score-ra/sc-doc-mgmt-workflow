# Email Subdomain Setup Validation Checklist

**Client Name:** ___________________________  
**Domain:** ___________________________  
**Setup Date:** ___________________________  
**Completed By:** ___________________________

---

## Pre-Setup Validation

- [ ] Client domain name confirmed and accessible
- [ ] DNS provider credentials obtained and tested
- [ ] GHL agency account access verified
- [ ] Subdomain prefix selected and documented
- [ ] Email purpose identified (general, marketing, transactional)

---

## DNS Configuration Validation

### SPF Record
- [ ] SPF record created with Type: TXT
- [ ] Record Name matches subdomain prefix
- [ ] Record Value: `v=spf1 include:mailgun.org ~all`
- [ ] TTL set to 3600
- [ ] Record saved in DNS provider

### DKIM Records
- [ ] First DKIM record added exactly as provided by GHL
- [ ] Second DKIM record added exactly as provided by GHL
- [ ] Both records use Type: TXT
- [ ] Both records have TTL: 3600
- [ ] No modifications made to GHL-provided values

### DMARC Record
- [ ] DMARC record added to root domain (not subdomain)
- [ ] Record Name: _dmarc
- [ ] Record Value: `v=DMARC1; p=none; rua=mailto:[email]`
- [ ] Email address for reports is valid and monitored
- [ ] TTL set to 3600

### DNS Propagation
- [ ] Waited minimum 15-30 minutes after adding records
- [ ] Verified records using whatsmydns.net or similar tool
- [ ] All records showing globally propagated
- [ ] No DNS errors or warnings displayed

---

## GHL Configuration Validation

### Domain Setup
- [ ] Dedicated sending domain created in GHL
- [ ] Subdomain entered correctly (no typos)
- [ ] DNS records copied from GHL interface

### Default Headers
- [ ] Default From Name configured
- [ ] From Name uses format: "[Name] from [Company]"
- [ ] From Name avoids generic terms (Admin, System)
- [ ] Default From Email configured
- [ ] From Email uses root domain (not subdomain)
- [ ] From Email domain matches root of sending subdomain
- [ ] Headers saved successfully

### Verification
- [ ] "Verify DNS" button clicked in GHL
- [ ] SPF shows green checkmark/verified status
- [ ] DKIM shows green checkmark/verified status
- [ ] DMARC shows green checkmark/verified status
- [ ] All three authentication methods passing

---

## Sub-Account Configuration Validation

- [ ] Navigated to Sub-Account Settings > Email Services
- [ ] Dedicated domain selected as default sending domain
- [ ] Email Verification toggle enabled
- [ ] Settings saved successfully
- [ ] Domain appears in email builder dropdown
- [ ] Domain selectable when creating new campaign

---

## Functional Testing

### Test Email Send
- [ ] Test email sent from subdomain
- [ ] Email delivered successfully (not bounced)
- [ ] Email received in inbox (not spam folder)
- [ ] Sender name displays correctly
- [ ] Reply-to address works as expected

### Authentication Testing
- [ ] Email sent to mail-tester.com
- [ ] Mail-tester score is 8/10 or higher
- [ ] SPF check passing in mail-tester report
- [ ] DKIM check passing in mail-tester report
- [ ] DMARC check passing in mail-tester report

### Multi-Provider Inbox Testing
- [ ] Test email sent to Gmail account - delivered to inbox
- [ ] Test email sent to Outlook account - delivered to inbox
- [ ] Test email sent to Yahoo account - delivered to inbox
- [ ] Email headers reviewed for authentication passes

---

## Post-Setup Validation (24-48 Hours Later)

- [ ] DNS records still showing as verified in GHL
- [ ] No DNS propagation issues reported
- [ ] Second round of test emails sent
- [ ] All test emails continue to pass authentication
- [ ] No deliverability warnings in GHL dashboard

---

## Documentation

- [ ] All DNS record values documented in client file
- [ ] Subdomain configuration details saved
- [ ] Default headers recorded for reference
- [ ] Setup completion date noted
- [ ] Warm-up start date scheduled (if applicable)
- [ ] Client notified of completion
- [ ] Client provided with warm-up timeline expectations
- [ ] Checklist filed in client documentation

---

## Sign-Off

**Setup Completed By:** ___________________________  
**Signature:** ___________________________  
**Date:** ___________________________

**Reviewed By:** ___________________________  
**Signature:** ___________________________  
**Date:** ___________________________

---

## Notes and Issues

_Document any deviations from standard procedure, issues encountered, or special configurations:_

___________________________________________________________________

___________________________________________________________________

___________________________________________________________________

___________________________________________________________________

---

## Next Steps

- [ ] Schedule domain warm-up (refer to Domain Warm-up SOP)
- [ ] Brief client on email best practices
- [ ] Schedule 30-day deliverability review
- [ ] Add domain to monitoring/reporting dashboard

---

**IMPORTANT:** All checklist items must be completed before domain is used for live campaigns. Any failed items must be resolved and rechecked before proceeding to warm-up phase.
