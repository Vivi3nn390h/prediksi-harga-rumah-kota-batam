/**
 * Prediction Page Controller & UI Renderer
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictForm');
  const btnDemo = document.getElementById('btnDemo');
  const btnReset = document.getElementById('btnReset');
  const alertContainer = document.getElementById('alertContainer');
  const resultCard = document.getElementById('resultCard');

  if (!form) return; // Exit if not on prediction page

  // Sample Demo Input preset
  const DEMO_DATA = {
    land_area: 120,
    building_area: 90,
    bedroom: 3,
    bathroom: 2,
    floor_count: 1,
    location: 'Batam Center'
  };

  // Demo Fill Handler
  if (btnDemo) {
    btnDemo.addEventListener('click', () => {
      document.getElementById('land_area').value = DEMO_DATA.land_area;
      document.getElementById('building_area').value = DEMO_DATA.building_area;
      document.getElementById('bedroom').value = DEMO_DATA.bedroom;
      document.getElementById('bathroom').value = DEMO_DATA.bathroom;
      document.getElementById('floor_count').value = DEMO_DATA.floor_count;
      document.getElementById('location').value = DEMO_DATA.location;
      hideAlert();
    });
  }

  // Form Reset Handler
  if (btnReset) {
    btnReset.addEventListener('click', () => {
      form.reset();
      hideAlert();
      renderEmptyResultState();
    });
  }

  // Form Submit Handler
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const rawData = {
      land_area: document.getElementById('land_area').value,
      building_area: document.getElementById('building_area').value,
      bedroom: document.getElementById('bedroom').value,
      bathroom: document.getElementById('bathroom').value,
      floor_count: document.getElementById('floor_count').value,
      location: document.getElementById('location').value
    };

    // Client-side validation
    const valResult = validatePredictionInput(rawData);
    if (!valResult.valid) {
      showAlert(valResult.errors, 'error');
      return;
    }

    // Submit payload
    const payload = {
      land_area: parseFloat(rawData.land_area),
      building_area: parseFloat(rawData.building_area),
      bedroom: parseInt(rawData.bedroom, 10),
      bathroom: parseInt(rawData.bathroom, 10),
      floor_count: parseInt(rawData.floor_count, 10),
      location: String(rawData.location)
    };

    renderLoadingState();

    try {
      const response = await predictHousePrice(payload);
      renderResultSuccess(response);
    } catch (err) {
      showAlert([err.message], 'error');
      renderEmptyResultState();
    }
  });

  function showAlert(messages, type = 'error') {
    if (!alertContainer) return;
    const msgList = messages.map(m => `<li>${escapeHtml(m)}</li>`).join('');
    alertContainer.innerHTML = `
      <div class="alert alert-${type}">
        <strong>Perhatian:</strong>
        <ul style="margin-top: 6px; padding-left: 18px;">${msgList}</ul>
      </div>
    `;
    alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function hideAlert() {
    if (alertContainer) alertContainer.innerHTML = '';
  }

  function renderLoadingState() {
    if (!resultCard) return;
    resultCard.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">⌛</div>
        <h3>Menganalisis Spesifikasi Properti...</h3>
        <p>Memproses input menggunakan model machine learning...</p>
      </div>
    `;
  }

  function renderEmptyResultState() {
    if (!resultCard) return;
    resultCard.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🏠</div>
        <h3>Belum Ada Hasil Prediksi</h3>
        <p>Isi form spesifikasi rumah di sebelah kiri dan klik tombol <strong>Hitung Prediksi Harga</strong>.</p>
      </div>
    `;
  }

  function renderResultSuccess(res) {
    if (!resultCard) return;

    const inp = res.input_summary;
    const disclaimerText = res?.disclaimer || 'Hasil prediksi merupakan estimasi berdasarkan pola data yang digunakan dalam penelitian dan bukan merupakan penilaian harga resmi properti.';

    resultCard.innerHTML = `
      <div class="result-header">
        <span class="tag">Hasil Estimasi Machine Learning</span>
        <div class="result-price">${res.formatted_price_idr}</div>
        <p class="result-subtext">Perkiraan harga pasar berdasarkan pola 3.150 data rumah Batam</p>
      </div>

      <div class="result-metrics-grid">
        <div class="metric-box">
          <div class="metric-box-label">Estimasi / m² Tanah</div>
          <div class="metric-box-value">${res.formatted_price_per_sqm}</div>
        </div>
        <div class="metric-box">
          <div class="metric-box-label">Rentang Wajar (MAE)</div>
          <div class="metric-box-value" style="font-size: 0.85rem;">
            ${res.formatted_lower_bound} - ${res.formatted_upper_bound}
          </div>
        </div>
      </div>

      <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 10px; color: var(--primary-color);">
        Ringkasan Input Spesifikasi
      </h4>
      <table class="summary-table">
        <tbody>
          <tr>
            <th>Luas Tanah</th>
            <td>${inp.land_area} m²</td>
          </tr>
          <tr>
            <th>Luas Bangunan</th>
            <td>${inp.building_area} m²</td>
          </tr>
          <tr>
            <th>Kamar Tidur / Mandi</th>
            <td>${inp.bedroom} KT / ${inp.bathroom} KM</td>
          </tr>
          <tr>
            <th>Jumlah Lantai</th>
            <td>${inp.floor_count} Lantai</td>
          </tr>
          <tr>
            <th>Zona Lokasi</th>
            <td>${escapeHtml(inp.location)}</td>
          </tr>
        </tbody>
      </table>

      <div class="alert alert-warning" style="margin-bottom: 0;">
        <strong>Disclaimer:</strong> ${escapeHtml(disclaimerText)}
      </div>
    `;
  }
});
