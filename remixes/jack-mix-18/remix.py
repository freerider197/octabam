"""jack-mix-18 -- lean: SYNTH MACHINE + SCALE QUANTIZER + TUNER (Tim v2.22) + USB (TRACKS PRE, MAIN, CUE, MIDI; 20 ch) + MUTE_MODES, all 14 stock effects."""
from remix.schema import Proof, Remix
REMIX = Remix(
    name="jack-mix-18", family="mods", proof=Proof.PORT,
    proof_note="not yet run as one image",
    doc="SYNTH MACHINE + SCALE QUANTIZER + TUNER (Tim v2.22) + USB at TRACKS MAIN CUE (20 ch) + MUTE_MODES; all 14 stock effects.",
    modules=("SYNTH MACHINE", "SCALE QUANTIZER", "TUNER", "USB", "MUTE_MODES",
             "FILTER", "EQUALIZER", "PHASER", "COMPRESSOR", "DELAY", "PLATE REV", "SPRING REV", "DARK REV",
             "SPATIALIZER", "FLANGER", "CHORUS", "LO-FI", "DJ EQ", "COMB FILTER"),
    fallback="NONE",
    settings={("octabam.usb", "TRACKS"): "PRE", ("octabam.usb", "MAIN"): 1,
              ("octabam.usb", "CUE"): 1, ("octabam.usb", "MASTER"): 0,
              ("octabam.usb", "IN"): "OFF"},
)
