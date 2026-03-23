# TV Keyboard Optimization

Better ways to type efficiently on smaller keyboards, such as a TV remote. This project aims to reduce keystrokes required to type text using only navigation keys.

## Overview

Typing on devices with minimal input options, like TVs with remotes, is often slow and frustrating. Most solutions rely on **voice recognition** or **gaze tracking**, but what if we could improve text input using just the arrow keys?

This project investigates a **decision-tree based input method** for QWERTY-style keyboards mapped to a remote control. It calculates **keystrokes needed per string** and compares traditional TV input with optimized methods.

* **TV-style keyboard layout**:

  ```
  q w e r t y u i o p
  a s d f g h j k l
  z x c v b n m
  ```

* **BFS Distance**: Calculates true “snap-path” cost between two keys using arrow navigation.

* **Keystrokes Calculation**: Counts the total number of keystrokes needed to type a string, assuming one character per navigation plus confirmation.

* **Efficiency Metric**:
  Measures input efficiency as:
  $$
  E = \frac{N_\text{keys}}{K_\text{avg} \cdot \max(N_\text{chars}, N_\text{keys})}
  $$
  where (K_\text{avg} = \lceil \log_{N_\text{keys}} N_\text{chars} \rceil).

---
## Comparison to TV Input

| Search Term   | TV Keystrokes | Optimized Keystrokes | % Decrease |
| ------------- | ------------- | -------------------- | ---------- |
| BTS           | 14            | 9                    | 35.71%     |
| pewdiepie     | 54            | 27                   | 50.00%     |
| Billie Eilish | 51            | 39                   | 23.53%     |
| baby shark    | 50            | 30                   | 40.00%     |
| old town road | 67            | 39                   | 41.79%     |
| music         | 34            | 15                   | 55.88%     |

*Full table available [here](http://vetrivln.github.io/2026/03/22/better-input-methods/).*

 Using this method, **average keystrokes are significantly reduced**, improving text input speed on limited keyboards.

---

## Goals

* Reduce typing effort on devices with minimal keys
* Explore new input methods based on **decision-tree navigation**

---

## License

MIT License © 2026
