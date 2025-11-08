# GHL Dashboard Build Guide - Step-by-Step

**Purpose:** Click-by-click instructions to build Phase 1 client dashboard in GoHighLevel
**Time:** 15-20 minutes per client (cloning); 25-30 minutes (manual rebuild on $297 plan)
**Result:** Single-page report with 5 sections
**Platform Version:** Verified for GoHighLevel as of November 2025

---

## ⚠️ Plan Requirements

**This guide requires specific GHL plan features. Verify your plan tier before proceeding:**

### $497+ Plan (Agency Unlimited) - RECOMMENDED
✅ Multiple custom dashboards (unlimited)
✅ Dashboard duplication to other sub-accounts
✅ PDF export and customization
✅ Full dashboard cloning capabilities
⏱️ **Time per client:** 15 minutes (using clone feature)

### $297 Plan (Agency Starter) - LIMITED
⚠️ Limited to 1 custom dashboard only
⚠️ NO dashboard duplication to other sub-accounts
✅ PDF export available (basic)
✅ Custom dashboard feature available
⏱️ **Time per client:** 25-30 minutes (manual rebuild required)

**If you have $297 plan:** You must manually rebuild this dashboard in each client sub-account. See Step 10 for plan-specific instructions.

---

## 🚀 Quick Reference

**TL;DR - What You're Building:**

```
THE WEEKLY REPORT (One Page, 5 Sections):
┌─────────────────────────────────────┐
│ 📊 NEW LEADS THIS WEEK: 25  ↑ +15% │
│                                     │
│ 📍 WHERE FROM:                      │
│   Website: 10 | Facebook: 8         │
│   GMB: 5 | Instagram: 2             │
│                                     │
│ 📈 TREND:                           │
│   Week 1: 15 → 18 → 22 → 25 ✅     │
│                                     │
│ 💡 YOUR ACTION:                     │
│   GMB converts best (60%). Post     │
│   2-3 times this week + get reviews │
│                                     │
│ Questions? Reply or schedule call   │
└─────────────────────────────────────┘
```

**Time Investment:**
- **Setup (one-time):** 20-30 minutes per client
- **Weekly update:** 2-3 minutes per client
- **Scales to:** 20-30 clients per account manager

**What You'll Create:** 5 widgets, single page, no scrolling

---

## Prerequisites

Before building dashboard, ensure:
- [ ] Client sub-account exists in GHL
- [ ] **Contact Type field configured:** Set to "Lead" for all lead contacts
- [ ] Custom field created: `lead_source_primary` (dropdown)
- [ ] Conversion tags exist: `lead-activity-appointment` or similar
- [ ] At least 1-2 weeks of data exists (for testing)

⚠️ **CRITICAL FILTER REQUIREMENT:** All widgets MUST filter by "Contact Type = Lead" to exclude non-lead contacts (customers, vendors, etc.) from lead metrics.

---

## Step 1: Create New Dashboard (2 minutes)

### 1.1 Access Dashboards
```
1. Log into GHL
2. Navigate to client sub-account
3. Click: Settings (gear icon)
4. Click: Dashboards (in left sidebar)
5. Click: "+ Create Dashboard" button (top right)
```

### 1.2 Dashboard Settings
```
Dashboard Name: [Client Name] - Weekly Report
Description: Client-facing weekly lead report
Type: Contact-based
Visibility: Specific users (select client + account manager)
Click: "Create"
```

**You now have a blank dashboard.**

---

## Step 2: Add Widget 1 - Key Number (6 minutes)

🔧 **Technical Limitation:** GHL cannot create a single adaptive widget that automatically switches between metrics based on client stage.

**Workaround:** Create TWO separate number widgets. Deploy both and configure visibility per client, OR create two template versions (one for early-stage, one for mature clients).

### 2.1 Add Widget 1A - Appointments (For Mature Clients)

#### 2.1.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Number" widget type
3. Click: "Next"
```

#### 2.1.2 Configure Data Source
```
Data Source: Contacts
Metric: Total Count
Date Filter: Created Date
Date Range: Last 7 days
Comparison: Previous Period (auto-calculates)

