"""
گام ۳ اختیاری — ML خیلی کوچک روی همان منحنی.

این جایگزینی برای فهم فیزیک گام ۲ نیست.
اگر ویژگی‌ها را نفهمیدی، فایل را ببند و به المپیاد برگرد.

    python 03_optional_ml.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

try:
    import lightkurve as lk
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
except ImportError as exc:
    raise SystemExit(
        "به lightkurve و scikit-learn نیاز است:\n"
        "  pip install -r requirements.txt"
    ) from exc

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

WINDOW = 48  # حدود 48 * 2 دقیقه ≈ 1.6 ساعت
SEED = 18


def windows(flux: np.ndarray, period_in_cadences: int, t0_index: int):
    """پنجره‌هایی روی منحنی می‌برد. برچسب ۱ اگر مرکز پنجره نزدیک ترانزیت تکرارشونده باشد."""
    n = len(flux)
    xs = []
    ys = []
    step = WINDOW // 2
    for start in range(0, n - WINDOW, step):
        chunk = flux[start : start + WINDOW]
        if np.any(~np.isfinite(chunk)):
            continue
        center = start + WINDOW // 2
        # فاصله تا نزدیک‌ترین ترانزیت فرضی با دورهٔ period_in_cadences
        dist = abs((center - t0_index) % period_in_cadences)
        dist = min(dist, period_in_cadences - dist)
        label = 1 if dist < WINDOW // 3 else 0
        feat = [
            float(np.mean(chunk)),
            float(np.std(chunk)),
            float(np.min(chunk)),
            float(np.median(chunk) - np.min(chunk)),
            float(np.percentile(chunk, 10)),
        ]
        xs.append(feat)
        ys.append(label)
    return np.array(xs), np.array(ys)


def main() -> None:
    search = lk.search_lightcurve("WASP-18", mission="TESS", author="SPOC", exptime=120)
    lc = search[0].download().remove_nans().normalize().flatten(window_length=1001)
    flux = np.array(lc.flux.value, dtype=float)
    time = np.array(lc.time.value, dtype=float)

    bls = lc.to_periodogram(method="bls", minimum_period=0.4, maximum_period=2.5)
    period_days = float(bls.period_at_max_power.value)
    t0 = float(bls.transit_time_at_max_power.value)

    dt = np.median(np.diff(time))
    period_cad = max(int(round(period_days / dt)), WINDOW + 1)
    t0_index = int(np.argmin(np.abs(time - t0)))

    x, y = windows(flux, period_cad, t0_index)
    if y.sum() < 10 or (len(y) - y.sum()) < 10:
        raise SystemExit("برچسب‌ها خیلی نامتوازن شد؛ اول گام ۲ را درست تمام کن.")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=SEED, stratify=y
    )
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    clf = LogisticRegression(max_iter=500, class_weight="balanced")
    clf.fit(x_train, y_train)
    pred = clf.predict(x_test)
    report = classification_report(y_test, pred, digits=3)
    print(report)
    print("ضریب ویژگی‌ها [mean, std, min, median-min, p10]:")
    print(clf.coef_)

    (OUT / "03_ml_report.txt").write_text(
        "این مدل فیزیک مدار را یاد نگرفته؛ فقط الگوی فرورفتگی را در پنجره می‌بیند.\n\n"
        + report
        + "\ncoefficients = "
        + str(clf.coef_)
        + "\n",
        encoding="utf-8",
    )
    print("نوشته شد:", OUT / "03_ml_report.txt")
    print("اگر فقط accuracy بالا دیدی ولی ویژگی‌ها بی‌معنی‌اند، این گام را تمام‌شده حساب نکن.")


if __name__ == "__main__":
    main()
