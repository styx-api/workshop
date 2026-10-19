"""Skull-strip and bias-field correct a T1w image using NiWrap."""

import shutil
from pathlib import Path

import niwrap
from niwrap import ants, fsl

niwrap.use_auto()

bet = fsl.bet(
    infile=snakemake.input.t1w,
    fractional_intensity=snakemake.params.bet_fractional_intensity,
)
n4 = ants.n4_bias_field_correction(
    input_image=bet.outfile,
    image_dimensionality=3,
    output=ants.n4_bias_field_correction_corrected_output_params(
        corrected_output_file_name=Path(snakemake.output.preproc_t1w).name
    ),
)

if n4.output_image_outfile is None:
    raise FileNotFoundError("Bias corrected image not found.")

Path(snakemake.output.preproc_t1w).parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(n4.output_image_outfile, snakemake.output.preproc_t1w)
