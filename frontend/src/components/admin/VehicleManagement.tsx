"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import IranLicensePlate from "iran-license-plate";
import "iran-license-plate/dist/License.css";
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
import { MoreHorizontal, Search, Plus, Edit, Trash, Car } from "lucide-react";
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

// Mock vehicle data
const mockVehicles = [
  {
    id: "1",
    userId: "1",
    userName: "علیرضا محمدی",
    licensePlate: "123ب456",
    brand: "پژو",
    model: "206 تیپ 5",
    manufactureYear: 1395,
    currentMileage: 85000,
    lastServiceDate: "1402/07/15",
  },
  {
    id: "2",
    userId: "2",
    userName: "فاطمه رضوی",
    licensePlate: "789الف123",
    brand: "پراید",
    model: "131",
    manufactureYear: 1398,
    currentMileage: 42000,
    lastServiceDate: "1402/06/22",
  },
  {
    id: "3",
    userId: "3",
    userName: "حسام کریمی",
    licensePlate: "456ج789",
    brand: "سمند",
    model: "سورن",
    manufactureYear: 1390,
    currentMileage: 120000,
    lastServiceDate: "1402/05/10",
  },
  {
    id: "4",
    userId: "4",
    userName: "مریم احمدی",
    licensePlate: "246ت357",
    brand: "دنا",
    model: "پلاس",
    manufactureYear: 1400,
    currentMileage: 25000,
    lastServiceDate: "1402/08/05",
  },
];

// Chart data
const brandData = [
  { name: 'پژو', value: mockVehicles.filter(v => v.brand === 'پژو').length },
  { name: 'پراید', value: mockVehicles.filter(v => v.brand === 'پراید').length },
  { name: 'سمند', value: mockVehicles.filter(v => v.brand === 'سمند').length },
  { name: 'دنا', value: mockVehicles.filter(v => v.brand === 'دنا').length },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export function VehicleManagement() {
  const [vehicles, setVehicles] = useState(mockVehicles);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredVehicles = vehicles.filter(vehicle => 
    vehicle.licensePlate.includes(searchTerm) || 
    vehicle.brand.includes(searchTerm) ||
    vehicle.model.includes(searchTerm) ||
    vehicle.userName.includes(searchTerm)
  );

  const handleDeleteVehicle = (vehicleId: string) => {
    setVehicles(vehicles.filter(vehicle => vehicle.id !== vehicleId));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">مدیریت خودروها</h1>
          <p className="text-muted-foreground">مدیریت خودروهای کاربران</p>
        </div>
        <Button>
          <Plus className="ml-2 h-4 w-4" />
          افزودن خودرو
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل خودروها</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{vehicles.length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">همه خودروهای ثبت شده</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کاربران دارای خودرو</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{new Set(vehicles.map(v => v.userId)).size.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">کاربرانی که خودرو ثبت کرده‌اند</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">برندهای خودرو</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{new Set(vehicles.map(v => v.brand)).size.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">تعداد برندهای مختلف</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>توزیع برندها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={brandData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [value.toLocaleString('fa-IR'), 'خودرو']}
                    labelFormatter={(label: string) => `برند: ${label}`}
                  />
                  <Bar dataKey="value" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>بر اساس برند</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={brandData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {brandData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => [value.toLocaleString('fa-IR'), 'خودرو']} />
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
            placeholder="جستجوی خودروها..."
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
                <TableHead>پلاک</TableHead>
                <TableHead>برند و مدل</TableHead>
                <TableHead>سال تولید</TableHead>
                <TableHead>کیلومتر</TableHead>
                <TableHead>آخرین سرویس</TableHead>
                <TableHead className="text-right">عملیات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredVehicles.map((vehicle) => (
                <TableRow key={vehicle.id}>
                  <TableCell>
                    <div className="font-medium">{vehicle.userName}</div>
                  </TableCell>
                  <TableCell>
                    <div className="flex justify-center">
                      <IranLicensePlate serial={vehicle.licensePlate} />
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{vehicle.brand} {vehicle.model}</div>
                  </TableCell>
                  <TableCell>{vehicle.manufactureYear.toLocaleString('fa-IR')}</TableCell>
                  <TableCell>{vehicle.currentMileage.toLocaleString('fa-IR')}</TableCell>
                  <TableCell>{vehicle.lastServiceDate}</TableCell>
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
                        <DropdownMenuItem onClick={() => handleDeleteVehicle(vehicle.id)}>
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