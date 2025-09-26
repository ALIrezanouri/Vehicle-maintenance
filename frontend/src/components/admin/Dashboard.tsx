"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Users, 
  Car, 
  Wrench, 
  Calendar, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from "recharts";

// Mock data for admin dashboard
const userData = [
  { name: 'فر', users: 400 },
  { name: 'آد', users: 300 },
  { name: 'خرد', users: 200 },
  { name: 'تی', users: 278 },
  { name: 'مر', users: 189 },
  { name: 'شه', users: 239 },
];

const vehicleData = [
  { name: 'پژو', vehicles: 240 },
  { name: 'پراید', vehicles: 139 },
  { name: 'سمند', vehicles: 380 },
  { name: 'دنا', vehicles: 200 },
  { name: 'آریسان', vehicles: 148 },
  { name: 'جیلی', vehicles: 131 },
];

const serviceStatusData = [
  { name: 'تکمیل شده', value: 2330 },
  { name: 'در انتظار', value: 120 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const serviceUrgencyData = [
  { name: 'عادی', value: 1200 },
  { name: 'مهم', value: 800 },
  { name: 'فوری', value: 450 },
];

const emergencyData = [
  { date: '1402/08/15', requests: 3 },
  { date: '1402/08/16', requests: 5 },
  { date: '1402/08/17', requests: 2 },
  { date: '1402/08/18', requests: 7 },
  { date: '1402/08/19', requests: 4 },
  { date: '1402/08/20', requests: 6 },
  { date: '1402/08/21', requests: 5 },
  { date: '1402/08/22', requests: 5 },
];

export function AdminDashboard() {
  const [stats, setStats] = useState({
    totalUsers: 1240,
    totalVehicles: 890,
    totalServices: 2450,
    pendingServices: 120,
    completedServices: 2330,
    upcomingServices: 89,
    emergencyRequests: 5,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">داشبورد مدیریت</h1>
        <p className="text-muted-foreground">خلاصه عملکرد سیستم</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کاربران کل</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalUsers.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">افزایش ۱۲٪ نسبت به ماه گذشته</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">خودروها</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalVehicles.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">افزایش ۸٪ نسبت به ماه گذشته</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">سرویس‌های تکمیل‌شده</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedServices.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">نسبت تکمیل ۹۵٪</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">درخواست‌های اضطراری</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.emergencyRequests.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">در ۲۴ ساعت گذشته</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>رشد کاربران</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={userData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [value.toLocaleString('fa-IR'), 'کاربران']}
                    labelFormatter={(label: string) => `ماه: ${label}`}
                  />
                  <Bar dataKey="users" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>توزیع خودروها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={vehicleData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [value.toLocaleString('fa-IR'), 'خودرو']}
                    labelFormatter={(label: string) => `برند: ${label}`}
                  />
                  <Bar dataKey="vehicles" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Additional Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>درخواست‌های اضطراری (۷ روز اخیر)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={emergencyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [value.toLocaleString('fa-IR'), 'درخواست']}
                    labelFormatter={(label: string) => `تاریخ: ${label}`}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="requests" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    activeDot={{ r: 8 }} 
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>وضعیت سرویس‌ها</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsPieChart>
                    <Pie
                      data={serviceStatusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {serviceStatusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value: number) => [value.toLocaleString('fa-IR'), 'سرویس']} />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>اهمیت سرویس‌ها</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsPieChart>
                    <Pie
                      data={serviceUrgencyData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {serviceUrgencyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value: number) => [value.toLocaleString('fa-IR'), 'سرویس']} />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>فعالیت‌های اخیر</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { id: 1, user: "علیرضا محمدی", action: "خودرو جدید ثبت کرد", time: "۲ دقیقه پیش", icon: Car },
              { id: 2, user: "فاطمه رضوی", action: "سرویس را تکمیل کرد", time: "۱۵ دقیقه پیش", icon: Wrench },
              { id: 3, user: "حسام کریمی", action: "درخواست اضطراری ایجاد کرد", time: "۳۰ دقیقه پیش", icon: AlertTriangle },
              { id: 4, user: "مریم احمدی", action: "بروزرسانی پروفایل", time: "۱ ساعت پیش", icon: Users },
            ].map((item) => (
              <div key={item.id} className="flex items-center">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                  <item.icon className="h-4 w-4" />
                </div>
                <div className="mr-4 flex-1 space-y-1">
                  <p className="text-sm font-medium leading-none">
                    {item.user}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {item.action}
                  </p>
                </div>
                <div className="text-xs text-muted-foreground">
                  {item.time}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}