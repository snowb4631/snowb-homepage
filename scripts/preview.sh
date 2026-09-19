#!/usr/bin/env bash
# 로컬 미리보기 — 두 가지 배포 형태를 그대로 재현한다.
#   local  : 커스텀 도메인(home.stock-snow.com)처럼 사이트가 루트(/)에 있는 형태
#   github : GitHub Pages 기본 주소(snowb4631.github.io/snowb-homepage/)처럼 하위 경로에 있는 형태
# 사용법: scripts/preview.sh [local|github|both]  (기본값 both)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_NAME="snowb-homepage"
LOCAL_PORT="${LOCAL_PORT:-8000}"
GITHUB_PORT="${GITHUB_PORT:-8001}"
MODE="${1:-both}"

pids=()
cleanup() { for p in "${pids[@]:-}"; do kill "$p" 2>/dev/null || true; done; [ -n "${GH_DIR:-}" ] && rm -rf "$GH_DIR"; }
trap cleanup EXIT INT TERM

serve_local() {
  python3 -m http.server "$LOCAL_PORT" --bind 127.0.0.1 --directory "$ROOT" >/dev/null 2>&1 &
  pids+=($!)
  echo "local  → http://localhost:$LOCAL_PORT/"
}

serve_github() {
  GH_DIR="$(mktemp -d)"
  ln -s "$ROOT" "$GH_DIR/$REPO_NAME"
  python3 -m http.server "$GITHUB_PORT" --bind 127.0.0.1 --directory "$GH_DIR" >/dev/null 2>&1 &
  pids+=($!)
  echo "github → http://localhost:$GITHUB_PORT/$REPO_NAME/"
}

case "$MODE" in
  local)  serve_local ;;
  github) serve_github ;;
  both)   serve_local; serve_github ;;
  *) echo "usage: $0 [local|github|both]" >&2; exit 1 ;;
esac

echo "Ctrl+C 로 종료"
wait
