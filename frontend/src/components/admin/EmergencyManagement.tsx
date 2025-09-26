"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MoreHorizontal, Search, Plus, Edit, Trash, AlertTriangle } from "lucide-react";
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
import ClientOnly from "@/components/ClientOnly";

// Mock emergency data
const mockEmergencies = [
  {
    id: "1",
    userId: "1",
    userName: "علیرضا محمدی",
    vehicleInfo: "پژو 206 - 123ب456",
    latitude: 35.6892,
    longitude: 51.3890,
    locationAddress: "تهران، خیابان ولیعصر",
    description: "پنچری لاستیک",
    status: "resolved",
    responder: "خدمات اضطراری تهران",
    createdAt: "1402/08/22 14:30",
    resolvedAt: "1402/08/22 15:15",
  },
  {
    id: "2",
    userId: "2",
    userName: "فاطمه رضوی",
    vehicleInfo: "پراید 131 - 789الف123",
    latitude: 35.7152,
    longitude: 51.4084,
    locationAddress: "تهران، میدان ونک",
    description: "خرابی موتور",
    status: "pending",
    responder: null,
    createdAt: "1402/08/22 16:45",
    resolvedAt: null,
  },
  {
    id: "3",
    userId: "3",
    userName: "حسام کریمی",
    vehicleInfo: "سمند سورن - 456ج789",
    latitude: 35.6961,
    longitude: 51.4234,
    locationAddress: "تهران، خیابان شریعتی",
    description: "آب رادیاتور کم است",
    status: "accepted",
    responder: "تعمیرگاه شریعتی",
    createdAt: "1402/08/22 10:20",
    resolvedAt: null,
  },
  {
    id: "4",
    userId: "4",
    userName: "مریم احمدی",
    vehicleInfo: "دنا پلاس - 246ت357",
    latitude: 35.7234,
    longitude: 51.3987,
    locationAddress: "تهران، پل سیدخندان",
    description: "لامپ روشنایی خراب",
    status: "resolved",
    responder: "خدمات جوال خودرو",
    createdAt: "1402/08/21 09:15",
    resolvedAt: "1402/08/21 09:45",
  },
];

// Chart data
const statusData = [
  { name: 'در انتظار', value: mockEmergencies.filter(e => e.status === 'pending').length },
  { name: 'در حال انجام', value: mockEmergencies.filter(e => e.status === 'accepted').length },
  { name: 'حل شده', value: mockEmergencies.filter(e => e.status === 'resolved').length },
  { name: 'لغو شده', value: mockEmergencies.filter(e => e.status === 'cancelled').length },
];

// Mock daily data for the last week
const dailyData = [
  { date: '1402/08/16', requests: 2 },
  { date: '1402/08/17', requests: 1 },
  { date: '1402/08/18', requests: 3 },
  { date: '1402/08/19', requests: 2 },
  { date: '1402/08/20', requests: 4 },
  { date: '1402/08/21', requests: 3 },
  { date: '1402/08/22', requests: 4 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export function EmergencyManagement() {
  const [emergencies, setEmergencies] = useState(mockEmergencies);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredEmergencies = emergencies.filter(emergency => 
    emergency.userName.includes(searchTerm) || 
    emergency.vehicleInfo.includes(searchTerm) ||
    emergency.locationAddress.includes(searchTerm) ||
    emergency.description.includes(searchTerm)
  );

  const handleDeleteEmergency = (emergencyId: string) => {
    setEmergencies(emergencies.filter(emergency => emergency.id !== emergencyId));
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "pending":
        return <Badge variant="secondary">در انتظار</Badge>;
      case "accepted":
        return <Badge variant="default">در حال انجام</Badge>;
      case "resolved":
        return <Badge variant="default">حل شده</Badge>;
      case "cancelled":
        return <Badge variant="destructive">لغو شده</Badge>;
      default:
        return <Badge variant="secondary">نامشخص</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">مدیریت اضطراری</h1>
          <p className="text-muted-foreground">مدیریت درخواست‌های اضطراری کاربران</p>
        </div>
        <Button>
          <Plus className="ml-2 h-4 w-4" />
          افزودن ارائه‌دهنده خدمات
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل درخواست‌ها</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{emergencies.length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">همه درخواست‌های اضطراری</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">در انتظار</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{emergencies.filter(e => e.status === 'pending').length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">درخواست‌های در انتظار پاسخ</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">در حال انجام</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{emergencies.filter(e => e.status === 'accepted').length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">درخواست‌های در حال انجام</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">حل شده</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{emergencies.filter(e => e.status === 'resolved').length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">درخواست‌های حل شده</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>وضعیت درخواست‌ها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => [value.toLocaleString('fa-IR'), 'درخواست']} />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>درخواست‌های اضطراری (۷ روز اخیر)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={dailyData}>
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
      </div>

      <div className="flex items-center space-x-2 rtl:space-x-reverse">
        <div className="relative flex-1">
          <Search className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="جستجوی درخواست‌های اضطراری..."
            className="pr-10 text-right"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <ClientOnly>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>کاربر</TableHead>
                <TableHead>خودرو</TableHead>
                <TableHead>موقعیت</TableHead>
                <TableHead>شرح مشکل</TableHead>
                <TableHead>وضعیت</TableHead>
                <TableHead>پاسخ‌دهنده</TableHead>
                <TableHead>تاریخ ثبت</TableHead>
                <TableHead>تاریخ حل</TableHead>
                <TableHead className="text-right">عملیات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEmergencies.map((emergency) => (
                <TableRow key={emergency.id}>
                  <TableCell>
                    <div className="font-medium">{emergency.userName}</div>
                  </TableCell>
                  <TableCell>{emergency.vehicleInfo}</TableCell>
                  <TableCell>
                    <div className="max-w-[200px] truncate" title={emergency.locationAddress}>
                      {emergency.locationAddress}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="max-w-[200px] truncate" title={emergency.description}>
                      {emergency.description}
                    </div>
                  </TableCell>
                  <TableCell>{getStatusBadge(emergency.status)}</TableCell>
                  <TableCell>
                    {emergency.responder || "-"}
                  </TableCell>
                  <TableCell>{emergency.createdAt}</TableCell>
                  <TableCell>
                    {emergency.resolvedAt || "-"}
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <span className="sr-only">باز کردن منو</span>
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>عملیات</DropdownMenuLabel>
                        <DropdownMenuItem>
                          <Edit className="ml-2 h-4 w-4" />
                          ویرایش
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDeleteEmergency(emergency.id)}>
                          <Trash className="ml-2 h-4 w-4" />
                          حذف
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </ClientOnly>
    </div>
  );
}