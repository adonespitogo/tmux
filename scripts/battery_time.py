#!/usr/bin/env python3
import subprocess
import re
import platform
import os

def get_battery_macos():
    """Get battery info on macOS"""
    result = subprocess.run(['ioreg', '-rn', 'AppleSmartBattery'], capture_output=True, text=True)
    data = result.stdout

    # Extract values
    current_capacity_match = re.search(r'"AppleRawCurrentCapacity"\s*=\s*(\d+)', data)
    max_capacity_match = re.search(r'"AppleRawMaxCapacity"\s*=\s*(\d+)', data)
    instant_amperage_match = re.search(r'"InstantAmperage"\s*=\s*(\d+)', data)
    
    if not all([current_capacity_match, max_capacity_match, instant_amperage_match]):
        return None
    
    current_capacity = int(current_capacity_match.group(1))  # type: ignore
    max_capacity = int(max_capacity_match.group(1))  # type: ignore
    instant_amperage_raw = int(instant_amperage_match.group(1))  # type: ignore

    # Convert unsigned to signed (macOS reports as unsigned 64-bit)
    if instant_amperage_raw > 2**63 - 1:
        instant_amperage = instant_amperage_raw - 2**64
    else:
        instant_amperage = instant_amperage_raw

    return current_capacity, max_capacity, instant_amperage

def get_battery_linux():
    """Get battery info on Linux"""
    # Try to find battery in /sys/class/power_supply/
    battery_path = None
    power_supply_path = '/sys/class/power_supply'
    
    if not os.path.exists(power_supply_path):
        return None
    
    # Find first battery
    for device in os.listdir(power_supply_path):
        if device.startswith('BAT'):
            battery_path = os.path.join(power_supply_path, device)
            break
    
    if not battery_path:
        return None
    
    try:
        # Read battery info
        with open(os.path.join(battery_path, 'energy_now'), 'r') as f:
            energy_now = int(f.read().strip())
        with open(os.path.join(battery_path, 'energy_full'), 'r') as f:
            energy_full = int(f.read().strip())
        with open(os.path.join(battery_path, 'power_now'), 'r') as f:
            power_now = int(f.read().strip())
        with open(os.path.join(battery_path, 'status'), 'r') as f:
            status = f.read().strip()
        
        # Convert to similar format as macOS (mAh equivalent)
        current_capacity = energy_now // 1000
        max_capacity = energy_full // 1000
        
        # Power is in µW, convert to mA equivalent (negative for discharging)
        if status == 'Discharging':
            instant_amperage = -(power_now // 1000)
        elif status == 'Charging':
            instant_amperage = power_now // 1000
        else:
            instant_amperage = 0
        
        return current_capacity, max_capacity, instant_amperage
    except (FileNotFoundError, ValueError):
        # Try alternative: charge_now/charge_full instead of energy_now/energy_full
        try:
            with open(os.path.join(battery_path, 'charge_now'), 'r') as f:
                current_capacity = int(f.read().strip()) // 1000
            with open(os.path.join(battery_path, 'charge_full'), 'r') as f:
                max_capacity = int(f.read().strip()) // 1000
            with open(os.path.join(battery_path, 'current_now'), 'r') as f:
                current_now = int(f.read().strip()) // 1000
            with open(os.path.join(battery_path, 'status'), 'r') as f:
                status = f.read().strip()
            
            if status == 'Discharging':
                instant_amperage = -current_now
            elif status == 'Charging':
                instant_amperage = current_now
            else:
                instant_amperage = 0
            
            return current_capacity, max_capacity, instant_amperage
        except (FileNotFoundError, ValueError):
            return None

try:
    # Detect OS and get battery info
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        battery_info = get_battery_macos()
    elif system == 'Linux':
        battery_info = get_battery_linux()
    else:
        battery_info = None
    
    if not battery_info:
        print("--", end='')
    else:
        current_capacity, max_capacity, instant_amperage = battery_info
        
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
except Exception:
    print("--", end='')
