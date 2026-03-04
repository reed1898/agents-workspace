# Side-by-side video compare

Create one comparison video by placing two videos left/right.

## Usage

```bash
./compare_side_by_side.sh left.mp4 right.mp4 output.mp4
```

## Optional flags

- mute output audio:

```bash
./compare_side_by_side.sh --mute left.mp4 right.mp4 output.mp4
```

- add LEFT/RIGHT labels:

```bash
./compare_side_by_side.sh --label left.mp4 right.mp4 output.mp4
```

- both:

```bash
./compare_side_by_side.sh --mute --label left.mp4 right.mp4 output.mp4
```
