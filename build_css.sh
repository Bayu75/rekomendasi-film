#!/usr/bin/env bash
# Build Tailwind v4 -> app/static/css/app.css
# Pakai: ./build_css.sh          (sekali, minified)
#        ./build_css.sh --watch  (otomatis saat template berubah)
set -euo pipefail
cd "$(dirname "$0")"
IN=app/static/css/input.css
OUT=app/static/css/app.css
if [ -x tools/tailwindcss ]; then
  TW=(tools/tailwindcss)
elif [ -x tools/tailwindcss.exe ]; then
  TW=(tools/tailwindcss.exe)
elif [ -x node_modules/.bin/tailwindcss ]; then
  TW=(node_modules/.bin/tailwindcss)
else
  # `npx @tailwindcss/cli` saja tidak memasang paket `tailwindcss`, jadi
  # `@import "tailwindcss"` di input.css gagal di-resolve. Pasang keduanya
  # di node_modules (di-gitignore). package.json sementara dihapus jika
  # repo ini belum punya package.json, supaya build tidak menambah file baru.
  echo "tools/tailwindcss tidak ada; memasang tailwindcss + @tailwindcss/cli lewat npm..."
  created_pkg=0
  if [ ! -f package.json ]; then
    created_pkg=1
  fi
  npm install --no-package-lock --silent tailwindcss@4 @tailwindcss/cli@4
  if [ "$created_pkg" = 1 ]; then
    rm -f package.json
  fi
  TW=(node_modules/.bin/tailwindcss)
fi
if [ "${1:-}" = "--watch" ]; then
  exec "${TW[@]}" -i "$IN" -o "$OUT" --watch
else
  "${TW[@]}" -i "$IN" -o "$OUT" --minify
fi
