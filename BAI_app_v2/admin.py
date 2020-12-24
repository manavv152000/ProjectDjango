from django.contrib import admin
from BAI_app_v2.models import ParticipantInfo, Speed, SafetynWellfare, Others, Economy, Project_info, Quality, Category, PaymentDetails

# Register your models here.
admin.site.register(ParticipantInfo)
admin.site.register(Speed)

admin.site.register(SafetynWellfare)
admin.site.register(Others)
admin.site.register(Economy)

admin.site.register(Project_info)
admin.site.register(Quality)

admin.site.register(Category)
admin.site.register(PaymentDetails)
