/* search_bar.js – tombol × di macro search_bar (pemilik: Frontend A)
 * - × muncul hanya jika input berisi; klik -> kosongkan + fokus.
 * - Kata kunci di-trim sebelum submit (sama seperti SearchBar.tsx).
 * Catatan: di React, × juga memanggil onSearch(""). Di SSR kita hanya mengosongkan input;
 * pengguna menekan "Cari" lagi untuk menampilkan semua film.
 */
(function () {
  "use strict";
  document.querySelectorAll("form[data-search-bar]").forEach(function (form) {
    var input = form.querySelector("[data-search-input]");
    var clear = form.querySelector("[data-search-clear]");
    if (!input || !clear) return;

    var sync = function () { clear.toggleAttribute("hidden", input.value === ""); };
    input.addEventListener("input", sync);
    sync();

    clear.addEventListener("click", function () {
      input.value = "";
      sync();
      input.focus();
    });

    form.addEventListener("submit", function () {
      input.value = input.value.trim();
    });
  });
})();
