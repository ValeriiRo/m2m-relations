from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scopes


class TagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        real_forms = [form for form in self.forms if not form.cleaned_data['DELETE']]
        tags_id = set([form.cleaned_data['tag'].id for form in real_forms])
        if len(tags_id) != len(real_forms):
            raise ValidationError('Обнаружены повторяющиеся теги')
        tags_is_main = [form for form in self.forms if form.cleaned_data['is_main'] is True]
        if len(tags_is_main) >= 2:
            raise ValidationError('Основным может быть только один раздел!')
        if len(tags_is_main) == 0:
            raise ValidationError('Укажите основной раздел!')
        return super().clean()


class ScopesInline(admin.TabularInline):
    model = Scopes
    extra = 0
    formset = TagsInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [ScopesInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
