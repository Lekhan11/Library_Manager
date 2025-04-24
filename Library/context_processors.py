from .models import Setting

def logo_context(request):
    setting = Setting.objects.first()
    return {
        'logo': setting.logo if setting else None 
    }