// Mengatur pergantian tema gelap dan terang
document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const buttons = document.querySelectorAll('[data-theme-toggle]');

  // Memperbarui ikon sesuai tema yang aktif
  const updateIcons = () => {
    const isLight = root.classList.contains('light');
    buttons.forEach((btn) => {
      btn.querySelector('[data-icon="sun"]')?.classList.toggle('hidden', isLight);
      btn.querySelector('[data-icon="moon"]')?.classList.toggle('hidden', !isLight);
      btn.setAttribute('aria-label', isLight ? 'Aktifkan mode gelap' : 'Aktifkan mode terang');
    });
  };

  // Mengganti tema dan menyimpan pilihan pengguna
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      root.classList.toggle('light');
      localStorage.setItem('theme', root.classList.contains('light') ? 'light' : 'dark');
      updateIcons();
    });
  });

  updateIcons();
});