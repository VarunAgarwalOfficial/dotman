#!/bin/bash

get_volume_bar() {
  # Get volume string (e.g., "0.45" or "1.00")
  vol_str=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ 2>/dev/null | grep -oP '\d+\.\d+' | head -1)

  # Check if muted
  if wpctl get-volume @DEFAULT_AUDIO_SINK@ | grep -q "MUTED"; then
    echo "░░░░░░░░░░"
    return
  fi

  # Convert decimal to integer percentage (handles over-amplification like 1.90)
  vol_pct=$(awk -v v="$vol_str" 'BEGIN {print int(v * 100)}')

  # Fallback for 0%
  [[ -z "$vol_pct" ]] && vol_pct=0

  # Calculate level (0-10)
  level=$((vol_pct / 10))
  ((level > 10)) && level=10

  # Build ASCII bar
  full="█"
  empty="░"
  bar=""
  for i in {0..9}; do
    if [ "$i" -lt "$level" ]; then
      bar="${bar}${full}"
    else
      bar="${bar}${empty}"
    fi
  done

  echo "$bar"
}

get_volume_bar
