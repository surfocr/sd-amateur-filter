# draco detail Node - Visual Preview

## How the Node Appears in ComfyUI

When you add the "draco detail" node to your ComfyUI workflow, it will have the following appearance:

```
╔═══════════════════════════════════════╗
║  draco detail                         ║  ← White background, black text
╠═══════════════════════════════════════╣
║                                       ║
║  images: [IMAGE INPUT]                ║
║                                       ║
║  sharpen_intensity: [====|----] 0.01  ║
║  desaturation_factor: [========|-] 0.85║
║  grain_amount: [==|--------] 0.02     ║  ← All sliders and controls
║  jpeg_quality: [========|--] 80       ║     appear on dark background
║  dynamic_range_factor: [=====|----] 1.0║
║  hsv_hue_var: [==|--------] 2         ║
║  hsv_sat_var: [===|-------] 5         ║
║  hsv_val_var: [===|-------] 6         ║
║  rgb_noise_var: [=|--------] 0.007    ║
║  warmth_factor: [===|------] 0.03     ║
║  contrast_alpha: [=====|----] 1.0     ║
║  contrast_beta: [===|-------] 3.0     ║
║                                       ║
║  images: [IMAGE OUTPUT]               ║
║                                       ║
╚═══════════════════════════════════════╝
    ↑
    Dark gray/black body (#222222)
    Slightly darker background (#1a1a1a)
```

## Color Specifications

### Title Bar
- Background: `#ffffff` (white)
- Text: `#000000` (black)
- **High contrast for easy readability**

### Node Body
- Primary color: `#222222` (dark gray)
- Background: `#1a1a1a` (slightly darker)
- **Monochrome aesthetic that stands out in workflows**

## Benefits of the Black & White Design

1. **High Contrast**: Easy to spot in complex node graphs
2. **Professional Look**: Clean, modern appearance
3. **Distinctive Identity**: Immediately recognizable as "draco detail"
4. **Accessibility**: Strong contrast ratio for better readability
5. **Consistency**: Monochrome theme works with any ComfyUI color scheme

## Finding the Node

1. Open ComfyUI
2. Right-click in the workflow area
3. Navigate to: **image/postprocessing**
4. Look for: **draco detail** (with black and white styling)

The distinctive color scheme makes it easy to identify among other nodes!
