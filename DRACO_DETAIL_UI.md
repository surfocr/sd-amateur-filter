# draco detail Node - UI Styling

## Overview
The "draco detail" node (formerly "Amateur Filter") features a distinctive black and white color scheme that makes it stand out in the ComfyUI node graph.

## Visual Design

### Color Scheme
- **Node Background**: Dark gray/black (#1a1a1a)
- **Node Body**: Slightly darker black (#222222)
- **Title Bar**: White background (#ffffff)
- **Title Text**: Black text (#000000)
- **Shape**: Box style

## Technical Implementation

### Files
- `__init__.py`: Contains the node definition and display name mapping
- `web/draco_detail.js`: JavaScript extension that applies the black and white color scheme

### How It Works
The JavaScript extension uses ComfyUI's `app.registerExtension` API to hook into the node creation process. When an "AmateurFilter" node is created, it applies custom styling properties:

```javascript
this.color = "#222222";         // Node body color
this.bgcolor = "#1a1a1a";       // Node background
this.title_bgcolor = "#ffffff"; // Title bar background
this.title_color = "#000000";   // Title text color
```

### Display Name
The node appears in the ComfyUI interface as "draco detail" instead of "Amateur Filter", making it more distinctive and easier to identify in workflows.

## Features
All original functionality of the Amateur Filter node is preserved:
- 12 adjustable parameters for image processing
- Slider-based UI controls
- Real-time image filtering
- ComfyUI batch processing support

The only changes are cosmetic:
- Display name: "draco detail"
- Color scheme: Black and white for better visibility
- Enhanced visual identity in node graphs
