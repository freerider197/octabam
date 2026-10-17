@AGENTS.md

# CLAUDE.md -- Jack's Octatrack firmware (octabam fork)

Handoff written 15 Oct 2026 from a long claude.ai session. Read "How to work with Jack" first.
Fill in the three `FILL IN` lines at the bottom of "Current builds" before relying on this file.

## What this is

Jack Fresia (DJ and producer, Amsterdam) runs an **Octatrack MK1 on OS 1.40C** with a custom firmware
built by **octabam** (github.com/sambanks/octabam, a remixer that composes modules into one image built
from the user's own official 1.40C). His fork of the repo is: https://github.com/freerider197/octabam.
Tim Hastie's modules (SYNTH MACHINE, SCALE QUANTIZER, TUNER, SY DRUM) come from
github.com/timhastie/octatrick-modules, pulled in as git submodules under `modules/*/upstream`.

Scope: **Octatrack only.** Jack also has a Digitone and a Rytm MK1; those are separate projects, keep them out.

## How to work with Jack (read first)

- He is frustrated by wasted time and tokens. Be short and plain. No crammed formatting.
- **Commands: one plain bash block for the whole sequence**, the usual flow: `make check` then `make image`.
  No clever tricks, no step-by-step across messages.
- **WORKFLOW (VERY IMPORTANT, set by Jack 17 Oct 2026): he ALWAYS builds on his own Mac. Never build an image
  here, never ask whether to.** Claude Code adds or removes modules, edits the remix, and checks everything
  that matches (module composition, selftest entry, hooks, anything it can run), then gives him the exact
  terminal commands as **one plain bash block**. He pastes and runs it himself. The block does: remix +
  selftest entry, then `make check` (logged to `out/jack-mix-N.check.log`) `&& make image REMIX=jack-mix-N
  BUILD=N VERSION=OCTAJACKN`, `shasum -a 256`, and copy the `.bin` to `octabam/out`.
  Say plainly what is verified versus assumed, never delete his old builds, and **stop after reporting, with
  no extras he did not ask for**.
- Files he uploads (OS zip, his `.bin`) are for reference or later use, not a request to build. Never read an
  upload or a "no" as permission to start work. Never invent module additions (fix modules etc.) as work to do;
  suggestions are ideas at the end of a report, and only when asked for a roundup.
- When he says "update" he wants: progress on the modules in his OS (v16 set) and a roundup of new releases
  (Tim's repo tags, octabam main, Lukas Paul's modules), short. Not edits to files.
- **Verify before he flashes.** Always say plainly what was *verified* versus *assumed*. Use octabam's own
  words: **measured** (on a unit), **port** (emulator), **inferred**.
- Do exactly the thing he asked, in one go, no more. When he says "I want the latest X with everything", add it
  to the remix and check it; do not ask twice. Do not add unrequested features, tests or doc changes.
- Never remove or tidy his old build files. He keeps every superseded `.bin` as backup history.
- Do not commit OS files or built `.bin` images to the public fork. octabam's rule is "no firmware distributed".
- He lost trust once this week after untested claims. Do not repeat that: if you have not run it, say so.

## Where things are

- `BASE = /Users/jacopofresia/Documents/ModularStuff/Octatrack Alternrative Firmware` (spelling is as on disk)
- `$BASE/octabam` -- old tree, pinned late Sept 2026. Its `out/` holds **all his built `.bin` files** (history).
  Contains `downloads/` (official OS zip) and `out/raw` (unpacked OS sections) that new trees copy from.
- `$BASE/octabam-2.11` -- new tree: octabam main at `a67a11126f8a00446e6fcda5c107c137aba77b1f` (10 Oct 2026),
  used for the Tim v2.11 and later builds. Do **not** move this folder: CMake caches absolute paths
  (it broke once; fix was `rm -rf vendor/dsp56300/build && make setup`).
- M1 MacBook Pro, macOS 12 (Homebrew has no bottles, everything builds from source), zsh.
  `m68k-elf-gcc` needed texinfo as an added build dependency in the local formula. `make docs` is a no-op;
  use `python3 tools/remix/index.py --write`.

## Current builds and status

Naming rule: remix `jack-mix-N` is built with `BUILD=N` and flashed as `OCTAJACKN` (version field, max 10
characters, uppercase; the unit accepted `OCTAJACK13`). Build numbers only go up, never reused.
Remix folder + `tools/remix/selftest.py` entry required for every remix.

| Build | Content | Status |
|---|---|---|
| OCTAJACK13 | lean set, Tim v2.9 + local quantizer patch, USB AUDIO EXTENDED (20 ch) | **flashed, works, the proven fallback** |
| OCTAJACK14 | same, Tim v2.11 (`5f3d7456a885d37c933b2f47fce2bed29176f3e6`), local patch | built (sha256 `7479fa30108e74846b2b4e5dddc65671dfb49d3282beddebd2aa4bbaa7123fc1`); FILL IN flashed? |
| OCTAJACK15 | OCTAJACK14 + SY DRUM | **flashed, SY DRUM misbehaved**: pitch drifts, tiny knob turn gives white noise. Not recommended |
| OCTAJACK16 | lean set, Tim v2.14 (`39dc5d8ca285c14674b66a452f58a5a0364efb96`), **no local patch**, no SY DRUM | built on his Mac, sha256 `26f12e36c50dcedfa94c9d2d3e413e8073b5bdf4bbec6110beb81d20ac911e9c`; FILL IN: check log result in `out/jack-mix-16.check.log`, flashed? |

Older: builds 1-7 ran Tim's pre-rename v9.1; builds 8-12 ran v2.9. Build 10 had CHARACTER, EUCLID, MINIVERB
(they loaded and played on his unit); he dropped them in build 12.

## The module set and the rules

**jack-mix-16 modules:** SYNTH MACHINE, SCALE QUANTIZER, TUNER, USB MIDI, USB AUDIO OUT TRACKS MAIN CUE, and all
14 stock effects: FILTER, EQUALIZER, PHASER, COMPRESSOR, DELAY, PLATE REV, SPRING REV, DARK REV, SPATIALIZER,
FLANGER, CHORUS, LO-FI, DJ EQ, COMB FILTER. `fallback="NONE"`.

USB audio is 20 channels: tracks 1-16 as stereo pairs (T1 on 1/2 ... T8 on 15/16), MAIN on 17/18, CUE on 19/20.

Rules learned:

- Move SYNTH MACHINE, SCALE QUANTIZER and TUNER to **the same Tim tag together** (they share internal data).
- Keep USB MIDI together with the USB audio module (shared USB interrupt and reset hooks). USB audio alone did not build.
- A ColdFire-only module goes in `modules=(...)`, never in `fx1=(...)`.
- Any folder under `modules/` that no remix uses fails `make check`; delete or use it.
- SY DRUM must be **symlinked, not copied**: `ln -sfn synth/upstream/sy-drum modules/sy-drum`
  (its manifest refers to `../synth/engine_abi.inc`).
- On octabam main (a67a111) the selftest entry goes after `_want = {"mods": (), ` (on the old tree the first
  `_want = {` was the right one; on main it is `_pin_want`, so a naive replace corrupts the wrong table).
- With a `BUILD` bump, rebuild `make check` for the new remix; it prints `[SKIP]` for checks that need the
  emulator or a project fixture. That is normal on his Mac.

## Build recipe (the usual way)

```bash
BASE="/Users/jacopofresia/Documents/ModularStuff/Octatrack Alternrative Firmware"
cd "$BASE/octabam-2.11"
# remixes/jack-mix-N/remix.py + README.md, then the selftest entry:
python3 - <<'EOF'
import re
p = "tools/remix/selftest.py"; s = open(p).read()
s = re.sub(r'"jack-mix-N": \(\), ', '', s)
a = '_want = {"mods": (), '
assert s.count(a) == 1, "selftest anchor not found"
s = s.replace(a, a + '"jack-mix-N": (), ')   # () = nothing given up
open(p, "w").write(s)
EOF
python3 tools/remix/index.py --write
set -o pipefail
make check REMIX=jack-mix-N 2>&1 | tee out/jack-mix-N.check.log && make image REMIX=jack-mix-N BUILD=N VERSION=OCTAJACKN
shasum -a 256 out/OCTATRACK_OCTAJACKN.bin
cp out/OCTATRACK_OCTAJACKN.bin "$BASE/octabam/out/"
```

Remix template (jack-mix-16 content): `modules=("SYNTH MACHINE", "SCALE QUANTIZER", "TUNER", "USB MIDI",
"USB AUDIO OUT TRACKS MAIN CUE", <the 14 stock effects>)`, `fallback="NONE"`, `family="mods"`,
`proof=Proof.PORT`. Bump Tim's modules with, in each of `modules/{synth,quantizer,tuner}/upstream`:
`git fetch origin <sha>; git checkout <sha>`.

Flash: copy `.bin` to the CF card root, PROJECT > OS UPGRADE > YES, check OS VERSION. Always back up the card;
the previous `.bin` in `out/` is the way back. Recovery is the startup menu plus MIDI via 5-pin DIN.

## Verifying an image without building

- `python3 tools/build/bin_decode.py file.bin -o decoded.bin` prints whether the checksum is valid.
  In the decoded file the version field is bytes 12..22 (e.g. `OCTAJACK16`).
- A sandbox build of his BUILD 8 matched his own file **byte for byte**, so the same inputs and toolchain
  (binutils 2.47 `m68k-elf`) reproduce the same image. A matching sha256 is real evidence.

## Local edits

**None right now.** Until Tim's v2.13 the quantizer needed a one-line patch (the MIDI-track CHROMATIC freeze):
the `qz_octnum` detour at `0x400449b8` displaced 8 bytes, but stock's MIDI branch at `0x400449b6` jumps to
`0x400449be`, into the middle of them. That skipped a stack push and crashed (illegal instruction, vector 4,
at `0x400bf124`). Tim fixed it in v2.13 by moving the hook to `0x400449be` (Modwerk #264). If you ever
go back to v2.9-v2.12, re-apply: `H("2039460d16fc" "2f00")` -> `H("2039460d16fc")` and drop `pad_to=8`.

## Known issues and open questions

- **Possible USB freeze (unconfirmed for Jack).** A briefing (`CF_METER_for_USB_freeze.md`, keep it in the repo)
  describes a 20-channel USB audio build that degrades then freezes while a host records the stream, worse with
  many synth voices. Frame interrupt budget is 362.8 us; another tester's MKII measured ~16.5 us per stock voice and
  20-out USB costing ~27-50 us per frame more than 4-out. SYNTH MACHINE renders in the frame interrupt, so overrun is
  plausible. **Ask Jack whether he actually sees freezes and on which build.** Options: (A) a build with the
  16-channel USB module, (B) CF METER + CF METER IDLE measured on his unit (analog capture of T8/cue, decode with
  `python3 tools/harness/cfmeter.py take.wav --lr 0,1 --analog`, needs DSP tools at current pins, best built on his
  Mac), (C) emulator instruction counts (not hardware proof). It composes on paper with his set (no ledger clash),
  never built.
- Earlier I told him the extra USB channels left "plenty of room"; that was an estimate and the briefing's
  measurements suggest less headroom.
- Earlier builds glitched with CHARACTER + MINIVERB on all 8 tracks while streaming USB multitrack.
- Double clock: if Ableton sends MIDI clock over both DIN (via his RME) and USB, the sequencer runs at double speed.
  Keep clock Sync on one output only.
- **SY DRUM** (Tim v2.11+): never run on hardware by its author; Jack's unit misbehaved. Skip until Tim reports hardware results.
- His MK1 has no FUNC + SRC for the machine list. Use: press the track key twice quickly, LEFT on `<< MACHINE`,
  DOWN to the machine, YES.
- Not verified on hardware: v2.12-v2.14 behavior, SCALE on MIDI tracks (v2.13), the USB MIDI replug fix.
- Tim's synth v2.9+ notes: LFO 3 on a synth track is the VOIC / CHRD slot; LEG in AMP SETUP; chord recording;
  FUNC + UP/DOWN with a trig held in GRID RECORDING moves the step an octave; `SYNTH*.wav` marker files should
  still work (per README, not tested).

## Why some things are not in his build

- **ANALOG BD beside SYNTH MACHINE:** both claim the FLEX renderer pointer `0x400d6438` and overlap at the
  machine-chooser commit (`0x40079816` vs `0x4007981c`). A local bridge was built and tested in the emulator, but
  Jack rejected it as too many tricks. Wait for an upstream shared registry.
- **CHARACTER on current octabam:** KEY/KLVL made it a bus client that forces SEND, which clashes with PLATE REV.
  The pre-KEY Character (commit `9dd8107~1`) is code-identical to what he ran. Later main has a separate
  CHARACTER TXTR module (not tested by me).
- **Newest octabam (15 Oct 2026, `2d1cbcf`)** merged the USB audio modules into one `usb-audio-out` module with
  layouts chosen through a new settings store (BRAIN). `USB AUDIO OUT TRACKS MAIN CUE` no longer exists there, so the
  remix must be rewritten. Not done.

## Watch list

Tim's repo (new tags), octabam main, Lukas Paul's OCTABAM V6 modules (USB GAIN, VELOCITY, PROJECT TEMPLATE; no public
code as of 10 Oct), a shared registry for ANALOG BD, USB AUDIO IN (he declined for now). Idea only, nothing decided:
a random-trigger generator on the MIDI track CTRL1 page (two knobs plus a push, modelled on a Digitone feature).
Check: the stock effect harvest rule (a kept effect may call routines inside a given-up effect's DSP code) if he
ever drops Dark Rev while keeping Plate Rev.

## Testing notes (emulator)

- Tools: `tools/emu/ot_emu` (needs `make emu-setup`; his Mac probably skips these checks), `tools/verify/*`.
- False alarms seen with a big runtime (SY DRUM, 292 KB): the emulator's stall detector
  (`g_stallBursts = 4` x 500,000 instructions in `machine.h`) flags the loader's hash loop as "unrecognised spin",
  and several USB gates run out of their default 50M instruction budget. These are test-tool limits, not firmware faults.
- `make verify-shared` stops at the knob-click census if the vendored DSP assembler is older than the pin; rebuild with
  `rm -rf vendor/dsp56300/build && make setup`.
- Machine-list key codes for scripts: track keys `0x10..0x17`, LEFT `0x34`, DOWN `0x20`, YES `0x31`, NO `0x32`,
  FUNCTION `0x2d`, MIDI `0x35`, page keys `0x22..0x26`, PLAY `0x28`, STOP `0x27` (octabam `docs/firmware/PANEL.md`).
