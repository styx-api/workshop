"""Register a preprocessed T1w image to template space using NiWrap."""

import shutil
from pathlib import Path

import niwrap
from niwrap import ants

niwrap.use_auto()

xfm_prefix = "t1w_to_template_"
xfm = ants.ants_registration_sy_n_quick_sh(
    dimensionality=3,
    fixed_image=snakemake.input.template_t1w,
    moving_image=snakemake.input.preproc_t1w,
    output_prefix=xfm_prefix,
)

# ANTs registration does not attribute individual outputs when using niwrap,
# so copy using root.
Path(snakemake.output.xfm_t1w).parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(xfm.root / f"{xfm_prefix}Warped.nii.gz", snakemake.output.xfm_t1w)
