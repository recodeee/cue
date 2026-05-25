---
description: Release the /freeze edit-scope lock so edits are allowed anywhere again.
---

# /unfreeze — release edit-scope lock

Removes the freeze marker so the `freeze-edit-scope` hook becomes a no-op.

```bash
rm -f ~/.config/cue/freeze-dir
echo "cue: edits unfrozen."
```

Idempotent. Safe to run when nothing is frozen.
