#!/usr/bin/env bash
set -euo pipefail

MANPAGE="rr2graph.1"
TARGET_DIR="/usr/local/share/man/man1"
TARGET_PATH="${TARGET_DIR}/${MANPAGE}"

echo "🧹 Uninstalling manpage: ${MANPAGE}"

# Check if installed
if [[ ! -f "${TARGET_PATH}" ]]; then
    echo "ℹ️  Manpage not found at ${TARGET_PATH}"
    echo "    Nothing to uninstall"
    exit 0
fi

# Remove file
echo "🗑  Removing ${TARGET_PATH}"
sudo rm -f "${TARGET_PATH}"

# Try updating man database (Homebrew mandb only)
if command -v mandb >/dev/null 2>&1; then
    echo "🗂  Updating man database via mandb"
    sudo mandb "${TARGET_DIR}" || true
else
    echo "ℹ️  'mandb' not installed — skipping database update"
fi

echo "✅ Uninstall complete"
echo "Test with:  man rr2graph   (should now show 'No manual entry')"
