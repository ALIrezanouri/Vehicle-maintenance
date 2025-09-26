// jalali.ts

// Helper function to convert a Gregorian date to Jalali date
export function toJalali(gDate) {
  const gregorianYear = gDate.getFullYear();
  const gregorianMonth = gDate.getMonth() + 1; // Month is 0-indexed in JS Date
  const gregorianDay = gDate.getDate();

  let gy = gregorianYear;
  let gm = gregorianMonth;
  let gd = gregorianDay;
  let g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  let jy = (gy <= 1600) ? 0 : 979 + 33 * Math.floor((gy - 1601) / 33) + 4 * Math.floor(((gy - 1601) % 33) / 4) + Math.floor(((gy - 1601) % 33) % 4);
  let days = 365 * (gy - 1) + Math.floor((gy - 1) / 4) - Math.floor((gy - 1) / 100) + Math.floor((gy - 1) / 400) + gd + g_d_m[gm - 1];
  if (gm > 2 && ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0))) {
    days++;
  }
  let j_d_m = [0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 366];
  let jd = days - (79 + 30 * jy + Math.floor(jy / 4));
  let jm = 0;
  while (jm < 12 && jd > j_d_m[jm]) {
    jm++;
  }
  jd -= j_d_m[jm - 1];
  return { jy: jy, jm: jm, jd: jd };
}

// Helper function to convert a Jalali date to Gregorian date
export function toGregorian(jy, jm, jd) {
  let sal_a = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365];
  let jal_a = [0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 366];
  let gy = (jy <= 1600) ? 0 : 1600;
  let days = 365 * (gy - 1) + Math.floor((gy - 1) / 4) - Math.floor((gy - 1) / 100) + Math.floor((gy - 1) / 400) + jd + jal_a[jm - 1];
  let leap = 0;
  if (jm > 2 && ((jy % 4 === 0 && jy % 100 !== 0) || (jy % 400 === 0))) {
    leap = 1;
  }
  let gd = days - (79 + 30 * jy + Math.floor(jy / 4));
  let gm = 0;
  while (gm < 12 && gd > sal_a[gm]) {
    gm++;
  }
  gd -= sal_a[gm - 1];
  if (gm > 2 && ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0))) {
    gd--;
  }
  return new Date(gy, gm - 1, gd);
}

export function getMonthName(month) {
  const monthNames = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
  ];
  return monthNames[month - 1];
}

export function getDaysInMonth(year, month) {
  if (month <= 6) { // Farvardin to Shahrivar (first 6 months)
    return 31;
  } else if (month <= 11) { // Mehr to Bahman (next 5 months)
    return 30;
  } else { // Esfand (last month)
    // Check for leap year
    const isLeap = (year % 33 === 1 || year % 33 === 5 || year % 33 === 9 || year % 33 === 13 || year % 33 === 17 || year % 33 === 22 || year % 33 === 26 || year % 33 === 30);
    return isLeap ? 30 : 29;
  }
}

export function getDayOfWeek(year, month, day) {
  // This is a simplified calculation and might not be perfectly accurate for all historical dates.
  // For a more robust solution, a full calendar conversion library would be needed.
  const gregorianDate = toGregorian(year, month, day);
  // JavaScript's getDay() returns 0 for Sunday, 1 for Monday, ..., 6 for Saturday.
  // We want to map it to the Jalali week, which typically starts on Saturday (شنبه).
  // So, Saturday (0) -> 0, Sunday (1) -> 1, ..., Friday (6) -> 6
  // The JalaliDatePicker component expects 'ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'
  // which corresponds to Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday.
  // So, if JS getDay() is 0 (Sunday), we want it to be 1 (یکشنبه).
  // If JS getDay() is 6 (Saturday), we want it to be 0 (شنبه).
  // (gregorianDate.getDay() + 1) % 7 will map Sunday (0) to 1, Monday (1) to 2, ..., Saturday (6) to 0.
  // This matches the order 'ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج' if 'ش' is Saturday.
  return (gregorianDate.getDay() + 1) % 7;
}
