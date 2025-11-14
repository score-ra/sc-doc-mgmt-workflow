---
title: Symphony Core Web Style Guide
tags: [brand, web, css, html]
---

# Symphony Core Web Style Guide

## HTML Structure

Use semantic HTML5 elements:

```
<header class="site-header">
  <nav class="main-nav">
    <a href="/" class="logo">Symphony Core</a>
  </nav>
</header>
```

## CSS Conventions

Follow BEM naming:

```
.card {
  border: 1px solid #e5e7eb;
}

.card__title {
  font-size: 1.25rem;
  font-weight: 600;
}
```

## Component Library

All components available at `/components`.
