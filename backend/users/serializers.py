"""
User serializers for MashinMan project.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from django.contrib.auth.hashers import make_password
from core.utils import validate_iranian_phone_number, normalize_iranian_phone_number
from core.exceptions import InvalidPhoneNumberException
from .models import User, UserSession, UserVerification, UserActivity


class UserRegistrationSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'name', 'phone', 'email', 'password', 'password_confirm',
            'city', 'emergency_contact_name', 'emergency_contact_phone'
        ]
    
    def validate_phone(self, value):
        """Validate Iranian phone number format."""
        if not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن وارد شده صحیح نیست.')
        
        # Check if phone already exists
        normalized_phone = normalize_iranian_phone_number(value)
        if User.objects(phone=normalized_phone).first():
            raise serializers.ValidationError('این شماره تلفن قبلاً ثبت شده است.')
        
        return normalized_phone
    
    def validate_emergency_contact_phone(self, value):
        """Validate emergency contact phone number."""
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن مخاطب اضطراری صحیح نیست.')
        return normalize_iranian_phone_number(value) if value else value
    
    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        
        if value.isdigit():
            raise serializers.ValidationError('رمز عبور نمی‌تواند تنها شامل عدد باشد.')
        
        if value.isalpha():
            raise serializers.ValidationError('رمز عبور باید شامل حروف و اعداد باشد.')
        
        return value
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'تکرار رمز عبور مطابقت ندارد.'
            })
        
        attrs.pop('password_confirm')
        return attrs
    
    def create(self, validated_data):
        """Create new user with hashed password."""
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate_phone(self, value):
        """Normalize phone number."""
        if not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن وارد شده صحیح نیست.')
        return normalize_iranian_phone_number(value)
    
    def validate(self, attrs):
        """Validate user credentials."""
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        try:
            user = User.objects(phone=phone, is_active=True).first()
            if not user:
                raise serializers.ValidationError('کاربری با این شماره تلفن یافت نشد.')
            
            if not user.check_password(password):
                raise serializers.ValidationError('رمز عبور اشتباه است.')
            
            attrs['user'] = user
            return attrs
            
        except Exception:
            raise serializers.ValidationError('خطا در احراز هویت.')


class UserProfileSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for user profile information.
    """
    vehicles_count = serializers.SerializerMethodField()
    active_services_count = serializers.SerializerMethodField()
    urgent_services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'name', 'phone', 'email', 'avatar', 'birth_date', 'city',
            'emergency_contact_name', 'emergency_contact_phone',
            'sms_notifications', 'email_notifications', 'push_notifications',
            'is_verified', 'created_at', 'last_login',
            'vehicles_count', 'active_services_count', 'urgent_services_count'
        ]
        read_only_fields = ['id', 'phone', 'is_verified', 'created_at', 'last_login']
    
    def get_vehicles_count(self, obj):
        """Get user's vehicles count."""
        return obj.get_vehicles_count()
    
    def get_active_services_count(self, obj):
        """Get user's active services count."""
        return obj.get_active_services_count()
    
    def get_urgent_services_count(self, obj):
        """Get user's urgent services count."""
        return obj.get_urgent_services_count()
    
    def validate_emergency_contact_phone(self, value):
        """Validate emergency contact phone number."""
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن مخاطب اضطراری صحیح نیست.')
        return normalize_iranian_phone_number(value) if value else value


class UserUpdateSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for updating user profile.
    """
    
    class Meta:
        model = User
        fields = [
            'name', 'email', 'avatar', 'birth_date', 'city',
            'emergency_contact_name', 'emergency_contact_phone',
            'sms_notifications', 'email_notifications', 'push_notifications'
        ]
    
    def validate_emergency_contact_phone(self, value):
        """Validate emergency contact phone number."""
        if value and not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن مخاطب اضطراری صحیح نیست.')
        return normalize_iranian_phone_number(value) if value else value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    current_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        
        if value.isdigit():
            raise serializers.ValidationError('رمز عبور نمی‌تواند تنها شامل عدد باشد.')
        
        if value.isalpha():
            raise serializers.ValidationError('رمز عبور باید شامل حروف و اعداد باشد.')
        
        return value
    
    def validate(self, attrs):
        """Validate password change data."""
        user = self.context['request'].user
        
        # Check current password
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({
                'current_password': 'رمز عبور فعلی اشتباه است.'
            })
        
        # Check new password confirmation
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'تکرار رمز عبور جدید مطابقت ندارد.'
            })
        
        # Check if new password is different from current
        if user.check_password(attrs['new_password']):
            raise serializers.ValidationError({
                'new_password': 'رمز عبور جدید باید متفاوت از رمز عبور فعلی باشد.'
            })
        
        return attrs


class UserVerificationSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for user verification.
    """
    
    class Meta:
        model = UserVerification
        fields = ['verification_type', 'code', 'target', 'expires_at']
        read_only_fields = ['expires_at']


