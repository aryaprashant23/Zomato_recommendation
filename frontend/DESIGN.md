---
name: Obsidian Epicure
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#e5bdbe'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#ac8889'
  outline-variant: '#5c3f40'
  surface-tint: '#ffb3b6'
  primary: '#ffb3b6'
  on-primary: '#68001a'
  primary-container: '#e11d48'
  on-primary-container: '#fffaf9'
  inverse-primary: '#be0037'
  secondary: '#ffb95f'
  on-secondary: '#472a00'
  secondary-container: '#ee9800'
  on-secondary-container: '#5b3800'
  tertiary: '#7bd0ff'
  on-tertiary: '#00354a'
  tertiary-container: '#007ca8'
  on-tertiary-container: '#f8fbff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b6'
  on-primary-fixed: '#40000c'
  on-primary-fixed-variant: '#920028'
  secondary-fixed: '#ffddb8'
  secondary-fixed-dim: '#ffb95f'
  on-secondary-fixed: '#2a1700'
  on-secondary-fixed-variant: '#653e00'
  tertiary-fixed: '#c4e7ff'
  tertiary-fixed-dim: '#7bd0ff'
  on-tertiary-fixed: '#001e2c'
  on-tertiary-fixed-variant: '#004c69'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 24px
  margin-mobile: 16px
  sidebar-width: 280px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system embodies a "Digital Sommelier" persona—sophisticated, predictive, and exclusive. It targets high-end food enthusiasts and tech-forward urbanites who view dining as an experience rather than a utility. 

The visual style is **Futuristic Glassmorphism**. It combines the depth of high-end automotive interfaces with the clarity of modern SaaS. The aesthetic relies on deep obsidian layers, high-contrast typography, and "light-leak" accents that simulate an AI engine humming beneath a polished glass surface. The emotional response should be one of "effortless luxury" and "intelligent precision."

## Colors
The palette is rooted in the "Deep Sea" spectrum of slates and obsidians to provide a canvas where food photography and AI highlights can pop.

- **Primary (Crimson Red):** Used for critical actions, branding, and "hot" recommendations. It represents passion and appetite.
- **Secondary (Amber):** Reserved for star ratings, premium "Gold" status, and highlighting specific AI-matched flavor profiles.
- **Surface Strategy:** Backgrounds utilize `#020617`. Interactive containers use a semi-transparent `#0F172A` with a `backdrop-filter: blur(20px)`.
- **Text:** Primary text uses `Slate-50` for maximum legibility against dark backgrounds, while secondary metadata uses `Slate-400`.

## Typography
The system pairs the geometric, high-fashion feel of **Outfit** for headings with the systematic precision of **Inter** for UI and body text.

- **Headings:** Should always use a tighter letter-spacing to maintain a "prestige" editorial look.
- **Contrast:** Maintain a sharp hierarchy. Use Crimson Red or Amber for specific keywords within headings to draw the eye to AI insights.
- **Accessibility:** Given the dark theme, avoid font weights below 400 for body text to prevent "haloing" and ensure readability.

## Layout & Spacing
The layout follows a **Fluid-Fixed Hybrid** model. The sidebar remains fixed to the viewport, while the main content area utilizes a fluid 12-column grid.

- **Desktop:** 12 columns, 24px gutters, 48px outer margins.
- **Tablet:** 8 columns, 16px gutters, 32px outer margins.
- **Mobile:** 4 columns, 16px gutters, 16px outer margins. Content should reflow vertically into a single column.
- **Rhythm:** Use a strict 8px base grid. All margins and paddings must be multiples of 8 to maintain visual balance across glass layers.

## Elevation & Depth
Depth is created through **Luminance and Blur** rather than traditional black shadows.

1.  **Level 0 (Base):** Solid `#020617`.
2.  **Level 1 (Cards):** Glass background (10% white opacity) + 1px border (20% white opacity) + 40px Backdrop Blur.
3.  **Level 2 (Modals/Hover):** Glass background (15% white opacity) + subtle outer glow using the primary color (`rgba(225, 29, 72, 0.1)`).
4.  **Borders:** Use linear-gradient borders (Top-Left to Bottom-Right) ranging from `white/20` to `transparent` to simulate light hitting the edges of a glass pane.

## Shapes
The design system uses a "Rounded" language to feel modern and approachable but avoids "Pill" shapes for large containers to maintain a sense of architectural structure.

- **Standard Containers:** 0.5rem (8px) for buttons and small cards.
- **Feature Cards:** 1rem (16px) for main restaurant previews.
- **Badges/Tags:** Full pill (999px) to contrast against the structured grid of the layout.

## Components

### Sidebar
The navigation must be a `sticky` container on the left. Apply `backdrop-blur-xl` and a 1px right-border of `white/10`. Active states should feature a vertical Crimson Red line on the far left and a subtle gradient background.

### Interactive Cards
Cards use a `hover-lift` effect: on hover, the element moves -4px on the Y-axis and the border opacity increases from `white/10` to `white/30`. Apply a `transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`.

### Inputs
Fields are transparent with a `white/5` fill and a `white/10` border. On focus, the border transitions to `Crimson Red` and adds a `0px 0px 12px rgba(225, 29, 72, 0.3)` outer glow.

### Badges & Ranks
AI Match percentages and restaurant ranks use pill shapes. Text should have a `text-shadow` glow effect matching the badge's accent color (Amber for high ranks) to signify "active intelligence."

### Skeletons
Instead of flat gray, skeletons are dark-base `#0F172A` with a diagonal shimmer gradient of `white/5` moving from left to right to mimic a scanning laser.

### Buttons
- **Primary:** Solid Crimson Red with white text.
- **Secondary:** Glass background with a white/20 border and a subtle inner glow.