# Fireflies Integration Guide for Symphony Core
*Living Document - Version 1.1*

## Symphony Core Business Context

Based on Symphony Core's Connecticut marketing automation focus, Fireflies will support:

- **Primary Services:** Marketing automation, lead generation systems, customer communication automation
- **Target Clients:** Connecticut businesses (home services, real estate, professional services)
- **Core Activities:** Sales calls, website/marketing project reviews, team coordination

## Phase 1: Current State & Immediate Setup

### 1.1 Verified Integrations

**Google Workspace:** Active  
**Slack:** Next priority integration  
**Single User:** rohit@symphonycore.com (Business plan)

### 1.2 Immediate Pain Point Resolution

**Current Issue:** Manual transfer of Fireflies exports from Google Drive to client folders

**Automated Solution Setup:**
1. Configure Fireflies Google Drive integration to use client-specific folder structure
2. Set up Zapier automation for intelligent file routing
3. Create naming convention that triggers automatic sorting

## Phase 2: Symphony Core Specific Channel Architecture

### 2.1 Client Channel Structure

**Format:** client-clientaccountname

**Examples Based on SC Service Types:**

```
client-upscalelegal
client-connecticuthomeservices
client-hartfordrealty
client-newhavenmedical
client-clientaccountname
```

### 2.2 Internal Operations Channels

```
internal-sales-pipeline
internal-project-reviews
internal-team-meetings
internal-strategy-sessions
```

### 2.3 Personal Audio Notes Channel

```
personal-audionotes-2025
personal-client-insights
personal-strategy-thoughts
```

**Separation Rule:** Personal channels are private and not integrated with client workflows

## Phase 3: Connecticut Business Topic Trackers
### Phase 3.1 Symphony Core Service Topics

Based on your marketing automation platform:

**Topic Name:** Lead Generation  
**Keywords:** lead, prospect, conversion, funnel, qualified, interested, follow-up

**Topic Name:** Marketing Automation  
**Keywords:** automation, workflow, campaign, email, sequence, trigger, nurture

**Topic Name:** Website Projects  
**Keywords:** website, design, development, launch, responsive, SEO, conversion

**Topic Name:** Connecticut Business Types  
**Keywords:** home services, real estate, professional services, Connecticut, CT, local business

**Topic Name:** Pain Points CT Businesses  
**Keywords:** local competition, seasonal business, Connecticut regulations, customer acquisition, lead quality, conversion rate

**Topic Name:** Budget Indicators  
**Keywords:** investment, budget, ROI, cost per lead, monthly, annual, package, pricing

**Topic Name:** Decision Making  
**Keywords:** owner, manager, partner, board, approval, decision, review, consider

**Topic Name:** Website Review  
**Keywords:** mobile, responsive, loading speed, SEO, conversion, lead capture, call-to-action

**Topic Name:** Marketing Campaign Performance  
**Keywords:** open rate, click rate, conversion, ROI, A/B test, optimization, performance

## Phase 4: Google Drive Automation Solution

### 4.1 Intelligent File Routing Setup

**Zapier Automation Workflow:**

```
Trigger: New Fireflies transcript in Google Drive
Condition: Parse meeting title for client name
Action: Move file to appropriate client folder
Format: /Clients/client-name/Meetings/date-type.pdf
```

### 4.2 Proposed Google Drive Structure

```
Symphony Core - Fireflies/
  Clients/
    client-upscalelegal/
      Meetings/
      Action-Items/
    client-name/
  Internal/
    Sales-Pipeline/
    Project-Reviews/
    Team-Meetings/
  Personal/
    Audio-Notes/
    Daily-Insights/
```

## Phase 5: Meeting Type Workflows

### 5.1 Sales Call with Connecticut Business

**Channel:** internal-sales-pipeline  
**Topic Trackers:** Connecticut business types, pain points, budget indicators  
**Auto-Actions:**
- Create follow-up task in project management system
- Update prospect status based on sentiment analysis
- Route transcript to Sales folder in Google Drive

### 5.2 Client Website/Marketing Review

**Channel:** client-clientname  
**Topic Trackers:** Website performance, marketing metrics, optimization  
**Auto-Actions:**
- Save to client-specific Google Drive folder
- Extract action items for project tracking
- Send summary to client communication channel

### 5.3 Internal Team Meeting

**Channel:** internal-team-meetings  
**Topic Trackers:** Project updates, team decisions, resource allocation  
**Auto-Actions:**
- Distribute summary via Slack
- Create tasks for action items
- Archive in Internal folder

