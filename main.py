import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    # Campi per inserire le informazioni del nuovo strumento
    tipo = ft.TextField(label="Tipo")
    marca = ft.TextField(label="Marca")
    anno = ft.TextField(label="Anno acquisto")

    # Contatore del valore dello strumento
    valore_corrente = 0
    valore = ft.TextField(value=str(valore_corrente),width=50, text_align=ft.TextAlign.CENTER, read_only=True)  #scriviamo read_only=True che impedisce
    # all'utente di modificare direttamente il numero digitando

    def handleAdd(e):
        currentVal = int(valore.value)     #trasformiamo in int per modificarlo e nella riga successiva lo ripassiamo in str dato che ritorna nel txt
        valore.value = str(currentVal + 1)
        valore.update()

    def handleRemove(e):
        currentVal = int(valore.value)

        if currentVal >0:  # così il valore non va mai sotto zero
            valore.value = str(currentVal - 1)

        valore.update()



    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO

    def aggiungi_strumento(e):
        tipo_strumento=tipo.value               # quel tipo.value significa accedi alla proprietà value dell'oggetto contenuto nella variabile tipo.
        marca_strumento=marca.value
        anno_strumento=anno.value

        if tipo_strumento == "" or marca_strumento == "" or anno_strumento == "":
            alert.show_alert("compila tutti i campi")
            return

        if not anno_strumento.isnumeric():
            alert.show_alert("l'anno deve essere un numero")
            return

        anno_strumento = int(anno_strumento)
        deposito.aggiungi_strumento(tipo_strumento, marca_strumento, anno_strumento, int(valore.value))     #chiama un metodo dell'ggetto

        tipo.value = ""
        marca.value = ""
        anno.value = ""

        valore.value = "0"

        aggiorna_lista_strumenti()
        page.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", icon_size=24, on_click=handleAdd)

    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO

        ft.Divider(),
        ft.Text("Aggiungi un nuovo strumento", size=20),

        ft.Row(
            controls=[tipo, marca, anno, btnMinus, valore, btnAdd],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Row(controls=[pulsante_aggiungi_strumento], alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
