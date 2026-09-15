const NAV = [
  {
    label: "شروع",
    items: [
      { id: "home", title: "خانه", icon: "home" },
      { id: "how", title: "با هم برنامه بریزیم", icon: "users" },
      { id: "path", title: "مسیر واقعی", icon: "compass" },
      { id: "stanford", title: "بعد از استنفورد", icon: "book" },
    ],
  },
  {
    label: "یادگیری",
    items: [
      { id: "olympiad", title: "المپیاد", icon: "star" },
      { id: "roadmap", title: "نقشه ۴ ماهه", icon: "cal" },
      { id: "weekly", title: "برنامه هفته", icon: "clock" },
      { id: "math", title: "ریاضی", icon: "sigma" },
      { id: "algo", title: "الگوریتم", icon: "code" },
    ],
  },
  {
    label: "کار واقعی",
    items: [
      { id: "tess", title: "پروژه TESS", icon: "planet" },
      { id: "nasa", title: "ناسا و CERN", icon: "sat" },
      { id: "links", title: "منابع و لینک‌ها", icon: "link" },
    ],
  },
  {
    label: "پیگیری",
    items: [
      { id: "progress", title: "پیشرفت", icon: "check" },
      { id: "portfolio", title: "پرونده و آینده", icon: "bag" },
    ],
  },
];

const FLAT = NAV.flatMap((g) => g.items);

const ICONS = {
  home: '<path d="M4 11.5 12 4l8 7.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1v-8.5Z"/>',
  users: '<circle cx="9" cy="8" r="3"/><circle cx="16" cy="9" r="2.4"/><path d="M4 19c.4-3 2.4-5 5-5s4.6 2 5 5M14 19c.2-2 1.3-3.5 3.2-4"/>',
  compass: '<circle cx="12" cy="12" r="9"/><path d="m9 15 1.8-5.2L16 8l-1.8 5.2L9 15Z"/>',
  book: '<path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H19v16H7.5A2.5 2.5 0 0 0 5 21.5V5.5Z"/><path d="M5 19.2A2.5 2.5 0 0 1 7.5 17H19"/>',
  star: '<path d="m12 3 2.3 6.2H21l-5.2 3.8 2 6.2L12 15.8 6.2 19.2l2-6.2L3 9.2h6.7L12 3Z"/>',
  cal: '<rect x="4" y="6" width="16" height="14" rx="2"/><path d="M8 4v4M16 4v4M4 11h16"/>',
  clock: '<circle cx="12" cy="12" r="8"/><path d="M12 8v4.5l3 1.5"/>',
  sigma: '<path d="M6 5h12L10 12l8 7H6"/>',
  code: '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13 6l-2 12"/>',
  planet: '<circle cx="12" cy="12" r="4"/><ellipse cx="12" cy="12" rx="10" ry="4"/>',
  sat: '<path d="m6 14 4 4M14 6l4 4M9 15l6-6M8 8l2-2 8 8-2 2-8-8Z"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.5.1l1.4-1.4a5 5 0 0 0-7-7L10.5 6M14 11a5 5 0 0 0-7.5-.1L7 12.3a5 5 0 0 0 7 7L15.5 18"/>',
  check: '<path d="M5 13.5 9.2 18 19 7"/>',
  bag: '<path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8V6.5A3 3 0 0 1 12 3.5 3 3 0 0 1 15 6.5V8"/>',
};

const RING = 2 * Math.PI * 15.5;
const KEY = "ymra-progress-v1";

function icon(name) {
  return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round">${ICONS[name] || ""}</svg>`;
}

function renderNav(active) {
  const root = document.getElementById("navGroups");
  root.innerHTML = NAV.map((g) => {
    const items = g.items
      .map((it) => {
        const cls = it.id === active ? "active" : "";
        return `<li><a class="${cls}" href="#/${it.id}">${icon(it.icon)}<span>${it.title}</span></a></li>`;
      })
      .join("");
    return `<div><div class="nav-label">${g.label}</div><ul class="nav-list">${items}</ul></div>`;
  }).join("");
}

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}");
  } catch {
    return {};
  }
}

function saveProgress(map) {
  localStorage.setItem(KEY, JSON.stringify(map));
}

function allCheckIds() {
  return (window.CHECKLIST || []).flatMap((g) => g.items.map((i) => i.id));
}

function progressStats() {
  const map = loadProgress();
  const ids = allCheckIds();
  const done = ids.filter((id) => map[id]).length;
  return { done, total: ids.length, pct: ids.length ? Math.round((done / ids.length) * 100) : 0 };
}

function bindChecks(root) {
  const map = loadProgress();
  root.querySelectorAll("input[data-check]").forEach((el) => {
    el.checked = !!map[el.dataset.check];
    el.closest(".check")?.classList.toggle("done", el.checked);
    el.addEventListener("change", () => {
      const next = loadProgress();
      next[el.dataset.check] = el.checked;
      saveProgress(next);
      el.closest(".check")?.classList.toggle("done", el.checked);
      updateProgressChrome();
    });
  });
}

function updateProgressChrome() {
  const { done, total, pct } = progressStats();
  document.querySelectorAll("[data-pct]").forEach((n) => (n.textContent = pct + "٪"));
  document.querySelectorAll("[data-done]").forEach((n) => (n.textContent = done));
  document.querySelectorAll("[data-total]").forEach((n) => (n.textContent = total));
  document.querySelectorAll(".progress-bar > span").forEach((n) => (n.style.width = pct + "%"));
  const ring = document.getElementById("ringFg");
  if (ring) ring.style.strokeDashoffset = String(RING * (1 - pct / 100));
}

