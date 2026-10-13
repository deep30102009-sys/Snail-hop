# Snail Hop

A simple endless jumping game made with Python and pygame. A snail slides toward you, and you have to jump over it. Collect coins on the way.

<img width="802" height="432" alt="Screenshot" src="https://github.com/user-attachments/assets/02ebc2a9-bc3b-4c60-a709-ac80646b9638" />


## How to play

| Key | Action |
|-----|--------|
| `SPACE` | Jump |
| `R` | Restart after game over |

- Jump over the snail. Touching it ends the game.
- You get 1 point every time you get past the snail.
- Jump to collect coins. Your coin total and high score are saved between runs.

## How to run

You need Python 3.8 or newer.

```
git clone https://github.com/deep30102009-sys/snail-hop.git
cd snail-hop
pip install -r requirements.txt
python main.py
```

On Mac or Linux, use `python3` instead of `python`.

## Project structure

```
snail-hop/
├── main.py            # the whole game
├── requirements.txt   # pygame
├── Graphics/          # character, snail, coin, sky and ground images
└── Sound/             # music and sound effects
```

## How it works

- **Jumping:** pressing SPACE gives the character an upward speed. Gravity reduces that speed a little every frame, so the character rises, slows down and falls.
- **Collisions:** the game checks if the character's rectangle overlaps the snail's or a coin's rectangle. The snail hitboxes are slightly smaller than the pictures so near-misses feel fair.
- **Coins:** coins come in groups of 1 to 3, stored in a list. Each frame they move left, and any that go off-screen are removed.
- **Saving:** the high score and coin total are written to small text files (`highscore.txt`, `coinwallet.txt`), which are created when you play.

## Credits

Code by Deepshikha.

Images and sounds are not mine. They belong to their creators:

- Character sprites: "ANIMATED CHARACTER" BY Sogomn , CCO,https://opengameart.org/content/animated-character (split into separate frames)
- Snail sprites: "Snail" by Flatlander, CC BY 3.0, https://opengameart.org/content/snail (split into separate frames)
- Coin sprites: "Rotating Coin" by Puddin, CC0, https://opengameart.org/content/rotating-coin (split into separate frames)
- Sky: "Sky Backdrop" by bart, CC BY 3.0, https://opengameart.org/content/sky-backdrop (resized)
- Ground:
- Music:"Party and Gameover loop" (happy theme) by gilzoide, CC0, https://opengameart.org/content/party-and-gameover-loop,converted.
- Sound effects (jump, coin, game over): CREATOR NAME, LINK
                  
