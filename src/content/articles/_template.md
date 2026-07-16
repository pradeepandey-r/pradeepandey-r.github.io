---
# Template: copy this file, drop the leading "_" from the name, edit, and delete draft: true.
title: "Article template"
description: "One-sentence summary shown in the article list and RSS feed."
date: 2026-07-14
math: true
draft: true
---

The opening paragraph is plain prose in Charter, with an [inline link](https://example.com), some *italic*, some **bold**, and inline code like `torch.softmax(x, dim=-1)`.

## Math

Inline math flows with the text: the loss gradient $\nabla_\theta \mathcal{L}(\theta)$ and a probability $p \in [0, 1]$. Display math gets its own block:

$$
\mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}}
$$

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
| ----- | ------ |
| Gemma-2 | 2B |
| Qwen2.5 | 1.5B |

That's everything an article needs.
