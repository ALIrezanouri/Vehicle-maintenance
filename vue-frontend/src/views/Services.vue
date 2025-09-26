<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold">{{ $t('services') }}</h1>
      <button @click="showScheduleModal = true" class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
        {{ $t('scheduleService') }}
      </button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="service in services" :key="service.id" class="bg-card border border-border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-semibold">{{ service.name }}</h3>
            <div class="mt-2 flex items-center space-x-2 space-x-reverse text-sm">
              <div class="h-4 w-4 text-muted-foreground">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="text-muted-foreground">{{ $t('vehicle') }}:</span>
              <span>{{ getVehicleName(service.vehicle) }}</span>
            </div>
          </div>
          <span :class="[
            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
            service.status === 'تکمیل شده' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
          ]">
            {{ service.status }}
          </span>
        </div>
        
        <div class="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div>
            <p class="text-muted-foreground">{{ $t('cost') }}</p>
            <p>{{ service.cost ? service.cost.toLocaleString() + ' ریال' : $t('notSet') }}</p>
          </div>
          <div>
            <p class="text-muted-foreground">{{ $t('date') }}</p>
            <p>{{ service.date }}</p>
          </div>
        </div>
        
        <div class="mt-6 flex space-x-3 space-x-reverse">
          <button 
            v-if="service.status === 'زمان‌بندی شده'" 
            @click="markAsCompleted(service)"
            class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90 text-sm"
          >
            {{ $t('markAsCompleted') }}
          </button>
          <button 
            v-else
            class="flex-1 bg-secondary text-secondary-foreground py-2 rounded-md hover:bg-secondary/90 text-sm"
            disabled
          >
            {{ $t('completed') }}
          </button>
          <button @click="editService(service)" class="flex-1 border border-border py-2 rounded-md hover:bg-muted text-sm">
            {{ $t('edit') }}
          </button>
          <button @click="deleteService(service)" class="flex-1 border border-border py-2 rounded-md hover:bg-muted text-sm text-destructive">
            {{ $t('delete') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Schedule Service Modal -->
    <div v-if="showScheduleModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">{{ $t('scheduleNewService') }}</h2>
        <form @submit.prevent="scheduleService" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('serviceName') }}</label>
            <select v-model="newService.name" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectService') }}</option>
              <option value="تعویض روغن">{{ $t('oilChange') }}</option>
              <option value="چرخش تایر">{{ $t('tireRotation') }}</option>
              <option value="بررسی ترمز">{{ $t('brakeInspection') }}</option>
              <option value="تعمیر موتور">{{ $t('engineTuneUp') }}</option>
              <option value="تعویض لنت ترمز">{{ $t('brakePadReplacement') }}</option>
              <option value="تعویض باتری">{{ $t('batteryReplacement') }}</option>
              <option value="بررسی سیستم خنک کننده">{{ $t('coolingSystemInspection') }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
            <select v-model="newService.vehicle" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectVehicle') }}</option>
              <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                {{ vehicle.brand }} {{ vehicle.model }} - {{ vehicle.licensePlate }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('cost') }} (ریال)</label>
            <input v-model="newService.cost" type="number" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50">
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('date') }}</label>
            <JalaliDatePicker 
              v-model="newService.date" 
              class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          
          <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 sm:space-x-reverse pt-4">
            <button type="submit" class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90">
              {{ $t('save') }}
            </button>
            <button @click="showScheduleModal = false" type="button" class="flex-1 border border-border py-2 rounded-md hover:bg-muted">
              {{ $t('cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Edit Service Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">{{ $t('editService') }}</h2>
        <form @submit.prevent="updateService" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('serviceName') }}</label>
            <select v-model="editingService.name" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectService') }}</option>
              <option value="تعویض روغن">{{ $t('oilChange') }}</option>
              <option value="چرخش تایر">{{ $t('tireRotation') }}</option>
              <option value="بررسی ترمز">{{ $t('brakeInspection') }}</option>
              <option value="تعمیر موتور">{{ $t('engineTuneUp') }}</option>
              <option value="تعویض لنت ترمز">{{ $t('brakePadReplacement') }}</option>
              <option value="تعویض باتری">{{ $t('batteryReplacement') }}</option>
              <option value="بررسی سیستم خنک کننده">{{ $t('coolingSystemInspection') }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
            <select v-model="editingService.vehicle" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectVehicle') }}</option>
              <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                {{ vehicle.brand }} {{ vehicle.model }} - {{ vehicle.licensePlate }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('cost') }} (ریال)</label>
            <input v-model="editingService.cost" type="number" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50">
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('date') }}</label>
            <JalaliDatePicker 
              v-model="editingService.date" 
              class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          
          <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 sm:space-x-reverse pt-4">
            <button type="submit" class="flex-1 bg-primary text-primary-foreground py-2 rounded-md hover:bg-primary/90">
              {{ $t('save') }}
            </button>
            <button @click="showEditModal = false" type="button" class="flex-1 border border-border py-2 rounded-md hover:bg-muted">
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
  name: 'Services',
  components: {
    IranianLicensePlate,
    JalaliDatePicker
  },
  data() {
    return {
      showScheduleModal: false,
      showEditModal: false,
      newService: {
        name: '',
        vehicle: '',
        cost: '',
        date: null
      },
      editingService: {
        id: null,
        name: '',
        vehicle: '',
        cost: '',
        date: null
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
      services: [
        {
          id: 1,
          name: 'تعویض روغن',
          vehicle: 1,
          cost: 450000,
          date: '1403/05/12',
          status: 'تکمیل شده'
        },
        {
          id: 2,
          name: 'چرخش تایر',
          vehicle: 2,
          cost: 200000,
          date: '1403/04/28',
          status: 'تکمیل شده'
        },
        {
          id: 3,
          name: 'بررسی ترمز',
          vehicle: 1,
          cost: 0,
          date: '1403/06/05',
          status: 'زمان‌بندی شده'
        }
      ]
    }
  },
  methods: {
    getServiceStatusVariant(status) {
      switch (status) {
        case 'تکمیل شده':
          return 'secondary';
        case 'زمان‌بندی شده':
          return 'default';
        default:
          return 'default';
      }
    },
    getVehicleName(vehicleId) {
      const vehicle = this.vehicles.find(v => v.id === vehicleId);
      return vehicle ? `${vehicle.brand} ${vehicle.model}` : 'نامشخص';
    },
    scheduleService() {
      const service = {
        id: this.services.length + 1,
        name: this.newService.name,
        vehicle: this.newService.vehicle,
        cost: this.newService.cost,
        date: this.newService.date,
        status: 'زمان‌بندی شده'
      };
      this.services.push(service);
      this.newService = {
        name: '',
        vehicle: '',
        cost: '',
        date: null
      };
      this.showScheduleModal = false;
    },
    markAsCompleted(service) {
      const index = this.services.findIndex(s => s.id === service.id);
      if (index !== -1) {
        this.services[index].status = 'تکمیل شده';
      }
    },
    editService(service) {
      this.editingService = {
        id: service.id,
        name: service.name,
        vehicle: service.vehicle,
        cost: service.cost,
        date: service.date
      };
      this.showEditModal = true;
    },
    updateService() {
      const index = this.services.findIndex(s => s.id === this.editingService.id);
      if (index !== -1) {
        this.services[index] = {
          id: this.editingService.id,
          name: this.editingService.name,
          vehicle: this.editingService.vehicle,
          cost: this.editingService.cost,
          date: this.editingService.date,
          status: this.services[index].status
        };
      }
      this.showEditModal = false;
    },
    deleteService(service) {
      if (confirm('آیا از حذف این سرویس اطمینان دارید؟')) {
        const index = this.services.findIndex(s => s.id === service.id);
        if (index !== -1) {
          this.services.splice(index, 1);
        }
      }
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
