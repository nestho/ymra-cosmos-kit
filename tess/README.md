<div dir="rtl" lang="fa">

# پروژهٔ TESS — پیدا کردن یک سیاره با دادهٔ ناسا

این پروژه کورس نیست. یک کار واقعی است: دادهٔ تلسکوپ فضایی **TESS** را از بایگانی ناسا می‌گیری و وجود سیاره را از روی کم‌نور شدن ستاره می‌سنجی.

هدف اول: ستارهٔ **WASP-18**. سیاره‌اش یک مشتری داغ با دورهٔ حدود **۰.۹۴ روز** است. فرورفتگی‌اش عمیق و واضح است؛ برای بار اول مناسب است.

اگر اینترنت یا MAST گیر داد، اسکریپت به‌طور خودکار سراغ **Kepler-8** می‌رود (آموزش کلاسیک Lightkurve).

---

## چرا این پروژه؟

- داده مال ناسا است، شهروندی نمی‌خواهد
- پایتونی که بلدی این‌جا علمی می‌شود
- فیزیک کپلر و قدر که برای المپیاد می‌خوانی این‌جا عدد می‌شود
- خروجی‌اش روی GitHub برای پرونده می‌ماند

قانون: کد را **خودت اجرا کن**. اگر خطا دیدی، اول متن خطا را بخوان. هوش مصنوعی را برای «کل پروژه را بنویس» باز نکن.

---

## پیش‌نیاز