⚠️ REQUIRED FILTERS (in order):
1. Filter: Contact Type = Lead (CRITICAL - always add first)
2. Filter: Add tag filter → "lead-activity-appointment"
```

#### 2.1.3 Configure Display
```
Widget Title: "Appointments Booked This Week"
Number Format: Auto
Show Comparison: YES (toggle on)
Comparison Display: Percentage change
Font Size: Large
Color: Auto (green for positive, red for negative)
```

#### 2.1.4 Position & Save
```
Position: Top of dashboard, full width
Size: Drag to make it prominent (full row)
Click: "Save Widget"
```

### 2.2 Add Widget 1B - New Leads (For Early-Stage Clients)

#### 2.2.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Number" widget type
3. Click: "Next"
```

#### 2.2.2 Configure Data Source
```
Data Source: Contacts
Metric: Total Count
Date Filter: Created Date
Date Range: Last 7 days
Comparison: Previous Period (auto-calculates)

⚠️ REQUIRED FILTER:
Filter: Contact Type = Lead (CRITICAL - ensures only leads counted)
```

#### 2.2.3 Configure Display
```
Widget Title: "New Leads This Week"
Number Format: Auto
Show Comparison: YES (toggle on)
Comparison Display: Percentage change
Font Size: Large
Color: Auto (green for positive, red for negative)
```

#### 2.2.4 Position & Save
```
Position: Top of dashboard, full width (same row as Widget 1A)
Size: Drag to make it prominent (full row)
Click: "Save Widget"
```

### 2.3 Dual Widget Deployment Strategy

**Option A - Deploy Both (Recommended):**
```
- Stack both widgets on dashboard
- Show appropriate one per client based on their stage
- Hide the non-applicable widget using visibility settings
- Easier to switch if client progresses to appointments
```

**Option B - Two Template Versions:**
```
- Create two master templates:
  - Template A: "Weekly Report - Early Stage" (Widget 1B only)
  - Template B: "Weekly Report - Mature Client" (Widget 1A only)
- Clone appropriate template per client
- More organized but less flexible
```

**Result:** Big number showing either appointments OR new leads with up/down arrow and percentage change.

---

## Step 3: Add Widget 2 - Lead Sources Table (4 minutes)

⚠️ **PREREQUISITE CHECK REQUIRED:** This widget requires source tracking data to function properly.

### 3.0 Prerequisite Validation (DO THIS FIRST)

**Before creating the table widget, verify the following:**

```
1. Navigate to: Contacts
2. Open: Any recent contact
3. Check: Custom field "lead_source_primary" exists
4. Verify: Field has a value populated (not empty)
5. Confirm: At least 5-10 contacts have this field populated
```

**If NO source data exists:**
- ❌ DO NOT create the table widget (it will fail silently)
- ✅ Create text placeholder widget instead with message:
  ```
  "📊 Source Tracking Setup in Progress

  Your lead source breakdown will be available here once
  source tracking is fully implemented. Expected: Next week."
  ```
- ✅ Return to this step after source tracking is configured
- ✅ Replace placeholder widget with table widget once data exists

**If source data EXISTS:**
- ✅ Proceed with Step 3.1 below

---

### 3.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Table" widget type
3. Click: "Next"
```

### 3.2 Configure Data Source
```
Data Source: Contacts
Group By: Custom Field → "lead_source_primary"
Date Filter: Created Date
Date Range: Last 7 days

⚠️ REQUIRED FILTER:
Filter: Contact Type = Lead (CRITICAL - add this first in Conditions tab)

⚠️ NOTE: If "lead_source_primary" field doesn't appear in the dropdown,
return to Step 3.0 prerequisite check above.
```

### 3.3 Configure Columns
```
Column 1:
  - Field: lead_source_primary
  - Label: "Source"
  - Display: Value

Column 2:
  - Field: Count (ID)
  - Label: "Leads"
  - Display: Number

Column 3 (Optional - if client has conversions):
  - Field: Custom filter with tag "lead-activity-appointment"
  - Label: "Appointments"
  - Display: Count
```

### 3.4 Configure Display
```
Widget Title: "Where Your Leads Came From"
Sort: By Leads (descending)
Limit: Top 5 sources
Show Totals: Yes (at bottom)
```

### 3.5 Position & Save
```
Position: Below key number, left side
Size: Half width
Click: "Save Widget"
```

**Result:** Table showing top 5 sources with lead counts.

---

## Step 4: Add Widget 3 - Trend Chart (3 minutes)

### 4.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Line Chart" (or "Bar Chart")
3. Click: "Next"
```

### 4.2 Configure Data Source
```
Data Source: Contacts
Metric: Count
X-Axis: Created Date (grouped by week OR day)
Y-Axis: Contact count
Date Range: Last 30 days

⚠️ REQUIRED FILTER:
Filter: Contact Type = Lead (CRITICAL - add in Conditions tab)
```

