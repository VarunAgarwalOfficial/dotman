#!/usr/bin/env bash
"""
fzf-drun - Themed fzf menu launcher

Pipes input to fzf running in a floating terminal.
Uses themed colors from dotman.

Usage:
  echo "options" | fzf-drun.sh
  fzf-drun.sh "option1" "option2" "option3"
  echo "options" | fzf-drun.sh --print-query  # Returns typed query + selection
"""

SCRIPT_DIR="$(dirname "$0")"
LIB_DIR="$(cd "$SCRIPT_DIR/../lib" && pwd)"

PRINT_QUERY=0

while [[ "$1" == --* ]]; do
  case "$1" in
    --print-query) PRINT_QUERY=1; shift ;;
    *) break ;;
  esac
done

export FZF_DEFAULT_OPTS=" \
--color=bg+:{{ bg2 }},bg:{{ bg0 }},spinner:{{ bright_yellow }},hl:{{ red }} \
--color=fg:{{ fg0 }},header:{{ red }},info:{{ magenta }},pointer:{{ bright_yellow }} \
--color=marker:{{ blue }},fg+:{{ fg0 }},prompt:{{ magenta }},hl+:{{ red }} \
--color=selected-bg:{{ bg3 }} \
--color=border:{{ bright_black }},label:{{ fg0 }}"

FZF_OPTS=""
if [ "$PRINT_QUERY" -eq 1 ]; then
  FZF_OPTS="--print-query"
fi

if [ $# -gt 0 ]; then
  printf "%s\n" "$@" >/tmp/fzf_input
else
  cat >/tmp/fzf_input
fi

TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE" /tmp/fzf_input' EXIT

# Launch fzf in floating terminal
"$LIB_DIR/floating-terminal" sh -c "cat /tmp/fzf_input | fzf $FZF_OPTS > $TMPFILE"

if [ "$PRINT_QUERY" -eq 1 ]; then
  tail -1 "$TMPFILE"
else
  cat "$TMPFILE"
fi