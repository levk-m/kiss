#!/usr/bin/env bash
set -euo pipefail

APP="kiss"
APP_PYPI="kiss-editor"

info()  { echo "  :: $*"; }
ok()    { echo "  ==> $*"; }
warn()  { echo "  !! $*"; }

run_with_spinner() {
    local pid=$1 msg=$2
    local spin='-\|/'
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r  :: %s %s" "$msg" "${spin:$i:1}"
        i=$(( (i+1) % 4 ))
        sleep 0.1
    done
    printf "\r  :: %s done\n" "$msg"
}

install_uv_if_missing() {
    if command -v uv &>/dev/null; then
        ok "uv already installed ($(uv --version))"
        return 0
    fi
    warn "uv not found — installing..."
    info "Downloading uv..."
    curl -# -fL https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv &>/dev/null; then
        echo "Error: uv installation failed. Add ~/.local/bin to PATH or install manually."
        exit 1
    fi
    ok "uv installed ($(uv --version))"
}

main() {
    echo ""
    echo "  Kiss — updater"
    echo "  ─────────────"
    echo ""

    install_uv_if_missing

    info "Installing $APP via uv..."
    uv tool install "$APP_PYPI" > /dev/null 2>&1 &
    run_with_spinner $! "Updating $APP with uv"
    wait $! 2>/dev/null || true

    echo ""
    ok "$APP has been successfully updated."
    info "Run '$APP' to start."
    echo ""
}

main "$@"