### 4.3 Configure Display
```
Widget Title: "Your Trend - Last 4 Weeks"
Chart Type: Line chart (clean, simple)
Colors: Single color (Symphony Core brand color)
Show Data Labels: Yes
Show Grid Lines: Optional
Legend: Hide (only one line)
```

### 4.4 Position & Save
```
Position: Below key number, right side (next to source table)
Size: Half width
Click: "Save Widget"
```

**Result:** Line chart showing lead growth over 4 weeks.

---

## Step 5: Add Widget 4 - Insight Text (2 minutes)

### 5.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Text" widget type (Rich Text / HTML)
3. Click: "Next"
```

### 5.2 Add Content
```
Widget Title: "What This Means"

Content (use rich text editor):

✅ What's Working:
[Leave blank - account manager updates weekly]

🎯 Action This Week:
[Leave blank - account manager updates weekly]

Example content for initial test:
"Your website is generating 40% of leads. Keep your contact
form prominent on the homepage and ensure quick response times."
```

### 5.3 Configure Display
```
Font Size: Medium
Alignment: Left
Background: Light color (optional)
Padding: Default
```

### 5.4 Position & Save
```
Position: Below source table and trend chart
Size: Full width
Click: "Save Widget"
```

**Result:** Text box with insights (manually updated weekly).

---

## Step 6: Add Widget 5 - Contact Section (1 minute)

### 6.1 Add Widget
```
1. Click: "+ Add Widget" button
2. Select: "Text" widget type (Simple)
3. Click: "Next"
```

### 6.2 Add Content
```
Widget Title: (Leave blank OR "Need Help?")

Content:
Questions about your numbers? Reply to this email or
schedule a quick call: [Insert Calendar Link]

- Your Symphony Core Team
```

### 6.3 Configure Display
```
Font Size: Small
Alignment: Center
Background: Light gray (optional)
```

### 6.4 Position & Save
```
Position: Bottom of dashboard
Size: Full width
Click: "Save Widget"
```

**Result:** Contact information at bottom.

---

## Step 7: Dashboard Settings & Permissions (4 minutes)

### 7.1 Configure Dashboard Settings
```
1. Click: Dashboard Settings (gear icon, top right)
2. Set Date Range Selector: Last 7 days (default)
3. Allow Date Range Changes: Yes
4. Auto-refresh: Optional (every 5 minutes)
```

### 7.2 Set Permissions (Role-Based Access)

✅ **GHL Capability:** GHL supports 4 permission levels with role-based hierarchy:
- **Full Access:** Create, edit, delete, and manage permissions
- **Edit:** Modify widgets and content (cannot change permissions)
- **View:** Read-only access
- **No Access:** Dashboard hidden from user

#### 7.2.1 Configure User Permissions
```
Agency Level (Symphony Core Team):
- Agency Admin: Full Access (your account)
- Agency Users: View Only (support team)

Sub-Account Level (Client Account):
- Account Admin: Edit (if client manages their own dashboard)
- Account Users: View Only (client team members)

Specific Users:
- Account Manager: Full Access (for weekly updates)
- Client Primary Contact: View Only
```

#### 7.2.2 Generate Public Link
```
1. Toggle: "Enable Public Link" (ON)
2. Optional: Enable "Password Protection"
   - Use if client wants secure access
   - Share password separately via secure channel
3. Copy: Public link URL (for email distribution)
```

#### 7.2.3 Public Link Permissions Note
```
⚠️ IMPORTANT: Public link permissions are tied to
dashboard visibility settings. Anyone with the link
can view the dashboard if:
- Public link is enabled
- Dashboard visibility allows public access

