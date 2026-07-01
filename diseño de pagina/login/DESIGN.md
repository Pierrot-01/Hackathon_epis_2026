---
name: Horizontes Educativos
colors:
  surface: '#f7fafc'
  surface-dim: '#d7dadd'
  surface-bright: '#f7fafc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f6'
  surface-container: '#ebeef0'
  surface-container-high: '#e6e8eb'
  surface-container-highest: '#e0e3e5'
  on-surface: '#181c1e'
  on-surface-variant: '#3f484c'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eef1f3'
  outline: '#6f787d'
  outline-variant: '#bec8cd'
  surface-tint: '#006781'
  primary: '#005a71'
  on-primary: '#ffffff'
  primary-container: '#0e7490'
  on-primary-container: '#d3f1ff'
  inverse-primary: '#81d1f0'
  secondary: '#545f73'
  on-secondary: '#ffffff'
  secondary-container: '#d5e0f8'
  on-secondary-container: '#586377'
  tertiary: '#794602'
  on-tertiary: '#ffffff'
  tertiary-container: '#965e1c'
  on-tertiary-container: '#ffe8d6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b9eaff'
  primary-fixed-dim: '#81d1f0'
  on-primary-fixed: '#001f29'
  on-primary-fixed-variant: '#004d62'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#ffdcbd'
  tertiary-fixed-dim: '#ffb86f'
  on-tertiary-fixed: '#2c1600'
  on-tertiary-fixed-variant: '#693c00'
  background: '#f7fafc'
  on-background: '#181c1e'
  surface-variant: '#e0e3e5'
  risk-low: '#16A34A'
  risk-medium: '#D97706'
  risk-high: '#DC2626'
  risk-null: '#94A3B8'
  risk-low-bg: '#F0FDF4'
  risk-medium-bg: '#FFFBEB'
  risk-high-bg: '#FEF2F2'
  risk-null-bg: '#F8FAFC'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
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
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  recommendation-text:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 26px
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
  margin-mobile: 1rem
  margin-desktop: 2rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style
The design system is anchored in the principles of **dignity, clarity, and institutional reliability**. It serves educators in diverse Peruvian contexts—from bustling urban-marginal districts to remote rural areas—providing a tool that feels professional yet deeply humanistic. The brand personality is **Empathetic and Observant**, acting as a supportive assistant rather than a cold analytical judge.

The chosen design style is **Corporate / Modern** with a focus on **utilitarian clarity**. It avoids unnecessary decorative elements to ensure low cognitive load for teachers who may be managing high-pressure classroom environments. The visual language emphasizes "Traceability-First," ensuring every automated insight is clearly linked to raw data, fostering trust through transparency. The aesthetic is clean, structured, and accessible, prioritizing high legibility and a "safe" emotional tone that avoids alarmism.

## Colors
The color palette is strictly semantic and functional. The **Primary Color** is a professional Teal (#0E7490), chosen for its calming, institutional qualities which differentiate it from the risk-based semantic colors. 

Risk levels use a "Traffic Light" system but are applied with restraint:
- **Success (Bajo riesgo):** Green, representing growth and stability.
- **Warning (Riesgo medio):** Amber, signaling a need for proactive conversation.
- **Danger (Riesgo alto):** Red, indicating an urgent need for support.
- **Neutral (Dato insuficiente):** Slate Gray, used when data points are missing to prevent false assumptions.

Each risk color is paired with a **Soft Tint background** for table row highlighting. This ensures that the risk level is communicated through the overall environment of the row, while keeping the text highly legible and non-aggressive.

## Typography
**Inter** is the sole typeface for this design system, selected for its exceptional legibility in digital dashboards and its neutral, professional character. 

- **Headlines:** Used for student names and dashboard sections to create a clear structural hierarchy.
- **Body Text:** Optimized for reading AI-generated explanations. The `recommendation-text` style uses a medium weight and slightly increased line height to distinguish professional advice from raw data.
- **Labels:** Utilized for table headers and metadata (ID, Grade).
- **Tone:** All typographic content must adhere to the project's ethical guidelines—replacing stigmatizing terms (e.g., "lazy") with constructive, action-oriented phrases (e.g., "requires family engagement").

## Layout & Spacing
The layout follows a **Fluid Grid** model with a maximum container width to maintain readability on ultra-wide monitors often found in administrative offices. 

- **Dashboard View:** A 12-column grid system is used. On desktop, the student table spans the full width, while the "Detail Sidebar" slides over the right-most 4 columns when a record is selected.
- **Table Rhythm:** Rows have a minimum height of 64px to ensure touch-friendliness and visual "breathing room" for teachers scanning lists quickly.
- **Mobile Adaptation:** On mobile devices, the table transforms into a "Card List" view, where each student's risk badge and name are prioritized, and details are accessed via full-screen modals.
- **Vertical Rhythm:** A base 8px (0.5rem) spacing scale ensures consistent alignment between data labels and their corresponding values.

## Elevation & Depth
This design system uses a **Tonal Layering** approach rather than heavy shadows to signify hierarchy, ensuring high performance on older hardware.

- **Level 0 (Surface):** The main dashboard background in a very light gray to reduce glare.
- **Level 1 (Card/Table):** Pure white surfaces for the primary data table and content containers.
- **Level 2 (Sidebar/Modals):** These use a low-opacity ambient shadow (Blur: 12px, Opacity: 8%) to indicate they are "closer" to the user.
- **Focus States:** High-contrast blue outlines are used instead of depth changes to assist with accessibility and keyboard navigation.
- **Status Overlay:** When the system enters "Fallback Mode" (API failure), a subtle amber top-bar or persistent banner is anchored to the top of the viewport to indicate data is cached.

## Shapes
The shape language is **Soft (0.25rem)**, providing a modern and friendly feel that remains grounded in institutional professionalism. 

- **Standard Elements:** Buttons, input fields, and table rows use the base 0.25rem radius.
- **Status Badges:** Use a `rounded-full` (pill) shape to clearly distinguish them from interactive buttons or data containers.
- **Sidebars:** The detail sidebar uses a larger 0.75rem radius on its leading corners to soften the transition from the main dashboard.

## Components
- **Data Tables:** Rows must support background tinting based on risk level. Hover states should darken the tint slightly.
- **Risk Badges:** Small pills containing an emoji (🟢, 🟡, 🔴, ⚪) and the text label. The emoji ensures accessibility for those with color-vision deficiencies.
- **Action Buttons:** Primary buttons use the Teal palette. Secondary buttons use a ghost style (outline only) to keep the focus on the primary task: student evaluation.
- **Detail Sidebar:** A slide-out panel that displays "The Why" (Raw variables like attendance %) and "The Recommendation" (AI Narrative). It must include a "Traceability" section with bullet points for evidence.
- **System Status Indicator:** A prominent icon/text combo (e.g., `⚠️ Fallback Active`) that appears when the 6-second API timeout is triggered.
- **Input Fields:** Large, clear text entry for search and filtering, with high-contrast borders for visibility in brightly lit (or poorly lit) classrooms.