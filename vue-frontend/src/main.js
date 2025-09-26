import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import datePicker from '@alireza-ab/vue-persian-datepicker'

// Import Tailwind CSS
import './assets/css/tailwind.css'

// Persian translations
const messages = {
  fa: {
    dashboard: 'داشبورد',
    vehicles: 'خودروها',
    services: 'سرویس‌ها',
    history: 'تاریخچه',
    emergency: 'اضطراری',
    admin: 'مدیریت',
    signIn: 'ورود',
    signOut: 'خروج',
    totalVehicles: 'تعداد خودروها',
    upcomingServices: 'سرویس‌های آتی',
    pendingEmergencies: 'اضطراری‌های در انتظار',
    totalExpenses: 'مجموع هزینه‌ها',
    recentServices: 'سرویس‌های اخیر',
    addNewVehicle: 'افزودن خودرو جدید',
    addVehicle: 'افزودن خودرو',
    scheduleService: 'ثبت سرویس',
    serviceHistory: 'تاریخچه سرویس',
    requestEmergencyService: 'درخواست سرویس اضطراری',
    emergencyContacts: 'شماره‌های اضطراری',
    recentRequests: 'درخواست‌های اخیر',
    name: 'نام',
    phone: 'تلفن',
    vehicle: 'خودرو',
    licensePlate: 'شماره پلاک',
    location: 'محل',
    emergencyType: 'نوع اضطراری',
    description: 'توضیحات',
    call: 'تماس',
    police: 'پلیس',
    ambulance: 'آمبولانس',
    roadsideAssistance: 'کمک‌جوی جاده‌ای',
    searchServices: 'جستجوی سرویس‌ها',
    allVehicles: 'همه خودروها',
    search: 'جستجو',
    year: 'سال',
    currentMileage: 'کیلومتر فعلی',
    lastService: 'آخرین سرویس',
    edit: 'ویرایش',
    oilChange: 'تعویض روغن',
    tireRotation: 'چرخش تایر',
    brakeInspection: 'بررسی ترمز',
    engineTuneUp: 'تعمیر موتور',
    completed: 'تکمیل شده',
    inProgress: 'در حال انجام',
    scheduled: 'زمان‌بندی شده',
    dueSoon: 'نزدیک به سررسید',
    pending: 'در انتظار',
    serviceName: 'نام سرویس',
    cost: 'هزینه',
    date: 'تاریخ',
    parts: 'قطعات',
    flatTire: 'ترکیدگی لاستیک',
    engineProblem: 'مشکل موتور',
    accident: 'تصادف',
    runningOutOfFuel: 'تمام شدن سوخت',
    lockout: 'قفل شدن درون خودرو',
    other: 'سایر',
    users: 'کاربران',
    serviceCenters: 'مراکز سرویس',
    pricing: 'قیمت‌گذاری',
    reports: 'گزارش‌ها',
    settings: 'تنظیمات',
    adminPanel: 'پنل مدیریت',
    deleteUser: 'حذف کاربر',
    editUser: 'ویرایش کاربر',
    addUser: 'افزودن کاربر',
    deleteVehicle: 'حذف خودرو',
    editVehicle: 'ویرایش خودرو',
    deleteService: 'حذف سرویس',
    editService: 'ویرایش سرویس',
    deleteEmergency: 'حذف اضطراری',
    editEmergency: 'ویرایش اضطراری',
    brand: 'برند',
    model: 'مدل',
    status: 'وضعیت',
    actions: 'عملیات',
    save: 'ذخیره',
    cancel: 'لغو',
    submit: 'ثبت',
    useGPS: 'استفاده از GPS',
    delete: 'حذف',
    notSet: 'تنظیم نشده',
    markAsCompleted: 'علامت‌گذاری به عنوان تکمیل شده',
    // Adding missing translation keys
    scheduleNewService: 'ثبت سرویس جدید',
    selectService: 'انتخاب سرویس',
    brakePadReplacement: 'تعویض لنت ترمز',
    batteryReplacement: 'تعویض باتری',
    coolingSystemInspection: 'بررسی سیستم خنک کننده',
    selectVehicle: 'انتخاب خودرو'
  }
}

const i18n = createI18n({
  locale: 'fa',
  fallbackLocale: 'fa',
  messages,
})

const app = createApp(App)

app.use(router)
app.use(i18n)
app.component('date-picker', datePicker)

app.mount('#app')