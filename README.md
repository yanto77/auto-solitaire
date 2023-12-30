# auto-solitaire

Automatic solver for [EXAPUNKS's](https://store.steampowered.com/app/716490/EXAPUNKS/) solitaire minigame. Demo: [video](./docs/demo.webm).

Dependencies:

```
$ apt install python3-opencv
$ pip3 install pyautogui pyscreeze
```

Usage:
1. Run solitaire from EXAPUNKS on one screen.
2. Run `python3 src/main.py` on another screen.

Note: The solution includes hard-coded values for finding the card and mouse locations. Your screen may require different values.