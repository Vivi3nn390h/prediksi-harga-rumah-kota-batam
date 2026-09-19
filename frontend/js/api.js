/**
 * API Service for Batam House Price Prediction application.
 */

const API_BASE = '/api';

/**
 * Fetches dataset metadata and zone options.
 */
async function fetchMetadata() {
  try {
    const response = await fetch(`${API_BASE}/metadata`);
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch metadata:', error);
    throw error;
  }
}

/**
 * Fetches model research metrics and academic notes.
 */
async function fetchModelInfo() {
  try {
    const response = await fetch(`${API_BASE}/model-info`);
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch model info:', error);
    throw error;
  }
}

/**
 * Submits house specs to API to calculate prediction.
 * @param {Object} payload 
 */
async function predictHousePrice(payload) {
  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      // Return custom validation messages array or detailed error
      const errorMessage = Array.isArray(data.detail)
        ? data.detail.join('. ')
        : (data.detail || data.message || 'Terjadi kesalahan pada server.');
      throw new Error(errorMessage);
    }

    return data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
}
