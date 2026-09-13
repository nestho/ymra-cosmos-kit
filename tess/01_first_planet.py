"""
گام ۱ — اولین منحنی نوری از دادهٔ ناسا.

هدف اصلی: WASP-18 (TESS / SPOC)
پشتیبان:   Kepler-8 (Kepler pipeline)

اجرا از پوشهٔ tess:

    python 01_first_planet.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import lightkurve as lk
except ImportError as exc:
    raise SystemExit(
        "lightkurve نصب نیست. اول README را بخوان:\n"
        "  python -m venv .venv\n"
        "  .venv را activate کن\n"
        "  pip install -r requirements.txt"
    ) from exc

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def save_plot(lc, png_path: Path, title: str) -> None:
    ax = lc.plot()
    ax.set_title(title)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(png_path, dpi=140)
    plt.close(fig)
    print(f"نمودار ذخیره شد: {png_path}")


def try_wasp18():
    print("جستجو در MAST: WASP-18 / TESS / SPOC …")
    search = lk.search_lightcurve(
        "WASP-18",
        mission="TESS",
        author="SPOC",
        exptime=120,
    )
    print(search)
    if len(search) == 0:
        raise RuntimeError("برای WASP-18 منحنی SPOC پیدا نشد.")
    lc = search[0].download()
    if lc is None:
        raise RuntimeError("دانلود WASP-18 خالی برگشت.")
    lc = lc.remove_nans()
    png = OUT / "01_wasp18_raw.png"
    save_plot(lc, png, "WASP-18 — TESS PDCSAP (raw)")
    return lc


def try_kepler8():
    print("پشتیبان: Kepler-8 / Kepler long cadence …")
    search = lk.search_lightcurve(
        "Kepler-8",
        mission="Kepler",
        author="Kepler",
        cadence="long",
        quarter=4,
    )
    print(search)
    if len(search) == 0:
        raise RuntimeError("برای Kepler-8 هم داده پیدا نشد.")
    lc = search.download()
    if lc is None:
        raise RuntimeError("دانلود Kepler-8 خالی برگشت.")
    lc = lc.remove_nans()
    png = OUT / "01_kepler8_raw.png"
    save_plot(lc, png, "Kepler-8 — Kepler Q4 PDCSAP (raw)")
    return lc


def main() -> None:
    print("Lightkurve", lk.__version__)
    print("خروجی:", OUT)
    try:
        lc = try_wasp18()
        target = "WASP-18"
    except Exception as err:
        print("WASP-18 نشد:", err)
        print("سراغ پشتیبان می‌روم.")
        lc = try_kepler8()
        target = "Kepler-8"

    print()
    print("هدف:", target)
    print("تعداد نقطه:", len(lc))
    print("ستون‌های جدول:", lc.colnames)
    flux_col = "pdcsap_flux" if "pdcsap_flux" in lc.colnames else "flux"
    print("ستون شار مورد استفاده در plot پیش‌فرض Lightkurve معمولاً PDCSAP است.")
    print()
    print("موفقیت گام ۱: یک PNG در tess/output/")
    print("حالا notes.md را بخوان: این نقاط نور ستاره در زمان‌اند.")
    print("اگر فرورفتگی‌های منظم دیدی، همان ترانزیت است — در گام ۲ دقیق می‌شود.")
    _ = flux_col


if __name__ == "__main__":
    main()