class VerifyCodeSerializer(serializers.Serializer):
    """
    Serializer for verifying verification code.
    """
    verification_type = serializers.ChoiceField(choices=UserVerification.VERIFICATION_TYPES)
    code = serializers.CharField(max_length=10)
    target = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        """Validate verification code."""
        user = self.context['request'].user
        
        verification = UserVerification.objects(
            user=user,
            verification_type=attrs['verification_type'],
            code=attrs['code'],
            target=attrs['target'],
            is_used=False
        ).first()
        
        if not verification:
            raise serializers.ValidationError('کد تایید نامعتبر است.')
        
        if not verification.is_valid():
            raise serializers.ValidationError('کد تایید منقضی شده یا نامعتبر است.')
        
        attrs['verification'] = verification
        return attrs


class UserActivitySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for user activity logs.
    """
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'activity_type', 'activity_type_display', 'description',
            'vehicle_id', 'service_id', 'ip_address', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserSessionSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for user sessions.
    """
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'device_info', 'ip_address', 'user_agent',
            'created_at', 'last_activity', 'expires_at', 'is_active', 'is_expired'
        ]
        read_only_fields = ['id', 'session_key', 'created_at', 'last_activity', 'expires_at']
    
    def get_is_expired(self, obj):
        """Check if session is expired."""
        return obj.is_expired()


class UserStatsSerializer(serializers.Serializer):
    """
    Serializer for user statistics.
    """
    total_vehicles = serializers.IntegerField()
    total_services = serializers.IntegerField()
    completed_services = serializers.IntegerField()
    pending_services = serializers.IntegerField()
    urgent_services = serializers.IntegerField()
    total_expenses = serializers.IntegerField()
    this_month_expenses = serializers.IntegerField()
    average_service_cost = serializers.FloatField()
    last_service_date = serializers.DateField()
    next_service_date = serializers.DateField()


class UserDashboardSerializer(serializers.Serializer):
    """
    Serializer for user dashboard data.
    """
    user = UserProfileSerializer()
    stats = UserStatsSerializer()
    recent_activities = UserActivitySerializer(many=True)
    upcoming_services = serializers.ListField()
    urgent_services = serializers.ListField()
    recent_expenses = serializers.ListField()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password request.
    """
    phone = serializers.CharField()
    
    def validate_phone(self, value):
        """Validate phone number and check if user exists."""
        if not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن وارد شده صحیح نیست.')
        
        normalized_phone = normalize_iranian_phone_number(value)
        user = User.objects(phone=normalized_phone, is_active=True).first()
        
        if not user:
            raise serializers.ValidationError('کاربری با این شماره تلفن یافت نشد.')
        
        return normalized_phone


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting password with verification code.
    """
    phone = serializers.CharField()
    verification_code = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate_phone(self, value):
        """Normalize phone number."""
        if not validate_iranian_phone_number(value):
            raise serializers.ValidationError('شماره تلفن وارد شده صحیح نیست.')
        return normalize_iranian_phone_number(value)
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        if len(value) < 8:
            raise serializers.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        
        if value.isdigit():
            raise serializers.ValidationError('رمز عبور نمی‌تواند تنها شامل عدد باشد.')
        
        if value.isalpha():
            raise serializers.ValidationError('رمز عبور باید شامل حروف و اعداد باشد.')
        
        return value
    
    def validate(self, attrs):
        """Validate password reset data."""
        phone = attrs.get('phone')
        verification_code = attrs.get('verification_code')
        
        # Check if passwords match
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'تکرار رمز عبور جدید مطابقت ندارد.'
            })
        
        # Find user
        user = User.objects(phone=phone, is_active=True).first()
        if not user:
            raise serializers.ValidationError('کاربری با این شماره تلفن یافت نشد.')
        
        # Validate verification code
        verification = UserVerification.objects(
            user=user,
            verification_type='password_reset',
            code=verification_code,
            target=phone,
            is_used=False
        ).first()
        
        if not verification or not verification.is_valid():
            raise serializers.ValidationError('کد تایید نامعتبر یا منقضی شده است.')
        
        attrs['user'] = user
        attrs['verification'] = verification
        attrs.pop('new_password_confirm')
        
        return attrs
