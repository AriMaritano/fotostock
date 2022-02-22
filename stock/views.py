from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from .forms import UploadStock, VerStock
from .models import File, Result
from django.conf import settings
from.tools import fotostockear, ver
from os import path
from django.utils import dateformat
from datetime import timedelta



def show_results(request):
    results = Result.objects.order_by('-date_created')
    results_list = []
    context = {
        'results_list': results_list,
    }
    for result in results:
        if len(results_list)>0:
            if results_list[-1]['data'] == result.data.split(", "):
                print("check")#, result.data.split(", "), "\n", results_list[-1]['data'])
                continue
        results_list.append({
            'pk': result.pk,
            'data': result.data.split(", "),
            'file1': result.file1.filename,
            'file2': result.file2.filename,
            'date_created': result.date_created + timedelta(hours=-3)
        })
    return render(request, "stock/results.html", context)


def show_files(request):
    files = File.objects.order_by('-date_uploaded')
    return render(request, "stock/files.html", {'files': files})


def fotostock(request):
    last_file = Result.objects.order_by('-date_created')[0].file2
    if request.method == "POST":
        if 'file3' in request.FILES:
            file3 = request.FILES['file3']
            if not path.isfile(path.join(settings.BASE_DIR, 'files', file3.name)):
                newfile3 = File(file=file3, filename=file3.name)
                newfile3.save()
            else:
                newfile3 = File.objects.get(filename=file3.name)
            results = fotostockear(last_file.file, file3)
            new_results = Result(data=", ".join(results), file1=last_file, file2=newfile3)
            new_results.save()
            return render(request, 'stock/fotostockear.html', {'last_file': last_file, 'results': results})
        file1 = request.FILES['file1']
        if not path.isfile(path.join(settings.BASE_DIR, 'files', file1.name)):
            newfile1 = File(file=file1, filename=file1.name)
            newfile1.save()
        else:
             newfile1 = File.objects.get(filename=file1.name)
        file2 = request.FILES['file2']
        if not path.isfile(path.join(settings.BASE_DIR, 'files', file2.name)):
            newfile2 = File(file=file2, filename=file2.name)
            newfile2.save()
        else:
            newfile2 = File.objects.get(filename=file2.name)
        results = fotostockear(file1, file2)
        new_results = Result(data=", ".join(results), file1=newfile1, file2=newfile2)
        new_results.save()
    else:
        results = None
    return render(request, 'stock/fotostockear.html', {'last_file': last_file, 'results': results})


def ver_stock(request):
    if request.method == 'POST':
        consulta = request.POST['consulta']
        file = File.objects.order_by('-date_uploaded')[0]
        resultados_busqueda = ver(consulta, file.file)
        form = VerStock()
        context = {
            'resultados_busqueda': resultados_busqueda,
            'consulta': consulta,
            'form': form,
            'file': file.filename,
            'date_uploaded': dateformat.format(file.date_uploaded, 'Y-m-d H:i:s')
        }
        if not resultados_busqueda:
            context['sin_resultados'] = True
    else:
        form = VerStock()
        context = {
            'resultados_busqueda': None,
            'form': form
        }
    return render(request, 'stock/ver_precios.html', context)
