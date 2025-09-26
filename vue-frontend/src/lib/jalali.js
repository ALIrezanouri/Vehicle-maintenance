// Convert Gregorian date to Jalali
export function toJalali(gy, gm, gd) {
  return gregorianToJalali(gy, gm, gd);
}

// Convert Jalali date to Gregorian
export function toGregorian(jy, jm, jd) {
  return jalaliToGregorian(jy, jm, jd);
}

// Get month name in Persian
export function getMonthName(month) {
  const monthNames = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
  ];
  return monthNames[month - 1] || '';
}

// Get number of days in a Jalali month
export function getDaysInMonth(year, month) {
  if (month <= 6) return 31;
  if (month <= 11) return 30;
  // For Esfand, check if it's a leap year
  return isJalaliLeapYear(year) ? 30 : 29;
}

// Get day of week for the first day of a Jalali month
export function getDayOfWeek(year, month, day = 1) {
  // Convert Jalali date to Gregorian
  const gregorianDate = jalaliToGregorian(year, month, day);
  // Create a Date object (months are 0-indexed in JS)
  const date = new Date(gregorianDate.gy, gregorianDate.gm - 1, gregorianDate.gd);
  // Get day of week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
  // In Jalali calendar, Saturday is the first day of the week
  const dayOfWeek = date.getDay();
  // Convert to Jalali day of week (0 = Saturday, 1 = Sunday, ..., 6 = Friday)
  return (dayOfWeek + 1) % 7;
}

// Helper functions
function gregorianToJalali(gy, gm, gd) {
  const g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
  
  if (gy <= 1600) {
    const jy = 0;
    gy -= 621;
  } else {
    const jy = 979;
    gy -= 1600;
  }
  
  if (gm > 2) {
    const gy2 = (gy + 1);
  } else {
    const gy2 = gy;
  }
  
  let days = (365 * gy) + (parseInt((gy2 + 3) / 4)) - (parseInt((gy2 + 99) / 100)) + 
             (parseInt((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1];
  
  const jy = jy + (parseInt(days / 12053) * 4) + (parseInt((days % 12053) / 1461));
  days = days % 1461;
  
  if (days > 365) {
    const jm = parseInt((days - 1) / 30.42) + 1;
    const jd = parseInt((days - 1) % 30.42) + 1;
  } else {
    const jm = 1;
    const jd = days + 1;
  }
  
  if (days > 365) {
    const jm = parseInt((days - 1) / 30.42) + 1;
    const jd = parseInt((days - 1) % 30.42) + 1;
  } else {
    const jm = 1;
    const jd = days + 1;
  }
  
  return { jy: jy, jm: jm, jd: jd };
}

function jalaliToGregorian(jy, jm, jd) {
  if (jy < 100) {
    jy += 1300;
  }
  
  const jalaliMonths = [
    [0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 365],
    [0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 366]
  ];
  
  const isLeap = isJalaliLeapYear(jy);
  const days = jalaliMonths[isLeap ? 1 : 0][jm - 1] + jd;
  
  let gy = jy + 621;
  let g_d_m;
  
  if (days > 286 + (isLeap ? 1 : 0)) {
    gy++;
    g_d_m = [
      0, 31, 62, 93, 124, 155, 186, 217, 248, 279, 310, 341, 
      372 - (isLeap ? 1 : 0)
    ];
  } else {
    g_d_m = [
      0, 31, 62, 93, 124, 155, 186, 217, 248, 279, 310, 341, 
      372 - (isLeap ? 1 : 0)
    ];
  }
  
  let i = 0;
  while (days > g_d_m[i]) {
    i++;
  }
  
  const gm = i;
  const gd = days - g_d_m[i - 1];
  
  return { gy: gy, gm: gm, gd: gd };
}

function isJalaliLeapYear(jy) {
  const breaks = [
    -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 
    1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178
  ];
  
  let bl = breaks.length;
  let jp = breaks[0];
  
  if (jy < jp || jy >= breaks[bl - 1]) {
    throw new Error('Invalid Jalali year: ' + jy);
  }
  
  let jump = 0;
  for (let i = 1; i < bl; i++) {
    const jt = breaks[i];
    jump = jt - jp;
    if (jy < jt) {
      break;
    }
    jp = jt;
  }
  
  const n = jy - jp;
  
  if (jump - n < 6) {
    return true;
  }
  
  return (jump % 33 % 4 === n % 33 % 4);
}