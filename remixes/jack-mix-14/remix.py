"""jack-mix-14 -- lean: SYNTH MACHINE + SCALE QUANTIZER + TUNER (Tim v2.11) + USB MIDI + USB AUDIO OUT TRACKS MAIN CUE, all 14 stock effects."""
from remix.schema import Proof, Remix
REMIX = Remix(
    name="jack-mix-14", family="mods", proof=Proof.PORT,
    proof_note="not yet run as one image",
    doc="SYNTH MACHINE + SCALE QUANTIZER + TUNER (Tim v2.11) + USB MIDI + USB AUDIO OUT TRACKS MAIN CUE; all 14 stock effects.",
    modules=("SYNTH MACHINE", "SCALE QUANTIZER", "TUNER", "USB MIDI", "USB AUDIO OUT TRACKS MAIN CUE",
             "FILTER", "EQUALIZER", "PHASER", "COMPRESSOR", "DELAY", "PLATE REV", "SPRING REV", "DARK REV",
             "SPATIALIZER", "FLANGER", "CHORUS", "LO-FI", "DJ EQ", "COMB FILTER"),
    fallback="NONE",
)
