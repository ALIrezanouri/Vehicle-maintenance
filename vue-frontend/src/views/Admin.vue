<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold">{{ $t('adminPanel') }}</h1>
    </div>
    
    <div class="bg-card border border-border rounded-lg overflow-hidden">
      <!-- Tabs -->
      <div class="border-b border-border">
        <nav class="flex -mb-px">
          <button 
            @click="activeTab = 'dashboard'" 
            class="py-4 px-6 text-center border-b-2 font-medium text-sm"
            :class="activeTab === 'dashboard' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'"
          >
            {{ $t('dashboard') }}
          </button>
          <button 
            @click="activeTab = 'vehicles'" 
            class="py-4 px-6 text-center border-b-2 font-medium text-sm"
            :class="activeTab === 'vehicles' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'"
          >
            {{ $t('vehicles') }}
          </button>
          <button 
            @click="activeTab = 'services'" 
            class="py-4 px-6 text-center border-b-2 font-medium text-sm"
            :class="activeTab === 'services' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'"
          >
            {{ $t('services') }}
          </button>
          <button 
            @click="activeTab = 'emergency'" 
            class="py-4 px-6 text-center border-b-2 font-medium text-sm"
            :class="activeTab === 'emergency' ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground'"
          >
            {{ $t('emergencyRequests') }}
          </button>
        </nav>
      </div>
      
      <!-- Dashboard Tab -->
      <div v-if="activeTab === 'dashboard'" class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-muted rounded-lg p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary/10 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-muted-foreground">{{ $t('totalVehicles') }}</p>
                <p class="text-2xl font-semibold">{{ vehicles.length }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-muted rounded-lg p-6">
            <div class="flex items-center">
              <div class="p-3 bg-green-500/10 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-muted-foreground">{{ $t('completedServices') }}</p>
                <p class="text-2xl font-semibold">{{ completedServicesCount }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-muted rounded-lg p-6">
            <div class="flex items-center">
              <div class="p-3 bg-yellow-500/10 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-muted-foreground">{{ $t('scheduledServices') }}</p>
                <p class="text-2xl font-semibold">{{ scheduledServicesCount }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-muted rounded-lg p-6">
            <div class="flex items-center">
              <div class="p-3 bg-destructive/10 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-destructive" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-muted-foreground">{{ $t('pendingRequests') }}</p>
                <p class="text-2xl font-semibold">{{ pendingRequestsCount }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-muted rounded-lg p-6">
            <h3 class="text-lg font-semibold mb-4">{{ $t('serviceStatistics') }}</h3>
            <div class="space-y-4">
              <div v-for="stat in serviceStats" :key="stat.type" class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span>{{ stat.type }}</span>
                  <span>{{ stat.count }} ({{ stat.percentage }}%)</span>
                </div>
                <div class="w-full bg-border rounded-full h-2">
                  <div 
                    class="bg-primary h-2 rounded-full" 
                    :style="{ width: stat.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-muted rounded-lg p-6">
            <h3 class="text-lg font-semibold mb-4">{{ $t('recentActivities') }}</h3>
            <div class="space-y-4">
              <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start">
                <div class="flex-shrink-0 p-2 bg-primary/10 rounded-full">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm">{{ activity.description }}</p>
                  <p class="text-xs text-muted-foreground">{{ activity.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Vehicles Tab -->
      <div v-if="activeTab === 'vehicles'" class="p-4">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-border">
            <thead>
              <tr>
                <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('brand') }}</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('model') }}</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider hidden sm:table-cell">{{ $t('licensePlate') }}</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('owner') }}</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('actions') }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-for="vehicle in vehicles" :key="vehicle.id">
                <td class="px-4 py-3 whitespace-nowrap">{{ vehicle.brand }}</td>
                <td class="px-4 py-3 whitespace-nowrap">{{ vehicle.model }}</td>
                <td class="px-4 py-3 whitespace-nowrap hidden sm:table-cell">
                  <IranianLicensePlate 
                    :model-value="parseLicensePlate(vehicle.licensePlate)" 
                    :type="vehicle.type || 'car'" 
                    readonly 
                    class="inline-block scale-75 origin-right"
                  />
                </td>
                <td class="px-4 py-3 whitespace-nowrap">{{ vehicle.owner }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                  <button class="text-primary hover:text-primary/80">{{ $t('edit') }}</button>
                  <button class="text-destructive hover:text-destructive/80">{{ $t('deleteVehicle') }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Services Tab -->
      <div v-if="activeTab === 'services'" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-border">
          <thead>
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('serviceName') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider hidden sm:table-cell">{{ $t('vehicle') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('cost') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider hidden sm:table-cell">{{ $t('date') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('status') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="service in services" :key="service.id">
              <td class="px-4 py-3 whitespace-nowrap">{{ service.name }}</td>
              <td class="px-4 py-3 whitespace-nowrap hidden sm:table-cell">{{ getVehicleName(service.vehicle) }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ service.cost.toLocaleString() }} ریال</td>
              <td class="px-4 py-3 whitespace-nowrap text-sm hidden sm:table-cell">{{ service.date }}</td>
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
                <button class="text-primary hover:text-primary/80">{{ $t('edit') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('delete') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Emergency Requests Tab -->
      <div v-if="activeTab === 'emergency'" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-border">
          <thead>
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('requester') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('vehicle') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider hidden sm:table-cell">{{ $t('licensePlate') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('type') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('status') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="request in emergencyRequests" :key="request.id">
              <td class="px-4 py-3 whitespace-nowrap">{{ request.requester }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ request.vehicle }}</td>
              <td class="px-4 py-3 whitespace-nowrap hidden sm:table-cell">{{ request.licensePlate }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ request.type }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="{
                  'bg-yellow-100 text-yellow-800': request.status === 'جدید',
                  'bg-blue-100 text-blue-800': request.status === 'در حال انجام',
                  'bg-green-100 text-green-800': request.status === 'تکمیل شده'
                }">
                  {{ request.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                <button class="text-primary hover:text-primary/80">{{ $t('view') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('delete') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import IranianLicensePlate from '@/components/IranianLicensePlate.vue';

export default {
  name: 'Admin',
  components: {
    IranianLicensePlate
  },
  data() {
    return {
      activeTab: 'dashboard',
      vehicles: [
        { id: 1, brand: 'پژو', model: '206', licensePlate: '59م648-88', owner: 'علی محمدی' },
        { id: 2, brand: 'سمند', model: 'SE', licensePlate: '345پ678-90', owner: 'مریم رضوی' },
        { id: 3, brand: 'دنا', model: 'Plus', licensePlate: '789ت012-34', owner: 'حسین احمدی' }
      ],
      services: [
        { id: 1, name: 'تعویض روغن', vehicle: 1, cost: 450000, date: '1403/05/12', status: 'تکمیل شده' },
        { id: 2, name: 'چرخش تایر', vehicle: 2, cost: 200000, date: '1403/04/28', status: 'تکمیل شده' },
        { id: 3, name: 'بررسی ترمز', vehicle: 1, cost: 0, date: '1403/06/05', status: 'زمان‌بندی شده' }
      ],
      emergencyRequests: [
        { id: 1, requester: 'علی محمدی', vehicle: 'پژو 206', licensePlate: '59م648-88', type: 'تخته شدن لاستیک', status: 'در حال انجام' },
        { id: 2, requester: 'مریم رضوی', vehicle: 'سمند SE', licensePlate: '345پ678-90', type: 'مشکل موتور', status: 'جدید' }
      ],
      serviceStats: [
        { type: 'تعویض روغن', count: 42, percentage: 70 },
        { type: 'چرخش تایر', count: 28, percentage: 45 },
        { type: 'بررسی ترمز', count: 18, percentage: 30 },
        { type: 'تعمیر موتور', count: 12, percentage: 20 }
      ],
      recentActivities: [
        { id: 1, icon: 'User', description: 'علی محمدی ثبت نام کرد', time: '۵ دقیقه پیش' },
        { id: 2, icon: 'Car', description: 'خودرو جدید اضافه شد: پژو 206', time: '۱ ساعت پیش' },
        { id: 3, icon: 'Wrench', description: 'سرویس جدید زمان‌بندی شد', time: '۲ ساعت پیش' },
        { id: 4, icon: 'CreditCard', description: 'پرداختی موفق: ۴۵۰,۰۰۰ ریال', time: '۳ ساعت پیش' }
      ]
    }
  },
  computed: {
    completedServicesCount() {
      return this.services.filter(service => service.status === 'تکمیل شده').length;
    },
    scheduledServicesCount() {
      return this.services.filter(service => service.status === 'زمان‌بندی شده').length;
    },
    pendingRequestsCount() {
      return this.emergencyRequests.filter(request => request.status === 'جدید').length;
    }
  },
  methods: {
    getVehicleName(vehicleId) {
      const vehicle = this.vehicles.find(v => v.id === vehicleId);
      return vehicle ? `${vehicle.brand} ${vehicle.model}` : 'نامشخص';
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