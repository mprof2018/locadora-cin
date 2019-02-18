from behave import *
from datetime import datetime

@given('que estou logado')
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/login')
    context.browser.find_element_by_id("id_login").send_keys("teste@bdd.com")
    context.browser.find_element_by_id("id_password").send_keys("123456")
    context.browser.find_element_by_id('id_btn_login').click()

@given('que estou na página de gênero "{page}"')
def open_page(context, page):
    context.browser.get(page)

@when(u'clicar no botão adicionar')
def click_bnt(context):
    context.browser.find_element_by_link_text('Adicionar').click()

@when('preencher o campo nome com uma descrição')
def insert_values_on_fields(context):
    context.browser.find_element_by_id('id_nome').send_keys("Drama - {}".format(datetime.now()))


@when('clicar no botão adicionar gênero')
def click_bnt(context):
    context.browser.find_element_by_class_name("btn-success").click()

@when('receber a mensagem de cadastro realizado com sucesso')
def tudo_certo(context):
    context.browser.find_element_by_class_name("alert-success")

@when('clicar no botão para voltar para listagem')
def click_bnt(context):
    context.browser.find_element_by_class_name("btn-info").click()

@then('serão listados os gêneros cadastrados')
def lista_generos(context):
        context.browser.find_element_by_class_name("fa-table")

@when('clicar no botão cancelar')
def click_bnt(context):
    context.browser.find_element_by_class_name("btn-danger").click()

#@then(u'será exibida a mensagem \'Preencha este campo\'.')
#def step_impl(context):
#    raise NotImplementedError(u'STEP: Then será exibida a mensagem \'Preencha este campo\'.')