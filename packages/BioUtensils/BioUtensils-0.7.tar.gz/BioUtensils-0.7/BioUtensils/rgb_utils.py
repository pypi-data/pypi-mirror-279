import tifffile
from pathlib import Path
import re
import numpy as np
from .normalize import normalize_image

from typing import Tuple

def find_unique_identifier(base_path: Path, identifier=r"\b\d{6}\b", file_ending="*.[tT][iI][fF]") -> Tuple[list, list]:

    all_files = list(base_path.glob(file_ending))
    unique_identifier = list(set([re.findall(identifier, str(x))[0] for x in all_files]))

    return all_files, unique_identifier


def load_rgb(files, identifier=["-r.", "-g.", "-b."]):

    stack = []
    for c in identifier:
        
        if c is None:
            stack.append(None)
            continue
        
        file = [x for x in files if c in str(x).lower()][0]
        stack.append(tifffile.imread(file))

    sizes = [im.shape for im in stack if im is not None]
    assert len(sizes) != 0
    size_to_fill = sizes[0]
    
    rgb_stack = []
    for im in stack:
        rgb_stack.append(im if im is not None else np.zeros(size_to_fill))
        
    rgb_image = normalize_image(np.stack(rgb_stack).transpose(1,2,0))

    return rgb_image


def get_matching_files(all_files, unique_identifier):

    matches = [x for x in all_files if unique_identifier in str(x)]

    return matches