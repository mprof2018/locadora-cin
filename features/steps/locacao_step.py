from behave import *
from selenium.webdriver.support.ui import Select
import time

@given(u'que estou na página de listagem de locações "{page}"')
def step_impl(context, page):
    context.browser.get(page)

@when(u'clicar no botão Realizar Locação')
def step_impl(context):
    context.browser.implicitly_wait(30)
    context.browser.find_element_by_link_text('Realizar Locação').click()

@when(u'selecionar o cliente da locação')
def step_impl(context):
    select = Select(context.browser.find_element_by_id('id_cliente'))
    select.select_by_index(1)

@when(u'clicar no botão Próximo')
def step_impl(context):
    context.browser.find_element_by_xpath(u'//button[text()="Próximo"]').click()

@when(u'clicar no botão Adicionar Item')
def step_impl(context):
    context.browser.find_element_by_class_name("js-add-item").click()

@when(u'selecionar um item')
def step_impl(context):
    form = context.browser.find_element_by_xpath("//form[@id='form-item-add']")
    select = Select(form.find_element_by_id('id_item'))
    select.select_by_index(1)
    time.sleep( 5 )

@when(u'clicar em Adicionar Item')
def step_impl(context):
    context.browser.find_element_by_id("add-item-modal").click()
    context.browser.find_element_by_class_name("alert-success")

@then(u'clicar no botão Próximo')
def step_impl(context):
    context.browser.find_element_by_xpath("//form[@id='form-avancar-locacao']").submit()
    # context.browser.find_element_by_class_name('form').submit()

@then(u'clicar no botão Concluir')
def step_impl(context):
    context.browser.find_element_by_xpath("//form[@id='form-concluir-locacao']").submit()
    # context.browser.find_element_by_id('form-concluir-locacao').submit()

@then(u'Locação concluída com sucesso.')
def step_impl(context):
    context.browser.find_element_by_class_name("alert-success")
