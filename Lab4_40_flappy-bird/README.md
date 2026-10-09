# Real-Time Flappy Bird Clone

This project is a Pygame Flappy Bird clone. It introduces students to interactive game design using object-oriented principles, real-time graphical rendering, collision detection, replay states, and sound feedback.

---

## What’s Provided

This version includes:

- A player-controlled bird that starts moving after the first `Space` press or mouse click
- Rect-based collision detection against both top and bottom pipes
- Scrolling pipes with randomized gaps
- Score display and sound feedback
- A game-over screen with final score
- Replay by choosing Easy, Medium, or Hard difficulty

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```


---

## Completed Tasks

The lab tasks implemented in this version are:

### Task 1: Refine Collision Detection

The collision bug was caused by checking only whether the bird's center point was inside a pipe. The game now uses the bird's full `pygame.Rect` and checks it with `Rect.colliderect()` against both the top and bottom pipe rectangles.

### Task 2: Implement Game Over Condition

When the bird hits the ground, ceiling, or a pipe, the game freezes and draws a game-over overlay in the Pygame window with the final score.

### Task 3: Add Replay Option

On the game-over screen, press:

- `E` for Easy: slower pipes and a larger gap
- `M` for Medium: default speed and gap
- `H` for Hard: faster pipes and a smaller gap
- `Q` or `Esc` to quit

Replay resets the bird, pipes, score, timer, game-over state, and start state.

### Task 4: Add Sound Feedback

The game uses `pygame.mixer` for sound effects:

- `sounds/flap.wav` when the bird flaps
- `sounds/score.wav` when the player scores
- `sounds/die.wav` when the game ends

Sounds are loaded safely, so the game still runs if a sound file is missing or the audio device is unavailable.

---

## Expected Behavior

- Bird waits in place until the first `Space` press or mouse click
- Bird flaps upward on `Space` or mouse click, then falls due to gravity
- Pipes spawn at a regular interval and scroll from right to left with a randomized gap
- Score increases by one each time the bird passes a pipe
- Game ends when the bird hits the ground, the ceiling, or a pipe
- Game-over screen shows the final score and replay/quit options

---

## Folder Structure

```
flappybird-main/
├── main.py
├── requirements.txt
├── sounds/
│   ├── flap.wav
│   ├── score.wav
│   └── die.wav
├── game/
│   ├── game_engine.py
│   ├── bird.py
│   └── pipe.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
