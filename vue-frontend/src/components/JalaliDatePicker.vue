<template>
  <input 
    type="text" 
    :value="formattedDate" 
    @focus="showCalendar = true" 
    @blur="hideCalendar"
    @input="handleInput"
    class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
    placeholder="انتخاب تاریخ"
  />
  <div v-if="showCalendar" class="absolute z-10 bg-card border border-border rounded-md shadow-lg mt-1">
    <div class="flex justify-between items-center p-2 border-b border-border">
      <button @mousedown.prevent="prevMonth" class="px-2 py-1 rounded-md hover:bg-muted">
        <
      </button>
      <span>{{ currentMonthName }} {{ currentYear }}</span>
      <button @mousedown.prevent="nextMonth" class="px-2 py-1 rounded-md hover:bg-muted">
        >
      </button>
    </div>
    <div class="grid grid-cols-7 gap-1 p-2 text-center text-sm">
      <span v-for="dayName in dayNames" :key="dayName" class="text-muted-foreground">{{ dayName }}</span>
      <span v-for="blankDay in firstDayOfMonthOffset" :key="'blank-' + blankDay" class="opacity-0">.</span>
      <button 
        v-for="day in daysInMonth" 
        :key="day" 
        @mousedown.prevent="selectDate(day)"
        :class="['px-2 py-1 rounded-md hover:bg-primary/10', { 'bg-primary text-primary-foreground': isSelected(day) }]"
      >
        {{ day }}
      </button>
    </div>
  </div>
</template>

<script>
import { toJalali, toGregorian, getMonthName, getDaysInMonth, getDayOfWeek } from '@frontend/lib/jalali';

export default {
  name: 'JalaliDatePicker',
  props: {
    modelValue: {
      type: String,
      default: null
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      showCalendar: false,
      currentDate: new Date(), // Gregorian date
      dayNames: ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'],
    };
  },
  computed: {
    jalaliDate() {
      return toJalali(this.currentDate);
    },
    currentYear() {
      return this.jalaliDate.jy;
    },
    currentMonth() {
      return this.jalaliDate.jm;
    },
    currentMonthName() {
      return getMonthName(this.currentMonth);
    },
    daysInMonth() {
      return getDaysInMonth(this.currentYear, this.currentMonth);
    },
    firstDayOfMonthOffset() {
      const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
      const jalaliFirstDay = toJalali(firstDay);
      return getDayOfWeek(jalaliFirstDay.jy, jalaliFirstDay.jm, 1);
    },
    formattedDate() {
      if (this.modelValue) {
        return this.modelValue;
      }
      return '';
    }
  },
  methods: {
    prevMonth() {
      const currentMonth = this.currentDate.getMonth();
      this.currentDate = new Date(this.currentDate.getFullYear(), currentMonth - 1, 1);
    },
    nextMonth() {
      const currentMonth = this.currentDate.getMonth();
      this.currentDate = new Date(this.currentDate.getFullYear(), currentMonth + 1, 1);
    },
    selectDate(day) {
      const selectedJalaliDate = { jy: this.currentYear, jm: this.currentMonth, jd: day };
      const gregorianDate = toGregorian(selectedJalaliDate.jy, selectedJalaliDate.jm, selectedJalaliDate.jd);
      
      const year = gregorianDate.getFullYear();
      const month = (gregorianDate.getMonth() + 1).toString().padStart(2, '0');
      const dayOfMonth = gregorianDate.getDate().toString().padStart(2, '0');
      
      const formatted = `${year}/${month}/${dayOfMonth}`;
      this.$emit('update:modelValue', formatted);
      this.showCalendar = false;
    },
    isSelected(day) {
      if (!this.modelValue) return false;
      const [year, month, dayOfMonth] = this.modelValue.split('/').map(Number);
      const gregorianModelDate = new Date(year, month - 1, dayOfMonth);
      const jalaliModelDate = toJalali(gregorianModelDate);

      return (
        jalaliModelDate.jy === this.currentYear &&
        jalaliModelDate.jm === this.currentMonth &&
        jalaliModelDate.jd === day
      );
    },
    handleInput(event) {
      // Allow direct input, but validate if possible
      const value = event.target.value;
      // Basic validation for Jalali date format (e.g., YYYY/MM/DD)
      const jalaliRegex = /^(\d{4})\/(\d{2})\/(\d{2})$/;
      if (jalaliRegex.test(value)) {
        this.$emit('update:modelValue', value);
      } else if (value === '') {
        this.$emit('update:modelValue', null);
      }
      // Keep calendar hidden if typing
      this.showCalendar = false;
    },
    hideCalendar() {
      // Delay hiding to allow click event on date to register
      setTimeout(() => {
        this.showCalendar = false;
      }, 150);
    }
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          // Assuming modelValue is in Gregorian format 'YYYY/MM/DD'
          const [year, month, day] = newValue.split('/').map(Number);
          this.currentDate = new Date(year, month - 1, day);
        } else {
          this.currentDate = new Date();
        }
      }
    }
  }
};
</script>

<style scoped>
/* Add any specific styles for your date picker here */
</style>
