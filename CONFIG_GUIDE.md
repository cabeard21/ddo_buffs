# DAoC Buffs Configuration Guide

This guide explains how to configure the `config.json` file for the DAoC Buffs application. The configuration file is located in the data directory (typically `~/.DAoC Buffs/` on Linux/Mac or `%USERPROFILE%\.DAoC Buffs\` on Windows).

## File Structure

The `config.json` file contains two main sections:

```json
{
    "buff_coordinates": [x1, y1, x2, y2],
    "buff_config": {
        "stack_buffs": [],
        "buff_order": [],
        "thresholds": {},
        "cooldowns": {}
    }
}
```

## Configuration Sections

### 1. buff_coordinates

**Purpose**: Defines the screen region where the application will look for buff icons.

**Format**: `[x1, y1, x2, y2]` where:
- `x1, y1`: Top-left corner coordinates
- `x2, y2`: Bottom-right corner coordinates

**Example**:
```json
"buff_coordinates": [373, 0, 954, 130]
```

**How to find your coordinates**:
1. Use the debug mode feature (if available) to capture a screenshot with detection boxes
2. Use screen capture tools to measure the buff area
3. Trial and error by adjusting values and testing detection

### 2. buff_config

This section contains all buff-related configuration options.

#### 2.1 stack_buffs

**Purpose**: Groups buffs that cannot be active simultaneously (e.g., different ranks of the same buff).

**Format**: Array of objects with `name` and `buffs` properties.

**Example**:
```json
"stack_buffs": [
    {
        "name": "haste_stack",
        "buffs": ["haste.png", "celerity.png"]
    }
]
```

**How it works**: When one buff from a stack is detected, any other buffs from the same stack will be removed from the display.

#### 2.2 buff_order

**Purpose**: Defines the display order of buff timers in the UI.

**Format**: Array of buff filenames (without path).

**Example**:
```json
"buff_order": [
    "celerity.png",
    "weaponskill.png",
    "evade.png",
    "melee_abs.png",
    "magic_abs.png"
]
```

**Note**: Buffs not listed in this array will appear at the end in alphabetical order.

#### 2.3 thresholds (Optional)

**Purpose**: Sets custom detection thresholds for specific buffs.

**Format**: Object with buff filename as key and threshold value (0.0 to 1.0) as value.

**Example**:
```json
"thresholds": {
    "celerity.png": 0.85,
    "weaponskill.png": 0.75
}
```

**Default**: 0.8 (if not specified)

**Usage**: Lower values make detection more sensitive, higher values make it more strict.

#### 2.4 cooldowns (Optional)

**Purpose**: Defines cooldown durations for buffs after they expire.

**Format**: Object with buff filename as key and cooldown duration in seconds as value.

**Example**:
```json
"cooldowns": {
    "celerity.png": 300,
    "weaponskill.png": 180
}
```

## Available Buff Icons

The following buff icons are included with the application:
- `celerity.png` - Celerity buff
- `weaponskill.png` - Weapon skill buff
- `evade.png` - Evade buff
- `melee_abs.png` - Melee absorption buff
- `magic_abs.png` - Magic absorption buff
- `haste.png` - Haste buff
- `parry.png` - Parry buff

## Complete Example Configuration

```json
{
    "buff_coordinates": [373, 0, 954, 130],
    "buff_config": {
        "stack_buffs": [
            {
                "name": "haste_stack",
                "buffs": ["haste.png", "celerity.png"]
            }
        ],
        "buff_order": [
            "celerity.png",
            "weaponskill.png",
            "evade.png",
            "melee_abs.png",
            "magic_abs.png",
            "haste.png",
            "parry.png"
        ],
        "thresholds": {
            "celerity.png": 0.85,
            "weaponskill.png": 0.75
        },
        "cooldowns": {
            "celerity.png": 300,
            "weaponskill.png": 180,
            "evade.png": 240
        }
    }
}
```

## Troubleshooting

### Buff Detection Issues

1. **Buffs not being detected**:
   - Check that `buff_coordinates` covers the correct screen area
   - Lower the detection threshold for problematic buffs
   - Ensure buff icons are properly placed in the `buffs` directory

2. **False positives**:
   - Increase the detection threshold for affected buffs
   - Refine the `buff_coordinates` to exclude similar-looking areas

3. **Performance issues**:
   - Reduce the size of the detection area in `buff_coordinates`
   - Remove unnecessary buffs from `buff_order`

### Configuration File Issues

1. **Invalid JSON**: Use a JSON validator to check syntax
2. **File not found**: Ensure the file is in the correct data directory
3. **Permission errors**: Check file permissions on the config file

## Data Directory Location

The configuration file is stored in the application's data directory:

- **Windows**: `%USERPROFILE%\.DAoC Buffs\config.json`
- **Linux/Mac**: `~/.DAoC Buffs/config.json`

## Backup and Restore

It's recommended to backup your `config.json` file before making changes. The application will create a default configuration if the file is missing or corrupted.

## Advanced Configuration

For advanced users, you can also modify:
- Buff icon files in the `buffs` directory
- Timer digit templates in the `templates` directory
- Application position in `position.json`

**Note**: Modifying these files may affect application functionality and should be done with caution. 