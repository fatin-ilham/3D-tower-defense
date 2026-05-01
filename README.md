# Tower Defense Game

An OpenGL GLUT-based tower defense game with player combat, tower upgrades, and boss enemies.

## Features

- **Wave-based combat**: Survive increasingly difficult enemy waves
- **Boss enemies**: Every 3rd round, face a powerful boss with 10x health
- **Tower system**: Place and upgrade towers to defend your castle
- **Coin economy**: Earn coins from kills, spend on towers and upgrades
- **Cheat mode**: Auto-aim and auto-shoot enemies

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
| Left Mouse | Shoot |
| A/D | Rotate gun (third person) |

### Tower Management
| Key | Action |
|-----|--------|
| Enter | Place tower (costs 50 coins) |
| U | Upgrade nearest tower (costs 30 coins, max level 3) |

### Round Rewards
| Key | Action |
|-----|--------|
| 1 | +100 max health (rounds 1-4) |
| 2 | Free tower placement (rounds 1-4) |

### Other
| Key | Action |
|-----|--------|
| C | Toggle cheat mode |
| P | Set health to 1000 |
| R | Restart game (game over) |

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

1. **Survive waves**: Enemies spawn and move toward the castle
2. **Shoot enemies**: Left-click to fire, don't miss too many shots
3. **Place towers**: After round 4, place defensive towers (50 coins each)
4. **Upgrade towers**: Press 'U' to upgrade nearest tower (max level 3)
5. **Boss rounds**: Every 3rd round features a purple boss enemy

## Coin System

- Start with 100 coins
- +10 coins per enemy kill
- Tower placement: 50 coins
- Tower upgrade: 30 coins

## Tower Levels

| Level | Scale | Color | Bonus |
|-------|-------|-------|-------|
| 1 | 1.0x | Gray | Normal |
| 2 | 1.2x | Green-tint | -30% cooldown |
| 3 | 1.5x | Red-tint | 2x damage |

## Credits

Made by:
- 22301068 - Mushfique Tajwar
- 22301130 - Aryan Rayeen Rahman
- 22301327 - Md. Obaidullah Ahrar

## License

This project is for educational purposes.
