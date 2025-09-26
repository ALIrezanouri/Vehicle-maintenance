<template>
  <div class="flex items-center space-x-2 space-x-reverse">
    <span :class="['w-3 h-3 rounded-full', { 'bg-green-500': isHealthy, 'bg-red-500': !isHealthy }]"></span>
    <span class="text-sm text-muted-foreground">{{ statusMessage }}</span>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BackendStatusIndicator',
  data() {
    return {
      isHealthy: false,
      statusMessage: 'Checking backend status...',
      backendUrl: 'http://localhost:8000/health' // Assuming backend runs on port 8000
    };
  },
  created() {
    this.checkBackendStatus();
    // Check status every 10 seconds
    setInterval(this.checkBackendStatus, 10000); 
  },
  methods: {
    async checkBackendStatus() {
      try {
        const response = await axios.get(this.backendUrl);
        if (response.data && response.data.status === 'healthy') {
          this.isHealthy = true;
          this.statusMessage = 'Backend is healthy';
        } else {
          this.isHealthy = false;
          this.statusMessage = 'Backend is unhealthy';
        }
      } catch (error) {
        this.isHealthy = false;
        this.statusMessage = 'Backend connection failed';
        console.error('Error checking backend status:', error);
      }
    }
  }
};
</script>

<style scoped>
/* No specific styles needed beyond Tailwind classes */
</style>
