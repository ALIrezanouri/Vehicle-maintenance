<template>
  <div class="container">
    <div class="license-plate" :class="{ 'motorcycle': type === 'motorcycle' }">
      <div class="blue-column">
        <div class="flag">
          <div></div>
          <div></div>
          <div></div>
        </div>
        <div class="text">
          <div>I.R.</div>
          <div>IRAN</div>
        </div>
      </div>

      <!-- Car plate input fields -->
      <template v-if="type === 'car' && !readonly">
        <input 
          v-model="plate.firstTwoDigits[0]" 
          @input="moveToNext($event, 'firstTwoDigits', 1)" 
          @keydown="handleKeyDown($event, 'firstTwoDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.firstTwoDigits[1]" 
          @input="moveToNext($event, 'firstTwoDigits', 2, 'letter')" 
          @keydown="handleKeyDown($event, 'firstTwoDigits', 1, 'firstTwoDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <select v-model="plate.letter" class="letter-select">
          <option value="">انتخاب حرف</option>
          <option v-for="letter in persianLetters" :key="letter" :value="letter">
            {{ letter }}
          </option>
        </select>
        <input 
          v-model="plate.nextThreeDigits[0]" 
          @input="moveToNext($event, 'nextThreeDigits', 1)" 
          @keydown="handleKeyDown($event, 'letter', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.nextThreeDigits[1]" 
          @input="moveToNext($event, 'nextThreeDigits', 2)" 
          @keydown="handleKeyDown($event, 'nextThreeDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.nextThreeDigits[2]" 
          @input="moveToNext($event, 'nextThreeDigits', 3, 'lastTwoDigits')" 
          @keydown="handleKeyDown($event, 'nextThreeDigits', 1)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <div class="iran-column">
          <span>ایــران</span>
          <div>
            <input 
              v-model="plate.lastTwoDigits[0]" 
              @input="moveToNext($event, 'lastTwoDigits', 1)" 
              @keydown="handleKeyDown($event, 'nextThreeDigits', 2)"
              type="text" 
              maxlength="1" 
              class="digit-input-small"
            >
            <input 
              v-model="plate.lastTwoDigits[1]" 
              @input="moveToNext($event, 'lastTwoDigits', 2)" 
              @keydown="handleKeyDown($event, 'lastTwoDigits', 0)"
              type="text" 
              maxlength="1" 
              class="digit-input-small"
            >
          </div>
        </div>
      </template>
      
      <!-- Car plate display (readonly) -->
      <template v-else-if="type === 'car' && readonly">
        <span>
          {{ plate.firstTwoDigits.join('') }}
        </span>
        <span class="alphabet-column">
          {{ plate.letter }}
        </span>
        <span>
          {{ plate.nextThreeDigits.join('') }}
        </span>
        <div class="iran-column">
          <span>ایــران</span>
          <strong>{{ plate.lastTwoDigits.join('') }}</strong>
        </div>
      </template>
      
      <!-- Motorcycle plate input fields -->
      <template v-else-if="type === 'motorcycle' && !readonly">
        <input 
          v-model="plate.motorcycleDigits[0]" 
          @input="moveToNext($event, 'motorcycleDigits', 1)" 
          @keydown="handleKeyDown($event, 'motorcycleDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.motorcycleDigits[1]" 
          @input="moveToNext($event, 'motorcycleDigits', 2)" 
          @keydown="handleKeyDown($event, 'motorcycleDigits', 1, 'motorcycleDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.motorcycleDigits[2]" 
          @input="moveToNext($event, 'motorcycleDigits', 3, 'motorcycleLetter')" 
          @keydown="handleKeyDown($event, 'motorcycleDigits', 2, 'motorcycleDigits', 1)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <select v-model="plate.motorcycleLetter" class="letter-select">
          <option value="">انتخاب حرف</option>
          <option v-for="letter in persianLetters" :key="letter" :value="letter">
            {{ letter }}
          </option>
        </select>
        <input 
          v-model="plate.motorcycleLastDigits[0]" 
          @input="moveToNext($event, 'motorcycleLastDigits', 1)" 
          @keydown="handleKeyDown($event, 'motorcycleLetter', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.motorcycleLastDigits[1]" 
          @input="moveToNext($event, 'motorcycleLastDigits', 2)" 
          @keydown="handleKeyDown($event, 'motorcycleLastDigits', 0)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <input 
          v-model="plate.motorcycleLastDigits[2]" 
          @input="moveToNext($event, 'motorcycleLastDigits', 3)" 
          @keydown="handleKeyDown($event, 'motorcycleLastDigits', 1)"
          type="text" 
          maxlength="1" 
          class="digit-input"
        >
        <div class="iran-column">
          <span>ایــران</span>
          <strong>۲۰</strong>
        </div>
      </template>
      
      <!-- Motorcycle plate display (readonly) -->
      <template v-else-if="type === 'motorcycle' && readonly">
        <span>
          {{ plate.motorcycleDigits.join('') }}
        </span>
        <span class="alphabet-column">
          {{ plate.motorcycleLetter }}
        </span>
        <span>
          {{ plate.motorcycleLastDigits.join('') }}
        </span>
        <div class="iran-column">
          <span>ایــران</span>
          <strong>۲۰</strong>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IranianLicensePlate',
  props: {
    type: {
      type: String,
      default: 'car' // or 'motorcycle'
    },
    modelValue: {
      type: Object,
      default: () => ({
        firstTwoDigits: ['', ''],
        letter: '',
        nextThreeDigits: ['', '', ''],
        lastTwoDigits: ['', ''],
        motorcycleDigits: ['', '', ''],
        motorcycleLetter: '',
        motorcycleLastDigits: ['', '', '']
      })
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      plate: this.modelValue,
      persianLetters: ['الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']
    }
  },
  watch: {
    plate: {
      handler(newVal) {
        this.$emit('update:modelValue', newVal)
      },
      deep: true
    },
    modelValue: {
      handler(newVal) {
        this.plate = newVal
      },
      deep: true
    }
  },
  methods: {
    moveToNext(event, field, nextIndex, nextField) {
      // Move to the next input field
      const value = event.target.value;
      if (value && nextIndex < this.plate[field].length) {
        const nextInput = event.target.nextElementSibling || 
                         event.target.parentElement.nextElementSibling || 
                         document.querySelector(`input[name="${nextField}"]`);
        if (nextInput) {
          nextInput.focus();
        }
      }
    },
    handleKeyDown(event, currentField, currentIndex, prevField, prevIndex) {
      // Handle backspace to move to previous field
      if (event.key === 'Backspace' && !this.plate[currentField][currentIndex] && prevField) {
        const prevInput = document.querySelector(`input[name="${prevField}"]`) || 
                         event.target.previousElementSibling;
        if (prevInput) {
          prevInput.focus();
        }
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dosis:wght@600&family=Markazi+Text:wght@600&display=swap');

.container {
  display: inline-block;
  font-size: 20px;
}

.license-plate {
  margin: 0 auto;
  min-width: 6.8em;
  display: inline-block;
  border-radius: 0.2em;
  border: 0.08em solid #333;
  font-family: "Markazi Text", serif;
  height: 1.2em;
  line-height: 1.1em;
  background-color: #ddd;
  text-align: center;
  color: rgb(40, 47, 37);
  box-shadow: inset 0.05em 0.05em 0.1em rgba(0, 0, 0, 0.3),
    inset -0.05em -0.05em 0.1em #ffffff, 0.05em 0.05em 0.1em rgba(0, 0, 0, 0.3);
  min-height: fit-content;
  position: relative;
}

.license-plate.motorcycle {
  background: linear-gradient(135deg, #009900, #00cc00);
}

.license-plate > .blue-column {
  width: 0.7em;
  height: inherit;
  float: left;
  background-color: #042591;
  position: relative;
}

.license-plate > .blue-column > .flag {
  margin: 0.1em;
}

.license-plate > .blue-column > .flag :nth-child(1) {
  height: 0.1em;
  background-color: green;
}

.license-plate > .blue-column > .flag :nth-child(2) {
  height: 0.1em;
  background-color: #fff;
}

.license-plate > .blue-column > .flag :nth-child(3) {
  height: 0.1em;
  background-color: red;
}

.license-plate > .blue-column > .text {
  color: #ffffff;
  font-size: 0.2em;
  line-height: 1em;
  text-align: left;
  font-family: sans-serif;
  position: absolute;
  bottom: 0.5em;
  left: 0.5em;
}

.license-plate > span,
.license-plate > .digit-input,
.license-plate > .digit-input-small,
.license-plate > .letter-select {
  margin: 0 0.1em;
  font-size: 1.3em;
  padding: 0.05em;
  display: inline-block;
  text-shadow: 0.02em 0.02em 0.03em rgba(0, 0, 0, 0.3),
    -0.03em -0.03em 0.02em #fff;
  float: left;
  border: none;
  background: transparent;
  color: inherit;
  font-family: "Markazi Text", serif;
  text-align: center;
  outline: none;
}

.license-plate > .digit-input,
.license-plate > .digit-input-small {
  width: 0.7em;
}

.license-plate > .digit-input-small {
  width: 0.5em;
  font-size: 1.1em;
}

.license-plate > .letter-select {
  width: 1em;
  font-size: 1.5em;
  line-height: 0.5em;
  margin: 0;
  padding: 0;
}

.license-plate > .alphabet-column {
  line-height: 0.5em;
  margin: 0;
}

.license-plate > .iran-column {
  width: 1.2em;
  text-align: center;
  float: right;
  border-left: 0.08em solid #333;
  height: inherit;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.license-plate > .iran-column > span {
  font-size: 0.3em;
  display: block;
  line-height: 1em;
}

.license-plate > .iran-column > strong {
  font-weight: normal;
  font-size: 1.1em;
  line-height: 0.9em;
  text-shadow: 0.03em 0.03em 0.03em rgba(0, 0, 0, 0.3),
    -0.04em -0.04em 0.02em #fff;
}

.license-plate > .iran-column > div {
  display: flex;
  justify-content: center;
}
</style>