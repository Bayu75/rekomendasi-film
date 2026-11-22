/* navbar.js – perilaku navbar (pemilik: Frontend A) */
(function () {
  "use strict";
  var header = document.getElementById("site-navbar");
  if (!header) return;

  // 1. Scroll
  var solid = (header.getAttribute("data-solid") || "").split(/\s+/).filter(Boolean);
  if (!header.hasAttribute("data-always-solid")) {
    var onScroll = function () {
      var on = window.scrollY > 16;
      solid.forEach(function (c) { header.classList.toggle(c, on); });
      header.classList.toggle("bg-transparent", !on);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // 2. Menu mobile
  var toggle = header.querySelector("[data-mobile-toggle]");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.hasAttribute("hidden");
      menu.toggleAttribute("hidden", !open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Tutup menu" : "Buka menu");
      toggle.querySelector("[data-icon-open]").classList.toggle("hidden", open);
      toggle.querySelector("[data-icon-close]").classList.toggle("hidden", !open);
    });
  }

  // 3. Dropdown pengguna
  var userMenu = header.querySelector("[data-user-menu]");
  if (userMenu) {
    var btn = userMenu.querySelector("[data-user-menu-button]");
    var panel = userMenu.querySelector("[data-user-menu-panel]");
    var caret = userMenu.querySelector("[data-user-menu-caret]");
    var setOpen = function (open) {
      panel.toggleAttribute("hidden", !open);
      btn.setAttribute("aria-expanded", String(open));
      if (caret) caret.classList.toggle("rotate-180", open);
    };
    btn.addEventListener("click", function () { setOpen(panel.hasAttribute("hidden")); });
    document.addEventListener("mousedown", function (e) {
      if (!userMenu.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // 4. Kotak cari kecil
  var openBtn = header.querySelector("[data-search-open]");
  var form = header.querySelector("[data-search-form]");
  if (openBtn && form) {
    var input = form.querySelector("input[name=q]");
    var closeBtn = form.querySelector("[data-search-close]");
    var showForm = function (show) {
      form.toggleAttribute("hidden", !show);
      openBtn.classList.toggle("sm:flex", !show);
      if (show) input.focus(); else input.value = "";
    };
    openBtn.addEventListener("click", function (e) { e.preventDefault(); showForm(true); });
    closeBtn.addEventListener("click", function () { showForm(false); });
    form.addEventListener("submit", function (e) {
      input.value = input.value.trim();
      if (!input.value) e.preventDefault();
    });
  }
})();