#!/usr/bin/env bash
set -euo pipefail

MANPAGE="rr2graph.1"
TARGET_DIR="/usr/local/share/man/man1"
TARGET_PATH="${TARGET_DIR}/${MANPAGE}"

echo "📦 Installing manpage: ${MANPAGE}"

# Check file exists
if [[ ! -f "${MANPAGE}" ]]; then
    echo "❌ Error: ${MANPAGE} not found in current directory"
    exit 1
fi

# Create directory if missing
if [[ ! -d "${TARGET_DIR}" ]]; then
    echo "📁 Creating directory ${TARGET_DIR}"
    sudo mkdir -p "${TARGET_DIR}"
fi

# Copy manpage
echo "➡️  Copying to ${TARGET_PATH}"
sudo cp "${MANPAGE}" "${TARGET_PATH}"

# Fix permissions
echo "🔧 Setting permissions"
sudo chmod 644 "${TARGET_PATH}"

# Try updating man database (Homebrew mandb only)
if command -v mandb >/dev/null 2>&1; then
    echo "🗂  Updating man database via mandb"
    sudo mandb "${TARGET_DIR}" || true
else
    echo "ℹ️  'mandb' not installed — skipping database update"
    echo "    (man rr2graph works trotzdem sofort)"
fi

echo "✅ Installation complete"
echo "Test with:  man rr2graph"
