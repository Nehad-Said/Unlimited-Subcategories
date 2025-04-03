from .models import Category
from django.shortcuts import render
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def category_list(request):
    try:
        categories = Category.objects.filter(parent__isnull=True)  # Retrieve only top-level categories
        return render(request, 'rightshero/categories.html', {'categories': categories})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Consider using a more secure approach in production
def manage_subcategories(request):
    if request.method == 'POST':
        try:
            parent_id = request.POST.get('parent_id')
            if not parent_id:
                return JsonResponse({'error': 'Parent ID is required'}, status=400)
                
            parent_category = Category.objects.get(id=parent_id)
            response_data = []
            
            # Generate specific subcategory names based on parent category
            for i in range(1, 3):  # always two subcategories are created
                subcategory_name = f"SUB {parent_category.name}-{i}"
                subcategory, created = Category.objects.get_or_create(name=subcategory_name, parent=parent_category)
                response_data.append({'id': subcategory.id, 'name': subcategory.name, 'created': created})
                
            return JsonResponse({'subcategories': response_data})
            
        except Category.DoesNotExist:
            return JsonResponse({'error': f'Category with ID {parent_id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    elif request.method == 'GET':
        try:
            category_id = request.GET.get('category_id')
            if not category_id:
                return JsonResponse({'error': 'Category ID is required'}, status=400)
                
            subcategories = Category.objects.filter(parent_id=category_id).values('id', 'name')
            return JsonResponse({'subcategories': list(subcategories)})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
