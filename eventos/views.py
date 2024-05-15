from datetime import datetime
import json
from django.db.models import Q, ForeignKey, CharField, DateTimeField, TextField
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AgendarEventoForms, ArtistaForm, PagamentosForms
from .models import AgendarEvento, Artista, Estado, OrigemDestinoKm,DescricaoStatus,Pagamentos
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import re
from django.views.generic import ListView,DetailView, UpdateView, DeleteView,CreateView, View
from itertools import groupby
from decouple import config
import ipdb
from urllib.parse import urlencode  # Importe urlencode do submódulo urllib.parse
import requests
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import constants

from django.db.models import F, Value
from django.db.models.functions import Concat


############################################################################################################################################################
# API
############################################################################################################################################################

def origem_destino(request):
    if request.method == 'GET':
        return redirect('eventos/listar_eventos/')

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        origem_evento = data.get('cidade')
        origem_uf = data.get('uf')
        uf = data.get('UF')
        artista = data.get('artista')
        vendedor = data.get('vendedor')
        ano = data.get('ano')
        mes = data.get('mes')
        status = data.get('status')

        eventos = AgendarEvento.objects.all()

        if artista:
            eventos = eventos.filter(artista__nome_social__icontains=artista)

        if vendedor:
            eventos = eventos.filter(nome_vendedor__icontains=vendedor)

        if uf:
            ufs_selecionados =[uf.strip() for uf in uf.split(";")]
            eventos = eventos.filter(uf__in=ufs_selecionados)

        if ano:
            ano_datetime = datetime(int(ano), 1, 1)
            eventos = eventos.filter(data_evento__year=ano_datetime.year)

        if mes:
            lista_meses = str(mes).replace(' ','').strip().split(';')
            eventos = eventos.filter(data_evento__month__in=lista_meses)

        if status:
            status_id = str(status).replace(' ','').strip().split(';')
            eventos = eventos.filter(status_id__in=status_id)

        destinos = eventos.annotate(cidade_uf=Concat(F('cidade'), Value(', '), F('uf')))
        lista_destinos = set(destinos.values_list('cidade_uf', flat=True))

        for destino_uf in lista_destinos:
            if origem_evento in destino_uf:
                origem_evento = destino_uf

        for destino in lista_destinos:
            try:
                result = OrigemDestinoKm.objects.get(origem=origem_evento, destino=destino)
            except OrigemDestinoKm.DoesNotExist:
                if origem_evento != destino:
                    distancia, horas = distancia_origem_destino(origem_evento, destino)
                    if distancia and horas:
                        novo_registro = OrigemDestinoKm(
                            origem=origem_evento,
                            destino=destino,
                            km=distancia.replace(',', '.'),
                            horas=horas
                        )
                        novo_registro.save()

        locais = OrigemDestinoKm.objects.filter(origem=origem_evento, destino__in=lista_destinos)
        locais_data = [
            {'destino': local.destino, 'km': local.km, 'horas': local.horas} for local in locais
        ]
        return JsonResponse({'locais': locais_data})

    return redirect('eventos/listar_eventos/')
   
def distancia_origem_destino(origin, destination):
    try:
        api_key = 'AIzaSyB6Zv-Pr_P6tm4ysw2B9OiOeEL8doYRRIk'

        base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        params = {
            'origins': f'{origin}, Brazil',
            'destinations': f'{destination}, Brazil',
            'key': api_key,
        }
        params_str = urlencode(params)

        full_url = f'{base_url}?{params_str}'

        response = requests.get(full_url)
        data = response.json()
        print(data)
        distance_km = ""
        horas = ""
        if response.status_code == 200 and data['status'] == 'OK':
            distance_km = data['rows'][0]['elements'][0]['distance']['text']
            horas = data['rows'][0]['elements'][0]['duration']['text']
            horas = formata_texto_horas(horas)
        else:
            distance_km = None 
            horas = None   

        return distance_km, horas
    except Exception as e:
        print(e)
        return '', ''

def formata_texto_horas(texto: str):
    if texto:
        texto_formatado = texto.replace('days', 'd')\
                            .replace('day', 'd')\
                            .replace('hours', 'h')\
                            .replace('hour', 'h')\
                            .replace('mins', 'm')\
                            .replace('min', 'm')
        return texto_formatado
############################################################################################################################################################
# PARCELAS
############################################################################################################################################################
def nova_parcela(request):
    if request.method == 'POST':
        ipdb.set_trace()
        data = request.POST.get('data')
        valor = request.POST.get('valor')

        novo_pgto = Pagamentos()

        novo_pgto(
            evento =1,
            semana = '1°',
            data_pagamento = data,
            valor = valor

        )

