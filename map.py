from collections import deque

layout = [
    list("1234567890"),
    list("qwertyuiop"),
    list("asdfghjkl"),
    list("zxcvbnm")
]

# build position map
pos = {}
for r in range(len(layout)):
    for c in range(len(layout[r])):
        pos[layout[r][c]] = (r, c)


def bfs_distance(a, b):
    """True snap-path cost between two keys"""
    if a == b:
        return 0

    sr, sc = pos[a]
    tr, tc = pos[b]

    q = deque([(sr, sc, 0)])
    visited = set()

    while q:
        r, c, d = q.popleft()

        if (r, c) == (tr, tc):
            return d

        if (r, c) in visited:
            continue
        visited.add((r, c))

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(layout) and 0 <= nc < len(layout[nr]):
                if layout[nr][nc] != " ":
                    q.append((nr, nc, d + 1))

    return float("inf")


def keystrokes_tv(text, start='a'):
    text = text.lower()
    current = start
    total = 0

    for ch in text:
        if ch not in pos:
            continue

        total += bfs_distance(current, ch)
        total += 1
        current = ch

    return total

### New method:

rows = [
    "1234567890-=",
    "qwertyuiop[]",
    "asdfghjkl;'",
    "zxcvbnm,./"
]

arrows = ["↑", "→", "↓", "←"]

row_arrows_map = {i: arrows[i] for i in range(len(rows))}

def char_to_three_arrows(char: str) -> str:
    """
    Convert a single character to three-arrow code:
    - Row arrow
    - Block arrow (every 4 chars in the row)
    - Position within block
    """
    c = char.lower()
    for row_index, row_chars in enumerate(rows):
        if c in row_chars:
            index = row_chars.index(c)
            r_arrow = row_arrows_map[row_index]
            b_arrow = arrows[(index // 4) % 4]
            p_arrow = arrows[index % 4]
            return r_arrow + b_arrow + p_arrow
    return "???"

def string_to_three_arrows(s: str) -> str:
    return "".join(char_to_three_arrows(c) for c in s)
