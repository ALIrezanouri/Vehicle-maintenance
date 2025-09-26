<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold">{{ $t('vehicles') }}</h1>
      <button @click="showAddVehicleModal = true" class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
        {{ $t('addVehicle') }}
      </button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="vehicle in vehicles" :key="vehicle.id" class="bg-card border border-border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-semibold">{{ vehicle.brand }} {{ vehicle.model }}</h3>
            <!-- Display license plate using our new component -->
            <div class="mt-2">
              <IranianLicensePlate 
                :model-value="parseLicensePlate(vehicle.licensePlate)" 
                :type="vehicle.type || 'car'" 
                readonly 
              />
            </div>
          </div>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
            {{ vehicle.year }}
          </span>
        </div>
        
        <div class="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div>
            <p class="text-muted-foreground">{{ $t('currentMileage') }}</p>
            <p>{{ vehicle.currentMileage.toLocaleString() }} کیلومتر</p>
          </div>
          <div>
            <p class="text-muted-foreground">{{ $t('lastService') }}</p>
            <p>{{ vehicle.lastServiceDate }}</p>
          </div>
        </div>
        
        <div class="mt-6 flex space-x-3 space-x-reverse">
          <button @click="viewServiceHistory(vehicle)" class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90 text-sm">
            {{ $t('serviceHistory') }}
          </button>
          <button @click="editVehicle(vehicle)" class="flex-1 border border-border py-2 rounded-md hover:bg-muted text-sm">
            {{ $t('edit') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Edit Vehicle Modal -->
    <div v-if="showEditVehicleModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">ویرایش خودرو</h2>
        <form @submit.prevent="updateVehicle" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">برند</label>
            <input v-model="editingVehicle.brand" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">مدل</label>
            <input v-model="editingVehicle.model" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">نوع خودرو</label>
            <select v-model="editingVehicle.type" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="car">سواری</option>
              <option value="motorcycle">موتورسیکلت</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">سال ساخت</label>
            <select v-model="editingVehicle.year" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">انتخاب سال</option>
              <option v-for="year in years" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>
          
          <!-- License plate input using our new component -->
          <div>
            <label class="block text-sm font-medium mb-1">شماره پلاک</label>
            <IranianLicensePlate 
              v-model="editingVehicle.licensePlateData" 
              :type="editingVehicle.type"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">کیلومتر فعلی</label>
            <input v-model.number="editingVehicle.currentMileage" type="number" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">آخرین سرویس</label>
            <JalaliDatePicker 
              v-model="editingVehicle.lastServiceDate" 
              class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          
          <div class="flex space-x-3 space-x-reverse pt-4">
            <button type="submit" class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90">
              {{ $t('save') }}
            </button>
            <button @click="showEditVehicleModal = false" type="button" class="flex-1 border border-border py-2 rounded-md hover:bg-muted">
              {{ $t('cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Add Vehicle Modal -->
    <div v-if="showAddVehicleModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">افزودن خودرو جدید</h2>
        <form @submit.prevent="addVehicle" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">برند</label>
            <input v-model="newVehicle.brand" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">مدل</label>
            <input v-model="newVehicle.model" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">نوع خودرو</label>
            <select v-model="newVehicle.type" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="car">سواری</option>
              <option value="motorcycle">موتورسیکلت</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">سال ساخت</label>
            <select v-model="newVehicle.year" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">انتخاب سال</option>
              <option v-for="year in years" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
          </div>
          
          <!-- License plate input using our new component -->
          <div>
            <label class="block text-sm font-medium mb-1">شماره پلاک</label>
            <IranianLicensePlate 
              v-model="newVehicle.licensePlateData" 
              :type="newVehicle.type"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">کیلومتر فعلی</label>
            <input v-model.number="newVehicle.currentMileage" type="number" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">آخرین سرویس</label>
            <JalaliDatePicker 
              v-model="newVehicle.lastServiceDate" 
              class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          
          <div class="flex space-x-3 space-x-reverse pt-4">
            <button type="submit" class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90">
              {{ $t('save') }}
            </button>
            <button @click="showAddVehicleModal = false" type="button" class="flex-1 border border-border py-2 rounded-md hover:bg-muted">
              {{ $t('cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import IranianLicensePlate from '@/components/IranianLicensePlate.vue';
import JalaliDatePicker from '@/components/JalaliDatePicker.vue';

export default {
  name: 'Vehicles',
  components: {
    IranianLicensePlate,
    JalaliDatePicker
  },
  data() {
    return {
      showAddVehicleModal: false,
      showEditVehicleModal: false,
      newVehicle: {
        brand: '',
        model: '',
        year: '',
        type: 'car',
        licensePlateData: {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        },
        currentMileage: 0,
        lastServiceDate: null
      },
      editingVehicle: {
        id: null,
        brand: '',
        model: '',
        year: '',
        type: 'car',
        licensePlateData: {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        },
        currentMileage: 0,
        lastServiceDate: null
      },
      vehicles: [
        {
          id: 1,
          brand: 'پژو',
          model: '206',
          year: '1385',
          type: 'car',
          licensePlate: '123ب456-78',
          currentMileage: 120000,
          lastServiceDate: '1403/05/12'
        },
        {
          id: 2,
          brand: 'سمند',
          model: 'SE',
          year: '1390',
          type: 'car',
          licensePlate: '345پ678-90',
          currentMileage: 85000,
          lastServiceDate: '1403/04/28'
        }
      ],
      years: this.generateYears()
    }
  },
  methods: {
    generateYears() {
      const currentYear = 1403;
      const years = [];
      for (let i = currentYear - 30; i <= currentYear; i++) {
        years.push(i.toString());
      }
      return years.reverse();
    },
    addVehicle() {
      const vehicle = {
        id: this.vehicles.length + 1,
        brand: this.newVehicle.brand,
        model: this.newVehicle.model,
        year: this.newVehicle.year,
        type: this.newVehicle.type,
        licensePlate: this.formatLicensePlate(this.newVehicle.licensePlateData, this.newVehicle.type),
        currentMileage: this.newVehicle.currentMileage,
        lastServiceDate: this.newVehicle.lastServiceDate || ''
      };
      this.vehicles.push(vehicle);
      this.newVehicle = {
        brand: '',
        model: '',
        year: '',
        type: 'car',
        licensePlateData: {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        },
        currentMileage: 0,
        lastServiceDate: null
      };
      this.showAddVehicleModal = false;
    },
    updateVehicle() {
      const index = this.vehicles.findIndex(v => v.id === this.editingVehicle.id);
      if (index !== -1) {
        // Format the license plate before saving
        const updatedVehicle = {
          id: this.editingVehicle.id,
          brand: this.editingVehicle.brand,
          model: this.editingVehicle.model,
          year: this.editingVehicle.year,
          type: this.editingVehicle.type,
          licensePlate: this.formatLicensePlate(this.editingVehicle.licensePlateData, this.editingVehicle.type),
          currentMileage: this.editingVehicle.currentMileage,
          lastServiceDate: this.editingVehicle.lastServiceDate ? this.editingVehicle.lastServiceDate : ''
        };
        // Update the vehicle in the array
        this.vehicles.splice(index, 1, updatedVehicle);
      }
      this.showEditVehicleModal = false;
    },
    viewServiceHistory(vehicle) {
      // Navigate to service history for this vehicle
      this.$router.push('/history')
    },
    editVehicle(vehicle) {
      // Copy vehicle data to editingVehicle
      this.editingVehicle = {
        id: vehicle.id,
        brand: vehicle.brand,
        model: vehicle.model,
        year: vehicle.year,
        type: vehicle.type || 'car',
        licensePlateData: this.parseLicensePlate(vehicle.licensePlate),
        currentMileage: vehicle.currentMileage,
        lastServiceDate: vehicle.lastServiceDate || ''
      };
      this.showEditVehicleModal = true;
    },
    // Format license plate data into a string
    formatLicensePlate(plateData, type) {
      if (!plateData) return '';
      
      const { firstTwoDigits, letter, nextThreeDigits, lastTwoDigits, 
              motorcycleDigits, motorcycleLetter, motorcycleLastDigits } = plateData;
      
      // Use the provided type parameter to determine format
      if (type === 'motorcycle') {
        return `${motorcycleDigits.join('')}${motorcycleLetter}${motorcycleLastDigits.join('')}`;
      }
      
      // Default to car plate format
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
      
      // Try to parse as car plate (format like "123ب456-78")
      const carMatch = plateString.match(/^(\d{2})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})-(\d{2})$/);
      if (carMatch) {
        return {
          firstTwoDigits: [carMatch[1].charAt(0), carMatch[1].charAt(1)],
          letter: carMatch[2],
          nextThreeDigits: [carMatch[3].charAt(0), carMatch[3].charAt(1), carMatch[3].charAt(2)],
          lastTwoDigits: [carMatch[4].charAt(0), carMatch[4].charAt(1)],
          motorcycleDigits: ['', '', ''],
          motorcycleLetter: '',
          motorcycleLastDigits: ['', '', '']
        };
      }
      
      // Try to parse as motorcycle plate (format like "12345678")
      const motorcycleMatch = plateString.match(/^(\d{3})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})$/);
      if (motorcycleMatch) {
        return {
          firstTwoDigits: ['', ''],
          letter: '',
          nextThreeDigits: ['', '', ''],
          lastTwoDigits: ['', ''],
          motorcycleDigits: [motorcycleMatch[1].charAt(0), motorcycleMatch[1].charAt(1), motorcycleMatch[1].charAt(2)],
          motorcycleLetter: motorcycleMatch[2],
          motorcycleLastDigits: [motorcycleMatch[3].charAt(0), motorcycleMatch[3].charAt(1), motorcycleMatch[3].charAt(2)]
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