############################################################################################################################################################
# EVENTOS
############################################################################################################################################################
class AgendarEventosListView(ListView):
    model = AgendarEvento
    template_name = 'eventos_list.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        eventos = AgendarEvento.objects.all().order_by('data_evento') 
        cidade = self.request.GET.get('Cidade')
        uf = self.request.GET.get('UF')
        vendedor = self.request.GET.get('Vendedor')
        ano = self.request.GET.get('Ano')
        mes = self.request.GET.get('Mes')
        status = self.request.GET.get('Status')
        artista = self.request.GET.get('Artista')

        if artista:
            eventos = eventos.filter(artista__nome_social=artista)
        if cidade:
            eventos = eventos.filter(cidade__icontains=cidade)
        if uf:
            ufs_selecionados =[uf.strip() for uf in uf.split(";")]
            eventos = eventos.filter(uf__in=ufs_selecionados)
        if vendedor:
            eventos = eventos.filter(nome_vendedor__icontains=vendedor)
        if ano:
            anos_selecionados = ano.split(";")
            eventos = eventos.filter(data_evento__year__in=anos_selecionados)
        if mes:
            meses_selecionados = mes.split(";")
            eventos = eventos.filter(data_evento__month__in=meses_selecionados)
        if status:
            ids_status = status.split(";")
            eventos = eventos.filter(status__id__in=ids_status)

        for key, group in groupby(eventos, key=lambda x: (x.data_evento.year, x.data_evento.month)):
            group_list = list(group)
            for i, evento in enumerate(group_list):
                evento.show_month_title = i == 0
                evento.show_year_title = i == 0 and evento.show_month_title

        return eventos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = AgendarEvento.objects.all()
        uf = self.request.GET.get('UF')
        artista = self.request.GET.get('Artista')
        artistas = query.values_list('artista__nome_social',flat=True).distinct()

        print(artista)
        if uf:
            ufs_selecionados =[uf.strip() for uf in uf.split(";")]
            query = query.filter(uf__in=ufs_selecionados)
        
        if artista:
            query = query.filter(artista__nome_social=artista)

        ufs = query.values_list('uf',flat=True).distinct().order_by('uf')
        cidades = query.values_list('cidade',flat=True).distinct().order_by('cidade')
  
        context['status'] = DescricaoStatus.objects.all()
        context['artistas'] = artistas
        context['cidades'] = cidades
        context['ufs'] = ufs
        context['anos'] = query.dates('data_evento', 'year')
        context['meses'] = query.dates('data_evento', 'month')

        return context

class AgendarEventosDetailView(DetailView):
    model = AgendarEvento
    template_name = 'eventos_detalhe.html'
    success_url = '/eventos/evento_detalhe/'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['form'] = AgendarEventoForms(instance =self.get_object())
        context['form1'] = PagamentosForms()
        context['pagamentos'] = Pagamentos.objects.filter(evento=self.get_object())
        context['status'] = DescricaoStatus.objects.filter()
        context['estados'] = Estado.objects.filter()
        context['status_diaria'] = AgendarEvento.TIPO_DIARIA
        context['artistas'] = Artista.objects.all()
        context['source_page'] = self.request.GET.get('source_page')

        return context
    
    def post(self, request, *args, **kwargs):
        
        form1 = PagamentosForms(request.POST)
        pgto_id = request.POST.get('pgto_id')
        source_page = request.POST.get('source_page')
        if form1.is_valid():
            try:
                if pgto_id:
                    update_pgto = Pagamentos.objects.get(pk=pgto_id)
                    form1 = PagamentosForms(request.POST, instance=update_pgto)
                novo_pagamento = form1.save(commit=False)
                novo_pagamento.evento = self.get_object()
                novo_pagamento.save()
                id_evento = self.get_object().pk
            except:
                pass
            return redirect(f'/eventos/evento_detalhe/{id_evento}')
        
        
        pagamentos = Pagamentos.objects.filter(evento=self.get_object())
        return render(request, self.template_name, {'form1': form1,
                                                    'pagamentos': pagamentos, 
                                                    'eventos': self.get_object(),
                                                    'source_page': source_page})
    
def remover_pagamento(request):
    id = request.POST.get('pagamento_id')
    pagamento = get_object_or_404(Pagamentos, pk=id)
    evento_pk = pagamento.evento.pk
    pagamento.delete()
    
    return redirect(f'/eventos/evento_detalhe/{evento_pk}')

def remover_evento(request):
    id = request.POST.get('evento_id')
    evento = get_object_or_404(AgendarEvento, pk=id)
    evento.delete()
    
    return redirect(f'/eventos/listar_eventos/')