### 5.4 Personal Audio Notes (Daily)

**Channel:** personal-audionotes-2025  
**Privacy:** Private (no team access)  
**Workflow:**
1. Upload from Philips recorder
2. Auto-transcribe with personal topic tracking
3. Store in separate personal folders
4. Optional: Link insights to relevant client work (manual decision)

## Phase 6: Slack Integration Setup

### 6.1 Slack Workflow Configuration

**Sales Call Notifications:**
- Channel: #sales-pipeline
- Content: Meeting summary + next steps + sentiment score

**Client Meeting Updates:**
- Channel: #client-updates
- Content: Client name + meeting type + key decisions + action items

**Internal Meeting Summaries:**
- Channel: #team-updates
- Content: Meeting highlights + decisions + task assignments

### 6.2 Slack Commands Setup

```
/fireflies search client-name - Find client meetings
/fireflies recent - Show last 5 meetings
/fireflies topics keyword - Search by topic
```

## Phase 7: Learning & Optimization System

### 7.1 Monthly Review Process

**Data Collection:**
- Meeting frequency by client type
- Most common topics by Connecticut business category
- Action item completion rates
- File routing accuracy

**Optimization Opportunities:**
- Refine topic trackers based on recurring themes
- Adjust channel structure based on usage patterns
- Update automation rules based on manual corrections needed

### 7.2 Recommendation Engine

**System learns from:**
- Manual file moves (indicates routing needs improvement)
- Frequently searched terms (suggests new topic trackers)
- Meeting patterns (suggests new channel categories)
- User corrections to transcripts (improves accuracy over time)

**Quarterly Recommendations:**
- New topic trackers for emerging themes
- Channel consolidation or expansion based on usage
- Integration opportunities with new tools
- Workflow optimizations based on pain points

## Phase 8: Implementation Roadmap

### Week 1: Foundation & Pain Point Resolution

- Verify Fireflies plan tier and update configuration
- Set up initial client channels using existing naming convention
- Configure Google Drive automation to solve manual transfer issue
- Set up basic topic trackers for Connecticut business types

### Week 2: Slack Integration & Workflows

- Complete Slack integration setup
- Configure notification workflows for different meeting types
- Test automated file routing with sample meetings
- Create personal audio notes workflow

### Week 3: Topic Refinement & Testing

- Monitor topic tracker accuracy
- Refine automation rules based on initial performance
- Test end-to-end workflows for each meeting type
- Document any issues or needed adjustments

### Week 4: Optimization & Documentation

- Analyze first month's usage patterns
- Create first set of learning-based recommendations
- Update configuration standard with actual settings
- Establish monthly review schedule

## Assumptions Being Validated

Following SC principles of not making assumptions, these items require validation:

### Technical Assumptions

- Current Google Drive folder structure and permissions
- Slack workspace configuration and admin permissions
- Philips audio recorder file format compatibility
- Internet connectivity requirements for daily uploads

### Business Process Assumptions

- Meeting frequency and types (validate against actual calendar)
- Client communication preferences (some may not want recorded meetings)
- Team expansion plans (impacts channel structure design)
- Integration priorities beyond Google Workspace and Slack

### User Workflow Assumptions

- Daily audio note recording consistency
- Meeting naming convention adherence
- Manual process documentation for current pain points
- Time available for system maintenance and optimization

## Success Metrics & Validation

### Immediate Success Indicators (Month 1)

- Elimination of manual file transfers from Google Drive
- 90%+ accuracy in automated client folder routing
- Successful daily personal audio note processing
- Complete Slack integration with relevant notifications

### Ongoing Optimization Metrics (Monthly)

- Topic tracker relevance score (% of meetings with meaningful topic matches)
- Channel utilization rates (identify underused or overloaded channels)
- Search effectiveness (time to find specific meetings reduced)
- Integration reliability (uptime and error rates)

### Learning Algorithm Inputs

- User search patterns → Suggest new topic trackers
- Manual file moves → Improve routing logic
- Channel usage statistics → Recommend structure changes
- Meeting type patterns → Suggest new automation workflows

## Next Document Updates

This living document will be updated based on:

1. **Configuration verification results** (Week 1)
2. **Initial usage patterns** (Month 1)
3. **First optimization cycle** (Month 3)
4. **User feedback and pain point resolution** (Ongoing)

---

*This guide follows Symphony Core standards of validation over assumption, creating a foundation that adapts based on actual usage patterns and measurable outcomes rather than theoretical best practices.*