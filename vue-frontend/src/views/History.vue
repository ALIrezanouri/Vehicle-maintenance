<template>
  <div class="space-y-6">
    <h1 class="text-2xl sm:text-3xl font-bold">{{ $t('history') }}</h1>
    
    <div class="bg-card border border-border rounded-lg shadow-sm overflow-hidden">
      <div class="border-b border-border p-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <h2 class="text-lg sm:text-xl font-semibold">{{ $t('serviceHistory') }}</h2>
          <div class="flex flex-col sm:flex-row gap-2">
            <input 
              type="text" 
              :placeholder="$t('searchServices')" 
              class="border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              v-model="searchQuery"
            >
            <select class="border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option>{{ $t('allVehicles') }}</option>
              <option>پژو 206 - 123ب456</option>
              <option>سمند - 345ب678</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="divide-y divide-border">
        <div v-for="record in filteredHistory" :key="record.id" class="p-4 hover:bg-muted/50">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
            <div>
              <h3 class="font-medium">{{ record.serviceName }}</h3>
              <p class="text-sm text-muted-foreground">{{ record.vehicle }}</p>
            </div>
            <div class="text-right">
              <p class="font-medium">{{ record.cost.toLocaleString() }} ریال</p>
              <p class="text-sm text-muted-foreground">{{ record.date }}</p>
            </div>
          </div>
          
          <div class="mt-2 flex flex-wrap gap-2">
            <span v-for="part in record.parts" :key="part" 
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-muted/20 text-muted-foreground">
              {{ part }}
            </span>
          </div>
          
          <div class="mt-3 text-sm">
            <p>{{ record.description }}</p>
          </div>
          
          <div class="mt-4 flex flex-col sm:flex-row sm:space-x-2 sm:space-x-reverse gap-2">
            <button class="px-3 py-1 bg-primary text-primary-foreground rounded text-sm hover:bg-primary/90">
              {{ $t('edit') }}
            </button>
            <button class="px-3 py-1 border border-border rounded text-sm hover:bg-muted">
              {{ $t('deleteService') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History',
  data() {
    return {
      searchQuery: '',
      history: [
        {
          id: 1,
          serviceName: 'تعویض روغن',
          vehicle: 'پژو 206 - 123ب456',
          cost: 450000,
          date: '1403/05/12',
          parts: ['روغن موتور', 'فیلتر روغن'],
          description: 'تعویض روغن موتور و فیلتر. استفاده از روغن با کیفیت بالا.'
        },
        {
          id: 2,
          serviceName: 'چرخش تایر',
          vehicle: 'سمند - 345ب678',
          cost: 200000,
          date: '1403/04/28',
          parts: [],
          description: 'چرخش کامل تایرها برای فرسایش یکنواخت.'
        },
        {
          id: 3,
          serviceName: 'بررسی ترمز',
          vehicle: 'پژو 206 - 123ب456',
          cost: 350000,
          date: '1403/03/15',
          parts: ['صفحه کلاچ'],
          description: 'تعویض صفحه کلاچ جلو. صفحه کلاچ عقب هنوز در شرایط خوبی است.'
        }
      ]
    }
  },
  computed: {
    filteredHistory() {
      if (!this.searchQuery) {
        return this.history
      }
      
      const query = this.searchQuery.toLowerCase()
      return this.history.filter(record => 
        record.serviceName.toLowerCase().includes(query) ||
        record.vehicle.toLowerCase().includes(query) ||
        record.description.toLowerCase().includes(query)
      )
    }
  }
}
</script>