class AgendarEventosCreateView(CreateView):
    model = AgendarEvento
    form_class = AgendarEventoForms
    template_name = 'eventos_criar.html'
    success_url = '/eventos/listar_eventos'

class ObterUFCidadesView(View):
    def get(self, request, *args, **kwargs):
        estado_id = request.GET.get('estado_id')
        estado = get_object_or_404(Estado, pk=estado_id)

        ufs = [estado.sigla]
        cidades = estado.cidades.split(',') if estado.cidades else []
        cidades = [re.sub(r'[\"[\]]', '', cidade) for cidade in cidades]

        data = {'ufs': ufs, 'cidades': cidades}
        return JsonResponse(data)

class AtualizarEvento(View):
    
    def post(self, request, *args, **kwargs):
        pk= request.POST.get('pk')
        novo_valor= request.POST.get('novo_valor')
        nomeColuna= request.POST.get('nomeColuna')
        try:
            evento = AgendarEvento.objects.get(pk=pk)
        except:
            pass

        if nomeColuna == 'pagamento_status':
            try:
                novo_status = Pagamentos.objects.get(pk=pk)
                novo_status.pagamento_status = novo_valor
                novo_status.save()
            except ValidationError as ve:
                print('erro')
                return JsonResponse({'error': str(ve)}, status=400)
            except Exception as e:
                print('erro2')
                return JsonResponse({'error': str(e)}, status=500)
    
        # ipdb.set_trace()
        if hasattr(AgendarEvento,nomeColuna):
            try:
                if nomeColuna == 'artista':
                    novo_valor = Artista.objects.get(pk=novo_valor)
                    setattr(evento,nomeColuna, novo_valor)
                if nomeColuna == 'status':
                    novo_valor = DescricaoStatus.objects.get(pk=novo_valor)
                    setattr(evento,nomeColuna, novo_valor)

                # elif nomeColuna in ['comissao', 'producao', 'valor_diaria']:
                #     novo_valor = str(novo_valor).replace('.','').replace(',','.')
                #     novo_valor = float(novo_valor)
                #     setattr(evento,nomeColuna, novo_valor)

                elif nomeColuna == 'diaria':
                    setattr(evento,nomeColuna, novo_valor)

                elif nomeColuna in ['cidade' , 'estado']:
                    
                    valores = request.POST.getlist('lista_valores[]',[])
                    novo_estado = Estado.objects.get(pk=int(valores[2]))
                    setattr(evento,'estado', novo_estado)
                    setattr(evento,'cidade', valores[0])
                    setattr(evento,'uf', valores[1])
                else:
                    # ipdb.set_trace()
                    setattr(evento,nomeColuna, novo_valor)

                evento.save()

            except ValidationError as ve:
                print('erro')
                return JsonResponse({'error': str(ve)}, status=400)
            except Exception as e:
                print('erro2')
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Atualização bem-sucedida'})

def cadastro_evento(request):

    if request.method == 'GET':
        form = AgendarEventoForms()
        artista = Artista.objects.all()
        estados = Estado.objects.all()

    elif request.method == 'POST':

        form = AgendarEventoForms(request.POST)

        # if form.is_valid():
        proc = request.POST.get('uf')
        estado = Estado.objects.get(sigla= proc)
        evento = AgendarEvento(
                data_evento = request.POST.get('data_evento'),
                artista_id = request.POST.get('artista'),
                estado = estado.estado,
                uf = request.POST.get('uf'),
                cidade = request.POST.get('cidade'),
                comissao = request.POST.get('comissao'),
                producao = request.POST.get('producao'),
                valor_show = request.POST.get('valor_show'),
                nome_vendedor =  request.POST.get('nome_vendedor'),
                status = request.POST.get('status'),
                obs = request.POST.get('obs')
            )
        evento.save()
        return redirect('/eventos/listar_eventos/')

    return render(request,'cadastrar_evento.html', {'form': form,
                                                    'artistas': artista,
                                                    'estados': estados})

