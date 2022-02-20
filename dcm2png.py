from pydicom import dcmread
from pydicom.pixel_data_handlers.util import (
    apply_voi_lut,
)
import cv2 as cv
import numpy as np
import os
import time

root_path = "./dcm"

dir_name = os.path.join("./", time.strftime("%Y-%m-%d-%H-%M-%S"))
os.mkdir(dir_name)
for i in os.listdir(root_path):
    if i.endswith("dcm") or i.endswith("DCM"):
        ds = dcmread(os.path.join(root_path, i))
        img = ds.pixel_array
        if ds["PhotometricInterpretation"] == "MONOCHROME1":
            img = np.max(img) + np.min(img) - img
        img = apply_voi_lut(img, ds)
        try:
            cv.imwrite(
                "{}/{}-{}-{}-{}-{}.png".format(
                    dir_name,
                    ds.Modality,
                    ds.PatientName,
                    ds.PatientID,
                    ds.PatientBirthDate,
                    ds.PatientSex,
                ),
                (np.maximum(img, 0) / img.max()) * 255,
            )
        except AttributeError:
            print(i)
