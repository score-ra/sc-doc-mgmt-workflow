# Phase 1 Report Specifications - Simplified Approach

**Version:** 2.1
**Date:** 2025-11-03
**Status:** Approved for Implementation
**Platform:** GoHighLevel (as of November 2025)
**Philosophy:** Essential metrics only - Maximum value, minimum complexity

---

## ⚠️ GHL Platform Capabilities Note

**This specification has been updated to reflect actual GoHighLevel platform capabilities:**

✅ **Verified Capabilities:**
- Contact-based custom dashboards with multiple widget types
- Number widgets with period comparisons and filters
- Table widgets with custom field grouping
- Line/Bar chart widgets for trend visualization
- Dashboard permissions and public link generation
- Dashboard cloning (plan-specific)

🔧 **Technical Limitations:**
- GHL does NOT support single adaptive widgets with conditional display logic
- Custom fields must exist and be populated before creating grouped widgets
- Dashboard cloning to other sub-accounts requires $497+ plan
- $297 plan limited to 1 custom dashboard per account

**Workarounds Documented:** All limitations have practical workarounds detailed in this specification.

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [The ONE Client Report](#the-one-client-report)
3. [Optional Deep-Dive Report](#optional-deep-dive-report)
4. [Minimal Internal Dashboard](#minimal-internal-dashboard)
5. [GHL Implementation Guide](#ghl-implementation-guide)
6. [Industry Customization Examples](#industry-customization-examples)

---

## Design Philosophy

### Core Principle
**Focus on essential metrics that drive client action and understanding.**

### The Problem with Complex Reports
- 3+ report types create maintenance burden
- 45+ widget specifications are overwhelming
- Multiple client versions double the work
- **Result:** Over-engineered, difficult to maintain, cognitive overload

### The Simplified Solution
**Focus on the essential metrics that deliver maximum client value:**

1. **Lead Volume** - Total contacts (this period)
2. **Lead Sources** - Where they come from
3. **Growth Trend** - Week-over-week or month-over-month
4. **Conversions** - When applicable (conditional display)
5. **One Action** - What to do next

**Everything else is optional and available on-demand.**

---

## The ONE Client Report

### Report Name
**"Your [Weekly/Monthly] Lead Report"**

### Strategic Purpose
- Show clients their lead generation is working
- Identify best-performing sources
- Give ONE clear action item
- **Adaptive**: Works for early-stage AND mature clients

### Report Structure
```
SIMPLE = POWERFUL

One page. No scrolling.
5 sections. No more.
Clear numbers. Clear action.
```

### Report Layout (Single Page)

```
┌─────────────────────────────────────────────────────────────────┐
│  YOUR WEEKLY LEAD REPORT                                         │
│  [Client Business Name] - Week of [Date Range]                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  📊 SECTION 1: YOUR KEY NUMBER                                   │
│  (Auto-selects based on client maturity)                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [IF CONVERSIONS > 0:]                                           │
│  🎯 APPOINTMENTS BOOKED THIS WEEK: 12    ↑ +20%                 │
│                                                                   │
│  [IF CONVERSIONS = 0:]                                           │
│  📈 NEW LEADS THIS WEEK: 25    ↑ +15%                           │
│                                                                   │
│  Supporting: [Secondary number]                                  │
│  - Early-stage: "Building your pipeline - 25 leads captured"    │
│  - Mature: "25 total leads generated"                           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  📍 SECTION 2: WHERE YOUR LEADS CAME FROM                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [SIMPLE BAR CHART OR TABLE]                                     │
│                                                                   │
│  Source              | Leads | Conversions                       │
│  ─────────────────────────────────────────────────                │
│  Website             | 10    | 5                                 │
│  Facebook Ads        | 8     | 3                                 │
│  Google My Business  | 5     | 3                                 │
│  Instagram           | 2     | 1                                 │
│                                                                   │
│  Top Performer: Google My Business (60% conversion rate)         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  📈 SECTION 3: YOUR TREND                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [SIMPLE LINE OR BAR CHART - Last 4 Weeks]                       │
│                                                                   │
│  Week 1: 15 leads                                                │
│  Week 2: 18 leads                                                │
│  Week 3: 22 leads                                                │
│  Week 4: 25 leads  ← This week                                   │
│                                                                   │
│  Direction: ✅ Growing +67% over 4 weeks                         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  💡 SECTION 4: WHAT THIS MEANS                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ✅ What's Working:                                              │
│  Your Google My Business is your best source - 60% of GMB       │
│  leads book appointments. Keep responding quickly to GMB         │
│  messages and posting weekly.                                    │
│                                                                   │
│  🎯 Action This Week:                                            │
│  Increase GMB optimization - add 2-3 posts this week and         │
│  encourage recent customers to leave reviews.                    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  📞 SECTION 5: NEED HELP?                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Questions about your numbers? Reply to this email or            │
│  schedule a quick call: [Calendar Link]                          │
│                                                                   │
│  - Your Symphony Core Team                                       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## The 5 Essential Widgets

### Widget 1: Key Number (Dual Widget Approach)

🔧 **Technical Limitation:** GHL does NOT support conditional display within a single widget. A single widget cannot automatically switch between showing conversions vs leads based on client stage.

**Type:** TWO Number Widgets (deploy both, configure visibility per client)

#### Widget 1A: Appointments/Conversions (For Mature Clients)
```
Widget Type: Number
Data Source: Contacts
Metric: COUNT
Date Filter: Created Date
Date Range: Last 7 days

⚠️ REQUIRED FILTERS (in Conditions tab, in order):
1. Filter: Contact Type = Lead (CRITICAL - ensures only leads counted)
2. Filter: Tag = "lead-activity-appointment" (or conversion tag)

Comparison: Previous Period (7 days)
Display: "Appointments Booked This Week: [X]  ↑ +20%"
```

#### Widget 1B: New Leads (For Early-Stage Clients)
```
Widget Type: Number
Data Source: Contacts
Metric: Total COUNT
Date Filter: Created Date
Date Range: Last 7 days

⚠️ REQUIRED FILTER (in Conditions tab):
Filter: Contact Type = Lead (CRITICAL - ensures only leads counted, not all contacts)

Comparison: Previous Period (7 days)
Display: "New Leads This Week: [X]  ↑ +15%"
```

**Implementation Strategy:**

**Option A - Deploy Both (Recommended):**
- Create both widgets on the same dashboard
- Stack vertically or position side by side
- Show the appropriate widget for each client's stage
- Hide the non-applicable widget using visibility settings
- Easier to switch if client progresses

**Option B - Two Template Versions:**
- Create two master dashboard templates:
  - "Weekly Report - Early Stage" (Widget 1B only)
  - "Weekly Report - Mature Client" (Widget 1A only)
- Clone appropriate template per client
- More organized but less flexible

**Why This Matters:**
- Early clients see lead generation success (builds confidence)
- Mature clients see conversion metrics (shows ROI)
- Manual deployment required but only once per client

⚠️ **Important:** This is NOT automatic conditional logic. You must choose which widget to display for each client during dashboard setup.

---

### Widget 2: Lead Sources Table

⚠️ **PREREQUISITE REQUIRED:** This widget requires `lead_source_primary` custom field to exist and be populated with data.

**Type:** Simple Table OR Horizontal Bar Chart

**Prerequisite Validation (DO THIS FIRST):**
```
Before creating this widget:
1. Verify custom field "lead_source_primary" exists
2. Verify at least 5-10 contacts have this field populated
3. Check that field has values in the last 7-30 days

If NO data exists:
- ❌ DO NOT create the table widget (it will fail silently)
- ✅ Create text placeholder widget instead (see below)
- ✅ Return to add table widget after source tracking is implemented
```

**Full Widget Configuration (If data exists):**

**Data Columns:**
1. Source Name (from `lead_source_primary` custom field)
2. Lead Count (COUNT)
3. Conversions (COUNT with conversion tag) - *optional, hide if zero across all sources*

**Configuration:**
- Group by: `lead_source_primary`
- Date range: Last 7 days (weekly) or 30 days (monthly)
- Sort: Descending by lead count
- Limit: Top 5 sources
- Show percentage if helpful: "(40% of total)"

**Placeholder Widget (If NO source tracking data exists):**
```
Widget Type: Text (Simple or Rich Text)
Widget Title: "Where Your Leads Came From"
Content:
"📊 Source Tracking Setup in Progress

Your lead source breakdown will be available here once
source tracking is fully implemented.

Expected availability: [Date/Next week]"

Size: Half width (same position as table would be)
```

**Why This Matters:**
- GHL table widgets fail silently if grouped field is empty
- Placeholder maintains dashboard layout and sets expectations
- Easy to replace placeholder with real table widget once data exists
- Prevents confusion about "missing" section

---

### Widget 3: Trend Chart
**Type:** Line Chart OR Simple Bar Chart

**Configuration:**
- X-axis: Week number (last 4 weeks) OR Day of month (last 30 days)
- Y-axis: Contact count
- Data: Contacts created by week/day
- Optional: Add trendline or growth percentage

**Keep It Simple:**
- No multiple lines
- No complex groupings
- Just: "Are we going up or down?"

---

### Widget 4: Insight Text
**Type:** Text Widget (Manual or Template-Based)

**Template Structure:**
```
✅ What's Working:
[Top performing source] is generating [X%] of your leads.
[Specific observation about quality or conversion]

🎯 Action This Week:
[ONE specific, actionable recommendation]
```

**Examples:**
- "Facebook ads are bringing in 40% of leads. Consider increasing budget."
- "Website contact form converts at 25% to appointments. Keep it prominent on homepage."
- "You had 5 GMB leads this week with 80% booking appointments. Optimize your GMB profile."

**Implementation:**
- Week 1-4: Manual updates by account manager
- Month 2+: Semi-automated with templates
- Keep to 2-3 sentences maximum

---

### Widget 5: Contact Section
**Type:** Simple Text

**Content:**
```
Questions about your numbers? Reply to this email or
schedule a call: [calendar link]

- Your Symphony Core Team
```

**Why Include:**
- Encourages engagement
- Low-pressure CTA
- Shows you're available

---

## Conditional Display Rules (Simplicity First)

### All Clients Show:
1. ✅ Key Number (leads or conversions, auto-select)
2. ✅ Trend (week-over-week or month-over-month)
3. ✅ Insight + Action

### Show IF Data Exists:
4. 🔄 Lead Sources table (only if `lead_source_primary` is populated)
5. 🔄 Conversions column (only if > 0 conversions)

### Never Show:
- ❌ Point system (internal calculation only)
- ❌ Response times (internal metric)
- ❌ Quality scores (confusing to clients)
- ❌ Complex formulas
- ❌ More than 5 sections

---

## Optional Deep-Dive Report

### When to Offer
- Client specifically requests more detail
- Multi-location businesses
- Clients with 5+ active lead sources
- Marketing-sophisticated clients

### Report Name
**"Lead Source Deep-Dive"**

### Additional Sections (Only When Requested)
1. **Campaign Breakdown** - If tracking Facebook/Google campaigns
2. **Location Breakdown** - For multi-location businesses
3. **Form Performance** - Which forms convert best
4. **Time-of-Day Analysis** - When leads come in

### Philosophy
- Not sent by default
- Created on-demand
- Shared as dashboard link (not weekly email)
- Updated live, not weekly PDFs

---

## Minimal Internal Dashboard

### Purpose
**Early warning system only** - not comprehensive analytics

### The 3 Critical Alerts

```
┌──────────────────────────────────────────────────────────────────┐
│  INTERNAL DASHBOARD - [CLIENT NAME]                              │
│  Quick Health Check                                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  🚨 ALERT 1: UNASSIGNED LEADS                                    │
├──────────────────────────────────────────────────────────────────┤
│  Contacts with no assigned user: 6                               │
│  Oldest unassigned: 3 days ago                                   │
│  ⚠️  ACTION NEEDED if >24 hours old                             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  🚨 ALERT 2: LEAD VOLUME DROP                                    │
├──────────────────────────────────────────────────────────────────┤
│  Leads this week: 8                                              │
│  Leads last week: 25                                             │
│  Change: ↓ -68%  ⚠️  INVESTIGATE                                │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  🚨 ALERT 3: MISSING DATA                                        │
├──────────────────────────────────────────────────────────────────┤
│  Contacts without phone: 15  (30% of new leads)                  │
│  Contacts without source: 8   (16% of new leads)                 │
│  ⚠️  ACTION NEEDED if >20%                                      │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  📊 QUICK STATS (This Month)                                     │
├──────────────────────────────────────────────────────────────────┤
│  Total Leads: 85  |  Conversions: 12  |  Rate: 14%              │
│  Top Source: Website (35 leads)                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Widget Count: 4-5 Maximum
1. Unassigned contacts count (with age filter)
2. Lead volume this week vs last week (percentage change)
3. Data quality check (missing phone/email/source %)
4. Quick stats summary (total leads, conversions, top source)
5. *(Optional)* Contact creation trend line (30 days)

### What We Don't Duplicate (Use GHL Standard Views Instead)
- ❌ Response time analysis → Use GHL contact timeline
- ❌ Activity type breakdown → Use GHL contact filters
- ❌ Tag distribution → Use GHL tag reports
- ❌ Assignee distribution → Use GHL user reports
- ❌ Company name tracking → Use GHL contact list
- ❌ Contact type breakdown → Use GHL standard filters

### Why This Works
- Account managers check **alerts only** (2 minutes)
- Everything else is in GHL's built-in views
- No duplicate dashboards
- Focus on **exceptions**, not all data

---

## GHL Implementation Guide

### ⚠️ Plan Requirements Check FIRST

**Before building dashboards, verify your GHL plan tier:**

**$497+ Plan (Agency Unlimited) - RECOMMENDED:**
- ✅ Multiple custom dashboards (unlimited)
- ✅ Dashboard duplication to other sub-accounts
- ✅ Full cloning capabilities
- ⏱️ Setup time: 15-20 minutes per client (using clone)

**$297 Plan (Agency Starter) - LIMITED:**
- ⚠️ Limited to 1 custom dashboard only
- ⚠️ Cannot duplicate to other sub-accounts
- ⚠️ Must manually rebuild for each client
- ⏱️ Setup time: 25-30 minutes per client (manual rebuild)

**Recommended:** If managing 10+ clients, upgrade to $497+ plan for significant time savings.

---

### Phase 1: ONE Client Dashboard

**Dashboard Name:** "[Client Name] - Weekly Report"

**Setup Time:**
- $497+ plan: 15-20 minutes (after first build)
- $297 plan: 25-30 minutes (manual rebuild each time)

**Widgets to Create:**

#### 1. Key Number Widget (DUAL APPROACH REQUIRED)

🔧 **GHL Limitation:** Cannot create single adaptive widget. Must create TWO separate widgets.

**Widget 1A - Appointments (Mature Clients):**
```
Widget: Number
Data Source: Contacts
Metric: COUNT
Filter: Created Date = Last 7 days

⚠️ REQUIRED FILTERS (in Conditions tab):
1. Filter: Contact Type = Lead (CRITICAL)
2. Filter: Tag = "lead-activity-appointment"

Comparison: Previous period (7 days before)
Title: "Appointments Booked This Week"
Size: Full width, large font
Position: Top of dashboard
```

**Widget 1B - New Leads (Early-Stage Clients):**
```
Widget: Number
Data Source: Contacts
Metric: Total COUNT
Filter: Created Date = Last 7 days

⚠️ REQUIRED FILTER (in Conditions tab):
Filter: Contact Type = Lead (CRITICAL)

Comparison: Previous period (7 days before)
Title: "New Leads This Week"
Size: Full width, large font
Position: Top of dashboard (same row as 1A)
```

**Deployment:**
- Create BOTH widgets
- Show appropriate one per client's stage
- Hide non-applicable widget using visibility settings
- OR create two template versions (one with 1A, one with 1B)

#### 2. Source Table Widget (WITH PREREQUISITE CHECK)

⚠️ **IMPORTANT:** Check data exists BEFORE creating this widget!

**Prerequisite Validation:**
```
1. Navigate to Contacts
2. Open recent contact
3. Verify "lead_source_primary" field exists and has value
4. Confirm 5-10+ contacts have this field populated
```

**If data EXISTS, create table widget:**
```
Widget: Table
Data Source: Contacts
Group By: Custom Field "lead_source_primary"

⚠️ REQUIRED FILTER (in Conditions tab):
Filter: Contact Type = Lead (CRITICAL)

Columns:
  - Source (from field)
  - Count (number of contacts)
  - [Optional] Conversions (filtered count with tag)
Date Range: Last 7 days
Sort: Descending by count
Limit: Top 5
Size: Half width
```

**If NO data exists, create placeholder:**
```
Widget: Text (Simple)
Title: "Where Your Leads Came From"
Content: "📊 Source tracking setup in progress.
          Available next week."
Size: Half width
```

#### 3. Trend Widget
```
Widget: Line Chart OR Bar Chart
Data Source: Contacts
Metric: Count by creation date

⚠️ REQUIRED FILTER (in Conditions tab):
Filter: Contact Type = Lead (CRITICAL)

X-Axis: Date (grouped by day or week)
Y-Axis: Contact count
Date Range: Last 30 days (for weekly view) OR Last 90 days (for monthly)
Size: Half width
```

#### 4. Insight Text Widget
```
Widget: Text (Rich Text / HTML)
Content: [Manually updated weekly]
Size: Full width

Template:
✅ What's Working: [observation]
🎯 Action This Week: [one specific action]
```

**Update Process:**
- Account manager updates every Monday before sending report
- Takes 2-3 minutes
- Based on quick dashboard review

#### 5. Contact Widget
```
Widget: Text (Simple)
Content:
"Questions? Reply to this email or schedule a call: [link]
- Symphony Core Team"
Size: Full width, bottom of dashboard
```

**Total Widgets:** 5
**Total Dashboard Setup Time:** 15-20 minutes per client

---

### Phase 2: Internal Alert Dashboard (Optional)

**Dashboard Name:** "INTERNAL - Client Health Alerts"

**Create One Dashboard for ALL Clients** (not per-client)

**Widgets:**
1. List widget: Unassigned contacts (all clients, filtered by age >24 hours)
2. Table widget: Lead volume by client (this week vs last week with % change)
3. Table widget: Data quality issues (missing phone/email by client)

**View:** Team members check ONCE per day (5 minutes)

**Alternative:** Use GHL's built-in reports instead. Only create if absolutely needed.

---

### Distribution Setup

#### Weekly Email Automation

**Workflow Name:** "Weekly Report - [Client Name]"

**Trigger:**
- Schedule: Every Monday, 8:00 AM

**Actions:**
1. Send email with dashboard link:
   - To: Client email
   - Subject: "Your Weekly Lead Report - [Client Name]"
   - Body: Simple email with dashboard link
   - BCC: Account manager

2. ⚠️ **PDF Export (Optional - Plan-Specific):**
   - **$297 Plan:** PDF export available (basic)
   - **$497+ Plan:** PDF export with full customization
   - **RECOMMENDED:** Use live dashboard link instead of PDF
     - More engaging and interactive
     - Updates in real-time
     - Better mobile experience
     - Reduces manual work
   - Only attach PDF if client explicitly requests offline access

**Email Template:**
```
Hi [Client Name],

Here's your weekly lead report for [Date Range].

🎯 This week's highlights:
- [X] new leads generated
- [Top source] was your best performer
- [One key insight]

📊 VIEW FULL REPORT: [Dashboard Link Button]

Questions? Just reply to this email.

Best,
Symphony Core Team
```

**Keep It Short:**
- 3-4 sentences max in email body
- Dashboard has the details
- Link is the main CTA

---

### Customization Per Client

**Minimal Customization Needed:**

1. **Frequency:** Weekly OR Monthly (based on lead volume)
   - High volume (10+ leads/week): Weekly
   - Low volume (<10/week): Monthly

2. **Key Metric:** Leads OR Conversions
   - Auto-select based on data
   - Manually override if needed

3. **Insight Text:** Custom per client weekly
   - Takes 2-3 minutes to update
   - Based on quick dashboard review

**No Other Customization:**
- Same widget set for all clients
- Same layout
- Same structure
- Easier to maintain

---

## Industry Customization Examples

### Example 1: Home Services (Plumbing, HVAC, Electrical)

**Terminology:**
- Leads → "Service Requests"
- Conversions → "Appointments Scheduled" or "Jobs Booked"

**Common Sources:**
- Google My Business (primary)
- Website contact form
- Phone calls (track with call tracking)
- Referrals
- Angi/HomeAdvisor

**Report Focus:**
- Emergency vs scheduled work
- Response time critical (show internally)
- Same-day booking rate

---

### Example 2: Professional Services (Law Firms, Accounting, Consulting)

**Terminology:**
- Leads → "Case Inquiries" or "Client Inquiries"
- Conversions → "Consultations Scheduled" or "Initial Consultations"

**Common Sources:**
- Referrals (often 40-60% of leads)
- Website contact form
- LinkedIn
- Legal/professional directories
- Networking events

**India-Specific for Law Firms:**
- WhatsApp Business (critical channel)
- Justdial, Sulekha
- Practice area tracking (optional)

**Report Focus:**
- Referral emphasis
- Consultation show rate
- Practice area distribution (if multi-practice)

---

### Example 3: Restaurants

**Terminology:**
- Leads → "Reservation Requests" or "Inquiries"
- Conversions → "Reservations Booked" or "Tables Reserved"

**Common Sources:**
- OpenTable / reservation platforms
- Website booking widget
- Instagram / social media
- Google My Business
- Walk-in requests

**Report Focus:**
- Reservation vs walk-in split
- Table utilization
- Peak time bookings

---

### Example 4: Real Estate

**Terminology:**
- Leads → "Property Inquiries"
- Conversions → "Showings Scheduled" or "Tours Booked"

**Common Sources:**
- Zillow, Realtor.com, Housing.com
- Website property listings
- Open house sign-ins
- Referrals
- Social media ads

**Report Focus:**
- Property-specific interest
- Showing attendance rate
- Buyer vs seller inquiries

---

## Implementation Checklist

### Prerequisites (From Technical Setup)
- [ ] Custom field created: `lead_source_primary`
- [ ] Tags created for conversions: `lead-activity-appointment`, `lead-activity-consultation`, etc.
- [ ] Basic workflows active (lead source tagging)

**Note:** Point system workflows optional - can add later if needed for internal tracking

### Week 1: Build Core Dashboard
- [ ] Create template dashboard in GHL (30 minutes)
- [ ] Test with 1 pilot client (review with team)
- [ ] Adjust layout based on feedback
- [ ] Document any client-specific notes

### Week 2: Deploy to 3-5 Pilot Clients
- [ ] Clone template dashboard for each client
- [ ] Customize insight text for each
- [ ] Set up weekly email automation
- [ ] Send first report manually (with introduction)
- [ ] Collect feedback

### Week 3-4: Rollout to All Clients
- [ ] Create dashboards for remaining clients
- [ ] Train account managers on dashboard updates
- [ ] Set up email automation for all
- [ ] Monitor open rates and engagement

### Month 2: Optimize
- [ ] Review which clients are engaging with reports
- [ ] Adjust frequency (weekly vs monthly) based on engagement
- [ ] Refine insight templates based on common patterns
- [ ] Add source tracking for clients missing it
- [ ] Consider adding optional deep-dive report for sophisticated clients

---

## Success Metrics

### Client Engagement
- **Goal:** 70%+ of clients click dashboard link monthly
- **Measure:** Email open rate + link click rate
- **Target:** 60% open, 40% click

### Client Conversations
- **Goal:** Clients reference report metrics in calls/emails
- **Measure:** Qualitative (account manager notes)
- **Good sign:** "I saw in my report that..." or "The report showed..."

### Operational Efficiency
- **Goal:** <15 minutes per client per week for reporting
- **Breakdown:**
  - Dashboard setup: 15 min (one-time)
  - Weekly insight update: 2-3 min
  - Email send: Automated (0 min)
- **Scale:** One account manager can handle reports for 20-30 clients

### Business Impact
- **Goal:** Improved client retention for clients receiving reports
- **Measure:** Retention rate comparison (reports vs no reports)
- **Timeline:** 6-month comparison

---

## When to Add Complexity

**Only add features when:**

1. **Multiple clients request same feature** (not just one)
2. **Clear ROI for additional complexity** (retention, upsell, time savings)
3. **Technical infrastructure supports it** (data is clean and reliable)
4. **Team has bandwidth to maintain it** (not just build it)

**Examples of "Maybe Later" Features:**
- Campaign-specific tracking (when 5+ clients have multiple campaigns)
- Cost-per-lead analysis (when clients provide ad spend data)
- Multi-location breakdowns (when 3+ multi-location clients exist)
- Time-of-day analysis (when clients ask for it)

**Guiding Principle:** If fewer than 20% of clients will use it, don't build it yet.

---

## Key Principles Summary

### For Client Reports:
1. **One page, no scrolling** - Everything visible at a glance
2. **5 sections maximum** - More is noise
3. **One action item** - Don't overwhelm with choices
4. **Adaptive not versioned** - Same template for all client stages
5. **Email is summary, dashboard is detail** - Link drives engagement

### For Internal Dashboard:
1. **Alerts only** - What needs action, not all data
2. **Use GHL standard views** - Don't duplicate built-in features
3. **2-5 minute check** - Quick daily review, not deep analysis
4. **Exceptions not trends** - Catch problems, not track everything

### For Implementation:
1. **Template-based** - One dashboard design for all clients
2. **15 minutes setup** - Not hours of customization
3. **2 minutes weekly update** - Sustainable for account managers
4. **Pilot before rollout** - Test with 3-5 clients first
5. **Iterate based on usage** - Add features only when needed

---

## Next Steps

### Immediate (This Week):
1. Review this simplified approach with team
2. Create ONE template dashboard (15-20 min)
3. Test with 1-2 pilot clients
4. Get feedback

### Short Term (Next 2 Weeks):
6. Refine template based on pilot feedback
7. Roll out to 5-10 clients
8. Train account managers on 2-minute weekly updates
9. Monitor engagement metrics
10. Document any issues

### Ongoing (Month 2+):
11. Review monthly: what's used vs what's ignored
12. Optimize insight templates (common patterns)
13. Add optional features ONLY when requested by 3+ clients
14. Measure client retention impact
15. Plan Phase 2 (engagement metrics) with same simplified lens

---

## Troubleshooting GHL Limitations

### Common Issues and Solutions

#### Issue 1: "Widget shows No Data"
**Cause:** Date range doesn't include contact creation dates, or filters are too restrictive
**Solutions:**
- Extend date range to 30+ days
- Remove filters and test
- Verify contacts exist in selected timeframe
- Check custom field actually has values

#### Issue 2: "Source table is empty"
**Cause:** `lead_source_primary` field is not populated
**Solutions:**
- Verify field exists in contact records
- Check field name matches exactly
- Use placeholder text widget until source tracking is implemented
- See Widget 2 prerequisite validation section

#### Issue 3: "Can't clone dashboard to other client"
**Cause:** Plan limitation - $297 plan doesn't support cross-account duplication
**Solutions:**
- Upgrade to $497+ plan for cloning capability
- OR manually rebuild dashboard in each client sub-account (25-30 min each)
- Document exact widget configurations for faster rebuilds

#### Issue 4: "Conditional widget not working"
**Cause:** GHL doesn't support conditional display within single widget
**Solutions:**
- This is not a bug - it's a platform limitation
- Use dual widget approach (Widget 1A + 1B)
- Create two template versions instead
- Configure visibility per client deployment

#### Issue 5: "PDF export not available"
**Cause:** Custom dashboard feature restrictions or plan limitations
**Solutions:**
- Verify you have $297+ plan (custom dashboards enabled)
- Use live dashboard link instead (recommended)
- PDF export is optional, not required

#### Issue 6: "Dashboard link not working for client"
**Cause:** Permissions or visibility settings issue
**Solutions:**
- Regenerate public link
- Check dashboard visibility settings
- Verify link wasn't deleted
- Test in incognito browser
- Check if password protection is enabled

---

## GHL Capability Summary

✅ **What GHL CAN Do:**
- Create multiple custom dashboards ($497+ plan)
- Number widgets with period comparisons
- Table widgets grouped by custom fields
- Line/Bar chart widgets for trends
- Text widgets for insights and contact info
- Dashboard permissions (Full, Edit, View, No Access)
- Public link generation with optional password
- Dashboard cloning within same account
- Dashboard duplication across sub-accounts ($497+ plan)
- Date range filtering and auto-refresh

🔧 **What GHL CANNOT Do:**
- Single adaptive widget with conditional logic
- Automatic switching between metrics based on client stage
- Table widgets without populated custom fields
- Dashboard duplication on $297 plan
- Multiple custom dashboards on $297 plan

**Bottom Line:** All specifications in this document work within GHL's actual capabilities. Workarounds are documented for all limitations.

---

**Document Owner:** Symphony Core Platform Team
**Last Updated:** 2025-11-03
**Platform Version:** GoHighLevel as of November 2025
**Validation Status:** ✅ Verified against actual GHL capabilities
**Next Review:** After pilot feedback (Week 2)
**Status:** Approved for Implementation

**Philosophy:** Simple scales. Complex breaks.
