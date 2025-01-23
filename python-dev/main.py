import flet as ft


def main(pagina):
    texto = ft.Text("Hashzap")
    chat = ft.Column()
    nome_usuario = ft.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        usuario_mensagem = mensagem["usuario"]

        mensagem_formatada = ""

        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            mensagem_formatada = ft.Text(f"{usuario_mensagem}: {texto_mensagem}")
        else:
            mensagem_formatada = ft.Text(
                f"{usuario_mensagem} entrou no chat",
                size=12,
                italic=True,
                color=ft.colors.ORANGE_500,
            )

        chat.controls.append(mensagem_formatada)

        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(_):
        pagina.pubsub.send_all(
            {
                "texto": campo_mensagem.value,
                "usuario": nome_usuario.value,
                "tipo": "mensagem",
            }
        )
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(
        label="Digite uma mensagem", on_submit=enviar_mensagem
    )
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(_):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})

        pagina.add(chat)

        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)

        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))

        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao Hashzap"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    def entrar_chat(_):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
