from django.http import JsonResponse


OK = JsonResponse(dict({'status': 'OK'}), status=200, safe=False)
CREATED = JsonResponse(dict({'status': 'CREATED'}), status=201, safe=False)
BAD_REQUEST = JsonResponse(dict({'status': 'BAD'}), status=400, safe=False)
NOT_FOUND = JsonResponse(dict({'status': 'NOT FOUND'}), status=404, safe=False)
PERMISSION_DENIED = JsonResponse(dict({'status': 'FORBIDDEN'}), status=403, safe=False)
