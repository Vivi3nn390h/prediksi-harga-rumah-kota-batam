/**
 * Formatting utilities for numbers, text, and Rupiah currency.
 */

/**
 * Formats a number to Indonesian Rupiah string format.
 * Example: 1250000000 -> "Rp 1.250.000.000"
 */
function formatRupiah(amount) {
  if (amount === null || amount === undefined || isNaN(amount)) return 'Rp 0';
  const val = Math.round(Number(amount));
  return 'Rp ' + val.toLocaleString('id-ID');
}

/**
 * Safely escapes strings for HTML rendering.
 */
function escapeHtml(str) {
  if (typeof str !== 'string') return str;
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
