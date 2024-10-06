from django.http import JsonResponse
from django.views import View
from .models import LogEntry
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def log_entry_list(request):
    query = request.GET.get("q", "")
    selected_category = request.GET.get("category", "all")

    # Получаем все уникальные категории
    categories = (
        LogEntry.objects.order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )

    # Фильтруем записи по категории и поисковому запросу
    if selected_category == "all":
        log_entries = LogEntry.objects.filter(
            Q(category__icontains=query)
            | Q(message__icontains=query)
            | Q(user__icontains=query)
        ).order_by("-timestamp")
    else:
        log_entries = LogEntry.objects.filter(
            Q(category=selected_category)
            & (Q(message__icontains=query) | Q(user__icontains=query))
        ).order_by("-timestamp")

    paginator = Paginator(log_entries, 10)  # 10 записей на странице
    page_number = request.GET.get("page")

    try:
        log_entries = paginator.get_page(page_number)
    except PageNotAnInteger:
        log_entries = paginator.get_page(1)
    except EmptyPage:
        log_entries = paginator.get_page(paginator.num_pages)

    context = {
        "log_entries": log_entries,
        "query": query,
        "categories": categories,
        "selected_category": selected_category,
    }
    return render(request, "logs/log_entry_list.html", context)


@method_decorator(csrf_exempt, name="dispatch")
class AddLogView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            category = data.get("category")
            message = data.get("message")
            user = data.get("user")

            if category is None:
                return JsonResponse(
                    {"error": "Вы забыли указать категорию"}, status=400
                )
            if user is None:
                return JsonResponse(
                    {"error": "Вы забыли указать имя пользователя"}, status=400
                )

            log_entry = LogEntry.objects.create(
                category=category,
                message=message,
                user=user,
            )
            return JsonResponse(
                {"id": log_entry.id, "message": "Лог добавлен"}, status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат данных"}, status=400)