For sensitive data, use password protection.
```

### 7.3 Plan Requirement Note

⚠️ **Plan Requirement:** Multiple custom dashboards and advanced cloning features require $497+ plan.

**If you have $297 plan:**
- You are limited to 1 custom dashboard
- Build this dashboard in your agency account first for testing
- Then manually rebuild in each client sub-account
- Cannot clone across sub-accounts

### 7.4 Save Settings
```
Click: "Save Dashboard Settings"
```

---

## Step 8: Test & Validate (3 minutes)

### 8.1 Check Each Widget
```
✓ Key Number shows correct count
✓ Comparison percentage makes sense
✓ Source table shows top sources
✓ Trend chart displays 4 weeks
✓ Insight text is readable
✓ Contact info is correct
```

### 8.2 Test Date Range Changes
```
1. Change date range to "Last 30 days"
2. Verify all widgets update correctly
3. Change back to "Last 7 days"
```

### 8.3 Check Mobile View
```
1. Click: Preview (eye icon)
2. Select: Mobile view
3. Verify: Layout is readable on mobile
4. Adjust widget sizes if needed
```

---

## Step 9: Set Up Email Automation (5 minutes)

### 9.1 Create Workflow
```
1. Navigate to: Automations → Workflows
2. Click: "+ Create Workflow"
3. Name: "Weekly Report - [Client Name]"
4. Type: Schedule-based
```

### 9.2 Configure Trigger
```
Trigger: Schedule
Frequency: Weekly
Day: Monday
Time: 8:00 AM
Timezone: Client's timezone
```

### 9.3 Add Email Action
```
1. Click: "+ Add Action"
2. Select: "Send Email"
3. Configure:
   - To: {{contact.email}} (client email)
   - From: Your Symphony Core email
   - Reply To: Account manager email
   - BCC: Account manager
   - Subject: "Your Weekly Lead Report - [Client Name]"
```

### 9.4 Email Template
```
Email Body (use HTML editor):

---

Hi {{contact.first_name}},

Here's your weekly lead report for [Date Range].

🎯 This week's highlights:
- [X] new leads generated
- [Top source] was your best performer
- [One key insight]

[Button: VIEW FULL REPORT]
Link: [Insert Dashboard Public Link]

Questions? Just reply to this email.

Best,
Symphony Core Team

---
```

### 9.5 PDF Export (Plan-Specific)

⚠️ **Plan Requirement:** PDF dashboard export requires custom dashboard feature.

**$297 Plan:**
```
✅ PDF export available (basic functionality)
✅ RECOMMENDED: Use live dashboard link instead of PDF
   - More engaging and interactive
   - Updates in real-time (no manual exports)
   - Better mobile experience
   - Reduces manual work
```

**$497+ Plan:**
```
✅ PDF export available with full customization
✅ Can automate PDF generation and email attachment
✅ Still recommended: Live dashboard link for better engagement
```

**If client explicitly requests PDF ($297 or $497+ plan):**
```
1. Add Action: Export Dashboard to PDF
2. Configure: Select dashboard
3. Add Action: Attach to Email
4. Link: PDF output to email action

⚠️ NOTE: This increases workflow complexity and
manual maintenance. Recommend live link unless
client has specific compliance requirement.
```

**Recommended Approach for All Plans:**
```
- Send live dashboard link via email (Step 9.4)
- Highlight benefits: Real-time data, interactive, mobile-friendly
- Reserve PDF for clients with offline viewing requirements
- Most clients prefer live dashboard link over PDF
```

### 9.6 Activate Workflow
```
1. Click: "Save Workflow"
2. Toggle: "Active" (turn on)
3. Test: Send test email to yourself first
```

---

## Step 10: Document & Clone/Rebuild (Plan-Specific)

### 10.1 Document Settings
```
Create note with:
- Dashboard name
- Public link URL
- Widget configurations
- Any client-specific customizations
- Plan tier used ($297 or $497+)
```

### 10.2 Deploy to Additional Clients (Plan-Specific Instructions)

⚠️ **CRITICAL:** Deployment process differs significantly based on your GHL plan tier.

---

#### **Option A: $497+ Plan - Dashboard Duplication (RECOMMENDED)**

✅ **GHL Capability:** Duplicate dashboard to other sub-accounts

**Time per client:** 15 minutes

**Steps:**
```
1. Open master template dashboard
2. Click: Settings (gear icon)
3. Select: "Duplicate to another sub-account"
4. Choose: Target client sub-account
5. Confirm: Dashboard duplicated successfully
6. Navigate: To client sub-account
7. Open: Newly duplicated dashboard
8. Update: Widget 4 (Insight) with client-specific observations
9. Update: Widget 5 (Contact) with client's account manager info
10. Generate: New public link for this client
11. Test: Verify all widgets display correct client data
12. Create: Email automation workflow (Step 9) for this client
```

**Benefits:**
- Fast deployment (15 min vs 30 min)
- Consistent formatting across all clients
- Easy to propagate updates across dashboards
- Can maintain multiple dashboard templates

---

#### **Option B: $297 Plan - Manual Rebuild (LIMITED)**

⚠️ **Plan Limitation:** $297 plan allows only 1 custom dashboard; cannot duplicate across sub-accounts

**Time per client:** 25-30 minutes

**Workaround Strategy:**
```
Option B1: Build in Agency Account (Testing Only)
- Build master template in agency account first
- Use for internal testing and validation
- Document exact configuration steps
- Manually rebuild in each client sub-account

