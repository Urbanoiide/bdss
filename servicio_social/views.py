from django.shortcuts import render
from .models import ResumenDocumentos
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    documentos_list = ResumenDocumentos.objects.select_related(
        'servicio_social__prestador', 'servicio_social__institucion'
    ).all()

    paginator = Paginator(documentos_list, 5)  # 5 registros por página
    page_number = request.GET.get('page')
    documentos = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'documentos': documentos,
        'total_documentos': documentos_list.count()
    })
