"""Check that the workshop environment works: data, Docker, FSL and ANTs images.

    uv run scripts/smoke_test.py
"""

import logging
import shlex
import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import niwrap
from niwrap import ants, fsl

T1W = Path("data/ds000001/sub-01/anat/sub-01_T1w.nii.gz")
IMAGES = ["brainlife/fsl:6.0.4-patched2", "antsx/ants:v2.5.3"]


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    sys.exit(1)


def check_data() -> None:
    if not T1W.exists():
        fail(f"{T1W} missing. Run: uv run scripts/fetch_data.py")
    print(f"ok    data ({T1W})")


def check_dry() -> None:
    dry = niwrap.DryRunner()
    fsl.bet(infile=T1W, binary_mask=True, runner=dry)
    print(f"ok    niwrap {version('niwrap')} builds commands: {shlex.join(dry.last_cargs)}")


def check_docker() -> None:
    if shutil.which("docker") is None:
        fail("docker not found on PATH. Use RUNNER = 'dry' in the notebooks (see SETUP.md).")
    if subprocess.run(["docker", "info"], capture_output=True).returncode != 0:
        fail("docker is installed but not running. Start Docker Desktop and retry.")
    for image in IMAGES:
        if subprocess.run(["docker", "image", "inspect", image], capture_output=True).returncode != 0:
            fail(f"image {image} not pulled. Run: bash scripts/prepull_images.sh")
    print("ok    docker running, images present")


def check_tools() -> None:
    runner = niwrap.use_docker(data_dir="work/smoke")
    logging.getLogger(runner.logger_name).setLevel(logging.WARNING)
    reoriented = fsl.fslreorient2std(input_image=T1W, output_image="t1w.nii.gz").output_image
    n4 = ants.n4_bias_field_correction(
        input_image=reoriented,
        image_dimensionality=3,
        shrink_factor=4,
        output=ants.n4_bias_field_correction_corrected_output_params(
            corrected_output_file_name="t1w_n4.nii.gz"
        ),
    )
    if not n4.output_image_outfile.exists():
        fail("ANTs ran but produced no output")
    print("ok    FSL and ANTs run in Docker")


if __name__ == "__main__":
    check_data()
    check_dry()
    check_docker()
    check_tools()
    print("\nAll good. See you at the workshop!")
