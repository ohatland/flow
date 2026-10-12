#!/usr/bin/env bash
# Prints the named sections of a markdown file, each up to the next heading of the same or
# a higher level. "_intro" is the text before the first "## " heading.
# Usage: sections.sh <file> <heading text>...   (match is a prefix of the heading text)
set -euo pipefail
file="$1"; shift
missing=0
for want in "$@"; do
  awk -v want="$want" '
    function level(l) { match(l, /^#+/); return RLENGTH }
    BEGIN { on = (want == "_intro") }
    /^[ \t]*```/ { fence = !fence }
    !fence && /^#+ / {
      lv = level($0); text = $0; sub(/^#+ +/, "", text)
      if (want == "_intro") { if (lv == 2) exit }
      else if (on && lv <= startlv) exit
      else if (!on && index(text, want) == 1) { on = 1; startlv = lv }
    }
    on { print }
    END { if (!on) exit 3 }
  ' "$file" || { echo "section not found: $want ($file)" >&2; missing=1; }
  echo
done
exit "$missing"
