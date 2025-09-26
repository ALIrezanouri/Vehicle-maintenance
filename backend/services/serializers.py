"""
Service serializers for MashinMan project using Django REST Framework.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from datetime import date, datetime
from .models import ServiceType, Service, ServiceReminder, ServiceCenter
from vehicles.models import Vehicle
from users.models import User
from core.utils import validate_iranian_phone, calculate_service_urgency


class ServiceTypeSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for ServiceType model.
    """
    
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'description', 'default_interval_days', 
            'default_interval_mileage', 'category', 'estimated_cost_min',
            'estimated_cost_max', 'requires_parts', 'requires_specialist',
            'estimated_duration_hours', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        Validate service type name uniqueness.
        """
        if self.instance:
            # Update case - exclude current instance
            if ServiceType.objects(name=value, id__ne=self.instance.id).first():
                raise serializers.ValidationError('نوع سرویس با این نام قبلاً ثبت شده است.')
        else:
            # Create case
            if ServiceType.objects(name=value).first():
                raise serializers.ValidationError('نوع سرویس با این نام قبلاً ثبت شده است.')
        return value
    
    def validate(self, data):
        """
        Validate service type data.
        """
        # Validate cost range
        if (data.get('estimated_cost_min') and data.get('estimated_cost_max') and 
            data['estimated_cost_min'] > data['estimated_cost_max']):
            raise serializers.ValidationError({
                'estimated_cost_max': 'حداکثر هزینه نمی‌تواند کمتر از حداقل هزینه باشد.'
            })
        
        # Validate intervals
        if data.get('default_interval_days', 0) <= 0:
            raise serializers.ValidationError({
                'default_interval_days': 'بازه زمانی باید بیشتر از صفر باشد.'
            })
        
        if data.get('default_interval_mileage', 0) <= 0:
            raise serializers.ValidationError({
                'default_interval_mileage': 'بازه کیلومتری باید بیشتر از صفر باشد.'
            })
        
        return data


class ServiceTypeListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for ServiceType list views.
    """
    
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'category', 'default_interval_days',
            'default_interval_mileage', 'estimated_cost_min', 'estimated_cost_max'
        ]


class ServiceSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for Service model.
    """
    
    # Related fields
    vehicle_id = serializers.CharField(write_only=True)
    service_type_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    # Read-only computed fields
    service_name = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()
    mileage_until_due = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    estimated_cost = serializers.SerializerMethodField()
    
    # Nested serializers for read operations
    vehicle = serializers.SerializerMethodField()
    service_type = ServiceTypeListSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'vehicle_id', 'vehicle', 'service_type_id', 'service_type',
            'custom_name', 'description', 'interval_days', 'interval_mileage',
            'last_service_date', 'last_service_mileage', 'next_service_date',
            'next_service_mileage', 'urgency', 'is_completed', 'completed_date',
            'completed_mileage', 'service_center', 'technician_name', 'cost',
            'parts_used', 'parts_cost', 'labor_cost', 'quality_rating', 'notes',
            'reminder_sent', 'reminder_date', 'receipt_image', 'before_images',
            'after_images', 'created_at', 'updated_at', 'service_name',
            'days_until_due', 'mileage_until_due', 'is_overdue', 'progress_percentage',
            'estimated_cost'
        ]
        read_only_fields = [
            'id', 'next_service_date', 'next_service_mileage', 'urgency',
            'created_at', 'updated_at', 'service_name', 'days_until_due',
            'mileage_until_due', 'is_overdue', 'progress_percentage', 'estimated_cost'
        ]
    
    def get_vehicle(self, obj):
        """
        Get simplified vehicle information.
        """
        return {
            'id': str(obj.vehicle.id),
            'display_name': obj.vehicle.get_display_name(),
            'license_plate': obj.vehicle.license_plate,
            'current_mileage': obj.vehicle.current_mileage
        }
    
    def get_service_name(self, obj):
        """
        Get service display name.
        """
        return obj.get_service_name()
    
    def get_days_until_due(self, obj):
        """
        Get days until service is due.
        """
        return obj.days_until_due()
    
    def get_mileage_until_due(self, obj):
        """
        Get mileage until service is due.
        """
        return obj.mileage_until_due()
    
    def get_is_overdue(self, obj):
        """
        Check if service is overdue.
        """
        return obj.is_overdue()
    
    def get_progress_percentage(self, obj):
        """
        Get service progress percentage.
        """
        return obj.get_progress_percentage()
    
    def get_estimated_cost(self, obj):
        """
        Get estimated cost range.
        """
        cost_range = obj.get_estimated_cost()
        if cost_range:
            return {
                'min': cost_range[0],
                'max': cost_range[1]
            }
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
    
    def validate_service_type_id(self, value):
        """
        Validate service type exists.
        """
        if value:
            try:
                return ServiceType.objects.get(id=value, is_active=True)
            except ServiceType.DoesNotExist:
                raise serializers.ValidationError('نوع سرویس مورد نظر یافت نشد.')
        return None
    
    def validate(self, data):
        """
        Validate service data.
        """
        # Validate that either service_type or custom_name is provided
        if not data.get('service_type_id') and not data.get('custom_name'):
            raise serializers.ValidationError(
                'باید نوع سرویس یا نام سفارشی را مشخص کنید.'
            )
        
        # Validate dates
        if data.get('last_service_date') and data['last_service_date'] > date.today():
            raise serializers.ValidationError({
                'last_service_date': 'تاریخ آخرین سرویس نمی‌تواند در آینده باشد.'
            })
        
        if data.get('completed_date') and data['completed_date'] > date.today():
            raise serializers.ValidationError({
                'completed_date': 'تاریخ انجام سرویس نمی‌تواند در آینده باشد.'
            })
        
        # Validate intervals
        if data.get('interval_days', 0) <= 0:
            raise serializers.ValidationError({
                'interval_days': 'بازه زمانی باید بیشتر از صفر باشد.'
            })
        
        if data.get('interval_mileage', 0) <= 0:
            raise serializers.ValidationError({
                'interval_mileage': 'بازه کیلومتری باید بیشتر از صفر باشد.'
            })
        
        # Validate mileage
        vehicle = data.get('vehicle_id')
        if vehicle and data.get('last_service_mileage', 0) > vehicle.current_mileage:
            raise serializers.ValidationError({
                'last_service_mileage': 'کیلومتر آخرین سرویس نمی‌تواند بیشتر از کیلومتر فعلی خودرو باشد.'
            })
        
        # Validate quality rating
        if data.get('quality_rating') and not (1 <= data['quality_rating'] <= 5):
            raise serializers.ValidationError({
                'quality_rating': 'امتیاز کیفیت باید بین ۱ تا ۵ باشد.'
            })
        
        # Validate cost breakdown
        parts_cost = data.get('parts_cost', 0) or 0
        labor_cost = data.get('labor_cost', 0) or 0
        total_cost = data.get('cost', 0) or 0
        
        if parts_cost + labor_cost > total_cost and total_cost > 0:
            raise serializers.ValidationError({
                'cost': 'مجموع هزینه قطعات و کارگری نمی‌تواند بیشتر از کل هزینه باشد.'
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new service.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id')
        service_type = validated_data.pop('service_type_id', None)
        
        # Create service
        service = Service(
            vehicle=vehicle,
            service_type=service_type,
            **validated_data
        )
        service.save()
        return service
    
    def update(self, instance, validated_data):
        """
        Update an existing service.
        """
        # Extract related field IDs
        vehicle = validated_data.pop('vehicle_id', None)
        service_type = validated_data.pop('service_type_id', None)
        
        # Update fields
        if vehicle:
            instance.vehicle = vehicle
        if 'service_type_id' in validated_data:
            instance.service_type = service_type
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ServiceListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for Service list views.
    """
    
    service_name = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'service_name', 'vehicle_name', 'urgency', 'is_completed',
            'next_service_date', 'days_until_due', 'is_overdue', 'progress_percentage',
            'cost', 'created_at'
        ]
    
    def get_service_name(self, obj):
        return obj.get_service_name()
    
    def get_vehicle_name(self, obj):
        return obj.vehicle.get_display_name()
    
    def get_days_until_due(self, obj):
        return obj.days_until_due()
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()
    
    def get_progress_percentage(self, obj):
        return obj.get_progress_percentage()


class ServiceCompletionSerializer(serializers.Serializer):
    """
    Serializer for completing a service.
    """
    
    completion_date = serializers.DateField(required=False)
    completion_mileage = serializers.IntegerField(required=False)
    cost = serializers.IntegerField(required=False)
    parts_cost = serializers.IntegerField(required=False)
    labor_cost = serializers.IntegerField(required=False)
    service_center = serializers.CharField(max_length=200, required=False)
    technician_name = serializers.CharField(max_length=100, required=False)
    quality_rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    notes = serializers.CharField(max_length=1000, required=False)
    parts_used = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    receipt_image = serializers.CharField(required=False)
    after_images = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    
    def validate_completion_date(self, value):
        """
        Validate completion date.
        """
        if value and value > date.today():
            raise serializers.ValidationError('تاریخ انجام سرویس نمی‌تواند در آینده باشد.')
        return value
    
    def validate(self, data):
        """
        Validate completion data.
        """
        # Validate cost breakdown
        parts_cost = data.get('parts_cost', 0) or 0
        labor_cost = data.get('labor_cost', 0) or 0
        total_cost = data.get('cost', 0) or 0
        
        if parts_cost + labor_cost > total_cost and total_cost > 0:
            raise serializers.ValidationError({
                'cost': 'مجموع هزینه قطعات و کارگری نمی‌تواند بیشتر از کل هزینه باشد.'
            })
        
        return data


class ServiceReminderSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for ServiceReminder model.
    """
    
    service_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    
    # Read-only fields
    service_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceReminder
        fields = [
            'id', 'service_id', 'user_id', 'reminder_type', 'days_before_due',
            'scheduled_date', 'is_sent', 'sent_at', 'message', 'is_acknowledged',
            'acknowledged_at', 'retry_count', 'last_retry_at', 'created_at',
            'service_name', 'user_name'
        ]
        read_only_fields = [
            'id', 'is_sent', 'sent_at', 'is_acknowledged', 'acknowledged_at',
            'retry_count', 'last_retry_at', 'created_at', 'service_name', 'user_name'
        ]
    
    def get_service_name(self, obj):
        """
        Get service name.
        """
        return obj.service.get_service_name()
    
    def get_user_name(self, obj):
        """
        Get user name.
        """
        return obj.user.get_full_name()
    
    def validate_service_id(self, value):
        """
        Validate service exists.
        """
        try:
            return Service.objects.get(id=value)
        except Service.DoesNotExist:
            raise serializers.ValidationError('سرویس مورد نظر یافت نشد.')
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_scheduled_date(self, value):
        """
        Validate scheduled date.
        """
        if value < date.today():
            raise serializers.ValidationError('تاریخ زمان‌بندی نمی‌تواند در گذشته باشد.')
        return value
    
    def create(self, validated_data):
        """
        Create a new service reminder.
        """
        service = validated_data.pop('service_id')
        user = validated_data.pop('user_id')
        
        reminder = ServiceReminder(
            service=service,
            user=user,
            **validated_data
        )
        reminder.save()
        return reminder


class ServiceCenterSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for ServiceCenter model.
    """
    
    # Computed fields
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCenter
        fields = [
            'id', 'name', 'description', 'phone', 'mobile', 'email', 'website',
            'address', 'city', 'postal_code', 'latitude', 'longitude',
            'specialties', 'supported_brands', 'working_hours', 'is_24_hours',
            'has_emergency_service', 'average_rating', 'total_reviews',
            'is_active', 'is_verified', 'created_at', 'updated_at', 'distance'
        ]
        read_only_fields = [
            'id', 'average_rating', 'total_reviews', 'created_at', 'updated_at', 'distance'
        ]
    
    def get_distance(self, obj):
        """
        Get distance from user's location if provided in context.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'query_params'):
            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            if lat and lng:
                try:
                    return obj.get_distance_from(float(lat), float(lng))
                except (ValueError, TypeError):
                    pass
        return None
    
    def validate_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone(value):
            raise serializers.ValidationError('شماره تلفن معتبر نیست.')
        return value
    
    def validate_mobile(self, value):
        """
        Validate Iranian mobile number.
        """
        if value and not validate_iranian_phone(value):
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')
        return value
    
    def validate_postal_code(self, value):
        """
        Validate Iranian postal code.
        """
        if value and (len(value) != 10 or not value.isdigit()):
            raise serializers.ValidationError('کد پستی باید ۱۰ رقم باشد.')
        return value
    
    def validate(self, data):
        """
        Validate service center data.
        """
        # Validate coordinates
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is not None and not (-90 <= latitude <= 90):
            raise serializers.ValidationError({
                'latitude': 'عرض جغرافیایی باید بین -۹۰ تا ۹۰ باشد.'
            })
        
        if longitude is not None and not (-180 <= longitude <= 180):
            raise serializers.ValidationError({
                'longitude': 'طول جغرافیایی باید بین -۱۸۰ تا ۱۸۰ باشد.'
            })
        
        return data


class ServiceCenterListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for ServiceCenter list views.
    """
    
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCenter
        fields = [
            'id', 'name', 'city', 'phone', 'average_rating', 'total_reviews',
            'is_24_hours', 'has_emergency_service', 'distance'
        ]
    
    def get_distance(self, obj):
        """
        Get distance from user's location if provided in context.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'query_params'):
            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            if lat and lng:
                try:
                    return obj.get_distance_from(float(lat), float(lng))
                except (ValueError, TypeError):
                    pass
        return None


class ServiceStatsSerializer(serializers.Serializer):
    """
    Serializer for service statistics.
    """
    
    total_services = serializers.IntegerField()
    completed_services = serializers.IntegerField()
    pending_services = serializers.IntegerField()
    overdue_services = serializers.IntegerField()
    urgent_services = serializers.IntegerField()
    total_cost = serializers.IntegerField()
    average_cost = serializers.FloatField()
    services_this_month = serializers.IntegerField()
    upcoming_services = serializers.ListField()
    
    class Meta:
        fields = [
            'total_services', 'completed_services', 'pending_services',
            'overdue_services', 'urgent_services', 'total_cost', 'average_cost',
            'services_this_month', 'upcoming_services'
        ]
