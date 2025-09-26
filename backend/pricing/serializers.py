"""
Pricing serializers for MashinMan project using Django REST Framework.
"""

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from datetime import date, datetime
from .models import CarPricing, PriceHistory, MarketAnalysis, PriceAlert
from users.models import User
from core.utils import get_iranian_car_brands


class CarPricingSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for CarPricing model.
    """
    
    # Read-only computed fields
    display_name = serializers.SerializerMethodField()
    estimated_price = serializers.SerializerMethodField()
    price_trend_display = serializers.SerializerMethodField()
    demand_supply_balance = serializers.SerializerMethodField()
    
    class Meta:
        model = CarPricing
        fields = [
            'id', 'brand', 'model', 'year', 'engine_capacity', 'fuel_type',
            'transmission_type', 'base_price', 'current_price',
            'excellent_condition_price', 'good_condition_price',
            'fair_condition_price', 'poor_condition_price',
            'low_mileage_price', 'medium_mileage_price', 'high_mileage_price',
            'market_trend', 'price_change_percentage', 'price_change_amount',
            'last_price_update', 'average_market_price', 'min_market_price',
            'max_market_price', 'demand_level', 'supply_level', 'data_source',
            'reliability_score', 'sample_size', 'tehran_price', 'isfahan_price',
            'mashhad_price', 'shiraz_price', 'tabriz_price', 'is_active',
            'is_verified', 'created_at', 'updated_at', 'display_name',
            'estimated_price', 'price_trend_display', 'demand_supply_balance'
        ]
        read_only_fields = [
            'id', 'price_change_percentage', 'price_change_amount',
            'last_price_update', 'created_at', 'updated_at', 'display_name',
            'estimated_price', 'price_trend_display', 'demand_supply_balance'
        ]
    
    def get_display_name(self, obj):
        """
        Get car display name.
        """
        return obj.get_display_name()
    
    def get_estimated_price(self, obj):
        """
        Get estimated price based on request parameters.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'query_params'):
            condition = request.query_params.get('condition', 'good')
            mileage = request.query_params.get('mileage', 100000)
            try:
                mileage = int(mileage)
                return obj.calculate_estimated_price(condition, mileage)
            except (ValueError, TypeError):
                pass
        return obj.current_price
    
    def get_price_trend_display(self, obj):
        """
        Get price trend display information.
        """
        trend_choices = dict(CarPricing._fields['market_trend'].choices)
        return {
            'trend': obj.market_trend,
            'trend_display': trend_choices.get(obj.market_trend, obj.market_trend),
            'change_percentage': obj.price_change_percentage,
            'change_amount': obj.price_change_amount
        }
    
    def get_demand_supply_balance(self, obj):
        """
        Get demand and supply balance information.
        """
        demand_choices = dict(CarPricing._fields['demand_level'].choices)
        supply_choices = dict(CarPricing._fields['supply_level'].choices)
        
        return {
            'demand_level': obj.demand_level,
            'demand_display': demand_choices.get(obj.demand_level, obj.demand_level),
            'supply_level': obj.supply_level,
            'supply_display': supply_choices.get(obj.supply_level, obj.supply_level)
        }
    
    def validate_brand(self, value):
        """
        Validate brand is in Iranian car brands list.
        """
        iranian_brands = get_iranian_car_brands()
        if value not in iranian_brands:
            raise serializers.ValidationError('برند وارد شده در لیست برندهای ایرانی موجود نیست.')
        return value
    
    def validate_year(self, value):
        """
        Validate year is reasonable.
        """
        current_year = datetime.now().year
        if value < 1350 or value > current_year + 2:  # Jalali years
            raise serializers.ValidationError('سال ساخت معتبر نیست.')
        return value
    
    def validate_engine_capacity(self, value):
        """
        Validate engine capacity is reasonable.
        """
        if value is not None and (value <= 0 or value > 10):
            raise serializers.ValidationError('حجم موتور باید بین ۰ تا ۱۰ لیتر باشد.')
        return value
    
    def validate_reliability_score(self, value):
        """
        Validate reliability score is between 0 and 1.
        """
        if value is not None and not (0 <= value <= 1):
            raise serializers.ValidationError('امتیاز قابلیت اطمینان باید بین ۰ تا ۱ باشد.')
        return value
    
    def validate(self, data):
        """
        Validate car pricing data.
        """
        # Validate price fields are positive
        price_fields = [
            'base_price', 'current_price', 'excellent_condition_price',
            'good_condition_price', 'fair_condition_price', 'poor_condition_price',
            'low_mileage_price', 'medium_mileage_price', 'high_mileage_price',
            'average_market_price', 'min_market_price', 'max_market_price',
            'tehran_price', 'isfahan_price', 'mashhad_price', 'shiraz_price', 'tabriz_price'
        ]
        
        for field in price_fields:
            value = data.get(field)
            if value is not None and value < 0:
                raise serializers.ValidationError({
                    field: 'قیمت نمی‌تواند منفی باشد.'
                })
        
        # Validate price ranges
        min_price = data.get('min_market_price')
        max_price = data.get('max_market_price')
        current_price = data.get('current_price')
        
        if min_price and max_price and min_price > max_price:
            raise serializers.ValidationError({
                'max_market_price': 'حداکثر قیمت نمی‌تواند کمتر از حداقل قیمت باشد.'
            })
        
        if min_price and current_price and current_price < min_price:
            raise serializers.ValidationError({
                'current_price': 'قیمت فعلی نمی‌تواند کمتر از حداقل قیمت بازار باشد.'
            })
        
        if max_price and current_price and current_price > max_price:
            raise serializers.ValidationError({
                'current_price': 'قیمت فعلی نمی‌تواند بیشتر از حداکثر قیمت بازار باشد.'
            })
        
        # Validate condition-based prices are in logical order
        excellent = data.get('excellent_condition_price')
        good = data.get('good_condition_price')
        fair = data.get('fair_condition_price')
        poor = data.get('poor_condition_price')
        
        prices = [p for p in [excellent, good, fair, poor] if p is not None]
        if len(prices) > 1 and prices != sorted(prices, reverse=True):
            raise serializers.ValidationError(
                'قیمت‌های وضعیت باید به ترتیب نزولی باشند (عالی > خوب > متوسط > ضعیف).'
            )
        
        return data


class CarPricingListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for CarPricing list views.
    """
    
    display_name = serializers.SerializerMethodField()
    price_trend_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CarPricing
        fields = [
            'id', 'brand', 'model', 'year', 'current_price', 'market_trend',
            'price_change_percentage', 'last_price_update', 'display_name',
            'price_trend_display'
        ]
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    
    def get_price_trend_display(self, obj):
        trend_choices = dict(CarPricing._fields['market_trend'].choices)
        return trend_choices.get(obj.market_trend, obj.market_trend)


class PriceHistorySerializer(me_serializers.DocumentSerializer):
    """
    Serializer for PriceHistory model.
    """
    
    # Related fields
    car_pricing_id = serializers.CharField(write_only=True)
    
    # Read-only fields
    car_display_name = serializers.SerializerMethodField()
    market_condition_display = serializers.SerializerMethodField()
    
    class Meta:
        model = PriceHistory
        fields = [
            'id', 'car_pricing_id', 'price', 'price_date', 'price_change',
            'price_change_percentage', 'market_condition', 'economic_factors',
            'seasonal_factors', 'data_source', 'created_at', 'car_display_name',
            'market_condition_display'
        ]
        read_only_fields = [
            'id', 'price_change', 'price_change_percentage', 'created_at',
            'car_display_name', 'market_condition_display'
        ]
    
    def get_car_display_name(self, obj):
        """
        Get car display name.
        """
        return obj.car_pricing.get_display_name()
    
    def get_market_condition_display(self, obj):
        """
        Get market condition display name.
        """
        if obj.market_condition:
            condition_choices = dict(PriceHistory._fields['market_condition'].choices)
            return condition_choices.get(obj.market_condition, obj.market_condition)
        return None
    
    def validate_car_pricing_id(self, value):
        """
        Validate car pricing exists.
        """
        try:
            return CarPricing.objects.get(id=value, is_active=True)
        except CarPricing.DoesNotExist:
            raise serializers.ValidationError('قیمت‌گذاری خودرو مورد نظر یافت نشد.')
    
    def validate_price_date(self, value):
        """
        Validate price date.
        """
        if value > date.today():
            raise serializers.ValidationError('تاریخ قیمت نمی‌تواند در آینده باشد.')
        return value
    
    def validate_price(self, value):
        """
        Validate price is positive.
        """
        if value <= 0:
            raise serializers.ValidationError('قیمت باید بیشتر از صفر باشد.')
        return value
    
    def create(self, validated_data):
        """
        Create a new price history record.
        """
        car_pricing = validated_data.pop('car_pricing_id')
        
        history = PriceHistory(
            car_pricing=car_pricing,
            **validated_data
        )
        history.save()
        return history


class MarketAnalysisSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for MarketAnalysis model.
    """
    
    # Read-only computed fields
    scope_display = serializers.SerializerMethodField()
    trend_display = serializers.SerializerMethodField()
    recommendation_display = serializers.SerializerMethodField()
    
    class Meta:
        model = MarketAnalysis
        fields = [
            'id', 'brand', 'model', 'year_range_start', 'year_range_end',
            'analysis_date', 'period_start', 'period_end', 'average_price',
            'median_price', 'price_volatility', 'overall_trend', 'trend_strength',
            'predicted_price_1_month', 'predicted_price_3_months',
            'predicted_price_6_months', 'prediction_confidence', 'demand_factors',
            'supply_factors', 'external_factors', 'buy_recommendation',
            'sell_recommendation', 'analysis_method', 'data_quality_score',
            'sample_size', 'key_insights', 'risk_factors', 'opportunities',
            'created_at', 'updated_at', 'scope_display', 'trend_display',
            'recommendation_display'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'scope_display', 'trend_display',
            'recommendation_display'
        ]
    
    def get_scope_display(self, obj):
        """
        Get analysis scope display.
        """
        return obj.get_scope_display()
    
    def get_trend_display(self, obj):
        """
        Get trend display information.
        """
        if obj.overall_trend:
            trend_choices = dict(MarketAnalysis._fields['overall_trend'].choices)
            return {
                'trend': obj.overall_trend,
                'trend_display': trend_choices.get(obj.overall_trend, obj.overall_trend),
                'strength': obj.trend_strength
            }
        return None
    
    def get_recommendation_display(self, obj):
        """
        Get recommendation display information.
        """
        buy_choices = dict(MarketAnalysis._fields['buy_recommendation'].choices)
        sell_choices = dict(MarketAnalysis._fields['sell_recommendation'].choices)
        
        return {
            'buy': {
                'recommendation': obj.buy_recommendation,
                'display': buy_choices.get(obj.buy_recommendation, obj.buy_recommendation)
            } if obj.buy_recommendation else None,
            'sell': {
                'recommendation': obj.sell_recommendation,
                'display': sell_choices.get(obj.sell_recommendation, obj.sell_recommendation)
            } if obj.sell_recommendation else None
        }
    
    def validate_analysis_date(self, value):
        """
        Validate analysis date.
        """
        if value > date.today():
            raise serializers.ValidationError('تاریخ تحلیل نمی‌تواند در آینده باشد.')
        return value
    
    def validate_year_range_start(self, value):
        """
        Validate year range start.
        """
        if value is not None:
            current_year = datetime.now().year
            if value < 1350 or value > current_year + 2:
                raise serializers.ValidationError('سال شروع بازه معتبر نیست.')
        return value
    
    def validate_year_range_end(self, value):
        """
        Validate year range end.
        """
        if value is not None:
            current_year = datetime.now().year
            if value < 1350 or value > current_year + 2:
                raise serializers.ValidationError('سال پایان بازه معتبر نیست.')
        return value
    
    def validate_trend_strength(self, value):
        """
        Validate trend strength is between 0 and 1.
        """
        if value is not None and not (0 <= value <= 1):
            raise serializers.ValidationError('قدرت روند باید بین ۰ تا ۱ باشد.')
        return value
    
    def validate_prediction_confidence(self, value):
        """
        Validate prediction confidence is between 0 and 1.
        """
        if value is not None and not (0 <= value <= 1):
            raise serializers.ValidationError('اطمینان پیش‌بینی باید بین ۰ تا ۱ باشد.')
        return value
    
    def validate_data_quality_score(self, value):
        """
        Validate data quality score is between 0 and 1.
        """
        if value is not None and not (0 <= value <= 1):
            raise serializers.ValidationError('امتیاز کیفیت داده باید بین ۰ تا ۱ باشد.')
        return value
    
    def validate(self, data):
        """
        Validate market analysis data.
        """
        # Validate period dates
        period_start = data.get('period_start')
        period_end = data.get('period_end')
        
        if period_start and period_end and period_start >= period_end:
            raise serializers.ValidationError({
                'period_end': 'تاریخ پایان دوره باید بعد از تاریخ شروع باشد.'
            })
        
        # Validate year range
        year_start = data.get('year_range_start')
        year_end = data.get('year_range_end')
        
        if year_start and year_end and year_start > year_end:
            raise serializers.ValidationError({
                'year_range_end': 'سال پایان بازه باید بعد از سال شروع باشد.'
            })
        
        # Validate price fields are positive
        price_fields = [
            'average_price', 'median_price', 'predicted_price_1_month',
            'predicted_price_3_months', 'predicted_price_6_months'
        ]
        
        for field in price_fields:
            value = data.get(field)
            if value is not None and value <= 0:
                raise serializers.ValidationError({
                    field: 'قیمت باید بیشتر از صفر باشد.'
                })
        
        return data


