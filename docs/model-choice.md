# Model Choice: Vision-Language Models for Minesweeper RL

Goal: find the smallest VLM that can process pixel screenshots and be RL-trained on a MacBook.

## Sub-256M VLMs

| Model | Params | Architecture | HuggingFace | License |
|-------|--------|-------------|-------------|---------|
| **nanoVLM-222M** | 222M | SigLIP-B/16 (85M) + SmolLM2-135M | `lusxvr/nanoVLM-222M` | Apache 2.0 |
| **SmolVLM-256M** | 256M | SigLIP-B/16 (93M) + SmolLM2-135M | `HuggingFaceTB/SmolVLM-256M-Instruct` | Apache 2.0 |
| **SmolVLM2-256M** | 256M | Same arch, adds video | `HuggingFaceTB/SmolVLM2-256M-Video-Instruct` | Apache 2.0 |

## Nearby alternatives (≤ 500M)

| Model | Params | Notes | HuggingFace |
|-------|--------|-------|-------------|
| nanoVLM-450M | 450M | Newer nanoVLM, smarter embedding packing | Default in `huggingface/nanoVLM` repo |
| SmolVLM-500M | 500M | Big perf bump over 256M | `HuggingFaceTB/SmolVLM-500M-Instruct` |
| Moondream 0.5B | 500M | Edge-optimized, strong for its size | `vikhyatk/moondream2` |

## Why not a plain CNN?

A 2-5M param CNN + DQN solves minesweeper easily (93% win rate on 6x6 in published work).
But the repo's goal is computer-use agents — skills learned here should transfer to the
conservation portal tasks. A VLM with LoRA/GRPO keeps us on that path.

## Recommendation

**nanoVLM-222M** for experimentation. Reasons:

1. Smallest available VLM (222M params, <1GB memory).
2. Pure PyTorch, ~750 lines — easy to hack for RL.
3. Same SigLIP + SmolLM2 architecture as SmolVLM, so findings transfer up.
4. Trainable on MacBook with LoRA (~1-5M trainable params).

Fallback to **SmolVLM-256M** if nanoVLM-222M underperforms — it has better instruction tuning.

## References

- [nanoVLM repo](https://github.com/huggingface/nanoVLM) — training code
- [nanoVLM-222M weights](https://huggingface.co/lusxvr/nanoVLM-222M)
- [SmolVLM paper](https://arxiv.org/abs/2504.05299)
- [NanoVLMs paper](https://arxiv.org/abs/2502.07838) — "how small can we go?"
- [SmolVLM 256M & 500M blog](https://huggingface.co/blog/smolervlm)
- [nanoVLM blog](https://huggingface.co/blog/nanovlm)
