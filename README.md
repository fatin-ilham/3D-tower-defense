# Tower Defense Game

An OpenGL GLUT-based tower defense game with player combat, defense upgrades, and boss foes.

## Features

- **Wave-based combat**: Survive increasingly difficult foe waves
- **Boss foes**: Every 3rd wave, face a powerful boss with 10x health
- **Defense system**: Place and upgrade defenses to defend your fortress
- **Currency economy**: Earn currency from eliminations, spend on defenses and upgrades
- **God mode**: Auto-aim and auto-shoot foes

## Controls

### Movement & Camera
| Key | Action |
|-----|--------|
| W/A/S/D | Move placement marker |
| Arrow Up/Down | Camera height |
| Arrow Left/Right | Rotate camera |
| Right Mouse | Toggle first/third person view |

### Combat
| Key | Action |
|-----|--------|
| Left Mouse | Fire weapon |
| A/D | Rotate turret (third person) |

### Defense Management
| Key | Action |
|-----|--------|
| Enter | Place defense (costs 50 currency) |
| U | Upgrade nearest defense (costs 30 currency, max level 3) |

### Wave Rewards
| Key | Action |
|-----|--------|
| 1 | +100 max health (waves 1-4) |
| 2 | Free defense placement (waves 1-4) |

### Other
| Key | Action |
|-----|--------|
| C | Toggle god mode |
| P | Set health to 1000 |
| R | Restart match (match over) |

## Quick Start

1. Open this folder in VS Code
2. Run `tower_defense.py`

That's it! All files are already included.

## Requirements

- Python 3.x
- PyOpenGL
- PyOpenGL_accelerate (optional)
- freeglut

## Installation

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

On Windows, download freeglut from https://www.transmissionzero.co.uk/software/freeglut-devel/ and copy `freeglut.dll` to your Python Scripts folder.

## Gameplay

1. **Survive waves**: Foes spawn and move toward the fortress
2. **Fire at foes**: Left-click to fire, don't miss too many shots
3. **Place defenses**: After wave 4, place defensive defenses (50 currency each)
4. **Upgrade defenses**: Press 'U' to upgrade nearest defense (max level 3)
5. **Boss waves**: Every 3rd wave features a purple boss foe

## Currency System

- Start with 100 currency
- +10 currency per foe elimination
- Defense placement: 50 currency
- Defense upgrade: 30 currency

## Defense Levels

| Level | Scale | Color | Bonus |
|-------|-------|-------|-------|
| 1 | 1.0x | Gray | Normal |
| 2 | 1.2x | Green-tint | -30% fire rate |
| 3 | 1.5x | Red-tint | 2x damage |

## Credits

**Project by:** Fatin Ilham

**Original game authors:**
- 22301068 - Mushfique Tajwar
- 22301130 - Aryan Rayeen Rahman
- 22301327 - Md. Obaidullah Ahrar

## License

This project is for educational purposes.
