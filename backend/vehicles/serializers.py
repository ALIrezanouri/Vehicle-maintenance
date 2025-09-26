"""
Vehicle serializers for MashinMan project.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from core.utils import (
    validate_iranian_license_plate, 
    normalize_license_plate,
    validate_mileage,
    get_iranian_car_brands,
    format_mileage
)
from core.exceptions import InvalidLicensePlateException, InvalidMileageException
from .models import Vehicle, VehicleMileageHistory, VehicleDocument


class VehicleSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for vehicle information.
    """
    display_name = serializers.SerializerMethodField()
    age_years = serializers.SerializerMethodField()
    total_mileage = serializers.SerializerMethodField()
    services_count = serializers.SerializerMethodField()
    pending_services_count = serializers.SerializerMethodField()
    urgent_services_count = serializers.SerializerMethodField()
    next_service_date = serializers.SerializerMethodField()
    insurance_status = serializers.SerializerMethodField()
    registration_status = serializers.SerializerMethodField()
    estimated_value_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'brand', 'model', 'manufacture_year',
            'engine_capacity', 'fuel_type', 'transmission_type', 'color',
            'current_mileage', 'purchase_mileage', 'purchase_date',
            'last_service_date', 'last_service_mileage',
            'insurance_company', 'insurance_expiry_date', 'registration_expiry_date',
            'condition', 'estimated_value', 'main_image', 'images',
            'is_active', 'is_primary', 'notes', 'created_at', 'updated_at',
            'display_name', 'age_years', 'total_mileage', 'services_count',
            'pending_services_count', 'urgent_services_count', 'next_service_date',
            'insurance_status', 'registration_status', 'estimated_value_display'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'display_name', 'age_years',
            'total_mileage', 'services_count', 'pending_services_count',
            'urgent_services_count', 'next_service_date', 'insurance_status',
            'registration_status', 'estimated_value_display'
        ]
    
    def validate_license_plate(self, value):
        """Validate Iranian license plate format."""
        if not validate_iranian_license_plate(value):
            raise serializers.ValidationError('شماره پلاک وارد شده صحیح نیست.')
        
        normalized_plate = normalize_license_plate(value)
        
        # Check for duplicate license plates (excluding current vehicle)
        user = self.context['request'].user
        existing_vehicle = Vehicle.objects(
            user=user,
            license_plate=normalized_plate
        ).first()
        
        if existing_vehicle and (not self.instance or existing_vehicle.id != self.instance.id):
            raise serializers.ValidationError('این شماره پلاک قبلاً ثبت شده است.')
        
        return normalized_plate
    
    def validate_current_mileage(self, value):
        """Validate current mileage."""
        if not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر وارد شده نامعتبر است.')
        
        # Check against purchase mileage if provided
        purchase_mileage = self.initial_data.get('purchase_mileage', 0)
        if purchase_mileage and value < purchase_mileage:
            raise serializers.ValidationError('کیلومتر فعلی نمی‌تواند کمتر از کیلومتر خرید باشد.')
        
        # Check against previous mileage if updating
        if self.instance and value < self.instance.current_mileage:
            raise serializers.ValidationError('کیلومتر جدید نمی‌تواند کمتر از کیلومتر فعلی باشد.')
        
        return value
    
    def validate_purchase_mileage(self, value):
        """Validate purchase mileage."""
        if value is not None and not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر خرید نامعتبر است.')
        return value
    
    def validate_manufacture_year(self, value):
        """Validate manufacture year."""
        from datetime import datetime
        current_year = datetime.now().year
        
        if value < 1300 or value > current_year + 1:
            raise serializers.ValidationError('سال ساخت نامعتبر است.')
        
        return value
    
    def validate(self, attrs):
        """Cross-field validation."""
        # Validate mileage consistency
        current_mileage = attrs.get('current_mileage')
        purchase_mileage = attrs.get('purchase_mileage', 0)
        
        if current_mileage and purchase_mileage and current_mileage < purchase_mileage:
            raise serializers.ValidationError({
                'current_mileage': 'کیلومتر فعلی نمی‌تواند کمتر از کیلومتر خرید باشد.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create vehicle with user assignment."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_display_name(self, obj):
        """Get vehicle display name."""
        return obj.get_display_name()
    
    def get_age_years(self, obj):
        """Get vehicle age in years."""
        return obj.get_age_years()
    
    def get_total_mileage(self, obj):
        """Get total mileage driven since purchase."""
        return obj.get_total_mileage()
    
    def get_services_count(self, obj):
        """Get total services count."""
        return obj.get_services_count()
    
    def get_pending_services_count(self, obj):
        """Get pending services count."""
        return obj.get_pending_services_count()
    
    def get_urgent_services_count(self, obj):
        """Get urgent services count."""
        return obj.get_urgent_services_count()
    
    def get_next_service_date(self, obj):
        """Get next service date."""
        return obj.get_next_service_date()
    
    def get_insurance_status(self, obj):
        """Get insurance status."""
        return obj.get_insurance_status()
    
    def get_registration_status(self, obj):
        """Get registration status."""
        return obj.get_registration_status()
    
    def get_estimated_value_display(self, obj):
        """Get formatted estimated value."""
        if obj.estimated_value:
            return f"{obj.estimated_value:,} تومان"
        return None


class VehicleCreateSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for creating a new vehicle.
    """
    
    class Meta:
        model = Vehicle
        fields = [
            'license_plate', 'brand', 'model', 'manufacture_year',
            'engine_capacity', 'fuel_type', 'transmission_type', 'color',
            'current_mileage', 'purchase_mileage', 'purchase_date',
            'insurance_company', 'insurance_expiry_date', 'registration_expiry_date',
            'condition', 'main_image', 'notes'
        ]
    
    def validate_license_plate(self, value):
        """Validate Iranian license plate format."""
        if not validate_iranian_license_plate(value):
            raise serializers.ValidationError('شماره پلاک وارد شده صحیح نیست.')
        
        normalized_plate = normalize_license_plate(value)
        
        # Check for duplicate license plates
        user = self.context['request'].user
        if Vehicle.objects(user=user, license_plate=normalized_plate).first():
            raise serializers.ValidationError('این شماره پلاک قبلاً ثبت شده است.')
        
        return normalized_plate
    
    def validate_current_mileage(self, value):
        """Validate current mileage."""
        if not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر وارد شده نامعتبر است.')
        return value
    
    def validate_purchase_mileage(self, value):
        """Validate purchase mileage."""
        if value is not None and not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر خرید نامعتبر است.')
        return value
    
    def validate_manufacture_year(self, value):
        """Validate manufacture year."""
        from datetime import datetime
        current_year = datetime.now().year
        
        if value < 1300 or value > current_year + 1:
            raise serializers.ValidationError('سال ساخت نامعتبر است.')
        
        return value
    
    def create(self, validated_data):
        """Create vehicle with user assignment."""
        validated_data['user'] = self.context['request'].user
        return Vehicle.objects.create(**validated_data)


class VehicleUpdateSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for updating vehicle information.
    """
    
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'engine_capacity', 'fuel_type', 'transmission_type',
            'color', 'insurance_company', 'insurance_expiry_date',
            'registration_expiry_date', 'condition', 'main_image', 'notes'
        ]


class VehicleMileageUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating vehicle mileage.
    """
    mileage = serializers.IntegerField()
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    source = serializers.ChoiceField(
        choices=VehicleMileageHistory._fields['source'].choices,
        default='manual'
    )
    
    def validate_mileage(self, value):
        """Validate mileage value."""
        if not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر وارد شده نامعتبر است.')
        
        # Check against current mileage
        vehicle = self.context['vehicle']
        if value < vehicle.current_mileage:
            raise serializers.ValidationError('کیلومتر جدید نمی‌تواند کمتر از کیلومتر فعلی باشد.')
        
        return value


class VehicleMileageHistorySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for vehicle mileage history.
    """
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    
    class Meta:
        model = VehicleMileageHistory
        fields = [
            'id', 'mileage', 'recorded_date', 'notes', 'source', 'source_display',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'source_display']


class VehicleDocumentSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for vehicle documents.
    """
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    is_expired = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleDocument
        fields = [
            'id', 'document_type', 'document_type_display', 'title', 'file_path',
            'issue_date', 'expiry_date', 'notes', 'created_at', 'updated_at',
            'is_expired', 'days_until_expiry'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_expired', 'days_until_expiry']
    
    def get_is_expired(self, obj):
        """Check if document is expired."""
        return obj.is_expired()
    
    def get_days_until_expiry(self, obj):
        """Get days until document expiry."""
        return obj.days_until_expiry()
    
    def create(self, validated_data):
        """Create document with vehicle assignment."""
        validated_data['vehicle'] = self.context['vehicle']
        return super().create(validated_data)


class VehicleListSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for vehicle list view (minimal data).
    """
    display_name = serializers.SerializerMethodField()
    pending_services_count = serializers.SerializerMethodField()
    urgent_services_count = serializers.SerializerMethodField()
    insurance_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'brand', 'model', 'manufacture_year',
            'current_mileage', 'main_image', 'is_primary', 'condition',
            'display_name', 'pending_services_count', 'urgent_services_count',
            'insurance_status'
        ]
    
    def get_display_name(self, obj):
        """Get vehicle display name."""
        return obj.get_display_name()
    
    def get_pending_services_count(self, obj):
        """Get pending services count."""
        return obj.get_pending_services_count()
    
    def get_urgent_services_count(self, obj):
        """Get urgent services count."""
        return obj.get_urgent_services_count()
    
    def get_insurance_status(self, obj):
        """Get insurance status."""
        return obj.get_insurance_status()


class VehicleDetailSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for detailed vehicle view.
    """
    display_name = serializers.SerializerMethodField()
    age_years = serializers.SerializerMethodField()
    total_mileage = serializers.SerializerMethodField()
    services_count = serializers.SerializerMethodField()
    pending_services_count = serializers.SerializerMethodField()
    urgent_services_count = serializers.SerializerMethodField()
    next_service_date = serializers.SerializerMethodField()
    insurance_status = serializers.SerializerMethodField()
    registration_status = serializers.SerializerMethodField()
    estimated_value_display = serializers.SerializerMethodField()
    recent_mileage_history = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'brand', 'model', 'manufacture_year',
            'engine_capacity', 'fuel_type', 'transmission_type', 'color',
            'current_mileage', 'purchase_mileage', 'purchase_date',
            'last_service_date', 'last_service_mileage',
            'insurance_company', 'insurance_expiry_date', 'registration_expiry_date',
            'condition', 'estimated_value', 'main_image', 'images',
            'is_active', 'is_primary', 'notes', 'created_at', 'updated_at',
            'display_name', 'age_years', 'total_mileage', 'services_count',
            'pending_services_count', 'urgent_services_count', 'next_service_date',
            'insurance_status', 'registration_status', 'estimated_value_display',
            'recent_mileage_history', 'documents'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'display_name', 'age_years',
            'total_mileage', 'services_count', 'pending_services_count',
            'urgent_services_count', 'next_service_date', 'insurance_status',
            'registration_status', 'estimated_value_display', 'recent_mileage_history',
            'documents'
        ]
    
    def get_display_name(self, obj):
        """Get vehicle display name."""
        return obj.get_display_name()
    
    def get_age_years(self, obj):
        """Get vehicle age in years."""
        return obj.get_age_years()
    
    def get_total_mileage(self, obj):
        """Get total mileage driven since purchase."""
        return obj.get_total_mileage()
    
    def get_services_count(self, obj):
        """Get total services count."""
        return obj.get_services_count()
    
    def get_pending_services_count(self, obj):
        """Get pending services count."""
        return obj.get_pending_services_count()
    
    def get_urgent_services_count(self, obj):
        """Get urgent services count."""
        return obj.get_urgent_services_count()
    
    def get_next_service_date(self, obj):
        """Get next service date."""
        return obj.get_next_service_date()
    
    def get_insurance_status(self, obj):
        """Get insurance status."""
        return obj.get_insurance_status()
    
    def get_registration_status(self, obj):
        """Get registration status."""
        return obj.get_registration_status()
    
    def get_estimated_value_display(self, obj):
        """Get formatted estimated value."""
        if obj.estimated_value:
            return f"{obj.estimated_value:,} تومان"
        return None
    
    def get_recent_mileage_history(self, obj):
        """Get recent mileage history."""
        recent_history = VehicleMileageHistory.objects(vehicle=obj).order_by('-recorded_date')[:5]
        return VehicleMileageHistorySerializer(recent_history, many=True).data
    
    def get_documents(self, obj):
        """Get vehicle documents."""
        documents = VehicleDocument.objects(vehicle=obj).order_by('-created_at')
        return VehicleDocumentSerializer(documents, many=True).data


class VehicleStatsSerializer(serializers.Serializer):
    """
    Serializer for vehicle statistics.
    """
    total_services = serializers.IntegerField()
    completed_services = serializers.IntegerField()
    pending_services = serializers.IntegerField()
    urgent_services = serializers.IntegerField()
    total_expenses = serializers.IntegerField()
    this_month_expenses = serializers.IntegerField()
    average_service_cost = serializers.FloatField()
    last_service_date = serializers.DateField()
    next_service_date = serializers.DateField()
    total_mileage_driven = serializers.IntegerField()
    average_monthly_mileage = serializers.FloatField()


class VehicleBrandsSerializer(serializers.Serializer):
    """
    Serializer for available vehicle brands.
    """
    brands = serializers.ListField(child=serializers.CharField())


class SetPrimaryVehicleSerializer(serializers.Serializer):
    """
    Serializer for setting primary vehicle.
    """
    vehicle_id = serializers.CharField()
    
    def validate_vehicle_id(self, value):
        """Validate vehicle ID and ownership."""
        user = self.context['request'].user
        
        try:
            vehicle = Vehicle.objects(id=value, user=user, is_active=True).first()
            if not vehicle:
                raise serializers.ValidationError('خودروی مورد نظر یافت نشد.')
            return vehicle
        except:
            raise serializers.ValidationError('شناسه خودرو نامعتبر است.')


class VehicleValueCalculationSerializer(serializers.Serializer):
    """
    Serializer for vehicle value calculation.
    """
    condition = serializers.ChoiceField(
        choices=[choice[0] for choice in Vehicle._fields['condition'].choices],
        default='good'
    )
    mileage = serializers.IntegerField(required=False)
    
    def validate_mileage(self, value):
        """Validate mileage if provided."""
        if value is not None and not validate_mileage(value):
            raise serializers.ValidationError('کیلومتر وارد شده نامعتبر است.')
        return value