Option B2: Build Directly in Client Sub-Account
- Choose your highest-priority client
- Build dashboard directly in their sub-account
- Take detailed screenshots of each widget configuration
- Use screenshots as reference to rebuild for other clients
```

**Manual Rebuild Steps for Each Client:**
```
1. Access: Client sub-account
2. Follow: Steps 1-9 from this guide exactly
3. Reference: Master template screenshots/documentation
4. Build: All 5 widgets from scratch (Steps 2-6)
5. Configure: Dashboard settings (Step 7)
6. Test: Validate data accuracy (Step 8)
7. Create: Email automation (Step 9)
8. Document: Client-specific configurations
9. Repeat: For next client
```

**Time Benchmarks ($297 Plan):**
```
- First dashboard: 30 minutes (learning curve)
- Subsequent dashboards: 25 minutes each
- 10 clients: ~4.5 hours total
- 20 clients: ~8.5 hours total
```

**Tips to Speed Up Manual Rebuild:**
```
- Create detailed checklist with exact widget settings
- Take screenshots of every configuration screen
- Copy/paste widget titles and text content from document
- Build 2-3 dashboards in one session to stay in flow
- Consider upgrading to $497+ plan if managing 10+ clients
```

---

### 10.3 Time Comparison

**$497+ Plan (Cloning):**
```
First dashboard:     27 min
Subsequent clients:  15 min each
10 clients total:    ~2.5 hours
20 clients total:    ~5 hours
```

**$297 Plan (Manual Rebuild):**
```
First dashboard:     30 min
Subsequent clients:  25 min each
10 clients total:    ~4.5 hours
20 clients total:    ~8.5 hours
```

**Time savings with $497+ plan:** ~50% faster for multi-client deployments

---

### 10.4 Plan Upgrade Recommendation

**Consider upgrading to $497+ plan if:**
- You manage 10+ client sub-accounts
- You need multiple dashboard templates (early-stage vs mature clients)
- You want to iterate and improve dashboards across all clients quickly
- Time savings (40+ hours/year) justify the plan cost difference
- You plan to scale client reporting as a core service offering

---

## Troubleshooting

### Widget Shows "No Data"
**Solutions:**
- Verify date range includes data
- Check custom field `lead_source_primary` exists
- Ensure contacts were created in selected timeframe
- Check filters aren't too restrictive

### Source Table is Empty
**Solutions:**
- Verify `lead_source_primary` field is populated on contacts
- Check if field name matches exactly
- Ensure data exists in last 7 days
- Consider showing "Source tracking coming soon" in insight text

### Trend Chart Shows Flat Line
**Solutions:**
- Extend date range to 30+ days
- Check if client has consistent lead flow
- Consider changing to monthly view for low-volume clients
- Normal for very new clients (not enough data yet)

### Email Automation Not Sending
**Solutions:**
- Verify workflow is active (toggle on)
- Check schedule settings (correct day/time)
- Ensure email address is valid
- Test with your own email first
- Check spam folder

### Dashboard Link Not Working
**Solutions:**
- Regenerate public link
- Check permissions (visibility settings)
- Verify link wasn't deleted
- Ensure client isn't blocked from viewing

---

## Time Benchmarks

### First Dashboard Build
```
Step 1: Create dashboard          2 min
Step 2: Key number widget         3 min
Step 3: Source table widget       4 min
Step 4: Trend chart widget        3 min
Step 5: Insight text widget       2 min
Step 6: Contact widget            1 min
Step 7: Dashboard settings        2 min
Step 8: Test & validate           3 min
Step 9: Email automation          5 min
Step 10: Document                 2 min
----------------------------------------
Total:                           27 min
```

### Subsequent Dashboards (Cloning)
```
Clone dashboard                   2 min
Update client-specific info       3 min
Update insight text               2 min
Create email automation           5 min
Test                             3 min
----------------------------------------
Total:                          15 min
```

**Goal:** Under 20 minutes per client after first one.

---

## Weekly Maintenance Checklist

**Every Monday morning (before 8 AM):**

```
For each client:
1. Open dashboard (30 sec)
2. Review key number and sources (30 sec)
3. Update insight text widget:
   - What's working: [observation] (1 min)
   - Action this week: [specific action] (30 sec)
