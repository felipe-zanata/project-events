from django.contrib import admin
from .models import Estado, Artista, AgendarEvento, Pagamentos,DescricaoStatus,OrigemDestinoKm

# Register your models here.
admin.site.register(Estado)
admin.site.register(Artista)
admin.site.register(AgendarEvento)
admin.site.register(Pagamentos)
admin.site.register(DescricaoStatus)
admin.site.register(OrigemDestinoKm)