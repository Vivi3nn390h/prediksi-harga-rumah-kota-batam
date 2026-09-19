"""
Formatting helpers and utility functions.
"""

def format_rupiah(amount: float) -> str:
    """
    Formats a numeric amount into standard Indonesian Rupiah currency string.
    Example: 1250000000 -> "Rp 1.250.000.000"
    """
    val = int(round(amount))
    if val < 0:
        val = 0
    formatted = f"{val:,}".replace(",", ".")
    return f"Rp {formatted}"


def format_rupiah_short(amount: float) -> str:
    """
    Formats a numeric amount into a compact Indonesian text format.
    Example: 1250000000 -> "1,25 Miliar"
    """
    val = float(amount)
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f}".replace(".", ",") + " Miliar"
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.1f}".replace(".", ",") + " Juta"
    elif val >= 1_000:
        return f"{val / 1_000:.0f}".replace(".", ",") + " Ribu"
    else:
        return f"{val:.0f}"
