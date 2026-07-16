---
# draft: true keeps this out of every build. It renders in `npm run dev` only,
# so the article layout can be judged with real-looking content in it.
title: "A Short Note on Numerically Stable Softmax"
description: "Sample article used to check how the layout holds with prose, math, code, and tables in it."
date: 2026-07-12
math: true
draft: true
---

This is placeholder content for layout testing. The opening paragraph runs long enough to show how a measure of body text sits against the column width, with an [inline link](https://example.com), some *italic*, some **bold**, and inline code like `torch.softmax(x, dim=-1)` mixed into the line.

## Math

Inline math flows with the text: the loss gradient $\nabla_\theta \mathcal{L}(\theta)$ and a probability $p \in [0, 1]$. Display math gets its own block:

$$
\mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}}
$$

Subtracting the row maximum leaves the result unchanged but keeps every exponent at or below zero, which is what stops the overflow.

## Code

```python
import numpy as np

def softmax(z: np.ndarray) -> np.ndarray:
    """Numerically stable softmax over the last axis."""
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

print(softmax(np.array([1.0, 2.0, 3.0])))
```

## Structure

> A blockquote, for quoting other work, set off with a hairline and muted italic.

A short list:

- behavioral robustness
- activation-level structure
- low-compute evaluation

| model | params |
| ------- | ------ |
| Gemma-2 | 2B |
| Qwen2.5 | 1.5B |

That covers everything an article needs.
