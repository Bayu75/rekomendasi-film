/* auth_form.js – halaman Masuk & Daftar (pemilik: Frontend A) */
(function () {
  "use strict";

  // 1. Mata sandi
  document.querySelectorAll("[data-toggle-password]").forEach(function (btn) {
    var input = document.getElementById(btn.getAttribute("data-toggle-password"));
    if (!input) return;
    btn.addEventListener("click", function () {
      var show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.setAttribute("aria-label", show ? "Sembunyikan" : "Tampilkan");
      btn.setAttribute("aria-pressed", String(show));
      btn.querySelector("[data-eye-open]").classList.toggle("hidden", show);
      btn.querySelector("[data-eye-closed]").classList.toggle("hidden", !show);
    });
  });

  // 2. Kekuatan sandi
  function strengthOf(pw) {
    if (!pw) return null;
    if (pw.length < 6) return { level: 0, label: "Terlalu pendek", color: "bg-red-500" };
    if (pw.length < 8) return { level: 1, label: "Lemah", color: "bg-orange-500" };
    if (/[A-Z]/.test(pw) && /[0-9]/.test(pw)) return { level: 3, label: "Kuat", color: "bg-emerald-500" };
    return { level: 2, label: "Sedang", color: "bg-yellow-500" };
  }
  var BAR_COLORS = ["bg-red-500", "bg-orange-500", "bg-yellow-500", "bg-emerald-500", "bg-border"];

  var pwInput = document.querySelector("[data-strength-source]");
  var strengthBox = document.querySelector("[data-strength]");
  function renderStrength() {
    if (!pwInput || !strengthBox) return;
    var s = strengthOf(pwInput.value);
    strengthBox.toggleAttribute("hidden", !s);
    if (!s) return;
    strengthBox.querySelectorAll("[data-strength-bar]").forEach(function (bar, i) {
      BAR_COLORS.forEach(function (c) { bar.classList.remove(c); });
      bar.classList.add(i < s.level ? s.color : "bg-border");
    });
    strengthBox.querySelector("[data-strength-label]").textContent = s.label;
  }

  // 3. Konfirmasi sandi
  var CONFIRM_STATES = {
    bad: "border-red-700/60 focus-within:border-red-600/60 focus-within:ring-red-500/20",
    ok: "border-emerald-700/60 focus-within:border-emerald-600/60 focus-within:ring-emerald-500/20",
    idle: "border-border focus-within:border-primary/50 focus-within:ring-primary/20",
  };
  var confirmBox = document.querySelector("[data-confirm-box]");
  var confirmInput = document.querySelector("[data-confirm-input]");
  function renderConfirm() {
    if (!confirmBox || !confirmInput || !pwInput) return;
    var v = confirmInput.value;
    var state = !v ? "idle" : v === pwInput.value ? "ok" : "bad";
    Object.keys(CONFIRM_STATES).forEach(function (k) {
      CONFIRM_STATES[k].split(" ").forEach(function (c) { confirmBox.classList.toggle(c, k === state); });
    });
    var icon = confirmBox.querySelector("[data-confirm-icon]");
    icon.toggleAttribute("hidden", state === "idle");
    icon.querySelector("[data-confirm-ok]").classList.toggle("hidden", state !== "ok");
    icon.querySelector("[data-confirm-bad]").classList.toggle("hidden", state !== "bad");
  }

  if (pwInput) pwInput.addEventListener("input", function () { renderStrength(); renderConfirm(); });
  if (confirmInput) confirmInput.addEventListener("input", renderConfirm);
  renderStrength();
  renderConfirm();

  // 4. Cek awal + spinner
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  function val(form, name) {
    var el = form.elements[name];
    return el ? el.value : "";
  }
  function checkLogin(form) {
    if (!val(form, "email").trim() || !val(form, "password")) return "Email dan kata sandi harus diisi.";
    return null;
  }
  function checkRegister(form) {
    var name = val(form, "name"), email = val(form, "email");
    var pw = val(form, "password"), cf = val(form, "confirm_password");
    if (!name.trim() || !email.trim() || !pw || !cf) return "Semua field harus diisi.";
    if (!EMAIL_RE.test(email.trim())) return "Format email tidak valid.";
    if (pw.length < 6) return "Kata sandi minimal 6 karakter.";
    if (pw !== cf) return "Konfirmasi kata sandi tidak cocok.";
    return null;
  }

  document.querySelectorAll("form[data-auth-form]").forEach(function (form) {
    var kind = form.getAttribute("data-auth-form");
    var box = form.querySelector("[data-form-error]");
    var text = box && box.querySelector("[data-form-error-text]");
    var btn = form.querySelector("[data-submit]");

    function showError(msg) {
      if (!box) return;
      text.textContent = msg || "";
      box.toggleAttribute("hidden", !msg);
    }

    form.addEventListener("submit", function (e) {
      var err = kind === "register" ? checkRegister(form) : checkLogin(form);
      if (err) {
        e.preventDefault();
        showError(err);
        return;
      }
      showError(null);
      if (form.elements.email) form.elements.email.value = form.elements.email.value.trim();
      if (btn) {
        btn.disabled = true;
        btn.querySelector("[data-spinner]").classList.remove("hidden");
        btn.querySelector("[data-submit-label]").textContent = btn.getAttribute("data-loading-label");
      }
    });
  });

  window.addEventListener("pageshow", function (e) {
    if (!e.persisted) return;
    document.querySelectorAll("[data-submit]").forEach(function (btn) {
      btn.disabled = false;
      btn.querySelector("[data-spinner]").classList.add("hidden");
      btn.querySelector("[data-submit-label]").textContent = btn.getAttribute("data-label");
    });
  });

  // 5. Isi Otomatis (demo)
  var demo = document.querySelector("[data-fill-demo]");
  if (demo) {
    demo.addEventListener("click", function () {
      var form = document.querySelector("form[data-auth-form]");
      form.elements.email.value = demo.getAttribute("data-demo-email");
      form.elements.password.value = demo.getAttribute("data-demo-password");
      var box = form.querySelector("[data-form-error]");
      if (box) box.setAttribute("hidden", "");
    });
  }
})();