- Python 3.10 یا جدیدتر: [python.org/downloads](https://www.python.org/downloads/)
- اینترنت برای دانلود منحنی نوری از [MAST](https://mast.stsci.edu/)
- حدود ۲۰۰–۴۰۰ مگ فضای دیسک برای اولین دانلود (بعداً کش می‌شود)

Windows: موقع نصب Python تیک **Add python to PATH** را بزن.

---

## نصب — گام به گام

در ترمینال، از ریشهٔ ریپو:

```bash
cd tess
python -m venv .venv
```

فعال کردن محیط:

- Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
- Windows (cmd): `.\.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

بعد:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

اگر `python` کار نکرد، `python3` را امتحان کن.

تست نصب:

```bash
python -c "import lightkurve as lk; print(lk.__version__)"
```

باید یک شماره نسخه چاپ شود.

مستندات بسته: [Lightkurve](https://lightkurve.github.io/lightkurve/)

---

## فیزیک را قبل از کد بخوان

فایل [notes.md](notes.md) را بخوان. سه ایده:

1. **ترانزیت:** سیاره از جلوی ستاره رد می‌شود → نور کمی کم می‌شود
2. **دوره \(P\):** فاصلهٔ زمانی بین دو کم‌نور شدن = دورهٔ مدار
3. **عمق:** \(\Delta F / F \approx (R_p / R_\star)^2\) → از روی عمق، نسبت شعاع درمی‌آید

اگر این سه را نفهمی، اسکریپت فقط دکمه است.

---

## گام ۱ — اولین نمودار (هفتهٔ ۲ مهر)

```bash
python 01_first_planet.py
```

باید:

1. در MAST دنبال WASP-18 بگردد (ماموریت TESS، نویسندهٔ SPOC = خط لولهٔ رسمی ناسا)
2. یک بخش (sector) را دانلود کند
3. نمودار را در `output/01_wasp18_raw.png` ذخیره کند

**موفقیت یعنی:** یک فایل PNG می‌بینی که محور افقی زمان است و محور عمودی شار نور. ممکن است نقاط پراکنده باشد. اشکال ندارد.

اگر دانلود شکست خورد، اسکریپت Kepler-8 را امتحان می‌کند و در `output/01_kepler8_raw.png` می‌نویسد. آن هم دادهٔ ناسا است.

### اگر خطا دیدی

| پیام | یعنی | چه کار کن |
|---|---|---|
| `No module named lightkurve` | محیط فعال نیست یا نصب نشده | venv را activate کن، دوباره pip |
| `Timeout` / `Connection` | اینترنت / فیلتر | VPN یا بعداً دوباره |
| `No data found` | نام هدف یا MAST | اسکریپت خودش fallback دارد؛ خروجی را بخوان |
| خیلی کند | دانلود بار اول | صبر کن؛ بار بعد از کش می‌آید |

آموزش رسمی جستجو: [search_lightcurve](https://lightkurve.github.io/lightkurve/reference/api/lightkurve.search_lightcurve.html)

---

## گام ۲ — دوره و شعاع (هفته‌های ۵–۷ آبان)

```bash
python 02_measure_planet.py
```

ترتیب داخل کد (باید در خروجی و کامنت‌ها ببینی، حفظ نکن):

1. حذف NaN
2. `flatten` — روند آهستهٔ ستاره را درمی‌آورد تا ترانزیت بماند
3. **BLS periodogram** — دوره‌هایی را جستجو می‌کند که «جعبهٔ کم‌نور شدن» تکرار شود
4. `fold` — همهٔ ترانزیت‌ها را روی هم می‌اندازد
5. عمق متوسط → نسبت شعاع
6. با قانون کپلر، اگر جرم ستاره را بدانی، تقریبی از \(a\) 

خروجی‌ها:

- `output/02_flat.png`
- `output/02_periodogram.png`
- `output/02_folded.png`
- `output/02_numbers.txt`

برای WASP-18 دوره باید **نزدیک ۰.۹۴ روز** دربیاید. اگر ۲ برابر یا نصف شد، هارمونیک است — در notes بخوان چرا.

مرجع مقایسه (بعد از حساب خودت، نه قبل):

- [NASA Exoplanet Catalog — WASP-18 b](https://exoplanets.nasa.gov/exoplanet-catalog/2105/wasp-18-b/)
- یا جستجو در [exoplanetarchive.ipac.caltech.edu](https://exoplanetarchive.ipac.caltech.edu/)

اختلاف ۱۰–۲۰٪ برای این روش ساده طبیعی است. تقلب نیست؛ مدل ما جعبهٔ ساده است نه fit حرفه‌ای.

آموزش BLS در Lightkurve: بخش science examples در [tutorials](https://lightkurve.github.io/lightkurve/tutorials/)

---

## گام ۳ — ML اختیاری (فقط بعد از گزارش)

```bash
python 03_optional_ml.py
```

یک طبقه‌بندی خیلی ساده: پنجره‌های زمانی «ترانزیت دارد / ندارد» با ویژگی‌های آماری، بعد یک مدل کوچک scikit-learn.

هدف این نیست که مقاله بدهی. هدف این است که بفهمی ML دورهٔ استنفورد روی دادهٔ واقعی نجوم یعنی چه. اگر دقت بالا آمد ولی ویژگی‌ها را نفهمیدی، اسکریپت را کنار بگذار.

---

## گزارش — قالب اجباری

فایل `tess/REPORT.md` را خودت بساز. بدون هوش مصنوعی. به فارسی.

```markdown
# گزارش WASP-18

## چه دیدم
(نمودار خام چه شکلی بود؟)

## دوره
عدد من: ... روز
عدد مرجع: ... روز
اختلاف: ...

## عمق ترانزیت و شعاع
عمق ≈ ...
R_p / R_star ≈ ...
اگر شعاع ستاره را X فرض کنم، شعاع سیاره ≈ ...

## چه چیزی را نفهمیدم
(صادق باش)

## بعد چه می‌کنم
```

وقتی این فایل را نوشتی، پروژه برای کلاس دهم **تمام** است.

---

## هدف دوم (اختیاری)

`Pi Mensae` — کشف معروف TESS. دورهٔ سیارهٔ b حدود ۶.۲۷ روز، کم‌عمق‌تر، سخت‌تر.

```python
search = lk.search_lightcurve("Pi Mensae", mission="TESS", author="SPOC", exptime=120)
```

مقالهٔ کشف: Huang et al. 2018. آموزش ناسا گاهی از همین هدف استفاده می‌کند.

---

## منابع همین پروژه

- [Lightkurve docs](https://lightkurve.github.io/lightkurve/)
- [TESS mission](https://heasarc.gsfc.nasa.gov/docs/tess/)
- [MAST](https://mast.stsci.edu/)
- [What is a transit? — NASA](https://exoplanets.nasa.gov/alien-worlds/ways-to-find-a-planet/#/2)
- [WASP-18 b — NASA catalog](https://exoplanets.nasa.gov/exoplanet-catalog/2105/wasp-18-b/)
</div>
