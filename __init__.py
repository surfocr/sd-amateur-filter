import os
import json
import cv2
import numpy as np
import torch
from PIL import Image

# --------------------------------------------------------------------------------
# Filter functions (extracted from amateur_filter.py)
# --------------------------------------------------------------------------------

def lower_dynamic_range(img, factor=1.0):
    return cv2.convertScaleAbs(img, alpha=factor, beta=0)

def add_hsv_noise(img, hue_var=2, sat_var=5, val_var=6):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
    h_noise = np.random.randint(-hue_var, hue_var, h.shape, dtype=np.int16)
    s_noise = np.random.randint(-sat_var, sat_var, s.shape, dtype=np.int16)
    v_noise = np.random.randint(-val_var, val_var, v.shape, dtype=np.int16)
    h = np.clip(h + h_noise, 0, 179).astype(np.uint8)
    s = np.clip(s + s_noise, 0, 255).astype(np.uint8)
    v = np.clip(v + v_noise, 0, 255).astype(np.uint8)
    merged = cv2.merge([h, s, v])
    return cv2.cvtColor(merged, cv2.COLOR_HSV2BGR)

def add_rgb_noise(img, var=0.007):
    noise_range = int(var * 255)
    noise = np.random.randint(-noise_range, noise_range, img.shape, dtype=np.int16)
    return np.clip(img + noise, 0, 255).astype(np.uint8)

def sharpen(img, intensity=0.01):
    kernel = np.array([
        [0, -intensity, 0],
        [-intensity, 1 + 4*intensity, -intensity],
        [0, -intensity, 0]
    ])
    return cv2.filter2D(img, -1, kernel)

def add_warm_tone(img, warmth_factor=0.03):
    b, g, r = cv2.split(img.astype(np.float32) / 255.0)
    g *= (1.0 - warmth_factor)
    b *= (1.0 - warmth_factor)
    merged = cv2.merge([b, g, r])
    return np.clip(merged * 255, 0, 255).astype(np.uint8)

def adjust_contrast(img, alpha=1.0, beta=0.0):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def desaturate(img, factor=1.0):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_img[..., 1] = (hsv_img[..., 1].astype(np.float32) * factor).clip(0,255).astype(np.uint8)
    return cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

def add_grain(img, grain_amount=0.02):
    if grain_amount <= 0:
        return img
    std_dev = grain_amount * 255
    noise = np.random.normal(0, std_dev, img.shape).astype(np.int16)
    blended = np.clip(0.5 * img + 0.5 * (img + noise), 0, 255).astype(np.uint8)
    return blended

def apply_amateur_filter_cv(
    image,
    dynamic_range_factor=1.0,
    hsv_hue_var=2,
    hsv_sat_var=5,
    hsv_val_var=6,
    rgb_noise_var=0.007,
    sharpen_intensity=0.01,
    warmth_factor=0.03,
    contrast_alpha=1.0,
    contrast_beta=3.0,
    desaturation_factor=0.85,
    grain_amount=0.02,
    jpeg_quality=80
):
    """Apply amateur filter to a BGR OpenCV image."""
    image = lower_dynamic_range(image, dynamic_range_factor)
    image = add_hsv_noise(image, hsv_hue_var, hsv_sat_var, hsv_val_var)
    image = add_rgb_noise(image, rgb_noise_var)
    image = sharpen(image, sharpen_intensity)
    image = add_warm_tone(image, warmth_factor)
    image = adjust_contrast(image, contrast_alpha, contrast_beta)
    image = desaturate(image, desaturation_factor)
    image = add_grain(image, grain_amount)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    success, encimg = cv2.imencode('.jpg', image, encode_param)
    if success:
        image = cv2.imdecode(encimg, cv2.IMREAD_COLOR)

    return image

# --------------------------------------------------------------------------------
# ComfyUI Node
# --------------------------------------------------------------------------------

class AmateurFilterNode:
    """
    A ComfyUI node that applies realistic amateur photography effects to images.
    Includes grain, noise, sharpening, desaturation, and JPEG compression.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "sharpen_intensity": ("FLOAT", {
                    "default": 0.01,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "desaturation_factor": ("FLOAT", {
                    "default": 0.85,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "grain_amount": ("FLOAT", {
                    "default": 0.02,
                    "min": 0.0,
                    "max": 0.3,
                    "step": 0.01,
                    "display": "slider"
                }),
                "jpeg_quality": ("INT", {
                    "default": 80,
                    "min": 10,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "dynamic_range_factor": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "hsv_hue_var": ("INT", {
                    "default": 2,
                    "min": 0,
                    "max": 30,
                    "step": 1,
                    "display": "slider"
                }),
                "hsv_sat_var": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "hsv_val_var": ("INT", {
                    "default": 6,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "rgb_noise_var": ("FLOAT", {
                    "default": 0.007,
                    "min": 0.0,
                    "max": 0.1,
                    "step": 0.001,
                    "display": "slider"
                }),
                "warmth_factor": ("FLOAT", {
                    "default": 0.03,
                    "min": 0.0,
                    "max": 0.3,
                    "step": 0.01,
                    "display": "slider"
                }),
                "contrast_alpha": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "contrast_beta": ("FLOAT", {
                    "default": 3.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 1.0,
                    "display": "slider"
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "apply_filter"
    CATEGORY = "image/postprocessing"
    
    def apply_filter(
        self,
        images,
        sharpen_intensity,
        desaturation_factor,
        grain_amount,
        jpeg_quality,
        dynamic_range_factor,
        hsv_hue_var,
        hsv_sat_var,
        hsv_val_var,
        rgb_noise_var,
        warmth_factor,
        contrast_alpha,
        contrast_beta
    ):
        """
        Apply amateur filter to input images.
        
        Args:
            images: ComfyUI IMAGE tensor in shape (B, H, W, C) with values in [0, 1]
            
        Returns:
            Filtered images in the same format
        """
        # Convert from ComfyUI format (B, H, W, C) float [0, 1] to numpy uint8
        batch_numpy = (images.cpu().numpy() * 255).astype(np.uint8)
        
        result_images = []
        
        for i in range(batch_numpy.shape[0]):
            # Get single image and convert RGB to BGR for OpenCV
            img_rgb = batch_numpy[i]
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # Apply the amateur filter
            filtered_bgr = apply_amateur_filter_cv(
                img_bgr,
                dynamic_range_factor=dynamic_range_factor,
                hsv_hue_var=hsv_hue_var,
                hsv_sat_var=hsv_sat_var,
                hsv_val_var=hsv_val_var,
                rgb_noise_var=rgb_noise_var,
                sharpen_intensity=sharpen_intensity,
                warmth_factor=warmth_factor,
                contrast_alpha=contrast_alpha,
                contrast_beta=contrast_beta,
                desaturation_factor=desaturation_factor,
                grain_amount=grain_amount,
                jpeg_quality=jpeg_quality
            )
            
            # Convert back to RGB
            filtered_rgb = cv2.cvtColor(filtered_bgr, cv2.COLOR_BGR2RGB)
            result_images.append(filtered_rgb)
        
        # Stack back into batch and convert to ComfyUI format
        result_batch = np.stack(result_images, axis=0)
        result_tensor = torch.from_numpy(result_batch.astype(np.float32) / 255.0)
        
        return (result_tensor,)

# --------------------------------------------------------------------------------
# ComfyUI Node Registration
# --------------------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "AmateurFilter": AmateurFilterNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AmateurFilter": "Amateur Filter",
}
