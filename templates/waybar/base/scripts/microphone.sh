#!/bin/bash
# Check microphone mute status and output appropriate icon

# Get the default source name
default_source=$(pactl info | grep "Default Source:" | awk '{print $3}')

# Get mute status for the default source
if [ -n "$default_source" ]; then
    mute_status=$(pactl list sources | grep -A 10 "Name: $default_source" | grep "Mute:" | head -1 | awk '{print $2}')
fi

if [ "$mute_status" = "yes" ]; then
  echo ""
else
  echo ""
fi
