from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Email

@csrf_exempt # Solo para desarrollo
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método no permitido'}, status=405)

    try:
        body = json.loads(request.body)
        email = body.get('ema_email')
        password = body.get('use_passwords')

        if not email or not password:
            return JsonResponse({'detail': 'Faltan campos'}, status=400)

        email_obj = Email.objects.get(ema_email=email)
        user = email_obj.use

        if user.use_passwords != password:
            return JsonResponse({'detail': 'Contraseña inválida'}, status=401)

        return JsonResponse({
            'use_id': user.use_id,
            'use_name': user.use_name,
            'uset_id': user.uset.uset_id,
            'uset_type': user.uset.uset_type,
        })

    except Email.DoesNotExist:
        return JsonResponse({'detail': 'Correo no registrado'}, status=404)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)
