/* poster.js – fallback poster (pemilik: Frontend A) */
(function () {
  "use strict";

  function showFallback(img) {
    var box = img.parentElement;
    var fb = box && box.querySelector("[data-poster-fallback]");
    if (fb) fb.classList.remove("hidden");
    img.remove();
  }

  document.addEventListener(
    "error",
    function (e) {
      var el = e.target;
      if (!el || el.tagName !== "IMG") return;
      if (el.hasAttribute("data-poster")) showFallback(el);
      else if (el.hasAttribute("data-hide-on-error")) el.style.display = "none";
    },
    true
  );

  function checkAlreadyBroken() {
    document.querySelectorAll("img[data-poster]").forEach(function (img) {
      if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) showFallback(img);
    });
    document.querySelectorAll("img[data-hide-on-error]").forEach(function (img) {
      if (img.complete && img.naturalWidth === 0 && img.getAttribute("src")) img.style.display = "none";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", checkAlreadyBroken);
  } else {
    checkAlreadyBroken();
  }
})();