# Elementor Pro Website Setup Best Practices Guide

---
**Version:** 1.0  
**Author:** Symphony Core Systems Team  
**Last Updated:** 2025-10-07  
**Category:** Best Practices  
**Tags:** [elementor-pro, wordpress, setup, design-system, best-practices]  
**Status:** Active  
---

![Active](https://img.shields.io/badge/status-active-green)

## Purpose

This guide provides comprehensive best practices for setting up WordPress websites using Elementor Pro. It covers the essential steps from initial installation through advanced configuration, including specific procedures for uploading logos, favicons, and establishing global design systems.

**Document Relationship:**
- **WordPress + GHL Developer Guide:** Strategic architecture and integration patterns
- **GHL WordPress Setup Procedures:** Platform-specific hosting configuration
- **This Document:** Elementor Pro implementation best practices

---

## Prerequisites

### Required Components
- WordPress installation (preferably on GHL hosting)
- Elementor Pro license and plugin files
- Hello Elementor theme installed and activated
- Client brand assets (logo, favicon, fonts, color palette)
- Basic understanding of WordPress admin interface

### Before You Begin
- Ensure WordPress is fully updated
- Verify Hello Elementor theme is active
- Have client brand guidelines and assets organized
- Clear browser cache and disable caching plugins during setup

---

## Phase 1: Initial Elementor Pro Setup

### Step 1: Install and Activate Elementor Pro

1. **Install Free Elementor Plugin**
   - Navigate to **Plugins > Add New**
   - Search for "Elementor"
   - Install and activate the free Elementor plugin first

2. **Install Elementor Pro**
   - Download Elementor Pro zip file from client portal
   - Navigate to **Plugins > Add New > Upload Plugin**
   - Upload the Elementor Pro zip file
   - Activate Elementor Pro

3. **License Activation**
   - Navigate to **Elementor > License**
   - Enter your Elementor Pro license key
   - Click **Activate License**
   - Verify "License Activated" status appears

### Step 2: Configure Essential Elementor Settings

1. **Disable Default Assets**
   - Navigate to **Elementor > Settings > General**
   - Check **"Disable Default Colors"**
   - Check **"Disable Default Fonts"**
   - Click **Save Changes**

   *Why: Forces use of global design system instead of Elementor defaults*

2. **Configure Editor Preferences**
   - Navigate to **Elementor > Settings > Editor**
   - Set **"Color Picker Format"** to **"HEX"**
   - Enable **"Default Editing Mode"** as **"Canvas"**
   - Click **Save Changes**

3. **Enable Performance Features**
   - Navigate to **Elementor > Settings > Experiments**
   - Enable **"Improved CSS Loading"**
   - Enable **"Optimized DOM Output"**
   - Enable **"Container"** (for newer layouts)
   - Click **Save Changes**

---

## Phase 2: Site Identity and Brand Assets

### Step 3: Upload Site Logo

1. **Access Site Identity Settings**
   - Navigate to **Appearance > Customize**
   - Click **Site Identity**

2. **Upload Logo**
   - Click **"Select Logo"** button
   - Upload logo file (recommended: PNG with transparent background, max 300px height)
   - Crop if necessary to maintain aspect ratio
   - Click **"Select"** to confirm

3. **Configure Logo Display**
   - Set logo width (typically 150-200px for header)
   - Preview logo appearance in customizer
   - Click **"Publish"** to save changes

**Logo Best Practices:**
- File format: PNG with transparent background
- Dimensions: 300px height maximum, scalable width
- File size: Under 100KB for optimal loading
- Provide both horizontal and stacked versions

### Step 4: Upload Favicon (Site Icon)

1. **Prepare Favicon File**
   - Create square image (minimum 512x512 pixels)
   - Use PNG format with transparent background
   - Keep design simple and recognizable at small sizes

2. **Upload via WordPress Customizer**
   - In **Appearance > Customize > Site Identity**
   - Scroll to **"Site Icon"** section
   - Click **"Select Site Icon"**
   - Upload prepared favicon image
   - WordPress will automatically generate required sizes
   - Click **"Publish"** to save

3. **Verify Favicon Display**
   - Check browser tab shows new favicon
   - Test across different browsers (Chrome, Firefox, Safari)
   - May take 24-48 hours to appear in all locations

**Favicon Technical Requirements:**
- Minimum size: 512x512 pixels
- Format: PNG recommended (supports transparency)
- Square ratio maintained
- Simple, recognizable design at 16x16 pixel size

---

## Phase 3: Global Design System Configuration

### Step 5: Set Up Global Colors

1. **Access Site Settings**
   - Edit any page with Elementor
   - Click hamburger menu (☰) in top-left corner
   - Select **"Site Settings"**

2. **Configure Primary Brand Colors**
   - Click **"Global Colors"**
   - Replace system colors with brand palette:
     - **Primary:** Main brand color
     - **Secondary:** Complementary/accent color  
     - **Text:** Primary text color (usually dark gray, not pure black)
     - **Accent:** Call-to-action color (high contrast)

3. **Add Additional Brand Colors**
   - Click **"+ Add Color"**
   - Name descriptively (e.g., "Brand Blue", "Warning Red")
   - Enter exact HEX values from brand guidelines
   - Create 6-8 total colors maximum

**Global Color Best Practices:**
- Use brand guideline HEX values exactly
- Name colors functionally, not descriptively ("Primary" vs "Blue")
- Include light/dark variations for backgrounds
- Test color contrast for accessibility (minimum 4.5:1 ratio)

### Step 6: Configure Global Typography

1. **Set Primary Font Stack**
   - In Site Settings, click **"Global Fonts"**
   - Click **"+ Add Font"**
   - Configure **Primary** font:
     - Font Family: Client's primary brand font
     - Font Weight: 400 (Regular)
     - Text Transform: None
     - Font Style: Normal
     - Text Decoration: None

2. **Configure Secondary Font**
   - Add **Secondary** font for headings or accents
   - Set appropriate font weights (300, 400, 600, 700)
   - Configure for each screen size if needed

3. **Set Up Typography Hierarchy**
   - Create global fonts for:
     - **H1:** Largest heading (32-48px)
     - **H2:** Section headings (24-32px)
     - **H3:** Subsection headings (20-24px)
     - **Body Text:** Paragraph text (16-18px)
     - **Small Text:** Captions, disclaimers (14px)

**Typography Best Practices:**
- Limit to 2 font families maximum
- Use web-safe fonts or local hosting
- Configure font weights: 400 (regular), 600 (semibold), 700 (bold)
- Test readability at smallest screen sizes
- Maintain consistent line-height ratios (1.4-1.6)

### Step 7: Configure Theme Style Settings

1. **Set Default Button Styles**
   - In Site Settings, navigate to **"Theme Style > Buttons"**
   - Configure default button appearance:
     - Background Color: Use global primary color
     - Text Color: White or contrasting color
     - Border: None or subtle outline
     - Border Radius: Consistent with brand (0px, 4px, or 8px)
     - Padding: Adequate touch target (12px vertical, 24px horizontal)

2. **Configure Form Field Styles**
   - Navigate to **"Theme Style > Form Fields"**
   - Set consistent styling:
     - Background: Light gray or white
     - Border: 1px solid light gray
     - Focus state: Highlight with primary color
     - Padding: Comfortable input size

3. **Set Image Default Styles**
   - Navigate to **"Theme Style > Images"**
   - Configure default border radius and shadows
   - Set consistent spacing and alignment

---

## Phase 4: Page Structure and Templates

### Step 8: Create Header Template

1. **Access Theme Builder**
   - Navigate to **Elementor > Theme Builder**
   - Click **"Add New"** > **"Header"**

2. **Design Header Structure**
   - Add Container/Section
   - Insert **Site Logo** widget
   - Add **Nav Menu** widget
   - Include **CTA Button** if needed
   - Configure responsive behavior

3. **Configure Header Settings**
   - Set sticky behavior if desired
   - Configure mobile menu breakpoint
   - Set display conditions to **"Entire Site"**
   - Click **"Publish"**

### Step 9: Create Footer Template

1. **Create Footer Template**
   - Navigate to **Theme Builder > Add New > Footer**
   - Design footer with:
     - Logo or company name
     - Contact information
     - Social media links
     - Copyright notice
     - Required legal links

2. **Configure Footer Display**
   - Set display conditions to **"Entire Site"**
   - Ensure responsive design works properly
   - Test footer on different page types

### Step 10: Optimize Global Settings

1. **Configure Layout Settings**
   - In Site Settings, navigate to **"Layout"**
   - Set **Content Width:** 1200px (standard)
   - Configure **Container Gap:** 20px
   - Set **Mobile Breakpoints:**
     - Mobile: 768px
     - Tablet: 1024px

2. **Set Default Background**
   - Navigate to **"Site Settings > Background"**
   - Set site-wide background color (usually white or light gray)
   - Configure for consistency across all pages

---

## Phase 5: Content Creation and Optimization

### Step 11: Create Page Templates

1. **Design Standard Page Template**
   - Create reusable sections for:
     - Hero/banner area
     - Content blocks
     - Call-to-action sections
     - Contact forms

2. **Save as Elementor Templates**
   - Select designed section
   - Right-click and **"Save as Template"**
   - Name descriptively for reuse
   - Organize in template library

### Step 12: Implement SEO Best Practices

1. **Configure Meta Information**
   - Set unique page titles using SEO plugins
   - Write compelling meta descriptions
   - Use header tags (H1, H2, H3) properly
   - Optimize images with alt text

2. **Implement SearchAtlas Integration**
   - Install SearchAtlas SEO Plugin
   - Configure OTTO pixel
   - Connect Google Search Console
   - Monitor automated optimizations

---

## Phase 6: Performance and Testing

### Step 13: Optimize for Performance

1. **Image Optimization**
   - Compress all images before upload
   - Use WebP format where supported
   - Implement lazy loading for images
   - Set appropriate image dimensions

2. **Font Performance**
   - Host fonts locally when possible
   - Use only necessary font weights
   - Implement font-display: swap
   - Preload critical fonts

3. **CSS and JavaScript Optimization**
   - Enable Elementor's improved CSS loading
   - Remove unused Elementor widgets
   - Minify CSS and JS files
   - Implement caching solutions

### Step 14: Mobile Responsiveness Testing

1. **Test Responsive Design**
   - Preview at mobile breakpoints (320px, 768px, 1024px)
   - Verify touch targets are minimum 44px
   - Ensure text remains readable
   - Test form functionality on mobile

2. **Cross-Browser Testing**
   - Test in Chrome, Firefox, Safari, Edge
   - Verify functionality across browsers
   - Check for CSS compatibility issues
   - Test form submissions and interactions

### Step 15: Integration Testing

1. **GHL Integration Verification**
   - Test LeadConnector plugin functionality
   - Verify chat widgets display correctly
   - Confirm form submissions route to GHL CRM
   - Test calendar booking widgets

2. **SEO Tools Integration**
   - Verify OTTO pixel firing
   - Test SearchAtlas dashboard connection
   - Confirm Google Search Console linking
   - Monitor initial SEO recommendations

---

## Quality Assurance Checklist

### Pre-Launch Verification

**Design System:**
- [ ] Global colors applied consistently
- [ ] Typography hierarchy implemented
- [ ] Logo displays properly in all contexts
- [ ] Favicon appears in browser tabs

**Performance:**
- [ ] Page load speeds under 3 seconds
- [ ] Images optimized and compressed
- [ ] Mobile responsive design tested
- [ ] Cross-browser compatibility verified

**Functionality:**
- [ ] All forms submit correctly
- [ ] Chat widgets function properly
- [ ] Navigation works on all devices
- [ ] Search functionality operational

**SEO:**
- [ ] OTTO pixel active and monitoring
- [ ] Meta titles and descriptions unique
- [ ] Header structure (H1, H2, H3) proper
- [ ] Image alt text implemented

**Integration:**
- [ ] GHL forms embedded correctly
- [ ] Chat widgets connect to proper inbox
- [ ] Calendar bookings sync properly
- [ ] Lead data flows to CRM correctly

---

## Maintenance and Updates

### Weekly Tasks
- Review OTTO Dashboard for new SEO suggestions
- Check form submission rates and functionality
- Monitor chat widget performance
- Verify backup completion

### Monthly Tasks
- Update Elementor Pro after staging tests
- Review and optimize page performance
- Clean up unused templates and assets
- Audit global design system usage

### Quarterly Tasks
- Comprehensive SEO performance review
- Design system evaluation and updates
- Performance benchmarking against competitors
- Template library organization and cleanup

---

## Troubleshooting Common Issues

### Design System Problems

**Issue:** Global colors not applying consistently
**Solution:**
1. Verify "Disable Default Colors" is checked
2. Regenerate CSS files in Elementor settings
3. Clear all caching systems
4. Re-save global color settings

**Issue:** Fonts not loading properly
**Solution:**
1. Check font hosting method (local vs Google Fonts)
2. Verify font weights are properly defined
3. Clear browser cache and CDN cache
4. Test with font-display: swap CSS property

### Performance Issues

**Issue:** Slow page loading with Elementor
**Solution:**
1. Enable Elementor's performance experiments
2. Optimize image sizes and formats
3. Remove unused Elementor widgets from settings
4. Implement proper caching strategy
5. Use minimal plugin approach

### Mobile Responsiveness Problems

**Issue:** Elements not displaying properly on mobile
**Solution:**
1. Use Elementor's responsive editing mode
2. Test at specific breakpoints (320px, 768px)
3. Adjust mobile-specific settings for each element
4. Verify touch targets meet 44px minimum
5. Test horizontal scrolling issues

---

## Advanced Tips and Best Practices

### Design System Optimization

1. **Color Psychology Application**
   - Use primary colors for main CTAs
   - Apply secondary colors for supporting elements
   - Reserve accent colors for urgent actions
   - Maintain sufficient contrast ratios

2. **Typography Hierarchy**
   - Establish clear visual hierarchy with font sizes
   - Use consistent spacing between elements
   - Limit line length to 60-70 characters
   - Implement proper paragraph spacing

3. **Component Reusability**
   - Create modular design components
   - Save frequently used sections as templates
   - Use global widgets for consistent elements
   - Document component usage guidelines

### Performance Optimization

1. **Resource Loading Strategy**
   - Preload critical fonts and images
   - Defer non-critical JavaScript
   - Implement lazy loading for below-fold content
   - Use CDN for static assets

2. **Database Optimization**
   - Regular database cleanup and optimization
   - Remove unused post revisions
   - Clean up unused media files
   - Optimize database tables

### User Experience Enhancement

1. **Accessibility Improvements**
   - Implement proper ARIA labels
   - Ensure keyboard navigation works
   - Provide alt text for all images
   - Maintain sufficient color contrast

2. **Conversion Optimization**
   - Place CTAs above the fold
   - Use contrasting colors for action buttons
   - Implement clear visual hierarchy
   - Reduce form field requirements

---

## Resource Links and Documentation

### Official Documentation
- [Elementor Pro Documentation](https://elementor.com/help/)
- [WordPress Customizer Guide](https://wordpress.org/support/article/customizer/)
- [Hello Elementor Theme](https://github.com/elementor/hello-elementor)

### Performance Resources
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix Performance Testing](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

### Design Resources
- [Adobe Color Wheel](https://color.adobe.com/)
- [Google Fonts](https://fonts.google.com/)
- [Coolors Palette Generator](https://coolors.co/)

---

## Document Status

**Status:** Active  
**Last Updated:** October 7, 2025  
**Version:** 1.0  
**Next Review:** January 7, 2026

**Update Triggers:**
- Elementor Pro major version releases
- WordPress core updates affecting customizer
- New SEO optimization requirements
- Performance optimization discoveries

**Feedback:** Submit suggestions to documentation team or project channel