from NostalgiaForInfinityX import NostalgiaForInfinityX


class NostalgiaForInfinityXLongOnly(NostalgiaForInfinityX):
    """Long-only variant of NostalgiaForInfinityX."""

    can_short = False
    optimize_side = 'long'
    enable_short_entries = False
