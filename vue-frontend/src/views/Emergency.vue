<template>
  <div class="space-y-6">
    <div class="text-center py-12">
      <div class="mx-auto w-24 h-24 bg-destructive/10 rounded-full flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-destructive" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h1 class="text-3xl font-bold mt-6">{{ $t('emergencyAssistance') }}</h1>
      <p class="text-muted-foreground mt-2 max-w-2xl mx-auto">
        {{ $t('emergencyAssistanceDescription') }}
      </p>
      <button @click="showEmergencyForm = true" class="mt-6 bg-destructive text-destructive-foreground px-6 py-3 rounded-md hover:bg-destructive/90 font-medium">
        {{ $t('requestEmergencyHelp') }}
      </button>
    </div>
    
    <!-- Emergency Request Form -->
    <div v-if="showEmergencyForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-semibold mb-4">{{ $t('emergencyRequestForm') }}</h2>
        <form @submit.prevent="submitEmergencyRequest" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('fullName') }}</label>
              <input v-model="emergencyRequest.name" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('phoneNumber') }}</label>
              <input v-model="emergencyRequest.phoneNumber" type="tel" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('vehicle') }}</label>
              <input v-model="emergencyRequest.vehicle" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('licensePlate') }}</label>
              <IranianLicensePlate 
                v-model="emergencyRequest.licensePlateData" 
                :type="emergencyRequest.vehicleType"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('vehicleType') }}</label>
              <select v-model="emergencyRequest.vehicleType" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
                <option value="car">{{ $t('car') }}</option>
                <option value="motorcycle">{{ $t('motorcycle') }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-1">{{ $t('problemType') }}</label>
              <select v-model="emergencyRequest.type" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
                <option value="">{{ $t('selectProblemType') }}</option>
                <option value="flatTire">{{ $t('flatTire') }}</option>
                <option value="engineProblem">{{ $t('engineProblem') }}</option>
                <option value="batteryDead">{{ $t('batteryDead') }}</option>
                <option value="fuelDelivery">{{ $t('fuelDelivery') }}</option>
                <option value="locksmith">{{ $t('locksmith') }}</option>
                <option value="accident">{{ $t('accident') }}</option>
                <option value="other">{{ $t('other') }}</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('location') }}</label>
            <input v-model="emergencyRequest.location" type="text" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">{{ $t('description') }}</label>
            <textarea v-model="emergencyRequest.description" rows="3" class="w-full border border-border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50"></textarea>
          </div>
          
          <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 sm:space-x-reverse pt-4">
            <button type="submit" class="flex-1 bg-destructive text-destructive-foreground py-2 rounded-md hover:bg-destructive/90">
              {{ $t('submitRequest') }}
            </button>
            <button @click="showEmergencyForm = false" type="button" class="flex-1 border border-border py-2 rounded-md hover:bg-muted">
              {{ $t('cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Success Message -->
    <div v-if="showSuccessMessage" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-card border border-border rounded-lg p-6 w-full max-w-md text-center">
        <div class="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold mt-4">{{ $t('requestSubmitted') }}</h3>
        <p class="text-muted-foreground mt-2">
          {{ $t('emergencyRequestSubmitted') }}
        </p>
        <button @click="showSuccessMessage = false" class="mt-6 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90">
          {{ $t('ok') }}
        </button>
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
      showEmergencyForm: false,
      showSuccessMessage: false,
      emergencyRequest: {
        name: '',
        phoneNumber: '',
        vehicle: '',
        licensePlateData: {
          plaqueLeftNo: '',
          plaqueMiddleChar: '',
          plaqueRightNo: '',
          plaqueSerial: ''
        },
        location: '',
        type: '',
        description: '',
        vehicleType: 'car'
      }
    }
  },
  methods: {
    submitEmergencyRequest() {
      // Form validation
      if (this.emergencyRequest.name && 
          this.emergencyRequest.phoneNumber && 
          this.emergencyRequest.vehicle && 
          this.emergencyRequest.location && 
          this.emergencyRequest.type) {
        
        // In a real app, you would send this data to your backend
        console.log('Emergency request submitted:', {
          ...this.emergencyRequest,
          licensePlate: this.formatLicensePlate(this.emergencyRequest.licensePlateData)
        });
        
        // Show success message
        this.showSuccessMessage = true;
        this.showEmergencyForm = false;
        
        // Reset form
        this.emergencyRequest = {
          name: '',
          phoneNumber: '',
          vehicle: '',
          licensePlateData: {
            plaqueLeftNo: '',
            plaqueMiddleChar: '',
            plaqueRightNo: '',
            plaqueSerial: ''
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
      
      const { plaqueLeftNo, plaqueMiddleChar, plaqueRightNo, plaqueSerial } = plateData;
      
      // Check if it's a motorcycle
      if (this.emergencyRequest.vehicleType === 'motorcycle') {
        return `${plaqueLeftNo}${plaqueMiddleChar}${plaqueRightNo}`;
      }
      
      // Default to car plate format
      return `${plaqueLeftNo}${plaqueMiddleChar}${plaqueRightNo}-${plaqueSerial}`;
    }
  }
}
</script>