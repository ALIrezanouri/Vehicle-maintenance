<template>
  <div class="space-y-6">
    <h1 class="text-3xl font-bold">{{ $t('emergencyServices') }}</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-card border border-border rounded-lg p-6 shadow-sm">
          <h2 class="text-xl font-semibold mb-4">{{ $t('requestEmergencyService') }}</h2>
          
          <form class="space-y-4" @submit.prevent="requestEmergencyService">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('name') }}</label>
                <input 
                  v-model="emergencyRequest.name"
                  type="text" 
                  class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  :placeholder="$t('name')"
                  required
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('phoneNumber') }}</label>
                <input 
                  v-model="emergencyRequest.phoneNumber"
                  type="tel" 
                  class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  :placeholder="$t('phoneNumber')"
                  required
                >
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
              <select 
                v-model="emergencyRequest.vehicle"
                class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                required
              >
                <option value="">{{ $t('selectYourVehicle') }}</option>
                <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                  {{ vehicle.brand }} {{ vehicle.model }} - {{ vehicle.licensePlate }}
                </option>
                <option value="other">{{ $t('other') }}</option>
              </select>
            </div>
            
            <div v-if="emergencyRequest.vehicle === 'other' || emergencyRequest.vehicle === ''">
              <label class="block text-sm font-medium mb-1">{{ $t('licensePlate') }}</label>
              <IranianLicensePlate 
                v-model="emergencyRequest.licensePlateData" 
                :type="emergencyRequest.vehicleType || 'car'"
              />
              <!-- Hidden input to store the formatted license plate string -->
              <input 
                type="hidden" 
                :value="formatLicensePlate(emergencyRequest.licensePlateData)" 
                required
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('location') }}</label>
              <div class="flex flex-col sm:flex-row gap-2">
                <input 
                  v-model="emergencyRequest.location"
                  type="text" 
                  class="flex-1 border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                  :placeholder="$t('location')"
                  required
                >
                <button @click="useGPS" type="button" class="px-4 py-2 border border-border rounded-md hover:bg-muted whitespace-nowrap">
                  {{ $t('useGPS') }}
                </button>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('emergencyType') }}</label>
              <select 
                v-model="emergencyRequest.type"
                class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                required
              >
                <option value="">{{ $t('selectEmergencyType') }}</option>
                <option value="flatTire">{{ $t('flatTire') }}</option>
                <option value="engineProblem">{{ $t('engineProblem') }}</option>
                <option value="accident">{{ $t('accident') }}</option>
                <option value="runningOutOfFuel">{{ $t('runningOutOfFuel') }}</option>
                <option value="lockout">{{ $t('lockout') }}</option>
                <option value="other">{{ $t('other') }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('description') }}</label>
              <textarea 
                v-model="emergencyRequest.description"
                rows="3"
                class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
                :placeholder="$t('description')"
              ></textarea>
            </div>
            
            <div class="pt-4">
              <button type="submit" class="w-full bg-destructive text-destructive-foreground py-2 rounded-md hover:bg-destructive/90 font-medium">
                {{ $t('requestEmergencyService') }}
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div class="space-y-6">
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
          <h2 class="text-lg sm:text-xl font-semibold mb-4">{{ $t('emergencyContacts') }}</h2>
          
          <div class="space-y-4">
            <div v-for="contact in emergencyContacts" :key="contact.id" class="flex items-center space-x-3 space-x-reverse">
              <div class="flex-shrink-0 w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <div class="h-5 w-5 text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
              </div>
              <div>
                <h3 class="font-medium">{{ contact.name }}</h3>
                <p class="text-sm text-muted-foreground">{{ contact.number }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
          <h2 class="text-lg sm:text-xl font-semibold mb-4">{{ $t('nearbyServiceProviders') }}</h2>
          
          <div class="space-y-4">
            <div v-for="provider in serviceProviders" :key="provider.id" class="border border-border rounded-md p-4">
              <div class="flex justify-between">
                <h3 class="font-medium">{{ provider.name }}</h3>
                <span class="text-sm bg-primary/10 text-primary px-2 py-1 rounded">
                  {{ provider.distance }} کیلومتر
                </span>
              </div>
              <p class="text-sm text-muted-foreground mt-1">{{ provider.services }}</p>
              <div class="flex items-center mt-2 text-sm">
                <div class="h-4 w-4 text-yellow-400 mr-1">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
                <span>{{ provider.rating }}</span>
                <span class="mx-2">•</span>
                <span>{{ provider.reviews }} نظر</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IranianLicensePlate from '@/components/IranianLicensePlate.vue';

export default {
  name: 'Emergency',
  components: {
    IranianLicensePlate
  },
  data() {
    return {
      emergencyRequest: {
        name: '',
        phoneNumber: '',
        vehicle: '',
        licensePlateData: {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        },
        location: '',
        type: '',
        description: '',
        vehicleType: 'car'
      },
      vehicles: [
        {
          id: 1,
          brand: 'پژو',
          model: '206',
          licensePlate: '123ب456-78'
        },
        {
          id: 2,
          brand: 'سمند',
          model: 'SE',
          licensePlate: '345پ678-90'
        }
      ],
      emergencyContacts: [
        {
          id: 1,
          name: 'اورژانس خودرو',
          number: '110'
        },
        {
          id: 2,
          name: 'پلیس راه',
          number: '112'
        },
        {
          id: 3,
          name: 'آتش نشانی',
          number: '125'
        },
        {
          id: 4,
          name: 'خدمات شهری',
          number: '115'
        }
      ],
      serviceProviders: [
        {
          id: 1,
          name: 'خدمات خودرو پارس',
          services: 'تعمیر موتور، تعویض لاستیک',
          rating: 4.5,
          reviews: 24,
          distance: 2.5
        },
        {
          id: 2,
          name: 'تعمیرگاه تهران',
          services: 'تعمیرات عمومی، برق خودرو',
          rating: 4.2,
          reviews: 18,
          distance: 3.1
        }
      ]
    }
  },
  methods: {
    useGPS() {
      // In a real app, this would get the user's location
      this.emergencyRequest.location = 'موقعیت فعلی شما';
    },
    requestEmergencyService() {
      // Process the emergency request
      if (this.emergencyRequest.name && this.emergencyRequest.phoneNumber && 
          (this.emergencyRequest.vehicle || this.emergencyRequest.licensePlateData) && 
          this.emergencyRequest.location && this.emergencyRequest.type) {
        alert('درخواست ارسال شد');
        // Reset form
        this.emergencyRequest = {
          name: '',
          phoneNumber: '',
          vehicle: '',
          licensePlateData: {
            firstTwoDigits: ['', ''],
            letter: '',
            nextThreeDigits: ['', '', ''],
            lastTwoDigits: ['', ''],
            motorcycleDigits: ['', '', ''],
            motorcycleLetter: '',
            motorcycleLastDigits: ['', '', '']
          },
          location: '',
          type: '',
          description: '',
          vehicleType: 'car'
        };
      } else {
        alert('لطفاً تمام فیلدهای اجباری را پر کنید');
      }
    },
    // Format license plate data into a string
    formatLicensePlate(plateData) {
      if (!plateData) return '';
      
      const { firstTwoDigits, letter, nextThreeDigits, lastTwoDigits } = plateData;
      return `${firstTwoDigits.join('')}${letter}${nextThreeDigits.join('')}-${lastTwoDigits.join('')}`;
    },
    // Parse license plate string into component data format
    parseLicensePlate(plateString) {
      if (!plateString) {
        // Return default empty plate
        return {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        };
      }
      
      // Simple parsing assuming format like "123ب456-78"
      const match = plateString.match(/^(\d{2})(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})-(\d{2})$/);
      if (match) {
        return {
          firstTwoDigits: [match[1].charAt(0), match[1].charAt(1)],
          letter: match[3],
          nextThreeDigits: [match[4].charAt(0), match[4].charAt(1), match[4].charAt(2)],
          lastTwoDigits: [match[5].charAt(0), match[5].charAt(1)],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        };
      }
      // Default empty plate
      return {
        firstTwoDigits: ['', ''],
        letter: '',
        nextThreeDigits: ['', '', ''],
        lastTwoDigits: ['', ''],
        motorcycleDigits: ['', '', ''],
        motorcycleLetter: '',
        motorcycleLastDigits: ['', '', '']
      };
    }
  }
}
</script>