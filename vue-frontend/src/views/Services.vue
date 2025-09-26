<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold">{{ $t('services') }}</h1>
      <button @click="showScheduleModal = true" class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
        {{ $t('scheduleService') }}
      </button>
    </div>
    
    <div class="bg-card border border-border rounded-lg p-6">
      <h2 class="text-xl font-semibold mb-4">{{ $t('upcomingServices') }}</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-border">
          <thead>
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('serviceName') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('vehicle') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('cost') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('date') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('status') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="service in services" :key="service.id">
              <td class="px-4 py-3 whitespace-nowrap">{{ service.name }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ getVehicleName(service.vehicle) }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ service.cost ? service.cost.toLocaleString() + ' ریال' : $t('free') }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-sm">{{ service.date }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="{
                  'bg-yellow-100 text-yellow-800': service.status === 'زمان‌بندی شده',
                  'bg-green-100 text-green-800': service.status === 'تکمیل شده',
                  'bg-blue-100 text-blue-800': service.status === 'در حال انجام'
                }">
                  {{ service.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                <button @click="editService(service)" class="text-primary hover:text-primary/80">{{ $t('edit') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('cancel') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Schedule Service Modal -->
    <div v-if="showScheduleModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">{{ $t('scheduleService') }}</h2>
        <form @submit.prevent="scheduleService" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('serviceName') }}</label>
            <input v-model="newService.name" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
            <select v-model="newService.vehicle" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectVehicle') }}</option>
              <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                {{ vehicle.brand }} {{ vehicle.model }} - {{ formatLicensePlateForDisplay(vehicle.licensePlate) }}
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
              {{ $t('schedule') }}
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
            <input v-model="editingService.name" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
            <select v-model="editingService.vehicle" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
              <option value="">{{ $t('selectVehicle') }}</option>
              <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">
                {{ vehicle.brand }} {{ vehicle.model }} - {{ formatLicensePlateForDisplay(vehicle.licensePlate) }}
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
          licensePlate: '59م648-88'
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
    scheduleService() {
      const service = {
        ...this.newService,
        id: this.services.length + 1,
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
    updateService() {
      const index = this.services.findIndex(s => s.id === this.editingService.id);
      if (index !== -1) {
        this.services.splice(index, 1, {...this.editingService});
      }
      this.showEditModal = false;
    },
    editService(service) {
      this.editingService = {...service};
      this.showEditModal = true;
    },
    getVehicleName(vehicleId) {
      const vehicle = this.vehicles.find(v => v.id === vehicleId);
      return vehicle ? `${vehicle.brand} ${vehicle.model}` : 'نامشخص';
    },
    formatLicensePlateForDisplay(licensePlate) {
      // Parse the license plate and format it for display
      if (!licensePlate) return '';
      
      // Try to parse as car plate (format like "123ب456-78")
      const carMatch = licensePlate.match(/^(\d{2})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})-(\d{2})$/);
      if (carMatch) {
        return `${carMatch[1]}${carMatch[2]}${carMatch[3]}-${carMatch[4]}`;
      }
      
      // Try to parse as motorcycle plate (format like "12345678")
      const motorcycleMatch = licensePlate.match(/^(\d{3})([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d{3})$/);
      if (motorcycleMatch) {
        return `${motorcycleMatch[1]}${motorcycleMatch[2]}${motorcycleMatch[3]}`;
      }
      
      // Return as is if it doesn't match any pattern
      return licensePlate;
    }
  }
}
</script>
