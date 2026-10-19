#!/usr/bin/env bash
# Pull the container images the workshop pipeline uses (notebooks and Snakemake).
# Tags are the defaults baked into niwrap 1.1.0; both images are linux/amd64 only.
set -euo pipefail

docker="${DOCKER:-docker}"
images=(
  brainlife/fsl:6.0.4-patched2  # FSL: ~7.1 GB download, ~23.5 GB on disk
  antsx/ants:v2.5.3             # ANTs: ~0.1 GB download, ~0.6 GB on disk
)

for image in "${images[@]}"; do
  echo "==> $image"
  "$docker" pull --platform linux/amd64 "$image"
done
