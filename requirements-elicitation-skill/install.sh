#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_FILE="$ROOT_DIR/SKILL.md"

if [[ ! -f "$SKILL_FILE" ]]; then
  echo "[ERROR] SKILL.md not found in $ROOT_DIR"
  exit 1
fi

SKILL_NAME="$(awk -F': ' '/^name: / {print $2; exit}' "$SKILL_FILE" | tr -d '\r')"
if [[ -z "${SKILL_NAME:-}" ]]; then
  echo "[ERROR] Could not parse skill name from SKILL.md frontmatter."
  exit 1
fi

DRY_RUN=0
UNINSTALL=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --uninstall) UNINSTALL=1 ;;
    *)
      echo "[ERROR] Unknown option: $arg"
      echo "Usage: ./install.sh [--dry-run] [--uninstall]"
      exit 1
      ;;
  esac
done

log() {
  echo "$1"
}

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

ensure_link_or_copy() {
  local src="$1"
  local dst="$2"
  local parent
  parent="$(dirname "$dst")"
  run_cmd "mkdir -p \"$parent\""
  run_cmd "rm -rf \"$dst\""
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] ln -s \"$src\" \"$dst\" (fallback to cp -R on failure)"
    return 0
  fi
  if ln -s "$src" "$dst" 2>/dev/null; then
    return 0
  fi
  cp -R "$src" "$dst"
}

remove_path() {
  local dst="$1"
  run_cmd "rm -rf \"$dst\""
}

# Shared skill directories
DESTS=(
  "$HOME/.claude/skills/$SKILL_NAME"
  "$HOME/.agents/skills/$SKILL_NAME"
  "$HOME/.codex/skills/$SKILL_NAME"
  "$HOME/.gemini/skills/$SKILL_NAME"
  "$HOME/.kiro/skills/$SKILL_NAME"
)

# Cursor / Windsurf adapters (project-local by default)
CURSOR_RULES_DIR="${CURSOR_RULES_DIR:-$PWD/.cursor/rules}"
WINDSURF_RULES_DIR="${WINDSURF_RULES_DIR:-$PWD/.windsurf/rules}"
CURSOR_RULE_FILE="$CURSOR_RULES_DIR/${SKILL_NAME}.mdc"
WINDSURF_RULE_FILE="$WINDSURF_RULES_DIR/${SKILL_NAME}.md"

write_cursor_rule() {
  local target="$1"
  local content
  content="---
description: requirements elicitation workflow guidance
globs:
  - \"**/*\"
alwaysApply: false
---
# ${SKILL_NAME}

Use the \`${SKILL_NAME}\` skill from:
\`$ROOT_DIR\`

When the user asks for requirements clarification, follow the runtime loop defined in \`SKILL.md\` and related \`references/\` files.
"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] write $target"
    return 0
  fi
  mkdir -p "$(dirname "$target")"
  printf "%s\n" "$content" > "$target"
}

write_windsurf_rule() {
  local target="$1"
  local content
  content="# ${SKILL_NAME}

Use the skill content at:
\`$ROOT_DIR\`

Trigger this rule for tasks about product requirements interviews, scope clarification, contradiction resolution, and requirements summarization.
"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] write $target"
    return 0
  fi
  mkdir -p "$(dirname "$target")"
  printf "%s\n" "$content" > "$target"
}

if [[ "$UNINSTALL" -eq 1 ]]; then
  log "Uninstalling skill '$SKILL_NAME'..."
  for dst in "${DESTS[@]}"; do
    remove_path "$dst"
  done
  remove_path "$CURSOR_RULE_FILE"
  remove_path "$WINDSURF_RULE_FILE"
  log "Done."
  exit 0
fi

log "Installing skill '$SKILL_NAME' from $ROOT_DIR"
for dst in "${DESTS[@]}"; do
  ensure_link_or_copy "$ROOT_DIR" "$dst"
  log "Installed: $dst"
done

write_cursor_rule "$CURSOR_RULE_FILE"
write_windsurf_rule "$WINDSURF_RULE_FILE"
log "Installed Cursor adapter: $CURSOR_RULE_FILE"
log "Installed Windsurf adapter: $WINDSURF_RULE_FILE"
log "Done."
