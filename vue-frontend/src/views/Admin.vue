<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <h1 class="text-2xl sm:text-3xl font-bold">{{ $t('adminPanel') }}</h1>
      <div class="flex space-x-2 space-x-reverse">
        <button class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
          {{ $t('exportData') }}
        </button>
        <button class="border border-border px-4 py-2 rounded-md hover:bg-muted">
          {{ $t('settings') }}
        </button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 text-blue-600">
            <div class="h-6 w-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
          <div class="mr-4">
            <p class="text-sm text-muted-foreground">{{ $t('totalUsers') }}</p>
            <p class="text-2xl font-bold">1,248</p>
          </div>
        </div>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 text-green-600">
            <div class="h-6 w-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </div>
          </div>
          <div class="mr-4">
            <p class="text-sm text-muted-foreground">{{ $t('totalVehicles') }}</p>
            <p class="text-2xl font-bold">2,456</p>
          </div>
        </div>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
            <div class="h-6 w-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
          </div>
          <div class="mr-4">
            <p class="text-sm text-muted-foreground">{{ $t('pendingServices') }}</p>
            <p class="text-2xl font-bold">142</p>
          </div>
        </div>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-red-100 text-red-600">
            <div class="h-6 w-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
          <div class="mr-4">
            <p class="text-sm text-muted-foreground">{{ $t('emergencyRequests') }}</p>
            <p class="text-2xl font-bold">8</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="bg-card border border-border rounded-lg shadow-sm">
      <div class="border-b border-border">
        <nav class="flex space-x-6 space-x-reverse px-6" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>
      
      <div v-if="activeTab === 'dashboard'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('statistics') }}</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-muted rounded-lg p-4">
            <h3 class="font-medium mb-4">{{ $t('servicesByType') }}</h3>
            <div class="space-y-3">
              <div v-for="stat in serviceStats" :key="stat.type" class="flex items-center justify-between">
                <span>{{ stat.type }}</span>
                <div class="flex items-center space-x-2 space-x-reverse">
                  <div class="w-24 bg-border rounded-full h-2">
                    <div 
                      class="bg-primary h-2 rounded-full" 
                      :style="{ width: stat.percentage + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm w-10">{{ stat.count }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-muted rounded-lg p-4">
            <h3 class="font-medium mb-4">{{ $t('recentActivity') }}</h3>
            <div class="space-y-4">
              <div v-for="activity in recentActivities" :key="activity.id" class="flex items-start">
                <div class="flex-shrink-0 mt-1">
                  <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <div class="h-4 w-4 text-primary">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                  </div>
                </div>
                <div class="mr-3">
                  <p class="text-sm">{{ activity.description }}</p>
                  <p class="text-xs text-muted-foreground">{{ activity.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="activeTab === 'users'" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-border">
          <thead>
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('name') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('email') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider hidden sm:table-cell">{{ $t('phoneNumber') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('status') }}</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">{{ $t('actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-for="user in users" :key="user.id">
              <td class="px-4 py-3 whitespace-nowrap">{{ user.name }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ user.email }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-sm hidden sm:table-cell">{{ user.phoneNumber }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  user.status === 'فعال' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                ]">
                  {{ user.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                <button class="text-primary hover:text-primary/80">{{ $t('edit') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('deleteUser') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="activeTab === 'vehicles'" class="overflow-x-auto">
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
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  service.status === 'تکمیل شده' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                ]">
                  {{ service.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                <button class="text-primary hover:text-primary/80">{{ $t('edit') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('deleteService') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
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
              <td class="px-4 py-3 whitespace-nowrap hidden sm:table-cell">
                <IranianLicensePlate 
                  :model-value="parseLicensePlate(request.licensePlate)" 
                  :type="request.vehicleType || 'car'" 
                  readonly 
                  class="inline-block scale-75 origin-right"
                />
              </td>
              <td class="px-4 py-3 whitespace-nowrap">{{ request.type }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  request.status === 'تکمیل شده' ? 'bg-green-100 text-green-800' : 
                  request.status === 'در حال انجام' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'
                ]">
                  {{ request.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm space-x-2 space-x-reverse">
                <button class="text-primary hover:text-primary/80">{{ $t('view') }}</button>
                <button class="text-destructive hover:text-destructive/80">{{ $t('cancel') }}</button>
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
// Icons from lucide-vue-next are replaced with SVG paths

export default {
  name: 'Admin',
  components: {
    IranianLicensePlate
  },
  data() {
    return {
      activeTab: 'dashboard',
      tabs: [
        { id: 'dashboard', name: 'داشبورد' },
        { id: 'users', name: 'کاربران' },
        { id: 'vehicles', name: 'خودروها' },
        { id: 'services', name: 'سرویس‌ها' },
        { id: 'emergency', name: 'اضطراری' }
      ],
      users: [
        { id: 1, name: 'علی محمدی', email: 'ali@example.com', phoneNumber: '09123456789', status: 'فعال' },
        { id: 2, name: 'مریم رضوی', email: 'maryam@example.com', phoneNumber: '09129876543', status: 'فعال' },
        { id: 3, name: 'حسین احمدی', email: 'hosein@example.com', phoneNumber: '09121112233', status: 'غیرفعال' }
      ],
      vehicles: [
        { id: 1, brand: 'پژو', model: '206', licensePlate: '123ب456-78', owner: 'علی محمدی' },
        { id: 2, brand: 'سمند', model: 'SE', licensePlate: '345پ678-90', owner: 'مریم رضوی' },
        { id: 3, brand: 'دنا', model: 'Plus', licensePlate: '789ت012-34', owner: 'حسین احمدی' }
      ],
      services: [
        { id: 1, name: 'تعویض روغن', vehicle: 1, cost: 450000, date: '1403/05/12', status: 'تکمیل شده' },
        { id: 2, name: 'چرخش تایر', vehicle: 2, cost: 200000, date: '1403/04/28', status: 'تکمیل شده' },
        { id: 3, name: 'بررسی ترمز', vehicle: 1, cost: 0, date: '1403/06/05', status: 'زمان‌بندی شده' }
      ],
      emergencyRequests: [
        { id: 1, requester: 'علی محمدی', vehicle: 'پژو 206', licensePlate: '123ب456-78', type: 'تخته شدن لاستیک', status: 'در حال انجام' },
        { id: 2, requester: 'مریم رضوی', vehicle: 'سمند SE', licensePlate: '345پ678-90', type: 'مشکل موتور', status: 'جدید' }
      ],
      serviceStats: [
        { type: 'تعویض روغن', count: 42, percentage: 70 },
        { type: 'چرخش تایر', count: 28, percentage: 45 },
        { type: 'بررسی ترمز', count: 18, percentage: 30 },
        { type: 'تعمیر موتور', count: 12, percentage: 20 }
      ],
      recentActivities: [
        { id: 1, description: 'علی محمدی ثبت نام کرد', time: '۵ دقیقه پیش' },
        { id: 2, description: 'خودرو جدید اضافه شد: پژو 206', time: '۱ ساعت پیش' },
        { id: 3, description: 'سرویس جدید زمان‌بندی شد', time: '۲ ساعت پیش' },
        { id: 4, description: 'پرداختی موفق: ۴۵۰,۰۰۰ ریال', time: '۳ ساعت پیش' }
      ]
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
    },
    viewEmergencyRequest(request) {
      alert('مشاهده درخواست اضطراری: ' + request.requester);
    },
    cancelEmergencyRequest(request) {
      if (confirm('آیا از لغو این درخواست اطمینان دارید؟')) {
        alert('درخواست لغو شد: ' + request.requester);
      }
    }
  }
}
</script>