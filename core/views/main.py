from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from core.models import *
from core.forms import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import date
from datetime import datetime
from datetime import timedelta 
from django.utils.formats import localize
from django.core.serializers import serialize
from django.db import transaction
import json
# Email com template html
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage
from threading import Thread
import threading


class SendMailHTML (threading.Thread):
	def __init__(self, titulo, mensagem, arquivos, email):
		threading.Thread.__init__(self)
		self.titulo = titulo
		self.mensagem = mensagem
		self.arquivos = arquivos
		self.email = email
	def run(self):
		msg = EmailMessage(self.titulo, self.mensagem, 'nao-responda@locadora-cin.com', ['' + self.email + ''], attachments=self.arquivos)
		msg.content_subtype = 'html'
		msg.send()

class SendMail(threading.Thread):
    def __init__(self, titulo, mensagem, email):
        threading.Thread.__init__(self)
        self.titulo = titulo
        self.mensagem = mensagem
        self.email = email

    def run(self):
        send_mail(
            self.titulo,
            self.mensagem,
            'nao-responda@locadora-cin.com', ['' + self.email + ''],
            fail_silently=False
        )

# como chamar a SendMailHTML (text_msg: String)
# SendMail('[CAMITA/IFAC] Solicitação de reinicialização de senha',text_msg, email).start()

# como chamar a SendMailHTML
# ctx = {
# 				'redes_sociais': redes_sociais,
# 				'topo': topo,
# 				'informativo': informativo,
# 				'ano_informativo': ano_informativo,
# 				'rodape': rodape,
# 				'dicionario_linha': dicionario_linha
# 			}
# 			mensagem = get_template('gerencia/email.html').render(ctx)
# 			resposta = SendMailPublicacao("Informativo eletrônico %d" % informativo.numero, mensagem, arquivos, email.valor).start()

class IndexView(generic.TemplateView):
    template_name = "core/index.html"

# Início das views de Reserva de filme

class ReservaListar(generic.ListView):
    model = Reserva
    paginate_by = 10
    template_name = 'core/reserva/lista.html'    

    def get_queryset(self):
        nome = self.request.GET.get('nome', '')
        return self.model.objects.filter(Q(filme__titulo__icontains = nome) | Q(filme__titulo_original__icontains=nome) | Q(cliente__user__first_name__icontains = nome) | Q(cliente__user__last_name__icontains = nome))
            # Q(cliente__codigo__icontains = nome) | 

