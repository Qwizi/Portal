from django.contrib import admin
from shop import models


admin.site.register(models.Payment)
admin.site.register(models.Premium)
admin.site.register(models.PremiumCache)
admin.site.register(models.Price)
admin.site.register(models.Bonus)
admin.site.register(models.SMSNumber)
admin.site.register(models.Service)
admin.site.register(models.PromotionCode)
admin.site.register(models.PromotionServicePrice)
