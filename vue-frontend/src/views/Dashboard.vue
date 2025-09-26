<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <h1 class="text-2xl sm:text-3xl font-bold">{{ $t('dashboard') }}</h1>
      <button @click="goToVehicles" class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 w-full sm:w-auto">
        {{ $t('addNewVehicle') }}
      </button>
    </div>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h3 class="text-base sm:text-lg font-semibold mb-2">{{ $t('totalVehicles') }}</h3>
        <p class="text-2xl sm:text-3xl font-bold text-primary">5</p>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h3 class="text-base sm:text-lg font-semibold mb-2">{{ $t('upcomingServices') }}</h3>
        <p class="text-2xl sm:text-3xl font-bold text-primary">3</p>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h3 class="text-base sm:text-lg font-semibold mb-2">{{ $t('pendingEmergencies') }}</h3>
        <p class="text-2xl sm:text-3xl font-bold text-primary">1</p>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h3 class="text-base sm:text-lg font-semibold mb-2">{{ $t('totalExpenses') }}</h3>
        <p class="text-2xl sm:text-3xl font-bold text-primary">2,450,000</p>
        <p class="text-xs sm:text-sm text-muted-foreground">ریال</p>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h2 class="text-lg sm:text-xl font-semibold mb-4">{{ $t('recentServices') }}</h2>
        <div class="space-y-4">
          <div v-for="service in recentServices" :key="service.id" class="border-b border-border pb-4 last:border-0 last:pb-0">
            <div class="flex justify-between flex-wrap gap-2">
              <h3 class="font-medium">{{ service.name }}</h3>
              <span class="text-sm text-muted-foreground">{{ service.date }}</span>
            </div>
            <p class="text-sm text-muted-foreground">{{ service.vehicle }}</p>
            <p class="text-sm mt-1">{{ service.description }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-card border border-border rounded-lg p-4 sm:p-6 shadow-sm">
        <h2 class="text-lg sm:text-xl font-semibold mb-4">{{ $t('upcomingServices') }}</h2>
        <div class="space-y-4">
          <div v-for="service in upcomingServices" :key="service.id" class="border-b border-border pb-4 last:border-0 last:pb-0">
            <div class="flex justify-between flex-wrap gap-2">
              <h3 class="font-medium">{{ service.name }}</h3>
              <span class="text-sm text-muted-foreground">{{ service.date }}</span>
            </div>
            <p class="text-sm text-muted-foreground">{{ service.vehicle }}</p>
            <div class="flex items-center mt-2">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-warning/20 text-warning">
                {{ service.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      recentServices: [
        {
          id: 1,
          name: 'تعویض روغن',
          date: '1403/05/12',
          vehicle: 'پژو 206 - 123ب456',
          description: 'تعویض روغن موتور و فیلتر'
        },
        {
          id: 2,
          name: 'چرخش تایر',
          date: '1403/04/28',
          vehicle: 'سمند - 345ب678',
          description: 'چرخش کامل تایرها'
        }
      ],
      upcomingServices: [
        {
          id: 1,
          name: 'بررسی ترمز',
          date: '1403/06/05',
          vehicle: 'پژو 206 - 123ب456',
          status: 'نزدیک به سررسید'
        },
        {
          id: 2,
          name: 'تعمیر موتور',
          date: '1403/06/15',
          vehicle: 'سمند - 345ب678',
          status: 'زمان‌بندی شده'
        }
      ]
    }
  },
  methods: {
    goToVehicles() {
      this.$router.push('/vehicles')
    }
  }
}
</script>