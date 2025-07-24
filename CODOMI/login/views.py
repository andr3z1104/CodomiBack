from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from login.models import Email
from supabase.auth import login_with_supabase

@csrf_exempt  # Solo en desarrollo
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método no permitido'}, status=405)

    try:
        body = json.loads(request.body)
        email = body.get('ema_email')
        password = body.get('use_passwords')

        if not email or not password:
            return JsonResponse({'detail': 'Faltan campos'}, status=400)

        # Hacemos login con Supabase Auth
        auth_response = login_with_supabase(email, password)
        jwt_token = auth_response.get('access_token')
        user_info = auth_response.get('user')

        # Buscamos en nuestra base de datos local los datos adicionales
        email_obj = Email.objects.get(ema_email=email)
        user = email_obj.use

        return JsonResponse({
            'token': jwt_token,
            'user_data': {
                'use_id': user.use_id,
                'use_name': user.use_name,
                'uset_id': user.uset.uset_id,
                'uset_type': user.uset.uset_type,
                'email': email
            }
        })

    except Email.DoesNotExist:
        return JsonResponse({'detail': 'Correo no registrado'}, status=404)
    except ValueError as ve:
        return JsonResponse({'detail': str(ve)}, status=401)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)
