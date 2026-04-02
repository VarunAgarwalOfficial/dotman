#!/bin/sh

LOCATION="${1:-Sydney}"
MODE="${2:-icon}"
DATA=$(curl -s "wttr.in/${LOCATION}?format=j1")
TEMP=$(echo "$DATA" | grep -o '"temp_C": "[^"]*"' | head -1 | cut -d'"' -f4)
CODE=$(echo "$DATA" | grep -o '"weatherCode": "[^"]*"' | head -1 | cut -d'"' -f4)

map_icon() {
  case "$1" in
    113) echo "" ;;  # Sunny - sun
    116) echo "" ;;  # Partly cloudy - cloud-sun
    119) echo "" ;;  # Cloudy - cloud
    122) echo "" ;;  # Overcast - clouds (using cloud)
    176|263|266|296|299|302|308|353|356|359) echo "" ;;  # Rain - cloud-rain
    362|365|368|371|377) echo "" ;;  # Snow - snowflake
    386|389) echo "" ;;  # Thunder - cloud-bolt
    *) echo "" ;;      # Default - cloud
  esac
}

case "$MODE" in
    temp|--temp)
        echo "${TEMP}°C"
        ;;
    *)
        if [ -z "$CODE" ]; then
            ICON="󰖐"
        else
            ICON=$(map_icon "$CODE")
        fi
        echo "$ICON"
        ;;
esac
