# =====================================================================
# rr2graph — Makefile (pipenv-aware, CI-ready, build + release)
# =====================================================================

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MAN_DIR          := man
MANPAGE          := $(MAN_DIR)/rr2graph.1
INSTALL_SCRIPT   := $(MAN_DIR)/install-man.sh
UNINSTALL_SCRIPT := $(MAN_DIR)/uninstall-man.sh

TEST_DIR         := tests

# Pipenv detection
PIPENV := $(shell command -v pipenv 2> /dev/null)

ifeq ($(PIPENV),)
$(error "pipenv not found — please install pipenv first")
endif

# ---------------------------------------------------------
# Help
# ---------------------------------------------------------

.PHONY: help
help:
	@echo ""
	@echo "📘 rr2graph — Available Make targets"
	@echo ""
	@echo "  make setup-dev        — Install dev dependencies"
	@echo "  make install          — Install rr2graph into venv (editable)"
	@echo ""
	@echo "  make ci               — Run full CI pipeline"
	@echo "  make ci-lint          — Run ruff linter"
	@echo "  make ci-style         — Run black style check"
	@echo "  make ci-test          — Run pytest with coverage"
	@echo ""
	@echo "  make format           — Auto-format code (ruff + black)"
	@echo "  make clean            — Remove build + cache artifacts"
	@echo "  make build            — Build wheel + sdist"
	@echo "  make release          — Build release artifacts"
	@echo ""
	@echo "  make version-patch    — Bump patch version (X.Y.Z → X.Y.(Z+1))"
	@echo "  make version-minor    — Bump minor version (X.Y.Z → X.(Y+1).0)"
	@echo "  make version-major    — Bump major version ((X+1).0.0)"
	@echo ""
	@echo "  make publish-test     — Upload build artifacts to TestPyPI"
	@echo "  make publish          — Upload build artifacts to PyPI"
	@echo ""
	@echo "  make install-man      — Install manpage"
	@echo "  make uninstall-man    — Uninstall manpage"
	@echo "  make man              — View manpage locally"
	@echo ""


# ---------------------------------------------------------
# Developer Setup
# ---------------------------------------------------------

.PHONY: setup-dev
setup-dev:
	@echo "📦 Installing development dependencies..."
	@pipenv install --dev
	@echo "✅ Dev environment ready"


# ---------------------------------------------------------
# CI Workflow
# ---------------------------------------------------------

.PHONY: ci ci-lint ci-style ci-test
ci: ci-lint ci-style ci-test
	@echo "✅ CI pipeline completed successfully"

ci-lint:
	@echo "🔎 Running linter..."
	@pipenv run ruff check rr2graph

ci-style:
	@echo "🎨 Checking code style..."
	@pipenv run black --check rr2graph

ci-test:
	@echo "🧪 Running tests..."
	@pipenv run pip install -e .
	@pipenv run pytest --cov=rr2graph --cov-branch --cov-report=xml --cov-report=term-missing tests
	@pipenv run coverage html

	
# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------

.PHONY: format
format:
	@echo "✨ Auto-formatting code..."
	@pipenv run ruff check rr2graph --fix
	@pipenv run black rr2graph
	@echo "✅ Code formatted"


# ---------------------------------------------------------
# Build + Release
# ---------------------------------------------------------

.PHONY: build clean release install
install:
	@echo "📦 Installing rr2graph into venv..."
	@pipenv run pip install -e .
	@echo "✅ Installed"

clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build dist *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage htmlcov
	@echo "✅ Clean"

build: clean
	@echo "📦 Building package..."
	@pipenv run python -m build
	@echo "✅ Build complete (dist/)"

release: build
	@echo "🚀 Release artifacts ready in dist/"
	@echo "To upload to PyPI:"
	@echo "  pipenv run twine upload dist/*"
	@echo "Or to TestPyPI:"
	@echo "  pipenv run twine upload --repository testpypi dist/*"


# ---------------------------------------------------------
# Manpage Installation / Uninstallation
# ---------------------------------------------------------

.PHONY: install-man uninstall-man man
install-man:
	@echo "📦 Installing manpage..."
	@$(INSTALL_SCRIPT)

uninstall-man:
	@echo "🧹 Uninstalling manpage..."
	@$(UNINSTALL_SCRIPT)

man:
	@man ./$(MANPAGE)


# ---------------------------------------------------------
# Version bumping (patch/minor/major)
# ---------------------------------------------------------

.PHONY: version-patch version-minor version-major
version-patch:
	@echo "🔧 Bumping patch version..."
	@pipenv run python -m rr2graph.tools.bump_version patch

version-minor:
	@echo "🔧 Bumping minor version..."
	@pipenv run python -m rr2graph.tools.bump_version minor

version-major:
	@echo "🔧 Bumping major version..."
	@pipenv run python -m rr2graph.tools.bump_version major


# ---------------------------------------------------------
# TestPyPI Upload
# ---------------------------------------------------------

.PHONY: publish-test
publish-test: build
	@echo "🚀 Uploading to TestPyPI..."
	@pipenv run twine upload --repository testpypi dist/*
	@echo "✅ Uploaded to TestPyPI"


# ---------------------------------------------------------
# PyPI Upload
# ---------------------------------------------------------

.PHONY: publish
publish:
	@echo "🚀 Uploading to PyPI..."
	@pipenv run twine upload dist/*
	@echo "✅ Uploaded to PyPI"
