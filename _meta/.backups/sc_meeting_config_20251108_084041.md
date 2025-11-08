# SC Meeting Software Configuration

## Overview

Symphony Core (SC) uses Google Meet as the standard video conferencing platform, integrated with Fireflies AI for automated meeting transcription and note-taking.

## Platform Components

### Google Meet
- **Primary video conferencing platform** for all internal and client meetings
- **Integration**: Connected to Google Workspace calendar system
- **Access**: Available through Google Calendar meeting links
- **Features**: Screen sharing, recording capabilities, dial-in options

### Fireflies AI
- **AI-powered meeting assistant** for automatic transcription and note-taking
- **Integration**: Joins Google Meet sessions automatically when invited
- **Output**: Generates searchable transcripts, action items, and meeting summaries
- **Storage**: Meeting data synced to designated workspace for team access

## Configuration Setup

### Google Meet Settings
- Default meeting length: 60 minutes
- Automatic calendar integration enabled
- Recording permissions: Host and co-hosts
- External participant access: By invitation only

### Fireflies Integration
- Auto-join meetings: Enabled for scheduled calendar events
- Meeting detection: Automatic for Google Meet links
- Transcript sharing: Automatic to meeting participants
- Action item extraction: Enabled with assignee tagging

## Meeting Workflow

1. **Meeting Scheduling**: Create Google Calendar event with Google Meet link
2. **Fireflies Invitation**: Add Fireflies bot (fred@fireflies.ai) to meeting attendees
3. **Meeting Execution**: Fireflies automatically joins and records
4. **Post-Meeting**: Transcript and summary delivered within 5 minutes
5. **Follow-up**: Action items distributed to relevant team members

## Access and Permissions

- All SC team members have Google Workspace access
- Fireflies workspace shared with authorized personnel
- Client meetings: Fireflies included only with explicit consent
- Sensitive meetings: Manual recording control available

## Data Management

- **Retention**: Meeting transcripts stored for 12 months
- **Privacy**: Client meeting recordings require consent
- **Security**: All data encrypted in transit and at rest
- **Backup**: Transcripts automatically synced to Google Drive