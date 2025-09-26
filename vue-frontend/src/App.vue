<template>
  <div id="app" class="min-h-screen bg-background text-foreground" dir="rtl">
    <header class="bg-card border-b border-border">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-2 space-x-reverse">
          <div class="w-8 h-8 bg-primary rounded-full"></div>
          <h1 class="text-xl font-bold">رخداد</h1>
          <BackendStatusIndicator />
        </div>
        <!-- Mobile menu button -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen" 
          class="md:hidden text-foreground focus:outline-none"
          :aria-expanded="mobileMenuOpen"
        >
          <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <!-- Desktop navigation -->
        <nav class="hidden md:flex space-x-6 space-x-reverse">
          <router-link to="/" class="hover:text-primary">{{ $t('dashboard') }}</router-link>
          <router-link to="/vehicles" class="hover:text-primary">{{ $t('vehicles') }}</router-link>
          <router-link to="/services" class="hover:text-primary">{{ $t('services') }}</router-link>
          <router-link to="/history" class="hover:text-primary">{{ $t('history') }}</router-link>
          <router-link to="/emergency" class="hover:text-primary">{{ $t('emergency') }}</router-link>
          <router-link to="/admin" class="hover:text-primary">{{ $t('admin') }}</router-link>
        </nav>
        <div class="hidden md:flex items-center space-x-4 space-x-reverse">
          <button class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 text-sm">
            {{ $t('signIn') }}
          </button>
        </div>
      </div>
      <!-- Mobile navigation -->
      <div v-if="mobileMenuOpen" class="md:hidden px-4 py-2 border-t border-border">
        <div class="flex flex-col space-y-3 py-3">
          <router-link @click="mobileMenuOpen = false" to="/" class="hover:text-primary">{{ $t('dashboard') }}</router-link>
          <router-link @click="mobileMenuOpen = false" to="/vehicles" class="hover:text-primary">{{ $t('vehicles') }}</router-link>
          <router-link @click="mobileMenuOpen = false" to="/services" class="hover:text-primary">{{ $t('services') }}</router-link>
          <router-link @click="mobileMenuOpen = false" to="/history" class="hover:text-primary">{{ $t('history') }}</router-link>
          <router-link @click="mobileMenuOpen = false" to="/emergency" class="hover:text-primary">{{ $t('emergency') }}</router-link>
          <router-link @click="mobileMenuOpen = false" to="/admin" class="hover:text-primary">{{ $t('admin') }}</router-link>
          <button class="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 text-sm w-full">
            {{ $t('signIn') }}
          </button>
        </div>
      </div>
    </header>
    
    <main class="container mx-auto px-4 py-6">
      <router-view />
    </main>
    
    <footer class="bg-card border-t border-border py-6 mt-12">
      <div class="container mx-auto px-4 text-center text-muted-foreground text-sm">
        <p>© 2025 رخداد. تمامی حقوق محفوظ است.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import BackendStatusIndicator from '@/components/BackendStatusIndicator.vue';

export default {
  name: 'App',
  components: {
    BackendStatusIndicator
  },
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  watch: {
    '$route'() {
      // Close mobile menu when route changes
      this.mobileMenuOpen = false
    }
  }
}
</script>
