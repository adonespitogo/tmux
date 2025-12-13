#!/usr/bin/env python3
import subprocess
import re

try:
    # Get battery data
    result = subprocess.run(['ioreg', '-rn', 'AppleSmartBattery'], capture_output=True, text=True)
    data = result.stdout

    # Extract values
    current_capacity_match = re.search(r'"AppleRawCurrentCapacity"\s*=\s*(\d+)', data)
    max_capacity_match = re.search(r'"AppleRawMaxCapacity"\s*=\s*(\d+)', data)
    instant_amperage_match = re.search(r'"InstantAmperage"\s*=\s*(\d+)', data)
    
    if not all([current_capacity_match, max_capacity_match, instant_amperage_match]):
        print("--", end='')
    else:
        current_capacity = int(current_capacity_match.group(1))  # type: ignore
        max_capacity = int(max_capacity_match.group(1))  # type: ignore
        instant_amperage_raw = int(instant_amperage_match.group(1))  # type: ignore

        # Convert unsigned to signed (macOS reports as unsigned 64-bit)
        if instant_amperage_raw > 2**63 - 1:
            instant_amperage = instant_amperage_raw - 2**64
        else:
            instant_amperage = instant_amperage_raw

        # Calculate time remaining
        if instant_amperage < 0:  # Discharging
            amperage = abs(instant_amperage)
            if amperage > 0:
                hours = current_capacity / amperage
                if hours < 1:  # Show red when < 1 hour
                    minutes = int(hours * 60)
                    print(f"#[fg=red]{minutes}m#[fg=#2E3440]", end='')
                else:
                    print(f"{hours:.1f}h", end='')
            else:
                print("--", end='')
        elif instant_amperage > 0:  # Charging
            remaining = max_capacity - current_capacity
            hours = remaining / instant_amperage
            print(f"⚡{hours:.1f}h", end='')
        else:
            print("--", end='')
except:
    print("--", end='')
