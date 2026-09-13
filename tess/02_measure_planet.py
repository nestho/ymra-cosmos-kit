"""
گام ۲ — flatten، جستجوی دوره (BLS)، fold، تخمین شعاع.

پیش‌فرض: WASP-18. دورهٔ مورد انتظار حدود 0.94 روز است.
اگر هارمونیک گرفتی (0.47 یا 1.88) در notes.md بخوان چرا.

    python 02_measure_planet.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    import lightkurve as lk
except ImportError as exc:
    raise SystemExit("lightkurve نصب نیست. README را بخوان.") from exc

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

# WASP-18: شعاع ستاره حدود 1.23 R_sun (مرجع کاتالوگ؛ خودت چک کن)
# منبع مقایسه بعد از حساب خودت:
# https://exoplanets.nasa.gov/exoplanet-catalog/2105/wasp-18-b/
R_STAR_RSUN = 1.23
R_SUN_TO_R_JUP = 9.731
R_JUP_TO_R_EARTH = 11.21

# دورهٔ شناخته‌شده فقط برای محدودهٔ جستجو، نه برای تقلب در جواب
P_HINT_DAY = 0.941


def save(ax, path: Path) -> None:
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    print("ذخیره:", path)


def download_target():
    search = lk.search_lightcurve(
        "WASP-18",
        mission="TESS",
        author="SPOC",
        exptime=120,
    )
    print(search)
    if len(search) == 0:
        raise SystemExit("WASP-18 پیدا نشد. اول 01_first_planet.py را اجرا کن.")
    lc = search[0].download()
    if lc is None:
        raise SystemExit("دانلود خالی بود.")
    return lc.remove_nans()


def main() -> None:
    lc = download_target()
    # شار نرمال‌شده کار را برای عمق راحت می‌کند
    lc = lc.normalize()

    ax = lc.plot()
    ax.set_title("WASP-18 normalized")
    save(ax, OUT / "02_normalized.png")

    # window_length باید از مدت ترانزیت بزرگ‌تر باشد و از فاصلهٔ بین ترانزیت‌ها کوچک‌تر
    flat = lc.flatten(window_length=1001)
    ax = flat.plot()
    ax.set_title("flattened — روند آهسته حذف شده")
    save(ax, OUT / "02_flat.png")

    # جستجوی دوره نزدیک مقدار فیزیکی معقول برای این هدف
    min_p = 0.4
    max_p = 2.5
    print(f"BLS روی بازهٔ {min_p} تا {max_p} روز …")
    bls = flat.to_periodogram(method="bls", minimum_period=min_p, maximum_period=max_p)
    ax = bls.plot()
    ax.set_title("BLS periodogram")
    save(ax, OUT / "02_periodogram.png")

    period = bls.period_at_max_power
    t0 = bls.transit_time_at_max_power
    duration = bls.duration_at_max_power
    print("دوره در اوج توان:", period)
    print("t0:", t0)
    print("مدت ترانزیت:", duration)

    folded = flat.fold(period=period, epoch_time=t0)
    ax = folded.scatter()
    ax.set_title(f"folded at P = {period}")
    save(ax, OUT / "02_folded.png")

    # تخمین عمق: اختلاف میانهٔ خارج ترانزیت و داخل ترانزیت
    phase = np.array(folded.phase.value)
    flux = np.array(folded.flux.value)
    # فاز Lightkurve معمولاً حدود -0.5 تا 0.5 است؛ مرکز ترانزیت نزدیک 0
    dur_phase = float(duration.value) / float(period.value)
    in_tr = np.abs(phase) < max(dur_phase, 0.02)
    out_tr = np.abs(phase) > max(1.5 * dur_phase, 0.06)
    if in_tr.sum() < 10 or out_tr.sum() < 10:
        depth = float(np.nanmedian(np.array(bls.depth_at_max_power)))
        print("نمونه برای عمق کم بود؛ از bls.depth_at_max_power استفاده شد.")
    else:
        depth = float(np.median(flux[out_tr]) - np.median(flux[in_tr]))

    depth = abs(depth)
    rp_over_rs = float(np.sqrt(depth)) if depth > 0 else float("nan")
    rp_rjup = rp_over_rs * R_STAR_RSUN * R_SUN_TO_R_JUP
    rp_rearth = rp_rjup * R_JUP_TO_R_EARTH

    lines = [
        f"period_days = {float(period.value):.6f}",
        f"bls_hint_catalog_days ≈ {P_HINT_DAY}",
        f"duration_days = {float(duration.value):.6f}",
        f"depth_delta_flux = {depth:.6f}",
        f"Rp_over_Rstar = {rp_over_rs:.4f}",
        f"assumed_Rstar_Rsun = {R_STAR_RSUN}",
        f"Rp_Rjup ≈ {rp_rjup:.3f}",
        f"Rp_Rearth ≈ {rp_rearth:.2f}",
        "",
        "اگر period حدود 0.94 روز است، مسیر درست است.",
        "اگر حدود 0.47 یا 1.88 است، هارمونیک است — notes.md",
        "عدد کاتالوگ را فقط بعد از این فایل نگاه کن.",
        "https://exoplanets.nasa.gov/exoplanet-catalog/2105/wasp-18-b/",
    ]
    text = "\n".join(lines) + "\n"
    (OUT / "02_numbers.txt").write_text(text, encoding="utf-8")
    print()
    print(text)
    print("موفقیت گام ۲: چهار تصویر + 02_numbers.txt")
    print("حالا tess/REPORT.md را به زبان خودت بنویس.")


if __name__ == "__main__":
    main()