class PriceAlertSerializer(me_serializers.DocumentSerializer):
    """
    Serializer for PriceAlert model.
    """
    
    # Related fields
    user_id = serializers.CharField(write_only=True)
    car_pricing_id = serializers.CharField(write_only=True)
    
    # Read-only fields
    car_display_name = serializers.SerializerMethodField()
    alert_type_display = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = PriceAlert
        fields = [
            'id', 'user_id', 'car_pricing_id', 'alert_type', 'target_price',
            'percentage_threshold', 'is_active', 'notification_methods',
            'last_triggered', 'trigger_count', 'created_at', 'updated_at',
            'car_display_name', 'alert_type_display', 'current_price'
        ]
        read_only_fields = [
            'id', 'last_triggered', 'trigger_count', 'created_at', 'updated_at',
            'car_display_name', 'alert_type_display', 'current_price'
        ]
    
    def get_car_display_name(self, obj):
        """
        Get car display name.
        """
        return obj.car_pricing.get_display_name()
    
    def get_alert_type_display(self, obj):
        """
        Get alert type display name.
        """
        type_choices = dict(PriceAlert._fields['alert_type'].choices)
        return type_choices.get(obj.alert_type, obj.alert_type)
    
    def get_current_price(self, obj):
        """
        Get current price of the car.
        """
        return obj.car_pricing.current_price
    
    def validate_user_id(self, value):
        """
        Validate user exists.
        """
        try:
            return User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('کاربر مورد نظر یافت نشد.')
    
    def validate_car_pricing_id(self, value):
        """
        Validate car pricing exists.
        """
        try:
            return CarPricing.objects.get(id=value, is_active=True)
        except CarPricing.DoesNotExist:
            raise serializers.ValidationError('قیمت‌گذاری خودرو مورد نظر یافت نشد.')
    
    def validate_target_price(self, value):
        """
        Validate target price is positive.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError('قیمت هدف باید بیشتر از صفر باشد.')
        return value
    
    def validate_percentage_threshold(self, value):
        """
        Validate percentage threshold is positive.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError('آستانه درصدی باید بیشتر از صفر باشد.')
        return value
    
    def validate(self, data):
        """
        Validate price alert data.
        """
        alert_type = data.get('alert_type')
        target_price = data.get('target_price')
        percentage_threshold = data.get('percentage_threshold')
        
        # Validate required fields based on alert type
        if alert_type == 'target_price' and not target_price:
            raise serializers.ValidationError({
                'target_price': 'برای هشدار قیمت هدف، باید قیمت هدف را مشخص کنید.'
            })
        
        if alert_type == 'percentage_change' and not percentage_threshold:
            raise serializers.ValidationError({
                'percentage_threshold': 'برای هشدار تغییر درصدی، باید آستانه درصدی را مشخص کنید.'
            })
        
        # Validate notification methods
        notification_methods = data.get('notification_methods', [])
        if not notification_methods:
            raise serializers.ValidationError({
                'notification_methods': 'حداقل یک روش اطلاع‌رسانی باید انتخاب شود.'
            })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new price alert.
        """
        user = validated_data.pop('user_id')
        car_pricing = validated_data.pop('car_pricing_id')
        
        alert = PriceAlert(
            user=user,
            car_pricing=car_pricing,
            **validated_data
        )
        alert.save()
        return alert
    
    def update(self, instance, validated_data):
        """
        Update an existing price alert.
        """
        user = validated_data.pop('user_id', None)
        car_pricing = validated_data.pop('car_pricing_id', None)
        
        if user:
            instance.user = user
        if car_pricing:
            instance.car_pricing = car_pricing
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class PriceAlertListSerializer(me_serializers.DocumentSerializer):
    """
    Simplified serializer for PriceAlert list views.
    """
    
    car_display_name = serializers.SerializerMethodField()
    alert_type_display = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = PriceAlert
        fields = [
            'id', 'alert_type', 'alert_type_display', 'target_price',
            'percentage_threshold', 'is_active', 'car_display_name',
            'current_price', 'last_triggered', 'trigger_count'
        ]
    
    def get_car_display_name(self, obj):
        return obj.car_pricing.get_display_name()
    
    def get_alert_type_display(self, obj):
        type_choices = dict(PriceAlert._fields['alert_type'].choices)
        return type_choices.get(obj.alert_type, obj.alert_type)
    
    def get_current_price(self, obj):
        return obj.car_pricing.current_price


class PriceComparisonSerializer(serializers.Serializer):
    """
    Serializer for price comparison data.
    """
    
    brand = serializers.CharField()
    model = serializers.CharField()
    year = serializers.IntegerField()
    current_price = serializers.IntegerField()
    market_trend = serializers.CharField()
    price_change_percentage = serializers.FloatField()
    
    class Meta:
        fields = ['brand', 'model', 'year', 'current_price', 'market_trend', 'price_change_percentage']


class MarketTrendSerializer(serializers.Serializer):
    """
    Serializer for market trend data.
    """
    
    date = serializers.DateField()
    average_price = serializers.IntegerField()
    price_change = serializers.IntegerField()
    price_change_percentage = serializers.FloatField()
    volume = serializers.IntegerField()
    
    class Meta:
        fields = ['date', 'average_price', 'price_change', 'price_change_percentage', 'volume']


class PriceEstimationSerializer(serializers.Serializer):
    """
    Serializer for price estimation requests.
    """
    
    brand = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    mileage = serializers.IntegerField()
    condition = serializers.ChoiceField(
        choices=[
            ('excellent', 'عالی'),
            ('good', 'خوب'),
            ('fair', 'متوسط'),
            ('poor', 'ضعیف'),
        ]
    )
    fuel_type = serializers.CharField(max_length=20, required=False)
    transmission_type = serializers.CharField(max_length=20, required=False)
    
    def validate_year(self, value):
        """
        Validate year is reasonable.
        """
        current_year = datetime.now().year
        if value < 1350 or value > current_year + 2:
            raise serializers.ValidationError('سال ساخت معتبر نیست.')
        return value
    
    def validate_mileage(self, value):
        """
        Validate mileage is reasonable.
        """
        if value < 0 or value > 1000000:
            raise serializers.ValidationError('کیلومتر معتبر نیست.')
        return value
    
    class Meta:
        fields = ['brand', 'model', 'year', 'mileage', 'condition', 'fuel_type', 'transmission_type']


class PriceEstimationResultSerializer(serializers.Serializer):
    """
    Serializer for price estimation results.
    """
    
    estimated_price = serializers.IntegerField()
    price_range_min = serializers.IntegerField()
    price_range_max = serializers.IntegerField()
    confidence_score = serializers.FloatField()
    market_trend = serializers.CharField()
    factors_affecting_price = serializers.ListField(child=serializers.CharField())
    recommendations = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        fields = [
            'estimated_price', 'price_range_min', 'price_range_max',
            'confidence_score', 'market_trend', 'factors_affecting_price',
            'recommendations'
        ]


class PricingStatsSerializer(serializers.Serializer):
    """
    Serializer for pricing statistics.
    """
    
    total_cars = serializers.IntegerField()
    average_price = serializers.IntegerField()
    median_price = serializers.IntegerField()
    price_range_min = serializers.IntegerField()
    price_range_max = serializers.IntegerField()
    trending_up_count = serializers.IntegerField()
    trending_down_count = serializers.IntegerField()
    stable_count = serializers.IntegerField()
    most_expensive_brands = serializers.ListField()
    most_affordable_brands = serializers.ListField()
    popular_models = serializers.ListField()
    
    class Meta:
        fields = [
            'total_cars', 'average_price', 'median_price', 'price_range_min',
            'price_range_max', 'trending_up_count', 'trending_down_count',
            'stable_count', 'most_expensive_brands', 'most_affordable_brands',
            'popular_models'
        ]
