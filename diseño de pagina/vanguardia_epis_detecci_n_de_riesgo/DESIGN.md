---
name: Vanguardia EPIS - Detección de Riesgo
colors:
  surface: '#fbf8ff'
  surface-dim: '#dad9e3'
  surface-bright: '#fbf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f2fc'
  surface-container: '#eeedf7'
  surface-container-high: '#e8e7f1'
  surface-container-highest: '#e3e1eb'
  on-surface: '#1a1b22'
  on-surface-variant: '#444653'
  inverse-surface: '#2f3037'
  inverse-on-surface: '#f1f0fa'
  outline: '#757684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3755c3'
  primary: '#00288e'
  on-primary: '#ffffff'
  primary-container: '#1e40af'
  on-primary-container: '#a8b8ff'
  inverse-primary: '#b8c4ff'
  secondary: '#5c5f61'
  on-secondary: '#ffffff'
  secondary-container: '#e0e3e5'
  on-secondary-container: '#626567'
  tertiary: '#611e00'
  on-tertiary: '#ffffff'
  tertiary-container: '#872d00'
  on-tertiary-container: '#ffa583'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#173bab'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#380d00'
  on-tertiary-fixed-variant: '#802a00'
  background: '#fbf8ff'
  on-background: '#1a1b22'
  surface-variant: '#e3e1eb'
  risk-low: '#22C55E'
  risk-medium: '#F59E0B'
  risk-high: '#EF4444'
  data-missing: '#94A3B8'
  surface-muted: '#F1F5F9'
  border-subtle: '#E2E8F0'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  status-badge:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 12px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 1.5rem
  margin-edge: 2rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style
The brand personality is **Ethical, Transparent, and Empathetic**. As a tool designed for educators in sensitive rural and urban-marginal contexts, the UI avoids "flashy" or distracting elements in favor of a **Corporate Modern** aesthetic that emphasizes institutional trust and functional clarity.

The design system prioritizes the "Dignity of the Student" by using a "Glassbox IA" approach—ensuring that every AI-generated recommendation is accompanied by the raw, deterministic data that triggered it. The visual style is clean and professional, using high-quality typography and a restrained color palette to prevent cognitive fatigue during long administrative sessions. It is a resilient tool that remains functional even in low-connectivity environments through explicit fallback states.

**Key Principles:**
- **Non-Stigmatizing:** Use of neutral containers and respectful terminology; avoid alarming iconography.
- **Auditable Logic:** Colors and indicators must have a 1:1 parity with student data thresholds.
- **Resilience:** Clear visual distinction between live data and cached/fallback information.

## Colors
The palette is rooted in an **Institutional Blue** to convey authority and reliability. The semantic system is strictly mapped to the Risk Levels defined in the project constitution:

- **Primary (Institutional Blue):** Used for navigation, primary actions, and headers.
- **Semantic Risk Tiers:**
    - **Green (#22C55E):** Low Risk. Used for students meeting all positive thresholds.
    - **Amber (#F59E0B):** Medium Risk. Used for warning signals and isolated negative data.
    - **Red (#EF4444):** High Risk. Used for critical alerts and immediate intervention needs.
    - **Gray (#94A3B8):** Insufficient Data. Used when variables are missing, avoiding false risk assessments.
- **Neutrals:** The background utilizes near-white surfaces (`#F8FAFC`) to minimize eye strain, with soft gray dividers to maintain structure without visual noise.

## Typography
The system uses **Inter** for all levels to ensure maximum legibility and a systematic, utilitarian feel. 

- **Hierarchy:** Headlines use tighter letter spacing and heavier weights to establish clear sections. Body text is optimized for readability in long-form AI explanations (max 2-3 sentences).
- **Contextual Roles:** 
    - **Label Caps:** Used for table headers and metadata categories (e.g., "ASISTENCIA", "PROMEDIO").
    - **Status Badge:** Specialized bold sizing for risk indicators to ensure they are scannable in dense tables.
- **Accessibility:** On mobile/tablet, headings scale down to maintain a comfortable reading width within the restricted viewport of school-issued devices.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid** model. The main dashboard is contained within a max-width of 1280px to prevent excessive line lengths on desktop monitors, while the internal grid is fluid to adapt to tablets.

- **Grid System:** A 12-column grid is used for the main dashboard. 
    - **Desktop/Laptop:** 12 columns.
    - **Tablet:** 6 columns, with the "Detail Panel" transitioning from a side-sheet to a full-screen overlay.
- **Rhythm:** A vertical rhythm of 8px increments (0.5rem) is used for component spacing. Tables use a "Functional Density" approach—rows are tall enough to be touch-friendly on tablets but compact enough to display 15-20 records without excessive scrolling.
- **Responsive Reflow:** On smaller screens, the "Recommendation" column in the table is hidden, requiring the user to click the row to view the detail panel.

## Elevation & Depth
This system uses **Tonal Layering** and **Low-Contrast Outlines** rather than heavy shadows to maintain a clean, professional "admin" feel.

- **Surface Levels:** 
    - **Level 0 (Background):** Neutral light gray (#F8FAFC).
    - **Level 1 (Cards/Table):** Pure white surface with a 1px border (#E2E8F0).
    - **Level 2 (Detail Panel):** Soft, ambient shadow (10% opacity, 20px blur) to indicate the panel is an overlay above the student list.
- **Interactive Depth:** Rows use a subtle background tint on hover rather than an elevation change.
- **Feedback Overlay:** If "Fallback Mode" is active, a top-anchored banner or warning icon (`⚠️`) uses a higher z-index to remain visible over all content.

## Shapes
The system utilizes **Soft** roundedness (0.25rem/4px). This subtle rounding maintains a professional and systematic character while feeling more modern and approachable than sharp corners.

- **UI Elements:** Buttons, input fields, and standard badges use 4px corners.
- **Status Badges:** Use `rounded-full` (pill-shaped) to distinguish them as status indicators rather than interactive buttons.
- **Containers:** Large cards and detail panels use `rounded-lg` (8px) to soften the overall interface.

## Components

### Buttons
- **Primary:** Institutional Blue background, white text. Soft rounded corners.
- **Secondary/Action:** Ghost style (border only) or muted background for secondary actions like "[🔄 Actualizar]".

### Risk Badges
- **Visuals:** Pill-shaped backgrounds using the semantic colors (Green, Amber, Red, Gray) with a high-contrast label. 
- **Iconography:** Include the colored circle symbol (`🟢`) next to the text for double-encoding (accessibility).

### Tables
- **Styling:** Clean rows with light gray horizontal dividers. 
- **Interactive:** Entire rows are clickable, showing a subtle `#F1F5F9` hover state.
- **Columns:** Consistent widths for Student Name, Risk Level (Badge), Grade (Numeric), and Main Motive.

### Detail Panel (Side-Sheet)
- **Structure:** Triggers on row click. Contains a header with the student name, a "Data Summary" section (deterministic), and an "AI Insights" section.
- **AI Block:** Background is slightly tinted with the risk color at 5% opacity to provide context. Uses bullet points for clarity in recommendations.

### Input Fields
- **Styling:** Minimalist with 1px gray borders. Focus state uses a 2px blue ring.

### System Indicators
- **Fallback Warning:** An amber-tinted banner with the `⚠️` icon to inform the user that recommendations are generated from cache due to connectivity issues.