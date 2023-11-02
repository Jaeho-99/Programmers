from django.contrib import admin
from .models import *

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문', {'fields' : ['question_text']}),
        ('생성일', {'fields' : ['pub_date'], 'classes' : ['collapse']}),
    ]
    # str 메소드를 사용하지 않고, 제목 / 날짜가 예쁘게 나오도록 리스트화.
    # (필드명, )
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    # 필터링 기능. 필드의 타입에 맞춰 자동으로 제공함.
    list_filter = ['pub_date']
    # 문자열 검색에 따른 필터링 기능. question_text와 choice_text에 대해 검색.
    search_fields = ['question_text', 'choice__choice_text']

admin.site.register(Question, QuestionAdmin)