class ReservaCriar(SuccessMessageMixin, generic.CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'core/reserva/novo.html'
    success_message = "Reserva adicionada com sucesso."

class ReservaDetalhe(generic.DetailView):
    model = Reserva
    context_object_name = 'reserva'
    template_name = 'core/reserva/detalhe.html'

class ReservaEditar(SuccessMessageMixin, generic.UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'core/reserva/editar.html'
    success_message = "Reserva editada com sucesso."

def carregar_tipo_midia(request):
    filme_id = request.GET.get('filme')
    midias = Midia.objects.filter(item_midia__filme_id=filme_id)    
    return render(request, 'core/ajax/partial_select_midia.html', {'midias': midias})

def reserva_cancelar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    print(reserva)
    if request.method == 'POST':
        reserva.status = 'Expirada'

        text_msg = "Olá, " + str(reserva.cliente) + ". \r\n\r\nInformamos que sua reserva para o filme "+ str(reserva.filme)+" ("+ str(reserva.midia) +") foi cancelada no dia " + str(localize(datetime.now())) + ". \r\n\r\nPara mais informações visite nossa loja e procure um de nossos funcionários. \r\n\r\nAtenciosamente, Locadora Imperial."
        # SendMail('[Locadora Imperial] Cancelamento de reserva',text_msg, reserva.cliente.user.email).start()
        messages.success(request, 'Reserva cancelada com sucesso.')
        return HttpResponseRedirect(reverse_lazy('core:reserva-listar'))
    
    return render(request, 'core/reserva/cancelar.html', {'reserva': reserva})



# Início das views de Locação

class LocacaoListar(generic.ListView):
    model = Locacao
    paginate_by = 10
    template_name = 'core/locacao/lista.html'   

# Step 1 - Locação
def realizar_locacao(request, pk = None):
    if pk:
        locacao = get_object_or_404(Locacao, pk=pk)
        if not locacao.is_editavel:
            messages.error(request, 'Locação não pode ser editada.')
            return HttpResponseRedirect(reverse_lazy('core:locacao-listar'))
        form = LocacaoForm(request.POST or None, instance=locacao)
    else:
        form = LocacaoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cliente = form.cleaned_data.get('cliente')
            lcs = Locacao.objects.filter(cliente=cliente)
            its = ItemLocacao.objects.filter(locacao__in=lcs)

            for i in its:
                if i.devolucao and i.locacao.situacao != 'PAGA':
                    messages.error(request, "O cliente '%s' está em atraso" % cliente)
                    return render(request, 'core/locacao/buscar_cliente.html', {'form': form})

            locacao = form.save()
            return HttpResponseRedirect(reverse('core:locacao-realizar-itens', kwargs={'pk': locacao.pk}))    
    return render(request, 'core/locacao/buscar_cliente.html', {'form': form})

# Step 2 - Locação
def seleciona_itens_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    if not locacao.is_editavel:
            messages.error(request, 'Locação não pode ser editada.')
            return HttpResponseRedirect(reverse_lazy('core:locacao-listar'))
    itens = ItemLocacao.objects.filter(locacao=locacao)
    if request.method == 'POST':
        if itens.count() > 0:
            return HttpResponseRedirect(reverse('core:locacao-confirmar', kwargs={'pk': locacao.pk}))
        else:
            messages.error(request, 'Você precisa selecionar pelo menos item para realizar a locação')
    return render(request, 'core/locacao/itens_locacao.html', {'itens_list': itens, 'locacao': locacao,})

# Step 3 - Locação
def confirmar_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    if not locacao.is_editavel:
            messages.error(request, 'Locação não pode ser editada.')
            return HttpResponseRedirect(reverse_lazy('core:locacao-listar'))
    itens = ItemLocacao.objects.filter(locacao=locacao)
    if request.method == 'POST':
        locacao.situacao = 'CONCLUIDA'
        locacao.save()
        messages.success(request, 'Locação concluída com sucesso.')
        return HttpResponseRedirect(reverse('core:locacao-finalizar', kwargs={'pk': locacao.pk}))
    return render(request, 'core/locacao/confirma.html', {'item_list': itens, 'locacao': locacao,})

# Step 4 - Locação
def finalizar_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    if not locacao.is_editavel:
            messages.error(request, 'Locação não pode ser editada.')
            return HttpResponseRedirect(reverse_lazy('core:locacao-listar'))
    itens = ItemLocacao.objects.filter(locacao=locacao)
    pagamentos = Pagamento.objects.filter(locacao=locacao)
    valor_restante = locacao.valor_total - locacao.valor_pago()
    if request.method == 'POST':
        if valor_restante == 0:
            locacao.situacao = 'PAGA'
        elif valor_restante < locacao.valor_total:
            locacao.situacao = 'PAGA_PARCIAL'
        locacao.save()
        messages.success(request, 'Locação realizada com sucesso.')
        return HttpResponseRedirect(reverse_lazy('core:locacao-listar'))
    return render(request, 'core/locacao/finalizar.html', {'item_list': itens, 'locacao': locacao, 'pagamentos': pagamentos, 'valor_restante': valor_restante,})


@transaction.atomic
def save_item_form(request, form, template_name, mensagem):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            locacao = form.cleaned_data.get('locacao')

            itens_list = ItemLocacao.objects.filter(locacao=locacao)
            
            soma = 0
            desconto = 0
            for i in itens_list:
                soma = soma + i.valor
                desconto = desconto + i.desconto

            locacao.sub_total = soma
            locacao.total_descontos = desconto
            locacao.save()

            data['qtd_item'] = itens_list.count()
            data['sub_total'] = localize(locacao.sub_total)
            data['total_descontos'] = localize(locacao.total_descontos)
            data['valor_total'] = localize(locacao.valor_total)
            data['html_item_list'] = render_to_string('core/ajax/partial_itens_list.html', {'itens_list': itens_list, })
        else:
            data['form_is_valid'] = False

    context = { 'form' : form }
    data['html_form'] = render_to_string(template_name, context, request=request,)
    return JsonResponse(data)

def item_add(request):
    form = ItemLocacaoForm(request.POST or None)
    return save_item_form(request, form, 'core/ajax/partial_item_add.html', 'Item adicionado com sucesso')


def item_edit(request, pk):
    item = get_object_or_404(ItemLocacao, pk=pk)
    form = ItemLocacaoForm(request.POST or None, instance=item)
    return save_item_form(request, form, 'core/ajax/partial_item_update.html', 'Item alterado com sucesso')


@transaction.atomic
def item_delete(request, pk):
    item = get_object_or_404(ItemLocacao, pk=pk)
    locacao = item.locacao
    data = dict()
    if request.method == 'POST':
        item.delete()
        data['form_is_valid'] = True
        itens_list = ItemLocacao.objects.filter(locacao=locacao)

        soma = 0
        desconto = 0
        for i in itens_list:
            soma = soma + i.valor
            desconto = desconto + i.desconto

        locacao.sub_total = soma
        locacao.total_descontos = desconto
        locacao.save()

        data['qtd_item'] = itens_list.count()
        data['sub_total'] = localize(locacao.sub_total)
        data['total_descontos'] = localize(locacao.total_descontos)
        data['valor_total'] = localize(locacao.valor_total)
        data['html_item_list'] = render_to_string('core/ajax/partial_itens_list.html', {'itens_list': itens_list, })
    else:
        context = {'item': item}
        data['html_form'] = render_to_string('core/ajax/partial_item_delete.html', context, request=request,)
    return JsonResponse(data)


def carregar_item_ajax(request):
    data = dict()
    item_id = request.GET.get('item')
    item = get_object_or_404(Item, pk=item_id)

    if item.filme.is_lancamento:
        data['valor'] = localize(item.tipo_midia.valor * 1.5)
    else:    
        data['valor'] = localize(item.tipo_midia.valor) 
    
    today = date.today()
    if item.filme.is_lancamento:
        data['data_devolucao'] = (today + timedelta(days=1)).strftime("%d/%m/%Y")   
    else:
        data['data_devolucao'] = (today + timedelta(days=3)).strftime("%d/%m/%Y")
    return JsonResponse(data)


class LocacaoDetalhe(generic.DetailView):
    model = Locacao
    context_object_name = 'locacao'
    template_name = 'core/locacao/detalhe.html'

    def get_context_data(self, **kwargs):
        context = super(LocacaoDetalhe, self).get_context_data(**kwargs)
        context['item_list'] = ItemLocacao.objects.filter(locacao=self.object)
        context['pagamentos'] = Pagamento.objects.filter(locacao=self.object)
        return context


@transaction.atomic
def pagamento_locacao(request):
    data = dict()
    formas_pagamento = FormaPagamento.objects.all()
    if request.method == 'POST':
        data['form_is_valid'] = True
        fp_id = request.POST.get('forma_pagamento')
        lc_id = request.POST.get('locacao')
        dv_id = request.POST.get('devolucao')

        if lc_id:
            locacao = Locacao.objects.get(pk=lc_id)
            
        if dv_id:
            devolucao = Devolucao.objects.get(pk=dv_id)
        else:
            devolucao = None
        
        forma_pagamento = FormaPagamento.objects.get(pk=fp_id)
        argumentos = ArgumentoPagamento.objects.filter(forma_pagamento=forma_pagamento)

        pagamento = Pagamento()
        pagamento.locacao = locacao
        if devolucao:
            pagamento.devolucao = devolucao
        pagamento.forma_pagamento = forma_pagamento
        pagamento.save()
        
        campos = dict()
        for arg in argumentos:
            campos[arg.slug()] = arg.pk

        for k, v in campos.items():
            vlr = request.POST.get(k)
            arg = ArgumentoPagamento.objects.get(pk=v)
            info_pg = InformacaoPagamento()
            info_pg.argumento = arg
            if arg.tipo_dado == 'TEXTO':
                info_pg.valor_texto = vlr
            elif arg.tipo_dado == 'INTEIRO':
                info_pg.valor_inteiro = vlr
            elif arg.tipo_dado == 'DECIMAL':
                info_pg.valor_decimal = vlr
            elif arg.tipo_dado == 'BOOLEAN':
                info_pg.valor_boolean = vlr
            elif arg.tipo_dado == 'DATA':
                info_pg.valor_data = vlr
            elif arg.tipo_dado == 'HORA':
                info_pg.valor_hora = vlr
            elif arg.tipo_dado == 'DATA_HORA':
                info_pg.valor_data_hora = vlr

            info_pg.pagamento = pagamento
            info_pg.save()
        
        valor_restante = locacao.valor_total - locacao.valor_pago()
        data['valor_restante'] = valor_restante
        
        if valor_restante == 0:
            locacao.situacao = 'PAGA'
            itens_list = ItemLocacao.objects.filter(locacao=locacao)
            
            for i in itens_list:
                i.is_pago = True
                i.save()

            locacao.save()

        elif valor_restante < locacao.valor_total:
            locacao.situacao = 'PAGA_PARCIAL'
            vt_pago = locacao.valor_pago()
            itens_list = ItemLocacao.objects.filter(locacao=locacao)

            for i in itens_list:
                if i.filme.is_lancamento:
                    if vt_pago - i.valor  >= 0:
                        i.is_pago = True
                        i.save()
                        vt_pago = vt_pago - i.valor

            for i in itens_list:
                if vt_pago - i.valor  >= 0:
                    i.is_pago = True
                    i.save()
                    vt_pago = vt_pago - i.valor

            locacao.save()

        pagamentos = Pagamento.objects.filter(Q(devolucao=devolucao) | Q(locacao=locacao))   
        data['valor_pago'] = locacao.valor_pago()
        data['valor_restante'] = valor_restante
        data['html_pg_list'] = render_to_string('core/ajax/partial_pagamentos_list.html', {'pagamentos': pagamentos, })
    context = {'formas_pagamento': formas_pagamento}
    data['html_form'] = render_to_string('core/ajax/partial_pagamento_novo.html', context, request=request,)
    return JsonResponse(data)


def carregar_argumento_forma_pagamento(request):
    forma_pagamento_id = request.GET.get('forma')
    argumentos = ArgumentoPagamento.objects.filter(forma_pagamento__id=forma_pagamento_id)
    return render(request, 'core/ajax/partial_campos_pagamento.html', {'argumentos': argumentos})


def detalhe_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    data = dict()
    context = {'pagamento': pagamento, 'dados_pagamento': pagamento.informacoes_pagamentos.all()}
    data['html_form'] = render_to_string('core/ajax/partial_detalhe_pagamento.html', context, request=request,)
    return JsonResponse(data)

    
# Início views devolução

class DevolucaoCriar(SuccessMessageMixin, generic.CreateView):
    model = Devolucao
    form_class = DevolucaoForm
    template_name = 'core/devolucao/novo.html'
    success_message = "Devolução adicionado com sucesso."

class DevolucaoListar(generic.ListView):
    model = Devolucao
    paginate_by = 10
    template_name = 'core/devolucao/lista.html'    

    # def get_queryset(self):
    #     nome = self.request.GET.get('nome', '')
    #     return self.model.objects.filter(nome__icontains = nome)

class DevolucaoDetalhe(generic.DetailView):
    model = Devolucao
    context_object_name = 'devolucao'
    template_name = 'core/devolucao/detalhe.html'

    def get_context_data(self, **kwargs):
        context = super(DevolucaoDetalhe, self).get_context_data(**kwargs)
        print(self.object.item.id)
        pagamentos = Pagamento.objects.filter(Q(devolucao=self.object) | Q(locacao=self.object.item.locacao))  
        context['pagamentos'] = pagamentos
        valor_restante = self.object.item.locacao.valor_total - self.object.item.locacao.valor_pago()
        context['valor_pago'] = self.object.item.locacao.valor_pago()
        context['valor_restante'] = valor_restante
        return context


def carrega_item_devolucao_ajax(request):
    data = dict()
    item_id = request.GET.get('item')
    item = get_object_or_404(ItemLocacao, pk=item_id)
    today = date.today()
    if today > item.data_devolucao():
        data['multa'] = item.calcular_multa(today)
    else: 
        data['multa'] = 0
    return JsonResponse(data)
