#!/bin/bash
export PYTHONPATH=/usr/src/app

case "${1:-}" in
  decode)
    exec python /usr/src/app/script/container/decode.py "${2}"
    ;;
  *)
    exec python -m provision
    ;;
esac
