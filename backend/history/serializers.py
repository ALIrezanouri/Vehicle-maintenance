"""
History serializers for MashinMan project using Django REST Framework.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from datetime import date, datetime
from .models import ServiceHistory, ServicePart, MaintenanceRecord, ExpenseCategory, VehicleExpenseSummary
from vehicles.models import Vehicle
from users.models import User
from services.models import Service
from core.utils import validate_iranian_phone, gregorian_to_jalali, format_jalali_date


class ServicePartSerializer(me_serializers.EmbeddedDocumentSerializer):
    """
    Serializer for ServicePart embedded document.
    """
    
    class Meta:
        model = ServicePart
        fields = [
            'part_name', 'part_number', 'brand', 'quantity', 'unit_price',
            'total_price', 'is_original', 'supplier', 'warranty_months',
            'condition', 'notes'
        ]
    
    def validate_quantity(self, value):
        """
        Validate quantity is positive.
        """
        if value <= 0:
            raise serializers.ValidationError('تعداد باید بیشتر از صفر باشد.')
        return value
    
    def validate_unit_price(self, value):
        """
        Validate unit price is positive.
        """
        if value is not None and value < 0:
            raise serializers.ValidationError('قیمت واحد نمی‌تواند منفی باشد.')
        return value
    
    def validate(self, data):
        """
        Validate part data and calculate total price.
        """
        quantity = data.get('quantity', 1)
        unit_price = data.get('unit_price')
        total_price = data.get('total_price')
        
        # Calculate total price if not provided
        if unit_price and not total_price:
            data['total_price'] = unit_price * quantity
        
        # Validate total price consistency
        if unit_price and total_price and total_price != unit_price * quantity:
            raise serializers.ValidationError({
                'total_price': 'قیمت کل باید برابر قیمت واحد ضربدر تعداد باشد.'
            })
        
        return data


class ServiceHistorySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for ServiceHistory model.
    """
    
    # Related fields
    service_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    vehicle_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    # Embedded documents
    parts_used = ServicePartSerializer(many=True, required=False)
    
    # Read-only computed fields
    jalali_service_date = serializers.SerializerMethodField()
    warranty_days_remaining = serializers.SerializerMethodField()
    is_warranty_expired = serializers.SerializerMethodField()
    cost_breakdown = serializers.SerializerMethodField()
    
    # Nested serializers for read operations
    vehicle = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceHistory
        fields = [
            'id', 'service_id', 'vehicle_id', 'user_id', 'vehicle', 'user',
            'service_name', 'service_type', 'description', 'service_date',
            'mileage', 'service_center', 'service_center_address',
            'technician_name', 'technician_phone', 'total_cost', 'parts_cost',
            'labor_cost', 'additional_cost', 'parts_used', 'quality_rating',
            'service_center_rating', 'technician_rating', 'notes', 'issues_found',
            'recommendations', 'receipt_image', 'before_images', 'after_images',
            'documents', 'warranty_duration_days', 'warranty_mileage',
            'warranty_expiry_date', 'warranty_terms', 'next_service_recommendation',
            'next_service_mileage', 'next_service_date', 'is_warranty_valid',
            'is_recalled', 'recall_reason', 'created_at', 'updated_at',
            'jalali_service_date', 'warranty_days_remaining', 'is_warranty_expired',
            'cost_breakdown'
        ]
        read_only_fields = [
            'id', 'warranty_expiry_date', 'created_at', 'updated_at',
            'jalali_service_date', 'warranty_days_remaining', 'is_warranty_expired',
            'cost_breakdown'
        ]
    
    def get_vehicle(self, obj):
        """
        Get simplified vehicle information.
        """
        return {
            'id': str(obj.vehicle.id),
            'display_name': obj.vehicle.get_display_name(),
            'license_plate': obj.vehicle.license_plate,
            'brand': obj.vehicle.brand,
            'model': obj.vehicle.model
        }
    
    def get_user(self, obj):
        """
        Get simplified user information.
        """
        return {
            'id': str(obj.user.id),
            'name': obj.user.get_full_name(),
            'phone': obj.user.phone
        }
    
    def get_jalali_service_date(self, obj):
        """
        Get service date in Jalali format.
        """
        return obj.get_jalali_service_date()
    
    def get_warranty_days_remaining(self, obj):
        """
        Get warranty days remaining.
        """
        return obj.get_warranty_days_remaining()
    
    def get_is_warranty_expired(self, obj):
        """
        Check if warranty is expired.
        """
        return obj.is_warranty_expired()
    
    def get_cost_breakdown(self, obj):
        """
        Get cost breakdown details.
        """
        return obj.get_cost_breakdown()
    
    def validate_service_id(self, value):
        """
        Validate service exists.
        """
        if value:
            try:
                return Service.objects.get(id=value)
            except Service.DoesNotExist:
                raise serializers.ValidationError('سرویس مورد نظر یافت نشد.')
        return None
    
    def validate_vehicle_id(self, value):
        """
        Validate vehicle exists and belongs to user.
        """
        try:
            vehicle = Vehicle.objects.get(id=value)
            # Check if vehicle belongs to current user
            request = self.context.get('request')
            if request and hasattr(request, 'user') and vehicle.owner != request.user:
                raise serializers.ValidationError('شما مجاز به دسترسی به این خودرو نیستید.')
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError('خودرو مورد نظر یافت نشد.')
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_technician_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone(value):
            raise serializers.ValidationError('شماره تلفن تکنسین معتبر نیست.')
        return value
    
    def validate_service_date(self, value):
        """
        Validate service date.
        """
        if value > date.today():
            raise serializers.ValidationError('تاریخ انجام سرویس نمی‌تواند در آینده باشد.')
        return value
    
    def validate(self, data):
        """
        Validate service history data.
        """
        # Validate ratings
        for rating_field in ['quality_rating', 'service_center_rating', 'technician_rating']:
            rating = data.get(rating_field)
            if rating is not None and not (1 <= rating <= 5):
                raise serializers.ValidationError({
                    rating_field: 'امتیاز باید بین ۱ تا ۵ باشد.'
                })
        
        # Validate cost breakdown
        total_cost = data.get('total_cost', 0)
        parts_cost = data.get('parts_cost', 0) or 0
        labor_cost = data.get('labor_cost', 0) or 0
        additional_cost = data.get('additional_cost', 0) or 0
        
        calculated_total = parts_cost + labor_cost + additional_cost
        if calculated_total > total_cost:
            raise serializers.ValidationError({
                'total_cost': 'مجموع هزینه‌های جزئی نمی‌تواند بیشتر از کل هزینه باشد.'
            })
        
        # Validate mileage
        vehicle = data.get('vehicle_id')
        if vehicle and data.get('mileage', 0) > vehicle.current_mileage:
            raise serializers.ValidationError({
                'mileage': 'کیلومتر سرویس نمی‌تواند بیشتر از کیلومتر فعلی خودرو باشد.'
            })
        
        # Validate warranty dates
        if data.get('warranty_expiry_date') and data.get('service_date'):
            if data['warranty_expiry_date'] <= data['service_date']:
                raise serializers.ValidationError({
                    'warranty_expiry_date': 'تاریخ انقضای گارانتی باید بعد از تاریخ سرویس باشد.'
                })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new service history record.
        """
        # Extract related field IDs
        service = validated_data.pop('service_id', None)
        vehicle = validated_data.pop('vehicle_id')
        user = validated_data.pop('user_id')
        parts_used = validated_data.pop('parts_used', [])
        
        # Create service history
        history = ServiceHistory(
            service=service,
            vehicle=vehicle,
            user=user,
            **validated_data
        )
        
        # Add parts
        for part_data in parts_used:
            part = ServicePart(**part_data)
            history.parts_used.append(part)
        
        history.save()
        return history
    
    def update(self, instance, validated_data):
        """
        Update an existing service history record.
        """
        # Extract related field IDs
        service = validated_data.pop('service_id', None)
        vehicle = validated_data.pop('vehicle_id', None)
        user = validated_data.pop('user_id', None)
        parts_used = validated_data.pop('parts_used', None)
        
        # Update fields
        if service is not None:
            instance.service = service
        if vehicle:
            instance.vehicle = vehicle
        if user:
            instance.user = user
        
        # Update parts if provided
        if parts_used is not None:
            instance.parts_used = []
            for part_data in parts_used:
                part = ServicePart(**part_data)
                instance.parts_used.append(part)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ServiceHistoryListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for ServiceHistory list views.
    """
    
    vehicle_name = serializers.SerializerMethodField()
    jalali_service_date = serializers.SerializerMethodField()
    is_warranty_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceHistory
        fields = [
            'id', 'service_name', 'vehicle_name', 'service_date', 'jalali_service_date',
            'total_cost', 'service_center', 'quality_rating', 'is_warranty_expired'
        ]
    
    def get_vehicle_name(self, obj):
        return obj.vehicle.get_display_name()
    
    def get_jalali_service_date(self, obj):
        return obj.get_jalali_service_date()
    
    def get_is_warranty_expired(self, obj):
        return obj.is_warranty_expired()


class MaintenanceRecordSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for MaintenanceRecord model.
    """
    
    # Related fields
    vehicle_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    # Read-only computed fields
    jalali_record_date = serializers.SerializerMethodField()
    fuel_efficiency = serializers.SerializerMethodField()
    
    # Nested serializers for read operations
    vehicle = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'vehicle_id', 'vehicle', 'user_id', 'record_type', 'title',
            'description', 'record_date', 'mileage', 'cost', 'location',
            'provider', 'fuel_amount', 'fuel_price_per_liter', 'fuel_type',
            'receipt_image', 'images', 'documents', 'notes', 'created_at',
            'updated_at', 'jalali_record_date', 'fuel_efficiency'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'jalali_record_date', 'fuel_efficiency'
        ]
    
    def get_vehicle(self, obj):
        """
        Get simplified vehicle information.
        """
        return {
            'id': str(obj.vehicle.id),
            'display_name': obj.vehicle.get_display_name(),
            'license_plate': obj.vehicle.license_plate
        }
    
    def get_jalali_record_date(self, obj):
        """
        Get record date in Jalali format.
        """
        return obj.get_jalali_record_date()
    
    def get_fuel_efficiency(self, obj):
        """
        Get fuel efficiency if applicable.
        """
        return obj.get_fuel_efficiency()
    
    def validate_vehicle_id(self, value):
        """
        Validate vehicle exists and belongs to user.
        """
        try:
            vehicle = Vehicle.objects.get(id=value)
            # Check if vehicle belongs to current user
            request = self.context.get('request')
            if request and hasattr(request, 'user') and vehicle.owner != request.user:
                raise serializers.ValidationError('شما مجاز به دسترسی به این خودرو نیستید.')
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError('خودرو مورد نظر یافت نشد.')
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_record_date(self, value):
        """
        Validate record date.
        """
        if value > date.today():
            raise serializers.ValidationError('تاریخ رکورد نمی‌تواند در آینده باشد.')
        return value
    
    def validate_cost(self, value):
        """
        Validate cost is not negative.
        """
        if value < 0:
            raise serializers.ValidationError('هزینه نمی‌تواند منفی باشد.')
        return value
    
    def validate_fuel_amount(self, value):
        """
        Validate fuel amount is positive.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError('مقدار سوخت باید بیشتر از صفر باشد.')
        return value
    
    def validate_fuel_price_per_liter(self, value):
        """
        Validate fuel price is positive.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError('قیمت سوخت باید بیشتر از صفر باشد.')
        return value
    
    def validate(self, data):
        """
        Validate maintenance record data.
        """
        record_type = data.get('record_type')
        
        # Validate fuel-specific fields
        if record_type == 'fuel':
            fuel_amount = data.get('fuel_amount')
            fuel_price = data.get('fuel_price_per_liter')
            cost = data.get('cost')
            
            # Calculate cost if not provided
            if fuel_amount and fuel_price and not cost:
                data['cost'] = int(fuel_amount * fuel_price)
            
            # Validate fuel cost consistency
            if fuel_amount and fuel_price and cost:
                calculated_cost = int(fuel_amount * fuel_price)
                if abs(cost - calculated_cost) > 100:  # Allow small rounding differences
                    raise serializers.ValidationError({
                        'cost': 'هزینه سوخت با محاسبه مقدار ضربدر قیمت مطابقت ندارد.'
                    })
        
        # Validate mileage
        vehicle = data.get('vehicle_id')
        if vehicle and data.get('mileage', 0) > vehicle.current_mileage:
            raise serializers.ValidationError({
                'mileage': 'کیلومتر رکورد نمی‌تواند بیشتر از کیلومتر فعلی خودرو باشد.'
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new maintenance record.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id')
        user = validated_data.pop('user_id')
        
        # Create maintenance record
        record = MaintenanceRecord(
            vehicle=vehicle,
            user=user,
            **validated_data
        )
        record.save()
        return record
    
    def update(self, instance, validated_data):
        """
        Update an existing maintenance record.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id', None)
        user = validated_data.pop('user_id', None)
        
        # Update fields
        if vehicle:
            instance.vehicle = vehicle
        if user:
            instance.user = user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class MaintenanceRecordListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for MaintenanceRecord list views.
    """
    
    vehicle_name = serializers.SerializerMethodField()
    jalali_record_date = serializers.SerializerMethodField()
    record_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'title', 'vehicle_name', 'record_type', 'record_type_display',
            'record_date', 'jalali_record_date', 'cost', 'location'
        ]
    
    def get_vehicle_name(self, obj):
        return obj.vehicle.get_display_name()
    
    def get_jalali_record_date(self, obj):
        return obj.get_jalali_record_date()
    
    def get_record_type_display(self, obj):
        """
        Get display name for record type.
        """
        type_choices = dict(MaintenanceRecord._fields['record_type'].choices)
        return type_choices.get(obj.record_type, obj.record_type)


class ExpenseCategorySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for ExpenseCategory model.
    """
    
    # Computed fields
    monthly_expenses = serializers.SerializerMethodField()
    
    class Meta:
        model = ExpenseCategory
        fields = [
            'id', 'name', 'description', 'color', 'icon', 'is_active',
            'is_system', 'monthly_budget', 'yearly_budget', 'created_at',
            'updated_at', 'monthly_expenses'
        ]
        read_only_fields = ['id', 'is_system', 'created_at', 'updated_at', 'monthly_expenses']
    
    def get_monthly_expenses(self, obj):
        """
        Get current month expenses for this category.
        """
        request = self.context.get('request')
        vehicle_id = None
        if request and hasattr(request, 'query_params'):
            vehicle_id = request.query_params.get('vehicle_id')
        
        vehicle = None
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                pass
        
        return obj.get_monthly_expenses(vehicle=vehicle)
    
    def validate_name(self, value):
        """
        Validate category name uniqueness.
        """
        if self.instance:
            # Update case - exclude current instance
            if ExpenseCategory.objects(name=value, id__ne=self.instance.id).first():
                raise serializers.ValidationError('دسته‌بندی با این نام قبلاً ثبت شده است.')
        else:
            # Create case
            if ExpenseCategory.objects(name=value).first():
                raise serializers.ValidationError('دسته‌بندی با این نام قبلاً ثبت شده است.')
        return value
    
    def validate_color(self, value):
        """
        Validate hex color format.
        """
        if value and not (value.startswith('#') and len(value) == 7):
            raise serializers.ValidationError('رنگ باید در فرمت hex باشد (مثال: #FF0000).')
        return value
    
    def validate(self, data):
        """
        Validate expense category data.
        """
        # Validate budgets
        monthly_budget = data.get('monthly_budget')
        yearly_budget = data.get('yearly_budget')
        
        if monthly_budget and monthly_budget < 0:
            raise serializers.ValidationError({
                'monthly_budget': 'بودجه ماهانه نمی‌تواند منفی باشد.'
            })
        
        if yearly_budget and yearly_budget < 0:
            raise serializers.ValidationError({
                'yearly_budget': 'بودجه سالانه نمی‌تواند منفی باشد.'
            })
        
        if monthly_budget and yearly_budget and monthly_budget * 12 > yearly_budget:
            raise serializers.ValidationError({
                'yearly_budget': 'بودجه سالانه باید حداقل ۱۲ برابر بودجه ماهانه باشد.'
            })
        
        return data


class VehicleExpenseSummarySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for VehicleExpenseSummary model.
    """
    
    # Related fields
    vehicle_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    # Read-only computed fields
    period_display = serializers.SerializerMethodField()
    
    # Nested serializers for read operations
    vehicle = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleExpenseSummary
        fields = [
            'id', 'vehicle_id', 'vehicle', 'user_id', 'year', 'month',
            'service_expenses', 'fuel_expenses', 'insurance_expenses',
            'maintenance_expenses', 'repair_expenses', 'other_expenses',
            'total_expenses', 'start_mileage', 'end_mileage', 'distance_driven',
            'cost_per_km', 'fuel_efficiency', 'created_at', 'updated_at',
            'period_display'
        ]
        read_only_fields = [
            'id', 'total_expenses', 'distance_driven', 'cost_per_km',
            'created_at', 'updated_at', 'period_display'
        ]
    
    def get_vehicle(self, obj):
        """
        Get simplified vehicle information.
        """
        return {
            'id': str(obj.vehicle.id),
            'display_name': obj.vehicle.get_display_name(),
            'license_plate': obj.vehicle.license_plate
        }
    
    def get_period_display(self, obj):
        """
        Get period display string.
        """
        return obj.get_period_display()
    
    def validate_vehicle_id(self, value):
        """
        Validate vehicle exists and belongs to user.
        """
        try:
            vehicle = Vehicle.objects.get(id=value)
            # Check if vehicle belongs to current user
            request = self.context.get('request')
            if request and hasattr(request, 'user') and vehicle.owner != request.user:
                raise serializers.ValidationError('شما مجاز به دسترسی به این خودرو نیستید.')
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError('خودرو مورد نظر یافت نشد.')
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_year(self, value):
        """
        Validate year is reasonable.
        """
        current_year = datetime.now().year
        if value < 1300 or value > current_year + 1:  # Jalali years
            raise serializers.ValidationError('سال وارد شده معتبر نیست.')
        return value
    
    def validate_month(self, value):
        """
        Validate month is between 1-12.
        """
        if value is not None and not (1 <= value <= 12):
            raise serializers.ValidationError('ماه باید بین ۱ تا ۱۲ باشد.')
        return value
    
    def validate(self, data):
        """
        Validate expense summary data.
        """
        # Validate all expense fields are non-negative
        expense_fields = [
            'service_expenses', 'fuel_expenses', 'insurance_expenses',
            'maintenance_expenses', 'repair_expenses', 'other_expenses'
        ]
        
        for field in expense_fields:
            value = data.get(field, 0)
            if value < 0:
                raise serializers.ValidationError({
                    field: 'هزینه نمی‌تواند منفی باشد.'
                })
        
        # Validate mileage
        start_mileage = data.get('start_mileage')
        end_mileage = data.get('end_mileage')
        
        if start_mileage and end_mileage and start_mileage > end_mileage:
            raise serializers.ValidationError({
                'end_mileage': 'کیلومتر پایان دوره باید بیشتر از کیلومتر شروع باشد.'
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new expense summary.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id')
        user = validated_data.pop('user_id')
        
        # Create expense summary
        summary = VehicleExpenseSummary(
            vehicle=vehicle,
            user=user,
            **validated_data
        )
        summary.save()
        return summary
    
    def update(self, instance, validated_data):
        """
        Update an existing expense summary.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id', None)
        user = validated_data.pop('user_id', None)
        
        # Update fields
        if vehicle:
            instance.vehicle = vehicle
        if user:
            instance.user = user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ExpenseStatsSerializer(serializers.Serializer):
    """
    Serializer for expense statistics.
    """
    
    total_expenses = serializers.IntegerField()
    monthly_expenses = serializers.IntegerField()
    yearly_expenses = serializers.IntegerField()
    average_monthly_cost = serializers.FloatField()
    cost_per_km = serializers.FloatField()
    fuel_efficiency = serializers.FloatField()
    expense_breakdown = serializers.DictField()
    monthly_trend = serializers.ListField()
    top_expense_categories = serializers.ListField()
    
    class Meta:
        fields = [
            'total_expenses', 'monthly_expenses', 'yearly_expenses',
            'average_monthly_cost', 'cost_per_km', 'fuel_efficiency',
            'expense_breakdown', 'monthly_trend', 'top_expense_categories'
        ]


class FuelEfficiencySerializer(serializers.Serializer):
    """
    Serializer for fuel efficiency data.
    """
    
    date = serializers.DateField()
    mileage = serializers.IntegerField()
    fuel_amount = serializers.FloatField()
    efficiency = serializers.FloatField()
    cost = serializers.IntegerField()
    
    class Meta:
        fields = ['date', 'mileage', 'fuel_amount', 'efficiency', 'cost']
