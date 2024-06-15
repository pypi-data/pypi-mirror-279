import numpy as np
from scipy.ndimage import binary_dilation
from skimage.morphology import disk

def subtract_background(image, masks, expand_masks=None):
    
    masks = masks.copy()
    masks[masks != 0] = 1
    
    if expand_masks is not None:
        masks = binary_dilation(masks, iterations=expand_masks, structure=disk(5)).astype(masks.dtype)
        
    background = np.median(image[masks == 0], axis=0)
    
    normed_image = np.clip(image - background, 0, 1)
    normed_image = np.clip((normed_image - normed_image.min(axis=(0,1))) / (np.percentile(image, 99.9, axis=(0,1)) - normed_image.min(axis=(0,1))),  0, 1)

    return normed_image
    
    
def normalize_image(image):
    # Check the data type of the image
    if image.dtype == np.uint8:
        # Normalize uint8 image: scale down to 0-1 range
        return image.astype(np.float32) / 255
    elif image.dtype in (np.float32, np.float64):
        # Check if normalization is needed
        if image.max() > 1:
            return image / 255
        else:
            return image
    else:
        raise TypeError("Unsupported image data type")