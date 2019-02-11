# from nose.tools import assert_equal, assert_true
# from behave import Given, When, Then
# from locacao.models import Cliente, Item, Locacao
#
# @given(u'Eu navego até a página de edição da locação')
# def step_impl(context):
#     context.browser.get("http://127.0.0.1:8000/atendente/locacao/nova/")
#     title = context.browser.title
#     if "Page not found" in title:
#         assert True is not True
#
# @when(u'Eu preencho o cpf que nao pertence a nenhum cliente')
# def step_impl(context):
#     context.browser.find_element_by_id("id_cpf").send_keys("90909090909")
#
# @then(u'clico em buscar cliente')
# def step_impl(context):
#     context.browser.find_element_by_id("id_buscar_cliente").click()
#
# @then(u'Eu recebo a msg de "Cliente não encontrado."')
# def step_impl(context):
#     assert_true(context.browser.find_element_by_class_name("alert-danger"), 'Cliente não encontrado.')
#
# # Adicionar Item
#
# @when(u'Eu clico em adicionar item')
# def step_impl(context):
#     context.browser.find_element_by_id("id_adicionar_item").click()
#
# @when(u'informo o codigo de barras')
# def step_impl(context):
#     item = Item.objects.first()
#     context.browser.find_element_by_id("id_item").send_keys(item.codigo_barras)
#
# @when(u'clico em salvar item')
# def step_impl(context):
#     context.browser.find_element_by_id("id_salvar_item").click()
#
# @then(u'Eu recebo a msg "Item adicionado com sucesso."')
# def step_impl(context):
#     assert_true(context.browser.find_element_by_class_name("alert-success"), "Item adicionado com sucesso.")
#
# # Excluir Item
# @when(u'Eu clico no botão excluir ao lado do item que quero excluir')
# def step_impl(context):
#     context.browser.find_element_by_class_name("btn-danger").click()
#
#
# @then(u'Eu sou questionado "Tem certeza que deseja remover este Item?"')
# def step_impl(context):
#     conteudo = context.browser.find_element_by_id("pergunta_delete").text
#     if "Você tem certeza que deseja remover este Item?" in conteudo:
#         assert True is not False
#     else:
#         assert True is not True
#
#
# @when(u'Clico em "Sim, tenho certeza"')
# def step_impl(context):
#     context.browser.find_element_by_id("btn_confirm_delete").click()
#
# @then(u'Eu recebo a msg "Item Excluido com Sucesso."')
# def step_impl(context):
#     assert_true(context.browser.find_element_by_class_name("alert-success"), "Gênero excluído com sucesso.")
#
#
# @when(u'Eu clico no botão Salvar')
# def step_impl(context):
#     context.browser.find_element_by_id("id_salvar_locacao").click()
#
#
# @then(u'Eu recebo a msg "Locação Salva com Sucesso!"')
# def step_impl(context):
#     assert_true(context.browser.find_element_by_class_name("alert-success"), "Locação Salva com Sucesso!")
