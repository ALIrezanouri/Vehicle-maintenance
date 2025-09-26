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
import { MoreHorizontal, Search, Plus, Edit, Trash, Wrench, Clock, CheckCircle } from "lucide-react";
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
  Cell
} from "recharts";
import ClientOnly from "@/components/ClientOnly";

// Mock service data
const mockServices = [
  {
    id: "1",
    vehicleId: "1",
    vehicleInfo: "پژو 206 - 123ب456",
    userName: "علیرضا محمدی",
    type: "تعویض روغن",
    name: "روغن موتور",
    interval: 5000,
    lastServiceMileage: 80000,
    lastServiceDate: "1402/07/15",
    nextServiceMileage: 85000,
    nextServiceDate: "1402/10/15",
    urgency: "normal",
    isCompleted: false,
  },
  {
    id: "2",
    vehicleId: "2",
    vehicleInfo: "پراید 131 - 789الف123",
    userName: "فاطمه رضوی",
    type: "تعویض تسمه تایم",
    name: "تسمه تایم",
    interval: 80000,
    lastServiceMileage: 35000,
    lastServiceDate: "1402/06/22",
    nextServiceMileage: 115000,
    nextServiceDate: "1404/06/22",
    urgency: "important",
    isCompleted: false,
  },
  {
    id: "3",
    vehicleId: "3",
    vehicleInfo: "سمند سورن - 456ج789",
    userName: "حسام کریمی",
    type: "تعویض لنت ترمز",
    name: "لنت ترمز جلو",
    interval: 30000,
    lastServiceMileage: 90000,
    lastServiceDate: "1402/05/10",
    nextServiceMileage: 120000,
    nextServiceDate: "1403/05/10",
    urgency: "urgent",
    isCompleted: true,
  },
  {
    id: "4",
    vehicleId: "4",
    vehicleInfo: "دنا پلاس - 246ت357",
    userName: "مریم احمدی",
    type: "تعویض فیلتر هوا",
    name: "فیلتر هوا",
    interval: 15000,
    lastServiceMileage: 15000,
    lastServiceDate: "1402/08/05",
    nextServiceMileage: 30000,
    nextServiceDate: "1403/02/05",
    urgency: "normal",
    isCompleted: false,
  },
];

// Chart data
const urgencyData = [
  { name: 'عادی', value: mockServices.filter(s => s.urgency === 'normal').length },
  { name: 'مهم', value: mockServices.filter(s => s.urgency === 'important').length },
  { name: 'فوری', value: mockServices.filter(s => s.urgency === 'urgent').length },
];

const statusData = [
  { name: 'تکمیل شده', value: mockServices.filter(s => s.isCompleted).length },
  { name: 'در انتظار', value: mockServices.filter(s => !s.isCompleted).length },
];

const typeData = [
  { name: 'تعویض روغن', value: mockServices.filter(s => s.type.includes('روغن')).length },
  { name: 'تعویض تسمه', value: mockServices.filter(s => s.type.includes('تسمه')).length },
  { name: 'تعویض لنت', value: mockServices.filter(s => s.type.includes('لنت')).length },
  { name: 'تعویض فیلتر', value: mockServices.filter(s => s.type.includes('فیلتر')).length },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export function ServiceManagement() {
  const [services, setServices] = useState(mockServices);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredServices = services.filter(service => 
    service.vehicleInfo.includes(searchTerm) || 
    service.userName.includes(searchTerm) ||
    service.type.includes(searchTerm) ||
    service.name.includes(searchTerm)
  );

  const handleDeleteService = (serviceId: string) => {
    setServices(services.filter(service => service.id !== serviceId));
  };

  const getUrgencyBadge = (urgency: string) => {
    switch (urgency) {
      case "urgent":
        return <Badge variant="destructive">فوری</Badge>;
      case "important":
        return <Badge variant="default">مهم</Badge>;
      default:
        return <Badge variant="secondary">عادی</Badge>;
    }
  };

  const getStatusBadge = (isCompleted: boolean) => {
    return (
      <Badge variant={isCompleted ? "default" : "secondary"}>
        {isCompleted ? "تکمیل شده" : "در انتظار"}
      </Badge>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">مدیریت سرویس‌ها</h1>
          <p className="text-muted-foreground">مدیریت سرویس‌های خودروهای کاربران</p>
        </div>
        <Button>
          <Plus className="ml-2 h-4 w-4" />
          افزودن سرویس
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل سرویس‌ها</CardTitle>
            <Wrench className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{services.length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">همه سرویس‌های ثبت شده</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">در انتظار</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{services.filter(s => !s.isCompleted).length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">سرویس‌های تکمیل نشده</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">تکمیل شده</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{services.filter(s => s.isCompleted).length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">سرویس‌های تکمیل شده</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>بر اساس اهمیت</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={urgencyData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {urgencyData.map((entry, index) => (
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
            <CardTitle>بر اساس وضعیت</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
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
                  <Tooltip formatter={(value: number) => [value.toLocaleString('fa-IR'), 'سرویس']} />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>بر اساس نوع</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={typeData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {typeData.map((entry, index) => (
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

      <div className="flex items-center space-x-2 rtl:space-x-reverse">
        <div className="relative flex-1">
          <Search className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="جستجوی سرویس‌ها..."
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
                <TableHead>نوع سرویس</TableHead>
                <TableHead>فاصله (کیلومتر)</TableHead>
                <TableHead>آخرین سرویس</TableHead>
                <TableHead>سرویس بعدی</TableHead>
                <TableHead>اهمیت</TableHead>
                <TableHead>وضعیت</TableHead>
                <TableHead className="text-right">عملیات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredServices.map((service) => (
                <TableRow key={service.id}>
                  <TableCell>
                    <div className="font-medium">{service.userName}</div>
                  </TableCell>
                  <TableCell>{service.vehicleInfo}</TableCell>
                  <TableCell>
                    <div className="font-medium">{service.type}</div>
                    <div className="text-sm text-muted-foreground">{service.name}</div>
                  </TableCell>
                  <TableCell>{service.interval.toLocaleString('fa-IR')}</TableCell>
                  <TableCell>
                    <div>{service.lastServiceMileage?.toLocaleString('fa-IR')}</div>
                    <div className="text-sm text-muted-foreground">{service.lastServiceDate}</div>
                  </TableCell>
                  <TableCell>
                    <div>{service.nextServiceMileage?.toLocaleString('fa-IR')}</div>
                    <div className="text-sm text-muted-foreground">{service.nextServiceDate}</div>
                  </TableCell>
                  <TableCell>{getUrgencyBadge(service.urgency)}</TableCell>
                  <TableCell>{getStatusBadge(service.isCompleted)}</TableCell>
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
                        <DropdownMenuItem onClick={() => handleDeleteService(service.id)}>
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