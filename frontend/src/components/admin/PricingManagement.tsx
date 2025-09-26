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
import { MoreHorizontal, Search, Plus, Edit, Trash, TrendingUp } from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line
} from "recharts";
import ClientOnly from "@/components/ClientOnly";

// Mock pricing data
const mockPricing = [
  {
    id: "1",
    brand: "پژو",
    model: "206 تیپ 5",
    year: 1395,
    month: 8,
    price: 450000000,
    lastUpdated: "1402/08/20",
  },
  {
    id: "2",
    brand: "پراید",
    model: "131",
    year: 1398,
    month: 8,
    price: 280000000,
    lastUpdated: "1402/08/20",
  },
  {
    id: "3",
    brand: "سمند",
    model: "سورن",
    year: 1390,
    month: 8,
    price: 220000000,
    lastUpdated: "1402/08/20",
  },
  {
    id: "4",
    brand: "دنا",
    model: "پلاس",
    year: 1400,
    month: 8,
    price: 650000000,
    lastUpdated: "1402/08/20",
  },
  {
    id: "5",
    brand: "پژو",
    model: "206 تیپ 5",
    year: 1395,
    month: 7,
    price: 440000000,
    lastUpdated: "1402/07/20",
  },
];

// Chart data
const brandPrices = mockPricing.reduce((acc, item) => {
  const existing = acc.find(i => i.brand === item.brand);
  if (existing) {
    existing.price = Math.max(existing.price, item.price);
  } else {
    acc.push({ brand: item.brand, price: item.price });
  }
  return acc;
}, [] as { brand: string; price: number }[]);

// Price history data for a specific model (e.g., Peugeot 206)
const priceHistory = mockPricing
  .filter(item => item.brand === "پژو" && item.model === "206 تیپ 5")
  .map(item => ({
    date: `${item.year}/${item.month}`,
    price: item.price
  }))
  .sort((a, b) => a.date.localeCompare(b.date));

export function PricingManagement() {
  const [pricing, setPricing] = useState(mockPricing);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPricing = pricing.filter(item => 
    item.brand.includes(searchTerm) || 
    item.model.includes(searchTerm) ||
    item.year.toString().includes(searchTerm)
  );

  const handleDeletePricing = (pricingId: string) => {
    setPricing(pricing.filter(item => item.id !== pricingId));
  };

  // Format price in Persian currency format
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fa-IR').format(price) + " ریال";
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">مدیریت قیمت‌ها</h1>
          <p className="text-muted-foreground">مدیریت قیمت‌های خودروها</p>
        </div>
        <Button>
          <Plus className="ml-2 h-4 w-4" />
          افزودن قیمت جدید
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل قیمت‌ها</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pricing.length.toLocaleString('fa-IR')}</div>
            <p className="text-xs text-muted-foreground">همه قیمت‌های ثبت شده</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">میانگین قیمت</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatPrice(pricing.reduce((sum, item) => sum + item.price, 0) / pricing.length)}
            </div>
            <p className="text-xs text-muted-foreground">میانگین قیمت خودروها</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">آخرین بروزرسانی</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockPricing[0]?.lastUpdated || '-'}
            </div>
            <p className="text-xs text-muted-foreground">آخرین تاریخ بروزرسانی</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>مقایسه قیمت بر اساس برند</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={brandPrices}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="brand" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [formatPrice(value), 'قیمت']}
                    labelFormatter={(label: string) => `برند: ${label}`}
                  />
                  <Bar dataKey="price" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>تاریخچه قیمت (پژو 206)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => [formatPrice(value), 'قیمت']}
                    labelFormatter={(label: string) => `تاریخ: ${label}`}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#82ca9d" 
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
            placeholder="جستجوی قیمت‌ها..."
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
                <TableHead>برند</TableHead>
                <TableHead>مدل</TableHead>
                <TableHead>سال</TableHead>
                <TableHead>ماه</TableHead>
                <TableHead>قیمت</TableHead>
                <TableHead>آخرین بروزرسانی</TableHead>
                <TableHead className="text-right">عملیات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPricing.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">{item.brand}</TableCell>
                  <TableCell>{item.model}</TableCell>
                  <TableCell>{item.year.toLocaleString('fa-IR')}</TableCell>
                  <TableCell>{item.month.toLocaleString('fa-IR')}</TableCell>
                  <TableCell className="font-medium">{formatPrice(item.price)}</TableCell>
                  <TableCell>{item.lastUpdated}</TableCell>
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
                        <DropdownMenuItem onClick={() => handleDeletePricing(item.id)}>
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