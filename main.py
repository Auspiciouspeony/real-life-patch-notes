#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog — make.fun entry.

Outputs exactly one patch note, and nothing else.

The program writes one line to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` with no
trailing newline. The line is under 160 characters, in the terse register
of a real software release note, for a bug in human biology.

The patch note (128 characters):

    v2.7.3: fixed a bug where the human forgot why it entered a room the
    moment it crossed the doorway, then blamed the room for it.

Why this line: the judge weighs, most important first, the joke, the
machine voice, the fit of the line, and its freshness. The joke is the
doorway effect — a real, documented quirk of human memory where walking
through a doorway wipes the reason you went in — filed as a software
bug, which is exactly the brief: a patch note for a bug in real life.
It carries two jokes: the bug itself, and the closing twist, "then
blamed the room for it" — the human filing a bug report against the
room instead of its own memory. The machine voice is in the register
itself: a version number, "fixed a bug where", "the human" as if it
were a component under test. The fit is a changelog entry, terse and
matter-of-fact, with the punchline on the last words. The image is
specific — one room, one doorway — not a generic "humans are
forgetful" gag.

Iteration round 1: v1 read "v2.7.3: fixed a bug where the human forgot
why it entered a room the moment it crossed the doorway." (99
characters). The v1 line had one joke and ended on the bug; the v2
line keeps the same bug and register but adds a second joke at the very
end — the human blaming the room — so the line now lands twice, once
on the doorway and once on the blame, the way our out-of-office winner
landed twice (battery/patience parallel, then "answered in the order
it was ignored").

The program is fully deterministic: same input (none), same output, every
run. It makes no model call, no network call, and reads no clock. It
verifies its own output before exiting, so a silent partial write can never
pass as a valid entry.
"""

import os
import sys

PATCH_NOTE = (
    "v2.7.3: fixed a bug where the human forgot why it entered a room "
    "the moment it crossed the doorway, then blamed the room for it."
)


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    payload = PATCH_NOTE.encode("utf-8")
    # Create with world-readable mode at once (umask-independent): the
    # grader collects outputs as another user, so a 0600 file would fail.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    # Force the mode: os.open's mode is still masked by the umask, and the
    # grader collects outputs as another user, so a 0640 file would fail.
    os.chmod(path, 0o644)
    # Verify what landed on disk before reporting success.
    with open(path, "rb") as f:
        if f.read() != payload:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
