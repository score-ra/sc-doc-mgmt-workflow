# Symphony Core KPI Framework: Single-Metric ROI System

---
**Document Information**
- **Title:** Symphony Core KPI Framework - Single-Metric ROI System
- **Version:** 2.0
- **Author:** Symphony Core Systems Team
- **Last Updated:** 2025-10-26
- **Category:** Standards & Frameworks
- **Tags:** [kpi, roi, metrics, reporting, client-success]
- **Status:** Approved

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Philosophy](#core-philosophy)
3. [The Primary KPI: Appointments Booked](#the-primary-kpi-appointments-booked)
4. [Client Onboarding Process](#client-onboarding-process)
5. [Technical Setup in GoHighLevel](#technical-setup-in-gohighlevel)
6. [Reporting System](#reporting-system)
7. [ROI Calculation](#roi-calculation)

---

## Executive Summary

### Purpose
This framework provides Symphony Core with a simple, repeatable system for measuring and demonstrating client ROI using **one metric: Appointments Booked**.

### Core Principle
**One Client. One Metric. One Clear ROI.**

### What This Document Covers
- Why we only track appointments
- How to set up tracking in GoHighLevel
- How to report results to clients
- How to calculate and communicate ROI

### What This Document Does NOT Cover
- Client capacity planning (handled after delivery)
- Multiple KPI tracking (we only use one)
- Complex optimization strategies (separate playbook)

---

## Core Philosophy

### The 80/20 Rule Applied

**The Problem We're Solving:**
Most agencies overcomplicate success metrics, confusing clients and diluting focus.

**Our Solution:**
Track the ONE metric that matters: **Appointments Booked**.

### Why Appointments?

**For Service Businesses:**
- Lawyers need consultations to sign cases
- Real estate agents need showings/listings to close deals
- Home services need estimates to win jobs
- Professional services need discovery calls to engage clients

**The appointment is where revenue happens.**

### Three Simple Truths

1. **We generate appointments** → Client closes them
2. **We track appointments** → Client tracks revenue
3. **We report appointments × value** → That's our ROI

---

## The Primary KPI: Appointments Booked

### Definition

**Appointment Booked =** A scheduled meeting on the client's calendar with valid contact information.

**That's it.** Nothing more complicated.

### What Counts

✅ **Counts as an appointment:**
- Scheduled on calendar
- Has name, email, and phone
- Client confirmed they can attend
- Booking confirmed via automation

### What Doesn't Count

❌ **Does NOT count:**
- Cancelled before appointment date
- Invalid contact information
- Duplicate bookings (same person, same timeframe)

### Simple Qualification

**We don't overthink qualification.** If someone books an appointment, it counts.

**Why?** 
- Client controls their booking requirements
- If junk leads book, we fix the traffic source
- We optimize AFTER seeing results, not before

---

## Client Onboarding Process

### Step 1: Value Discovery (15 minutes)

Ask the client THREE questions:

#### Question 1: "What's your average customer worth?"

**What we're getting:**
- Average sale/case/deal value
- Document the number
- Don't argue if it seems high/low

**Example answers:**
- Personal injury lawyer: "$15,000 per case"
- Real estate agent: "$12,000 commission per deal"
- HVAC company: "$8,000 per job"
- Business consultant: "$25,000 per engagement"

#### Question 2: "What percentage of appointments become customers?"

**What we're getting:**
- Their close rate
- Document the number
- Don't argue if it seems high/low

**Example answers:**
- "About 1 in 3, so 33%"
- "Maybe 40% if I'm being realistic"
- "I close about half, so 50%"

#### Question 3: "How many appointments per month would make you happy?"

**What we're getting:**
- Their goal number
- This becomes our target
- Start with their number, adjust later if needed

**Example answers:**
- "15 appointments would be amazing"
- "If I could get 25, I'd be thrilled"
- "Even 10 would be great right now"

### Step 2: Calculate Value Per Appointment

**Simple formula:**

```
Value Per Appointment = Average Customer Value × Close Rate
```

**Examples:**

**Personal Injury Lawyer:**
- $15,000 average case × 33% close rate = **$5,000 per appointment**

**Real Estate Agent:**
- $12,000 commission × 40% close rate = **$4,800 per appointment**

**HVAC Company:**
- $8,000 job value × 30% close rate = **$2,400 per appointment**

### Step 3: Complete the KPI Worksheet

Use this simple one-page worksheet:

---

#### SYMPHONY CORE KPI WORKSHEET

**Client:** _______________________  
**Date:** _______________________

**1. AVERAGE CUSTOMER VALUE**
"What's a typical customer worth to you?"
Answer: $__________

**2. CLOSE RATE**  
"What % of appointments become customers?"
Answer: ________%

**3. VALUE PER APPOINTMENT**  
(Customer Value × Close Rate)
**= $__________** ← This is our key number

**4. MONTHLY GOAL**  
"How many appointments per month would make you happy?"
Answer: ________ appointments

**5. MONTHLY VALUE TARGET**  
(Goal Appointments × Value Per Appointment)
**= $__________** ← This is what we're delivering

**6. SYMPHONY CORE FEE**  
Monthly investment: $__________

**7. TARGET ROI**  
(Monthly Value ÷ Symphony Core Fee)
**= ________ : 1 return** ← This is what we're proving

---

**Client Signature:** _______________________  
**Symphony Core Rep:** _______________________

---

### That's It. That's The Entire Onboarding.

**Time Required:** 15-20 minutes  
**Information Captured:** Everything we need  
**Next Step:** Set up tracking

---

## Technical Setup in GoHighLevel

### Overview

We need THREE things working:

1. Calendar booking that counts appointments
2. Automation that notifies when appointments happen
3. Dashboard that shows the count

**Setup time:** 30-45 minutes per client

### Setup Step 1: Calendar Configuration

**Navigate to:** Settings → Calendars

**Create New Calendar:**
- Name: "[Client Name] - Appointments"
- Duration: Set to client's typical appointment length
- Availability: Set to client's working hours

**Enable These Settings:**
- ✅ Require contact information (name, email, phone)
- ✅ Send confirmation email
- ✅ Send reminder emails/SMS

**Custom Fields to Add:**
- "Service Interest" (Dropdown with 3-5 options)
- "How Did You Hear About Us?" (Dropdown for source tracking)

**That's it for calendar setup.**

### Setup Step 2: Appointment Tracking Automation

**Create New Workflow:**

**Name:** "KPI Tracker - Appointments Booked"

**Trigger:** Calendar Event Booked (select the client's calendar)

**Actions:**

1. **Add Tag:** "Appointment-Booked-[Month-Year]"
   - Example: "Appointment-Booked-Oct-2025"
   - This lets us count by month

2. **Send Internal Email:**
   - To: Client + Symphony Core account manager
   - Subject: "✅ New Appointment Booked - [Contact Name]"
   - Body:
     ```
     New appointment booked!
     
     Contact: {{contact.name}}
     Phone: {{contact.phone}}
     Email: {{contact.email}}
     Date/Time: {{appointment.start_time}}
     Service Interest: {{contact.custom_field_value}}
     
     View contact: {{contact.link}}
     ```

3. **Create Opportunity (Optional):**
   - Pipeline: Main Sales Pipeline
   - Stage: "Appointment Scheduled"
   - Value: [Value Per Appointment from worksheet]
   - This helps track potential revenue

**Save and activate workflow.**

### Setup Step 3: Dashboard Creation

**Navigate to:** Dashboards → Create New

**Dashboard Name:** "[Client Name] - Primary KPI"

**Add 4 Widgets:**

#### Widget 1: Main KPI Counter
- **Type:** Number
- **Metric:** Contacts with tag "Appointment-Booked-[Current-Month]"
- **Display:** Large number
- **Label:** "Appointments This Month"
- **Size:** Full width, prominent

#### Widget 2: Goal Progress
- **Type:** Progress Bar
- **Current:** Appointments this month
- **Goal:** Target from worksheet
- **Label:** "Progress to Goal"

#### Widget 3: Monthly Trend
- **Type:** Line Chart
- **Data:** Appointments per week
- **Timeframe:** Last 12 weeks
- **Label:** "Weekly Trend"

#### Widget 4: Source Breakdown
- **Type:** Pie Chart
- **Data:** Appointments by "How Did You Hear About Us"
- **Timeframe:** Current month
- **Label:** "Appointment Sources"

**Set Dashboard Permissions:**
- Client: View only
- Symphony Core team: Full access

### Setup Step 4: Test the System

**Run a test booking:**
1. Book a test appointment on the calendar
2. Verify email notification sent
3. Verify tag added to contact
4. Verify dashboard counter increased
5. Delete test appointment

**Setup is complete.**

---

## Reporting System

### Weekly Snapshot (Automated Email)

**Frequency:** Every Monday at 9:00 AM  
**Recipients:** Client primary contact + account manager  
**Format:** Simple email

**Template:**

```
Subject: Weekly Appointments - [Client Name] - Week of [Date]

Hi [Client Name],

Quick update on your appointments:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THIS WEEK: [X] APPOINTMENTS
Last Week: [Y] appointments
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONTH TO DATE: [Z] appointments
Monthly Goal: [Goal] appointments
Progress: [%]% of goal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VALUE DELIVERED THIS WEEK:
[X] appointments × $[Value] = $[Total]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View your dashboard: [Link]

Best,
[Your Name]
Symphony Core
```

**Setup:** Configure in GHL Reporting → Scheduled Reports

### Monthly Report (PDF)

**Frequency:** 1st of each month  
**Format:** 2-page PDF

#### Page 1: Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MONTHLY PERFORMANCE REPORT
[Client Name] - [Month Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRIMARY KPI: APPOINTMENTS BOOKED

This Month: [X] appointments
Goal: [Goal] appointments
Achievement: [%]%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RETURN ON INVESTMENT

Appointments: [X]
Value Per Appointment: $[Amount]
Total Value Delivered: $[Total]

Symphony Core Investment: $[Fee]
Net Return: $[Total - Fee]
ROI: [X]:1 return

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GROWTH TREND

[Simple bar chart showing last 3 months]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP PERFORMING SOURCES

1. [Source]: [X] appointments ([%]%)
2. [Source]: [Y] appointments ([%]%)
3. [Source]: [Z] appointments ([%]%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Page 2: Next Month

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT MONTH FOCUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GOAL: [X] appointments

ACTIVE CAMPAIGNS:
• [Campaign 1 name and budget]
• [Campaign 2 name and budget]
• [Campaign 3 name and budget]

OPTIMIZATION PRIORITIES:
• [Priority 1]
• [Priority 2]
• [Priority 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questions? Let's discuss in our monthly call.

Scheduled: [Date/Time]
```

### Monthly Review Call

**Frequency:** Once per month, same day/time  
**Duration:** 30 minutes  
**Agenda:**

**Minutes 0-10: Results Review**
- Show dashboard
- Review appointment count
- Celebrate wins or discuss challenges

**Minutes 10-20: ROI Confirmation**
- Show ROI calculation
- Ask: "Are these appointments converting?"
- Document actual close rate if different from estimate

**Minutes 20-30: Next Month Planning**
- Confirm goal for next month
- Discuss any needed adjustments
- Answer questions

**That's the entire reporting system.**

---

## ROI Calculation

### The Simple Formula

```
Monthly ROI = (Appointments × Value Per Appointment) - Symphony Core Fee
```

### Example Calculations

#### Example 1: Personal Injury Lawyer

**Monthly Results:**
- Appointments Booked: 18
- Value Per Appointment: $5,000
- Symphony Core Fee: $3,000

**ROI Calculation:**
```
Total Value = 18 × $5,000 = $90,000
Symphony Investment = $3,000
Net Return = $90,000 - $3,000 = $87,000
ROI = $87,000 ÷ $3,000 = 29:1 return
```

**What We Say to Client:**
"We delivered 18 appointments this month. Based on your close rate, that's $90,000 in potential revenue. Your investment was $3,000. That's a 29-to-1 return."

#### Example 2: HVAC Company

**Monthly Results:**
- Appointments Booked: 32
- Value Per Appointment: $2,400
- Symphony Core Fee: $2,500

**ROI Calculation:**
```
Total Value = 32 × $2,400 = $76,800
Symphony Investment = $2,500
Net Return = $76,800 - $2,500 = $74,300
ROI = $74,300 ÷ $2,500 = 29.7:1 return
```

**What We Say to Client:**
"We delivered 32 estimate appointments this month. Based on your close rate, that's $76,800 in potential revenue. Your investment was $2,500. That's a 30-to-1 return."

#### Example 3: Real Estate Agent

**Monthly Results:**
- Appointments Booked: 12
- Value Per Appointment: $4,800
- Symphony Core Fee: $2,000

**ROI Calculation:**
```
Total Value = 12 × $4,800 = $57,600
Symphony Investment = $2,000
Net Return = $57,600 - $2,000 = $55,600
ROI = $55,600 ÷ $2,000 = 27.8:1 return
```

**What We Say to Client:**
"We delivered 12 buyer/seller appointments this month. Based on your close rate, that's $57,600 in potential commission. Your investment was $2,000. That's a 28-to-1 return."

### ROI Communication Rules

**Rule 1: Always Use Client's Numbers**
- Don't adjust their average customer value
- Don't adjust their close rate
- Use what they told us in onboarding

**Rule 2: Call It "Potential Revenue"**
- We don't know if they closed every deal
- We're showing the VALUE of appointments delivered
- Language: "Based on your close rate, that's $X in potential revenue"

**Rule 3: Show Net Return, Not Just Ratio**
- "$87,000 net return" is more impactful than "29:1"
- Show both, but emphasize the dollar amount

**Rule 4: Never Apologize for Success**
- If ROI is 10:1 or higher, that's incredible
- Don't downplay results
- Celebrate wins confidently

### When Results Are Below Expectations

**If appointments are below goal:**

```
"We delivered [X] appointments this month. That's [%]% of our goal. 
Here's what we're doing to improve:

1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

Goal for next month: [Y] appointments."
```

**If client reports low close rate:**

```
"Thanks for the feedback on close rates. Let's adjust our value 
calculation to match reality:

Old calculation: [X] appointments × $[Y] = $[Z]
New calculation: [X] appointments × $[Updated Y] = $[Updated Z]

This is still a [ratio]:1 return. Would you like us to adjust 
our appointment targeting to focus on [higher quality indicators]?"
```

**Key principle:** We fix forward, not backward.

---

## Quick Reference Guide

### For Account Managers

**Setting Up New Client (45 minutes total):**
1. Complete KPI Worksheet (15 min)
2. Set up calendar in GHL (10 min)
3. Create tracking automation (10 min)
4. Build dashboard (10 min)

**Weekly Tasks (10 minutes):**
1. Check dashboard Monday morning
2. Send weekly email
3. Note any issues

**Monthly Tasks (60 minutes):**
1. Generate monthly report (20 min)
2. Conduct review call (30 min)
3. Update next month goals (10 min)

### For Clients

**What You'll See:**
- Real-time dashboard showing appointment count
- Weekly email every Monday
- Monthly PDF report
- Monthly review call

**What We Track:**
- One thing: Appointments booked on your calendar

**What You Do:**
- Take the appointments
- Close the deals
- Tell us if results don't match projections

**That's it.**

---

## Appendix: Common Questions

### "What if the client wants to track other metrics?"

**Answer:** "We focus on appointments because that's what drives your revenue. We monitor other metrics internally for optimization, but your dashboard shows the one number that matters: appointments booked."

### "What if appointments aren't the right metric for this client?"

**Answer:** For 95% of service businesses, appointments ARE the right metric. The 5% exception is handled case-by-case, but default to appointments first.

### "What if the client's close rate is really low?"

**Answer:** Focus on volume. If they close 10% instead of 30%, they need 3x the appointments. We deliver more volume, not different metrics.

### "What if we're not hitting the goal?"

**Answer:** Report honestly, show the ROI anyway (even if below target), and communicate what we're adjusting. Never hide results.

### "How do we handle show rates and no-shows?"

**Answer:** We track booked appointments only. Show rate is the client's concern. If no-shows become a pattern, we can help implement reminder systems, but it doesn't change our primary metric.

---

**END OF FRAMEWORK**

This framework is designed to be simple, repeatable, and scalable. One metric. One clear ROI story. No complexity.