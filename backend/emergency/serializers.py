"""
Emergency serializers for MashinMan project using Django REST Framework.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from datetime import datetime, date
from .models import EmergencyRequest, EmergencyServiceProvider, EmergencyContact, EmergencyNotification
from vehicles.models import Vehicle
from users.models import User
from core.utils import validate_iranian_phone_number, normalize_iranian_phone_number


class EmergencyRequestSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for EmergencyRequest model.
    """
    
    # Related fields
    user_id = serializers.CharField(write_only=True)
    vehicle_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    assigned_provider_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    # Read-only computed fields
    emergency_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    response_time_minutes = serializers.SerializerMethodField()
    completion_time_minutes = serializers.SerializerMethodField()
    estimated_cost_display = serializers.SerializerMethodField()
    
    # Nested serializers for read operations
    user = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    assigned_provider = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyRequest
        fields = [
            'id', 'user_id', 'vehicle_id', 'assigned_provider_id', 'user', 'vehicle',
            'assigned_provider', 'emergency_type', 'status', 'priority', 'latitude',
            'longitude', 'location_address', 'location_description', 'contact_phone',
            'alternative_contact', 'description', 'additional_info', 'assigned_at',
            'estimated_arrival_time', 'actual_arrival_time', 'completed_at',
            'resolution_description', 'estimated_cost', 'actual_cost', 'payment_status',
            'user_rating', 'user_feedback', 'provider_notes', 'emergency_contacts_notified',
            'notification_sent_at', 'images', 'documents', 'created_at', 'updated_at',
            'emergency_type_display', 'status_display', 'priority_display',
            'response_time_minutes', 'completion_time_minutes', 'estimated_cost_display'
        ]
        read_only_fields = [
            'id', 'assigned_at', 'actual_arrival_time', 'completed_at',
            'emergency_contacts_notified', 'notification_sent_at', 'created_at',
            'updated_at', 'emergency_type_display', 'status_display', 'priority_display',
            'response_time_minutes', 'completion_time_minutes', 'estimated_cost_display'
        ]
    
    def get_user(self, obj):
        """
        Get simplified user information.
        """
        return {
            'id': str(obj.user.id),
            'name': obj.user.get_full_name(),
            'phone': obj.user.phone
        }
    
    def get_vehicle(self, obj):
        """
        Get simplified vehicle information.
        """
        if obj.vehicle:
            return {
                'id': str(obj.vehicle.id),
                'display_name': obj.vehicle.get_display_name(),
                'license_plate': obj.vehicle.license_plate,
                'brand': obj.vehicle.brand,
                'model': obj.vehicle.model
            }
        return None
    
    def get_assigned_provider(self, obj):
        """
        Get simplified provider information.
        """
        if obj.assigned_provider:
            return {
                'id': str(obj.assigned_provider.id),
                'name': obj.assigned_provider.name,
                'phone': obj.assigned_provider.phone,
                'average_rating': obj.assigned_provider.average_rating
            }
        return None
    
    def get_emergency_type_display(self, obj):
        """
        Get emergency type display name.
        """
        type_choices = dict(EmergencyRequest._fields['emergency_type'].choices)
        return type_choices.get(obj.emergency_type, obj.emergency_type)
    
    def get_status_display(self, obj):
        """
        Get status display name.
        """
        status_choices = dict(EmergencyRequest._fields['status'].choices)
        return status_choices.get(obj.status, obj.status)
    
    def get_priority_display(self, obj):
        """
        Get priority display name.
        """
        priority_choices = dict(EmergencyRequest._fields['priority'].choices)
        return priority_choices.get(obj.priority, obj.priority)
    
    def get_response_time_minutes(self, obj):
        """
        Get response time in minutes.
        """
        return obj.get_response_time_minutes()
    
    def get_completion_time_minutes(self, obj):
        """
        Get completion time in minutes.
        """
        return obj.get_completion_time_minutes()
    
    def get_estimated_cost_display(self, obj):
        """
        Get estimated cost with formatting.
        """
        if obj.estimated_cost:
            return f"{obj.estimated_cost:,} تومان"
        return None
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_vehicle_id(self, value):
        """
        Validate vehicle exists and belongs to user.
        """
        if value:
            try:
                vehicle = Vehicle.objects.get(id=value)
                # Check if vehicle belongs to current user
                request = self.context.get('request')
                if request and hasattr(request, 'user') and vehicle.owner != request.user:
                    raise serializers.ValidationError('شما مجاز به دسترسی به این خودرو نیستید.')
                return vehicle
            except Vehicle.DoesNotExist:
                raise serializers.ValidationError('خودرو مورد نظر یافت نشد.')
        return None
    
    def validate_assigned_provider_id(self, value):
        """
        Validate provider exists and is active.
        """
        if value:
            try:
                return EmergencyServiceProvider.objects.get(id=value, is_active=True)
            except EmergencyServiceProvider.DoesNotExist:
                raise serializers.ValidationError('ارائه‌دهنده سرویس مورد نظر یافت نشد.')
        return None
    
    def validate_contact_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن تماس معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_alternative_contact(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن جایگزین معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_user_rating(self, value):
        """
        Validate user rating is between 1 and 5.
        """
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError('امتیاز باید بین ۱ تا ۵ باشد.')
        return value
    
    def validate(self, data):
        """
        Validate emergency request data.
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
        
        # Validate cost fields
        estimated_cost = data.get('estimated_cost')
        actual_cost = data.get('actual_cost')
        
        if estimated_cost is not None and estimated_cost < 0:
            raise serializers.ValidationError({
                'estimated_cost': 'هزینه تخمینی نمی‌تواند منفی باشد.'
            })
        
        if actual_cost is not None and actual_cost < 0:
            raise serializers.ValidationError({
                'actual_cost': 'هزینه واقعی نمی‌تواند منفی باشد.'
            })
        
        # Validate time fields
        estimated_arrival = data.get('estimated_arrival_time')
        if estimated_arrival and estimated_arrival <= datetime.now():
            raise serializers.ValidationError({
                'estimated_arrival_time': 'زمان تخمینی رسیدن باید در آینده باشد.'
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new emergency request.
        """
        # Extract related field IDs
        user = validated_data.pop('user_id')
        vehicle = validated_data.pop('vehicle_id', None)
        assigned_provider = validated_data.pop('assigned_provider_id', None)
        
        # Create emergency request
        request = EmergencyRequest(
            user=user,
            vehicle=vehicle,
            assigned_provider=assigned_provider,
            **validated_data
        )
        request.save()
        return request
    
    def update(self, instance, validated_data):
        """
        Update an existing emergency request.
        """
        # Extract related field IDs
        user = validated_data.pop('user_id', None)
        vehicle = validated_data.pop('vehicle_id', None)
        assigned_provider = validated_data.pop('assigned_provider_id', None)
        
        # Update fields
        if user:
            instance.user = user
        if 'vehicle_id' in validated_data:
            instance.vehicle = vehicle
        if 'assigned_provider_id' in validated_data:
            instance.assigned_provider = assigned_provider
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class EmergencyRequestListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for EmergencyRequest list views.
    """
    
    emergency_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    vehicle_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyRequest
        fields = [
            'id', 'emergency_type', 'emergency_type_display', 'status', 'status_display',
            'priority', 'priority_display', 'vehicle_name', 'provider_name',
            'location_address', 'estimated_cost', 'created_at'
        ]
    
    def get_emergency_type_display(self, obj):
        type_choices = dict(EmergencyRequest._fields['emergency_type'].choices)
        return type_choices.get(obj.emergency_type, obj.emergency_type)
    
    def get_status_display(self, obj):
        status_choices = dict(EmergencyRequest._fields['status'].choices)
        return status_choices.get(obj.status, obj.status)
    
    def get_priority_display(self, obj):
        priority_choices = dict(EmergencyRequest._fields['priority'].choices)
        return priority_choices.get(obj.priority, obj.priority)
    
    def get_vehicle_name(self, obj):
        return obj.vehicle.get_display_name() if obj.vehicle else None
    
    def get_provider_name(self, obj):
        return obj.assigned_provider.name if obj.assigned_provider else None


class EmergencyServiceProviderSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for EmergencyServiceProvider model.
    """
    
    # Read-only computed fields
    distance = serializers.SerializerMethodField()
    availability_status = serializers.SerializerMethodField()
    service_types_display = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyServiceProvider
        fields = [
            'id', 'name', 'company_name', 'description', 'phone', 'mobile',
            'email', 'website', 'address', 'city', 'postal_code', 'latitude',
            'longitude', 'service_radius_km', 'service_types', 'supported_vehicle_types',
            'is_24_hours', 'working_hours_start', 'working_hours_end', 'working_days',
            'base_service_fee', 'per_km_rate', 'emergency_surcharge',
            'average_response_time_minutes', 'average_rating', 'total_requests_completed',
            'success_rate', 'fleet_size', 'equipment_list', 'certifications',
            'is_active', 'is_verified', 'verification_date', 'is_currently_available',
            'current_active_requests', 'max_concurrent_requests', 'created_at',
            'updated_at', 'last_activity', 'distance', 'availability_status',
            'service_types_display'
        ]
        read_only_fields = [
            'id', 'average_response_time_minutes', 'average_rating',
            'total_requests_completed', 'success_rate', 'current_active_requests',
            'created_at', 'updated_at', 'last_activity', 'distance',
            'availability_status', 'service_types_display'
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
                    return obj.calculate_distance(float(lat), float(lng))
                except (ValueError, TypeError):
                    pass
        return None
    
    def get_availability_status(self, obj):
        """
        Get availability status information.
        """
        return {
            'is_active': obj.is_active,
            'is_currently_available': obj.is_currently_available,
            'current_requests': obj.current_active_requests,
            'max_requests': obj.max_concurrent_requests,
            'capacity_percentage': (obj.current_active_requests / obj.max_concurrent_requests * 100) 
                                 if obj.max_concurrent_requests > 0 else 0
        }
    
    def get_service_types_display(self, obj):
        """
        Get service types with display names.
        """
        type_choices = dict(EmergencyServiceProvider._fields['service_types'].field.choices)
        return [
            {
                'type': service_type,
                'display': type_choices.get(service_type, service_type)
            }
            for service_type in obj.service_types
        ]
    
    def validate_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_mobile(self, value):
        """
        Validate Iranian mobile number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره موبایل معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_postal_code(self, value):
        """
        Validate Iranian postal code.
        """
        if value and (len(value) != 10 or not value.isdigit()):
            raise serializers.ValidationError('کد پستی باید ۱۰ رقم باشد.')
        return value
    
    def validate_service_radius_km(self, value):
        """
        Validate service radius is reasonable.
        """
        if value is not None and (value <= 0 or value > 1000):
            raise serializers.ValidationError('شعاع سرویس باید بین ۱ تا ۱۰۰۰ کیلومتر باشد.')
        return value
    
    def validate_average_rating(self, value):
        """
        Validate average rating is between 0 and 5.
        """
        if value is not None and not (0 <= value <= 5):
            raise serializers.ValidationError('میانگین امتیاز باید بین ۰ تا ۵ باشد.')
        return value
    
    def validate(self, data):
        """
        Validate emergency service provider data.
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
        
        # Validate pricing fields
        price_fields = ['base_service_fee', 'per_km_rate', 'emergency_surcharge']
        for field in price_fields:
            value = data.get(field)
            if value is not None and value < 0:
                raise serializers.ValidationError({
                    field: 'هزینه نمی‌تواند منفی باشد.'
                })
        
        # Validate capacity
        max_requests = data.get('max_concurrent_requests')
        if max_requests is not None and max_requests <= 0:
            raise serializers.ValidationError({
                'max_concurrent_requests': 'حداکثر درخواست‌های همزمان باید بیشتر از صفر باشد.'
            })
        
        return data


class EmergencyServiceProviderListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for EmergencyServiceProvider list views.
    """
    
    distance = serializers.SerializerMethodField()
    availability_status = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyServiceProvider
        fields = [
            'id', 'name', 'city', 'phone', 'average_rating', 'average_response_time_minutes',
            'is_24_hours', 'is_currently_available', 'service_types', 'distance',
            'availability_status'
        ]
    
    def get_distance(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'query_params'):
            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            if lat and lng:
                try:
                    return obj.calculate_distance(float(lat), float(lng))
                except (ValueError, TypeError):
                    pass
        return None
    
    def get_availability_status(self, obj):
        return {
            'is_available': obj.is_currently_available,
            'capacity_percentage': (obj.current_active_requests / obj.max_concurrent_requests * 100) 
                                 if obj.max_concurrent_requests > 0 else 0
        }


class EmergencyContactSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for EmergencyContact model.
    """
    
    # Related fields
    user_id = serializers.CharField(write_only=True)
    
    # Read-only fields
    relationship_display = serializers.SerializerMethodField()
    contact_method_display = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'user_id', 'name', 'relationship', 'phone', 'alternative_phone',
            'email', 'priority', 'notify_for_emergencies', 'notify_for_services',
            'preferred_contact_method', 'is_active', 'created_at', 'updated_at',
            'relationship_display', 'contact_method_display'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'relationship_display', 'contact_method_display'
        ]
    
    def get_relationship_display(self, obj):
        """
        Get relationship display name.
        """
        relationship_choices = dict(EmergencyContact._fields['relationship'].choices)
        return relationship_choices.get(obj.relationship, obj.relationship)
    
    def get_contact_method_display(self, obj):
        """
        Get contact method display name.
        """
        method_choices = dict(EmergencyContact._fields['preferred_contact_method'].choices)
        return method_choices.get(obj.preferred_contact_method, obj.preferred_contact_method)
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_alternative_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن جایگزین معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_priority(self, value):
        """
        Validate priority is between 1 and 10.
        """
        if value is not None and not (1 <= value <= 10):
            raise serializers.ValidationError('اولویت باید بین ۱ تا ۱۰ باشد.')
        return value
    
    def create(self, validated_data):
        """
        Create a new emergency contact.
        """
        user = validated_data.pop('user_id')
        
        contact = EmergencyContact(
            user=user,
            **validated_data
        )
        contact.save()
        return contact
    
    def update(self, instance, validated_data):
        """
        Update an existing emergency contact.
        """
        user = validated_data.pop('user_id', None)
        
        if user:
            instance.user = user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class EmergencyNotificationSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for EmergencyNotification model.
    """
    
    # Related fields
    emergency_request_id = serializers.CharField(write_only=True)
    recipient_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    emergency_contact_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    # Read-only fields
    notification_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyNotification
        fields = [
            'id', 'emergency_request_id', 'recipient_id', 'emergency_contact_id',
            'notification_type', 'message', 'status', 'created_at', 'sent_at',
            'delivered_at', 'read_at', 'retry_count', 'last_retry_at', 'error_message',
            'notification_type_display', 'status_display', 'recipient_name'
        ]
        read_only_fields = [
            'id', 'sent_at', 'delivered_at', 'read_at', 'retry_count', 'last_retry_at',
            'created_at', 'notification_type_display', 'status_display', 'recipient_name'
        ]
    
    def get_notification_type_display(self, obj):
        """
        Get notification type display name.
        """
        type_choices = dict(EmergencyNotification._fields['notification_type'].choices)
        return type_choices.get(obj.notification_type, obj.notification_type)
    
    def get_status_display(self, obj):
        """
        Get status display name.
        """
        status_choices = dict(EmergencyNotification._fields['status'].choices)
        return status_choices.get(obj.status, obj.status)
    
    def get_recipient_name(self, obj):
        """
        Get recipient name.
        """
        if obj.recipient:
            return obj.recipient.get_full_name()
        elif obj.emergency_contact:
            return obj.emergency_contact.name
        return None
    
    def validate_emergency_request_id(self, value):
        """
        Validate emergency request exists.
        """
        try:
            return EmergencyRequest.objects.get(id=value)
        except EmergencyRequest.DoesNotExist:
            raise serializers.ValidationError('درخواست اضطراری مورد نظر یافت نشد.')
    
    def validate_recipient_id(self, value):
        """
        Validate recipient exists.
        """
        if value:
            try:
                return User.objects.get(id=value)
            except User.DoesNotExist:
                raise serializers.ValidationError('گیرنده مورد نظر یافت نشد.')
        return None
    
    def validate_emergency_contact_id(self, value):
        """
        Validate emergency contact exists.
        """
        if value:
            try:
                return EmergencyContact.objects.get(id=value)
            except EmergencyContact.DoesNotExist:
                raise serializers.ValidationError('مخاطب اضطراری مورد نظر یافت نشد.')
        return None
    
    def validate(self, data):
        """
        Validate notification data.
        """
        recipient = data.get('recipient_id')
        emergency_contact = data.get('emergency_contact_id')
        
        if not recipient and not emergency_contact:
            raise serializers.ValidationError(
                'باید گیرنده یا مخاطب اضطراری را مشخص کنید.'
            )
        
        return data
    
    def create(self, validated_data):
        """
        Create a new emergency notification.
        """
        emergency_request = validated_data.pop('emergency_request_id')
        recipient = validated_data.pop('recipient_id', None)
        emergency_contact = validated_data.pop('emergency_contact_id', None)
        
        notification = EmergencyNotification(
            emergency_request=emergency_request,
            recipient=recipient,
            emergency_contact=emergency_contact,
            **validated_data
        )
        notification.save()
        return notification


class EmergencyStatsSerializer(serializers.Serializer):
    """
    Serializer for emergency statistics.
    """
    
    total_requests = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    completed_requests = serializers.IntegerField()
    cancelled_requests = serializers.IntegerField()
    average_response_time = serializers.FloatField()
    average_completion_time = serializers.FloatField()
    most_common_emergency_types = serializers.ListField()
    requests_by_priority = serializers.DictField()
    monthly_trend = serializers.ListField()
    
    class Meta:
        fields = [
            'total_requests', 'pending_requests', 'completed_requests',
            'cancelled_requests', 'average_response_time', 'average_completion_time',
            'most_common_emergency_types', 'requests_by_priority', 'monthly_trend'
        ]


class SOSRequestSerializer(serializers.Serializer):
    """
    Serializer for SOS emergency requests.
    """
    
    emergency_type = serializers.ChoiceField(
        choices=[
            ('breakdown', 'خرابی خودرو'),
            ('accident', 'تصادف'),
            ('flat_tire', 'پنچری'),
            ('battery_dead', 'باتری خالی'),
            ('fuel_empty', 'تمام شدن سوخت'),
            ('engine_overheat', 'داغ شدن موتور'),
            ('locked_out', 'قفل شدن در خودرو'),
            ('medical', 'اورژانس پزشکی'),
            ('security', 'مسائل امنیتی'),
            ('other', 'سایر'),
        ]
    )
    vehicle_id = serializers.CharField(required=False, allow_null=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    location_address = serializers.CharField(max_length=500, required=False)
    description = serializers.CharField(max_length=1000)
    contact_phone = serializers.CharField(max_length=15, required=False)
    priority = serializers.ChoiceField(
        choices=[
            ('low', 'کم'),
            ('medium', 'متوسط'),
            ('high', 'زیاد'),
            ('critical', 'بحرانی'),
        ],
        default='medium'
    )
    
    def validate_latitude(self, value):
        """
        Validate latitude is within valid range.
        """
        if not (-90 <= value <= 90):
            raise serializers.ValidationError('عرض جغرافیایی باید بین -۹۰ تا ۹۰ باشد.')
        return value
    
    def validate_longitude(self, value):
        """
        Validate longitude is within valid range.
        """
        if not (-180 <= value <= 180):
            raise serializers.ValidationError('طول جغرافیایی باید بین -۱۸۰ تا ۱۸۰ باشد.')
        return value
    
    def validate_contact_phone(self, value):
        """
        Validate Iranian phone number.
        """
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن تماس معتبر نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    class Meta:
        fields = [
            'emergency_type', 'vehicle_id', 'latitude', 'longitude',
            'location_address', 'description', 'contact_phone', 'priority'
        ]


class ProviderAvailabilitySerializer(serializers.Serializer):
    """
    Serializer for provider availability data.
    """
    
    provider_id = serializers.CharField()
    provider_name = serializers.CharField()
    distance = serializers.FloatField()
    estimated_arrival_time = serializers.DateTimeField()
    estimated_cost = serializers.IntegerField()
    average_rating = serializers.FloatField()
    is_available = serializers.BooleanField()
    
    class Meta:
        fields = [
            'provider_id', 'provider_name', 'distance', 'estimated_arrival_time',
            'estimated_cost', 'average_rating', 'is_available'
        ]
