"""jack-mix-15 -- jack-mix-14 plus SY DRUM (Tim v2.11) beside SYNTH MACHINE."""
from remix.schema import Proof, Remix
REMIX = Remix(
    name="jack-mix-15", family="mods", proof=Proof.PORT,
    proof_note="not yet run as one image",
    doc="SYNTH MACHINE + SY DRUM + SCALE QUANTIZER + TUNER (Tim v2.11) + USB MIDI + USB AUDIO OUT TRACKS MAIN CUE; all 14 stock effects.",
    modules=("SYNTH MACHINE", "SY DRUM", "SCALE QUANTIZER", "TUNER", "USB MIDI", "USB AUDIO OUT TRACKS MAIN CUE",
             "FILTER", "EQUALIZER", "PHASER", "COMPRESSOR", "DELAY", "PLATE REV", "SPRING REV", "DARK REV",
             "SPATIALIZER", "FLANGER", "CHORUS", "LO-FI", "DJ EQ", "COMB FILTER"),
    fallback="NONE",
)
