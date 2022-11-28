from rest_framework import serializers


class LanguageSerizlizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    code = serializers.CharField()
    icon = serializers.ImageField()


class LevelSerizlizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TagSerizlizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class DictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    lang = serializers.SerializerMethodField()
    lang_from = LanguageSerizlizer(source='language_from')
    lang_to = LanguageSerizlizer(source='language_to')
    level = serializers.CharField(source="level.name")
    tags = serializers.ListSerializer(child=serializers.CharField(source="name"))
    rating = serializers.SerializerMethodField()

    def get_lang(self, dictionary):
        return f"{dictionary.language_from.code.upper()}-{dictionary.language_to.code.upper()}"

    def get_rating(self, dictionary):
        return dictionary.average_rate or "-"


class DictionaryDetailSerializer(DictionarySerializer):
    owner = serializers.CharField(source='owner.username')
    rates_count = serializers.IntegerField(source='rates_cnt')
    date = serializers.DateField(source='date_created')
    pinned = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    last_date = serializers.SerializerMethodField()

    def get_pinned(self, obj):
        return obj.pinned.filter(id=self.context['request'].user.id).exists()

    def get_is_mine(self, obj):
        return obj.owner == self.context['request'].user

    def get_count(self, obj):
        return obj.words.count()

    def get_last_date(self, obj):
        attempt = obj.attempts.order_by("-date").first()
        return attempt and attempt.date
