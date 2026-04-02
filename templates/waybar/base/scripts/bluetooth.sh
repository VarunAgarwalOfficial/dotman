#!/bin/bash
# Get bluetooth device battery percentage and output ASCII bar + icon

# Try to get battery percentage from bluetoothctl
battery=$(bluetoothctl info 2>/dev/null | grep "Battery Percentage" | grep -oP '\(\K\d+(?=\))' | head -1)

# If not found via bluetoothctl, try alternative methods
if [ -z "$battery" ]; then
    # Check if any device is connected and has battery info via dbus
    device_path=$(bluetoothctl info 2>/dev/null | grep "Device" | head -1 | awk '{print $2}' | tr ':' '_')
    if [ -n "$device_path" ]; then
        battery=$(dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_${device_path} org.freedesktop.DBus.Properties.Get string:org.bluez.Device1 string:BatteryPercentage 2>/dev/null | grep "byte" | awk '{print $3}' | tr -d ')')
    fi
fi

# Default to 0 if no battery found
battery=${battery:-0}

# Calculate bar level (0-10)
level=$((battery / 10))
[ "$level" -gt 10 ] && level=10
[ "$level" -lt 0 ] && level=0

# ASCII bar (10 segments)
full="█"
empty="░"
bar=""
for i in {0..9}; do
    if [ $i -lt $level ]; then
        bar="${bar}${full}"
    else
        bar="${bar}${empty}"
    fi
done

echo "${bar}"
