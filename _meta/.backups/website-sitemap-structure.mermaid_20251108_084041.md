# SC Local Business Website Structure Guide

## Overview

This guide outlines the standard website structure for Symphony Core local business websites. The structure is designed to provide optimal user experience, clear navigation, and effective organization of business information across different content categories.

## Structure Philosophy

The website structure follows a hub-based organizational model where content is logically grouped into four main categories (hubs). These hubs are **conceptual groupings** rather than actual pages, serving to organize the site's information architecture.

## Core Structure Elements

### Homepage
The central landing page that connects to all main content areas and provides the primary entry point for visitors.

### Four Content Hubs

1. **Brand Hub** - Company identity and relationship pages
2. **Service Hub** - Service offerings and capabilities
3. **Resource Hub** - Educational and trust-building content
4. **Location Hub** - Geographic presence and local market information

### Page Hierarchy

```mermaid
flowchart LR
    A[HOMEPAGE] --> B[Brand]
    A --> C[Service Hub]
    A --> D[Resource Hub]
    A --> E[Location Hub]
    
    B --> B1[About Us]
    B --> B2[Contact Us]
    B --> B3[Work with Us]
    
    C --> C1[Service 1]
    C --> C2[Service 2]
    
    D --> D1[Blog]
    D --> D2[Case Studies]
    D --> D3[Testimonials]
    
    E --> E1[Location 1]
    E --> E2[Location 2]
    E --> E3[Location 3]
    
    E1 --> E1A[Strength 5]
    E1 --> E1B[Strength 6]
    
    E2 --> E2A[Strength 4]
    E2 --> E2B[Strength 7]
    
    E3 --> E3A[Strength 8]
    
    classDef homepage fill:#7dd3c0
    classDef mainHub fill:#4a9eff
    classDef subPage fill:#8b5cf6
    classDef strength fill:#ec4899
    
    class A homepage
    class B,C,D,E mainHub
    class B1,B2,B3,C1,C2,D1,D2,D3,E1,E2,E3 subPage
    class E1A,E1B,E2A,E2B,E3A strength
```

## Detailed Structure Breakdown

### Brand Hub
**Purpose**: Establish company identity and facilitate customer relationships

- **About Us**: Company history, mission, values, team
- **Contact Us**: Contact information, forms, office details
- **Work with Us**: Career opportunities, partnerships, vendor information

### Service Hub
**Purpose**: Present business offerings and capabilities

- **Service 1**: Primary service offering with detailed information
- **Service 2**: Secondary service offering with detailed information
- *Note: Additional services can be added as needed (Service 3, 4, etc.)*

### Resource Hub
**Purpose**: Provide valuable content that builds trust and demonstrates expertise

- **Blog**: Regular content updates, industry insights, company news
- **Case Studies**: Detailed project examples and success stories
- **Testimonials**: Client feedback and reviews

### Location Hub
**Purpose**: Address geographic markets and local presence

- **Location 1/2/3**: Individual location pages for different geographic markets
- **Strength Items**: Specific local advantages, partnerships, or capabilities unique to each location

## Implementation Guidelines

### Navigation Structure
- Hubs should be reflected in main navigation categories
- Sub-pages should be accessible through dropdown menus or section navigation
- Breadcrumb navigation should reflect the hub structure

### Content Strategy
- Each hub should have consistent design and layout patterns
- Cross-linking between hubs should be strategic and purposeful
- Local content should be tailored to specific geographic markets

### SEO Considerations
- Hub structure supports topic clustering for improved search performance
- Location pages enable local SEO optimization
- Resource hub provides ongoing content marketing opportunities

## Customization Notes

- Service offerings can be expanded beyond the basic two services shown
- Location hubs can be scaled based on business geographic footprint
- Strength items under locations should reflect actual local competitive advantages
- Additional resource types can be added to the Resource Hub as needed

This structure provides a scalable, organized foundation for local business websites that supports both user experience and business objectives.