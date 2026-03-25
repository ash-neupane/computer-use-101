# Brainstorm

## Thesis

Train small (1B–3B) vision-language models via RL to automate conservation data entry on archaic web portals that have no API. Open-source friendly framing; skills transfer to any repetitive admin work on archaic portals.

## Why conservation?

- ML tools (MegaDetector, BirdNET) generate data 5x faster than humans can enter it
- The bottleneck is ingestion into portals designed for one-at-a-time human entry
- Only ONE browser automation tool exists across all of conservation tech (a CBC Puppeteer script)
- WILDLABS 2022 survey: 44% rated technical barriers as major/critical, 67% cited duplication from fragmented systems

## Design constraints (RL at 1B–3B scale)

- 3–10 actions per episode (small models can't reason through 20-step workflows)
- Binary or shaped reward — programmatic check, no reward model
- Procedurally generated training data (randomized inputs → infinite episodes)
- Tasks decompose into discrete actions: click, type, select

## Target selection filter

Only automate portals where: no write API, no reliable bulk upload, high manual volume.

### Automate (no write API)

| Platform | Notes |
|----------|-------|
| **eBird** | Read-only API, CSV upload is interactive wizard |
| **EDDMapS** | No API, bulk upload human-mediated |
| **iMapInvasives** | No API, bulk upload admin-only |
| **USFWS ePermits** | ServiceNow, zero public API |
| **State rehab portals** | 50 states, 50 systems, zero APIs |
| **Raven Pro / Kaleidoscope** | Desktop apps, no CLI — pixel-only |
| **Wildlife Insights** | No public API despite claims |

### Do NOT automate (good APIs exist)

iNaturalist, GBIF, Arbimon, BirdNET, MegaDetector, WRMD v3

## Top projects (in order)

### 1. Wildlife Rehab Annual Reports — start here
- WRMD generates data but can't submit to state portals
- Table form: species × disposition counts (released/died/euthanized/etc)
- Densest shaped reward: `correct_cells / total_cells`
- Closest analog to any table-based admin portal
- 1,200+ rehab centers face this annually

### 2. eBird Upload Wizard — most GitHub stars
- Navigate multi-step CSV import: upload, match location on map, confirm species, resolve rarities, submit
- Every BirdNET-Pi/Go user wants this
- Pitch: "Your BirdNET station runs 24/7. This agent files the eBird checklists."

### 3. Raven Pro Spectrogram Labeler — research novelty
- Pixel-only (no DOM, no tool-call possible)
- Click detection → label species → advance
- Spectrogram visuals = great README gifs
- May need 3B model

### 4. EDDMapS / iMapInvasives — stretch
- Map interactions, taxonomy search, polygon drawing

## Architecture

```
class ConservationTaskEnv:
    def reset() -> screenshot, task_description
    def step(action) -> screenshot, reward, done, info
    def verify() -> dict  # field-by-field vs ground truth
```

Two versions per task:
1. **Pixel-based** — agent sees screenshots, outputs mouse/keyboard
2. **MCP tool-call** — agent sees structured state, outputs tool calls

Compare learning curves to establish baselines.

## Model stack

- **Base:** Qwen2-VL-1.5B (fits 24GB with RL overhead), scale to 3B for harder tasks
- **RL:** GRPO (Group Relative Policy Optimization)
- **Framework:** TRL or OpenRLHF for training, Gymnasium for env interface
- **Target:** 10,000+ procedurally generated episodes per task

## Transfer to other domains

| Conservation task | General equivalent |
|---|---|
| Rehab report table | Any table-based data entry portal |
| Species taxonomy search | Hierarchical code lookup (e.g. CPT, ICD, NAICS) |
| Multi-page permit wizard | Any multi-step government form |
| Rare species confirmation | Exception/alert handling dialogs |
| Rejected submission fix | Error correction and resubmission |