4. Save changes (10 sec)

Total: 2-3 minutes per client
```

**For 20 clients:** 40-60 minutes every Monday

---

## Quick Reference Card

**Dashboard Structure:**
```
┌─────────────────────────────────────┐
│ 1. KEY NUMBER (full width)         │
├──────────────────┬──────────────────┤
│ 2. SOURCES       │ 3. TREND         │
│    (half width)  │    (half width)  │
├──────────────────┴──────────────────┤
│ 4. INSIGHT (full width)             │
├─────────────────────────────────────┤
│ 5. CONTACT (full width)             │
└─────────────────────────────────────┘
```

**GHL Widget Types Used:**
1. Number widget (key metric)
2. Table widget (sources)
3. Line chart widget (trend)
4. Text widget x2 (insight + contact)

**Total:** 5 widgets, single page, no scrolling

---

## Next Steps After Build

1. **Test with pilot clients** (1-2 clients first)
2. **Collect feedback** (what's clear, what's confusing?)
3. **Refine template** (adjust based on feedback)
4. **Roll out to 5-10 more clients** (week 2)
5. **Scale to all clients** (weeks 3-4)

**Ready to build?** Start with Step 1!

---

## GHL Widget Types Reference

✅ **Verified GHL Widget Categories Available:**

### Contact-Based Widgets
- **Number Widget:** Display contact count with period comparison
- **Table Widget:** Group contacts by custom fields, tags, or source
- **Chart Widgets:** Line, Bar, Horizontal Bar, Donut for contact trends

### Appointment Widgets
- Count by status, confirmed, showed, cancelled, no-shows
- Trend analysis over time

### Text & Embed Widgets
- **Rich Text Widget:** HTML-formatted content (for insights)
- **Simple Text Widget:** Plain text (for contact information)
- **Embed Widget:** External content via iframe

### Visualization Options
- Period comparisons (automatic calculation)
- Date range filtering (7, 30, 90 days, custom)
- Grouping by day, week, month
- Top N filtering (e.g., top 5 sources)

---

## Widget Configuration Limits

🔧 **Known GHL Technical Limitations:**

### Conditional Display
- ❌ **NOT SUPPORTED:** Single widget that auto-switches between metrics
- ❌ **NOT SUPPORTED:** Conditional logic within widget configuration
- ✅ **WORKAROUND:** Create multiple widgets, configure visibility per deployment

### Data Requirements
- ⚠️ **Custom fields must exist and be populated** before creating widgets
- ⚠️ **Empty custom fields cause widget to fail silently** (shows "No Data")
- ✅ **BEST PRACTICE:** Always validate data exists before creating grouped/filtered widgets

### Plan-Specific Limitations
- **$297 Plan:**
  - ⚠️ Limited to 1 custom dashboard
  - ⚠️ Cannot duplicate to other sub-accounts
  - ✅ PDF export available (basic)

- **$497+ Plan:**
  - ✅ Unlimited custom dashboards
  - ✅ Dashboard duplication across sub-accounts
  - ✅ PDF export with full customization

### Public Link Permissions
- ⚠️ Public link permissions tied to dashboard visibility settings
- ⚠️ Anyone with link can view if public access enabled
- ✅ Use password protection for sensitive data

### Widget Refresh
- ✅ Auto-refresh available (configurable: 1, 5, 15 min)
- ✅ Manual refresh via date range selector
- ⚠️ Some widgets may have slight delay in data updates

---

## Validation Checklist

**Before considering this guide "production-ready," verify:**

- [ ] No mention of single "conditional" widget for appointments vs leads
- [ ] Dual widget approach clearly explained in Step 2
- [ ] Lead sources table includes prerequisite check (Step 3.0)
- [ ] All permission configurations documented (Step 7.2)
- [ ] Plan requirements stated at document start
- [ ] Cloning instructions are plan-specific (Step 10)
- [ ] Email automation doesn't assume PDF export (Step 9.5)
- [ ] All widget types mentioned are verified as available
- [ ] Custom field requirements are explicit
- [ ] Mobile view testing included (Step 8.3)
- [ ] Troubleshooting section includes GHL-specific limitations
- [ ] Version date and platform update notes added

---

**Document Owner:** Symphony Core Platform Team
**Last Updated:** 2025-11-03
**Platform Version:** GoHighLevel as of November 2025
**Validation Status:** ✅ Verified against actual GHL capabilities
**Related:** `phase-1-simplified-specifications.md` (full specs)
