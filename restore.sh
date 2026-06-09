#!/bin/bash
# Restore AI tool configs to a new machine
# Run: bash restore.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Restoring AI configs from $SCRIPT_DIR..."

# Claude
mkdir -p ~/.claude/skills ~/.claude/plugins
cp -r "$SCRIPT_DIR/claude/skills/." ~/.claude/skills/ 2>/dev/null && echo "✓ Claude skills"
cp -r "$SCRIPT_DIR/claude/plugins/." ~/.claude/plugins/ 2>/dev/null && echo "✓ Claude plugins"
[ -f "$SCRIPT_DIR/claude/settings.json" ] && cp "$SCRIPT_DIR/claude/settings.json" ~/.claude/ && echo "✓ Claude settings"

# Cursor
mkdir -p ~/.cursor/skills-cursor ~/.cursor/plans ~/.cursor/plugins
[ -f "$SCRIPT_DIR/cursor/argv.json" ] && cp "$SCRIPT_DIR/cursor/argv.json" ~/.cursor/
[ -f "$SCRIPT_DIR/cursor/mcp.json" ] && cp "$SCRIPT_DIR/cursor/mcp.json" ~/.cursor/
cp -r "$SCRIPT_DIR/cursor/skills-cursor/." ~/.cursor/skills-cursor/ 2>/dev/null && echo "✓ Cursor skills"
cp -r "$SCRIPT_DIR/cursor/plans/." ~/.cursor/plans/ 2>/dev/null && echo "✓ Cursor plans"
cp -r "$SCRIPT_DIR/cursor/plugins/." ~/.cursor/plugins/ 2>/dev/null && echo "✓ Cursor plugins"

# Kiro
mkdir -p ~/.kiro/powers ~/.kiro/skills ~/.kiro/steering ~/.kiro/tasks
[ -f "$SCRIPT_DIR/kiro/argv.json" ] && cp "$SCRIPT_DIR/kiro/argv.json" ~/.kiro/
cp -r "$SCRIPT_DIR/kiro/powers/." ~/.kiro/powers/ 2>/dev/null && echo "✓ Kiro powers"
cp -r "$SCRIPT_DIR/kiro/skills/." ~/.kiro/skills/ 2>/dev/null && echo "✓ Kiro skills"
cp -r "$SCRIPT_DIR/kiro/steering/." ~/.kiro/steering/ 2>/dev/null && echo "✓ Kiro steering"
cp -r "$SCRIPT_DIR/kiro/tasks/." ~/.kiro/tasks/ 2>/dev/null && echo "✓ Kiro tasks"

# Agents
cp -r "$SCRIPT_DIR/agents/." ~/.agents/ 2>/dev/null && echo "✓ .agents"
cp -r "$SCRIPT_DIR/cagent/." ~/.cagent/ 2>/dev/null && echo "✓ .cagent"
cp -r "$SCRIPT_DIR/twigs-mcp/." ~/.twigs-mcp/ 2>/dev/null && echo "✓ .twigs-mcp"

echo ""
echo "Done! Restart Claude Code, Cursor, and Kiro to pick up the restored configs."
