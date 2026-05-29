#!/usr/bin/env bash
set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/workspace}"
cd "${PROJECT_ROOT}"

echo "=== fetal_vein_segmentation — entrypoint ==="
echo "PROJECT_ROOT=${PROJECT_ROOT}"

# Bootstrap antes do Jupyter
python 00-common/bootstrap/bootstrap.py ${BOOTSTRAP_ARGS:-}

TOKEN="${JUPYTER_TOKEN:-fetal-dev}"
PORT="${JUPYTER_PORT:-8888}"

echo "=== A iniciar JupyterLab na porta ${PORT} ==="

if [ "$#" -eq 0 ]; then
  set -- jupyter lab --ip=0.0.0.0 --port="${PORT}" --no-browser --allow-root
fi

exec "$@" \
  --ServerApp.token="${TOKEN}" \
  --ServerApp.allow_origin='*' \
  --ServerApp.root_dir="${PROJECT_ROOT}"