class CompartilharEventosListView(ListView):
    model = AgendarEvento
    template_name = 'eventos_compartilhar.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        eventos = AgendarEvento.objects.all().order_by('data_evento') 
        lista = super().get_queryset()
        cidade = self.request.GET.get('Cidade')
        vendedor = self.request.GET.get('Vendedor')
        ano = self.request.GET.get('Ano')
        mes = self.request.GET.get('Mes')
        status = self.request.GET.get('Status')
        artista = self.request.GET.get('artista')

        if artista:
            eventos = eventos.filter(artista__nome_social=artista)
        if cidade:
            eventos = eventos.filter(cidade__icontains=cidade)
        if vendedor:
            eventos = eventos.filter(nome_vendedor__icontains=vendedor)
        if ano:
            anos_selecionados = ano.split(";")
            eventos = eventos.filter(data_evento__year__in=anos_selecionados)
        if mes:
            meses_selecionados = mes.split(";")
            eventos = eventos.filter(data_evento__month__in=meses_selecionados)
        if status:
            ids_status = status.split(";")
            eventos = eventos.filter(status__id__in=ids_status)

        for key, value in self.request.GET.items():
            if key not in ['page']:
                if value:
                    if key == 'filtro_geral':
                        filter_query = Q()
                        for field in self.model._meta.get_fields():
                            if isinstance(field, CharField):
                                try:
                                    if field.get_internal_type() == 'DateField':
                                        filter_query |= Q(**{f'{field.name}__date': value})
                                    else:
                           
                                        filter_query |= Q(**{f'{field.name}__icontains': value})
                                except Exception as e:
                                    print(e)
                                    pass
                            elif isinstance(field, TextField):
                                try:
                                    filter_query |= Q(**{f'{field.name}__icontains': value})
                                except Exception as e:
                                    print(e)
                                    pass
                            elif isinstance(field, DateTimeField):
                                try:
                                    dta_formatada = datetime.strptime(value, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                                    valor_data_hora = timezone.make_aware(datetime.strptime(dta_formatada, "%Y-%m-%d %H:%M:%S"))
                                    filter_query |= Q(**{f'{field.name}__date': valor_data_hora})
                                except Exception as e:
                                    print(e)
                                    pass

                            elif isinstance(field, ForeignKey):
                                try:
                                    if field.name == 'artista':
                                        filtro = {'nome_social__icontains': value}
                                    else:
                                        filtro = {f'{field.name}__icontains': value}

                                    model = field.related_model.__name__
                                    related_id = globals()[model].objects.get(**filtro).id
                                    filter_query |= Q(**{f'{field.name}__id': related_id})
                                except Exception as e:
                                    pass

                        eventos = eventos.filter(filter_query)

        for key, group in groupby(eventos, key=lambda x: (x.data_evento.year, x.data_evento.month)):
            group_list = list(group)
            for i, evento in enumerate(group_list):
                evento.show_month_title = i == 0
                evento.show_year_title = i == 0 and evento.show_month_title

        return eventos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artistas = AgendarEvento.objects.values_list('artista__nome_social',flat=True).distinct()
        # cidades = AgendarEvento.objects.values_list('artista__cidade',flat=True).distinct()
        context['status'] = DescricaoStatus.objects.all()
        context['artistas'] = artistas
        # context['cidades'] = cidades
        context['anos'] = AgendarEvento.objects.dates('data_evento', 'year')
        context['meses'] = AgendarEvento.objects.dates('data_evento', 'month')

        return context
    
def obter_cidades(request):
    uf = request.GET.get('uf', None)

    if uf:
        estado = get_object_or_404(Estado, sigla=uf)
        cidades = estado.cidades.split(',') if estado.cidades else []
        cidades = [re.sub(r'[\"[\]]', '', cidade) for cidade in cidades]
        return JsonResponse({'cidades': cidades})

    return JsonResponse({'cidades': []})

############################################################################################################################################################
# ARTISTAS
############################################################################################################################################################
def artistas_list(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artistas_list')
        
    artistas = Artista.objects.all()
    form = ArtistaForm()
    context = {'artistas': artistas, 'form': form}

    return render(request, 'artistas_list.html', context)

def adicionar_artista(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artistas_list')
    else:
        artistas = Artista.objects.all()
        form = ArtistaForm()
    return render(request, 'artistas_list.html', {'artistas': artistas,'form': form})

def alterar_artista(request, id):
    artista = get_object_or_404(Artista, pk=id)
    if request.method == 'POST':
        form = ArtistaForm(request.POST, instance=artista)

        if form.is_valid():
            form.save()
            return redirect('artistas_list')
        else:
            artistas = Artista.objects.all()
            form = ArtistaForm(instance=artista)
            context = {'artistas': artistas, 'form': form}
    else:
        artistas = Artista.objects.all()
        form = ArtistaForm(instance=artista)
        context = {'artistas': artistas, 'form': form}

    return render(request, 'artistas_list.html', context)

def deletar_artista(request):
    try:
        id = request.POST.get('artista_id')
        artista = Artista.objects.get(id=id)
        artista.delete()
        return redirect('/eventos/artistas_list')
    except Exception as e:
        messages.add_message(request, constants.WARNING, 'Artista não removido: Apague todos os eventos relacionados antes de remove-lo!')
        return redirect('/eventos/artistas_list')


