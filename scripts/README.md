# Scripts

## `minimal_render.py`

Renders a short sine tone using a non-realtime `Score`.

> **Note**
> SuperCollider's `scsynth` must be installed and available on your `PATH` for
> non-realtime rendering to work.

### Run

```bash
python scripts/minimal_render.py
```

### Output

By default, the script writes the file to:

```
./scripts/output/minimal_render.wav
```

You can override the output location with:

```bash
python scripts/minimal_render.py --output /path/to/output.wav
```

## `gatogen_anthem_01.py`

Renders a longer, layered non-realtime cue inspired by the SuperCollider
Gatogen Anthem patch.

> **Note**
> SuperCollider's `scsynth` must be installed and available on your `PATH` for
> non-realtime rendering to work.

### Run

```bash
python scripts/gatogen_anthem_01.py /path/to/output.wav
```
