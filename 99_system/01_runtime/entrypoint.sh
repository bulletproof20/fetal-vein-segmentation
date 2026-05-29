#!/usr/bin/env bash
set -euo pipefail

export PROJECT_ROOT="${PROJECT_ROOT:-/workspace}"
cd "${PROJECT_ROOT}"

PROFILE="${BOOTSTRAP_PROFILE:-local_cpu}"
echo "=== fetal_vein_segmentation — entrypoint ==="
echo "PROJECT_ROOT=${PROJECT_ROOT}"
echo "BOOTSTRAP_PROFILE=${PROFILE}"

case "${PROFILE}" in
  local_cpu|local-cpu|cpu)
    python "${PROJECT_ROOT}/99_system/01_runtime/local_cpu/adapter.py" || true
    ;;
  local_gpu|local-gpu|gpu)
    python "${PROJECT_ROOT}/99_system/01_runtime/local_gpu/adapter.py" || true
    ;;
  kaggle)
    python "${PROJECT_ROOT}/99_system/01_runtime/kaggle/adapter.py" || true
    ;;
esac

python "${PROJECT_ROOT}/99_system/02_bootstrap/bootstrap.py" ${BOOTSTRAP_ARGS:-}

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