function bindCopy(root) {
  root.querySelectorAll("pre").forEach((pre) => {
    if (pre.parentElement?.classList.contains("pre-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "pre-wrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(pre.innerText);
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = "Copy"), 1200);
      } catch {
        btn.textContent = "Err";
      }
    });
    wrap.appendChild(btn);
  });
}

function bindChips(root) {
  const chips = root.querySelectorAll("[data-filter]");
  if (!chips.length) return;
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const cat = chip.dataset.filter;
      chips.forEach((c) => c.classList.toggle("on", c === chip));
      root.querySelectorAll("[data-cat]").forEach((el) => {
        el.hidden = cat !== "all" && el.dataset.cat !== cat;
      });
      root.querySelectorAll("[data-cat-title]").forEach((el) => {
        el.hidden = cat !== "all" && el.dataset.catTitle !== cat;
      });
    });
  });
}

function renderPager(id) {
  const i = FLAT.findIndex((p) => p.id === id);
  const pager = document.getElementById("pager");
  if (i < 0) {
    pager.innerHTML = "";
    return;
  }
  const prev = FLAT[i - 1];
  const next = FLAT[i + 1];
  pager.innerHTML = `
    <a href="#/${prev ? prev.id : ""}" ${prev ? "" : "hidden"}><span class="pg-k">قبلی</span>${prev ? prev.title : ""}</a>
    <a class="next" href="#/${next ? next.id : ""}" ${next ? "" : "hidden"}><span class="pg-k">بعدی</span>${next ? next.title : ""}</a>
  `;
}

function closeMenu() {
  document.getElementById("nav").classList.remove("open");
  document.getElementById("scrim").classList.remove("on");
}

const TITLES = Object.fromEntries(FLAT.map((p) => [p.id, p.title]));

function currentId() {
  return (location.hash.replace(/^#\/?/, "") || "home").split("?")[0];
}

function route() {
  const id = currentId();
  const html = (window.PAGES && window.PAGES[id]) || window.PAGES.home;
  const view = document.getElementById("view");
  view.innerHTML = typeof html === "function" ? html() : html;
  const known = !!window.PAGES[id];
  renderNav(known ? id : "home");
  renderPager(known ? id : "home");
  bindChecks(view);
  bindCopy(view);
  bindChips(view);
  updateProgressChrome();
  closeMenu();
  window.scrollTo({ top: 0, behavior: "instant" });
  document.title = (TITLES[id] || "کیت کیهان") + " · کیت کیهان";
}

function searchItems() {
  const pages = FLAT.map((p) => ({
    href: `#/${p.id}`,
    title: p.title,
    hint: "صفحه",
    ext: false,
  }));
  const links = (window.SEARCH_LINKS || []).map((l) => ({
    href: l.href,
    title: l.title,
    hint: l.hint,
    ext: true,
  }));
  return pages.concat(links);
}

function openSearch() {
  const box = document.getElementById("search");
  box.hidden = false;
  const input = document.getElementById("searchInput");
  input.value = "";
  drawSearch("");
  input.focus();
}

function closeSearch() {
  document.getElementById("search").hidden = true;
}

function drawSearch(q) {
  const list = document.getElementById("searchList");
  const query = q.trim().toLowerCase();
  const items = searchItems().filter(
    (it) => !query || it.title.toLowerCase().includes(query) || (it.hint || "").toLowerCase().includes(query)
  );
  list.innerHTML =
    items
      .slice(0, 18)
      .map(
        (it, i) =>
          `<a class="search-item${i === 0 ? " active" : ""}" href="${it.href}" ${it.ext ? 'target="_blank" rel="noopener"' : ""}><b>${it.title}</b><span>${it.hint}</span></a>`
      )
      .join("") || `<div class="search-item"><b>چیزی پیدا نشد</b></div>`;
}

function paintStars() {
  const c = document.getElementById("stars");
  if (!c) return;
  const ctx = c.getContext("2d");
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const pts = Array.from({ length: 90 }, () => ({
    x: Math.random(),
    y: Math.random(),
    r: Math.random() * 1.15 + 0.2,
    a: 0.12 + Math.random() * 0.45,
  }));
  function resize() {
    c.width = innerWidth * dpr;
    c.height = innerHeight * dpr;
    c.style.width = innerWidth + "px";
    c.style.height = innerHeight + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    pts.forEach((p) => {
      ctx.beginPath();
      ctx.fillStyle = `rgba(232,236,242,${p.a})`;
      ctx.arc(p.x * innerWidth, p.y * innerHeight, p.r, 0, Math.PI * 2);
      ctx.fill();
    });
  }
  resize();
  window.addEventListener("resize", resize);
}

document.getElementById("menuBtn").addEventListener("click", () => {
  document.getElementById("nav").classList.add("open");
  document.getElementById("scrim").classList.add("on");
});
document.getElementById("scrim").addEventListener("click", closeMenu);
document.getElementById("searchBtn").addEventListener("click", openSearch);
document.getElementById("searchBtnMobile").addEventListener("click", openSearch);
document.getElementById("search").addEventListener("click", (e) => {
  if (e.target.id === "search") closeSearch();
});
document.getElementById("searchInput").addEventListener("input", (e) => drawSearch(e.target.value));
document.getElementById("searchList").addEventListener("click", (e) => {
  if (e.target.closest("a")) closeSearch();
});

window.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    const box = document.getElementById("search");
    if (box.hidden) openSearch();
    else closeSearch();
  }
  if (e.key === "Escape") {
    closeSearch();
    closeMenu();
  }
  if (document.getElementById("search").hidden === false && e.key === "Enter") {
    const first = document.querySelector(".search-item");
    if (first && first.href) {
      e.preventDefault();
      if (first.target === "_blank") window.open(first.href, "_blank", "noopener");
      else location.href = first.href;
      closeSearch();
    }
  }
});

paintStars();
window.addEventListener("hashchange", route);
route();
