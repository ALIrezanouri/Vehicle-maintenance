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
              :type="newVehicle.type || 'car'"
            />
            <!-- Hidden input to store the formatted license plate string -->
            <input 
              type="hidden" 
              :value="formatLicensePlate(newVehicle.licensePlateData)" 
              required
            >
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
          
          <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 sm:space-x-reverse pt-4">
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
          plaqueLeftNo: '',
          plaqueMiddleChar: '',
          plaqueRightNo: '',
          plaqueSerial: ''
        },
        currentMileage: 0,
        lastServiceDate: ''
      },
      editingVehicle: {
        id: null,
        brand: '',
        model: '',
        year: '',
        type: 'car',
        licensePlateData: {
          plaqueLeftNo: '',
          plaqueMiddleChar: '',
          plaqueRightNo: '',
          plaqueSerial: ''
        },
        currentMileage: 0,
        lastServiceDate: ''
      },
      vehicles: [
        {
          id: 1,
          brand: 'پژو',
          model: '206',
          year: '1385',
          type: 'car',
          licensePlate: '59م648-88',
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
        ...this.newVehicle,
        id: this.vehicles.length + 1,
        licensePlate: this.formatLicensePlate(this.newVehicle.licensePlateData)
      };
      // Remove the licensePlateData property as we only need the formatted licensePlate
      delete vehicle.licensePlateData;
      this.vehicles.push(vehicle);
      this.newVehicle = {
        brand: '',
        model: '',
        year: '',
        type: 'car',
        licensePlateData: {
          plaqueLeftNo: '',
          plaqueMiddleChar: '',
          plaqueRightNo: '',
          plaqueSerial: ''
        },
        currentMileage: 0,
        lastServiceDate: ''
      };
      this.showAddVehicleModal = false;
    },
    updateVehicle() {
      const index = this.vehicles.findIndex(v => v.id === this.editingVehicle.id);
      if (index !== -1) {
        // Format the license plate before saving
        const updatedVehicle = {
          ...this.editingVehicle,
          licensePlate: this.formatLicensePlate(this.editingVehicle.licensePlateData)
        };
        // Remove the licensePlateData property as we only need the formatted licensePlate
        delete updatedVehicle.licensePlateData;
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
    formatLicensePlate(plateData) {
      if (!plateData) return '';
      
      const { plaqueLeftNo, plaqueMiddleChar, plaqueRightNo, plaqueSerial } = plateData;
      
      // Check if it's a motorcycle
      if (this.newVehicle?.type === 'motorcycle' || this.editingVehicle?.type === 'motorcycle') {
        return `${plaqueLeftNo}${plaqueMiddleChar}${plaqueRightNo}`;
      }
      
      // Default to car plate format
      return `${plaqueLeftNo}${plaqueMiddleChar}${plaqueRightNo}-${plaqueSerial}`;
    },
    // Parse license plate string into component data format
    parseLicensePlate(plateString) {
      if (!plateString) {
        // Return default empty plate
        return {
          plaqueLeftNo: '',
          plaqueMiddleChar: '',
          plaqueRightNo: '',
          plaqueSerial: ''
        };
      }
      
      // Try to parse as car plate (format like "123ب456-78")
      const carMatch = plateString.match(/^(\d{2})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})-(\d{2})$/);
      if (carMatch) {
        return {
          plaqueLeftNo: carMatch[1],
          plaqueMiddleChar: carMatch[2],
          plaqueRightNo: carMatch[3],
          plaqueSerial: carMatch[4]
        };
      }
      
      // Try to parse as motorcycle plate (format like "12345678")
      const motorcycleMatch = plateString.match(/^(\d{3})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})$/);
      if (motorcycleMatch) {
        return {
          plaqueLeftNo: motorcycleMatch[1],
          plaqueMiddleChar: motorcycleMatch[2],
          plaqueRightNo: motorcycleMatch[3],
          plaqueSerial: ''
        };
      }
      
      // Default empty plate
      return {
        plaqueLeftNo: '',
        plaqueMiddleChar: '',
        plaqueRightNo: '',
        plaqueSerial: ''
      };
    }
  }
}
</script>