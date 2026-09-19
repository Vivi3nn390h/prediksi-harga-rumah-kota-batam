/**
 * Client-side validation logic for Batam House Prediction inputs.
 */

const LIMITS = {
  land_area: { min: 20, max: 2000 },
  building_area: { min: 20, max: 2000 },
  bedroom: { min: 1, max: 20 },
  bathroom: { min: 1, max: 20 },
  floor_count: { min: 1, max: 10 }
};

function validatePredictionInput(data) {
  const errors = [];

  const landArea = parseFloat(data.land_area);
  const buildingArea = parseFloat(data.building_area);
  const bedroom = parseInt(data.bedroom, 10);
  const bathroom = parseInt(data.bathroom, 10);
  const floorCount = parseInt(data.floor_count, 10);
  const location = data.location ? String(data.location).trim() : '';

  // 1. Basic field checks
  if (isNaN(landArea) || landArea < LIMITS.land_area.min || landArea > LIMITS.land_area.max) {
    errors.push(`Luas tanah harus diisi antara ${LIMITS.land_area.min} m² dan ${LIMITS.land_area.max} m².`);
  }

  if (isNaN(buildingArea) || buildingArea < LIMITS.building_area.min || buildingArea > LIMITS.building_area.max) {
    errors.push(`Luas bangunan harus diisi antara ${LIMITS.building_area.min} m² dan ${LIMITS.building_area.max} m².`);
  }

  if (isNaN(bedroom) || bedroom < LIMITS.bedroom.min || bedroom > LIMITS.bedroom.max) {
    errors.push(`Jumlah kamar tidur harus antara ${LIMITS.bedroom.min} dan ${LIMITS.bedroom.max}.`);
  }

  if (isNaN(bathroom) || bathroom < LIMITS.bathroom.min || bathroom > LIMITS.bathroom.max) {
    errors.push(`Jumlah kamar mandi harus antara ${LIMITS.bathroom.min} dan ${LIMITS.bathroom.max}.`);
  }

  if (isNaN(floorCount) || floorCount < LIMITS.floor_count.min || floorCount > LIMITS.floor_count.max) {
    errors.push(`Jumlah lantai harus antara ${LIMITS.floor_count.min} dan ${LIMITS.floor_count.max}.`);
  }

  if (!location) {
    errors.push(`Pilih salah satu zona lokasi properti di Kota Batam.`);
  }

  // If basic errors exist, return early before cross-field check
  if (errors.length > 0) {
    return { valid: false, errors };
  }

  // 2. Cross-field rationality rules
  const maxBuildingAllowed = landArea * floorCount;
  if (buildingArea > maxBuildingAllowed) {
    errors.push(`Luas bangunan (${buildingArea} m²) melebihi kapasitas maksimum tanah (${landArea} m² x ${floorCount} lantai = ${maxBuildingAllowed} m²).`);
  }

  const maxBathroomAllowed = bedroom + 2;
  if (bathroom > maxBathroomAllowed) {
    errors.push(`Jumlah kamar mandi (${bathroom}) secara rasional tidak boleh melebihi kamar tidur + 2 (${bedroom} + 2 = ${maxBathroomAllowed}).`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
