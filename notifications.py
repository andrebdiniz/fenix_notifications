import feedparser
from pushover import init, Client
import time
import os
import html2text
from config import PUSHOVER_API_TOKEN, PUSHOVER_USER_KEY

# Lista de URLs dos feeds RSS
rss_urls = [
    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDadosi2/2023-2024/1-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/ARC/2023-2024/1-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDI4-0/2023-2024/1-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/ETPN/2023-2024/1-semestre/rss/announcement",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/AGI/2023-2024/1-semestre/rss/announcement",

    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDadosi2/2023-2024/1-semestre/rss/content",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/ARC/2023-2024/1-semestre/rss/content",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/CDI4-0/2023-2024/1-semestre/rss/content",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/ETPN/2023-2024/1-semestre/rss/content",
    "https://fenix.tecnico.ulisboa.pt/disciplinas/AGI/2023-2024/1-semestre/rss/content",
]

# Dicionário para armazenar os IDs de anúncios notificados para cada feed
notified_ids = {url: [] for url in rss_urls}

def load_notified_ids():
    notified_ids_file = "notified_ids.txt"

    if os.path.exists(notified_ids_file):
        with open(notified_ids_file, "r") as file:
            return {url: [line.strip() for line in file.readlines()] for url in rss_urls}
    else:
        return {url: [] for url in rss_urls}

def save_notified_ids():
    notified_ids_file = "notified_ids.txt"

    with open(notified_ids_file, "w") as file:
        for url, ids in notified_ids.items():
            file.write(f"{url}:\n")
            file.write("\n".join(ids))
            file.write("\n")

def send_pushover_notification(title, message):
    init(PUSHOVER_API_TOKEN)
    client = Client(PUSHOVER_USER_KEY)
    client.send_message(message, title=title)

    print("Pushover notification sent")

def check_for_updates(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        html_parser = html2text.HTML2Text()

        for entry in feed.entries:
            entry_id = entry.id

            # Verifica se o ID do anúncio já foi notificado para este feed
            if entry_id not in notified_ids[feed_url]:
                title = entry.title
                summary = html_parser.handle(entry.description)
                link = entry.link

                # Determina o tipo do link (Content, Anúncio ou Outro) com base no formato do RSS
                if "/rss/content" in feed_url:
                    link_type = "Content"
                elif "announcement" in feed_url:
                    link_type = "Anúncio"
                else:
                    link_type = "Outro"

                # Envia notificação push
                send_pushover_notification(f"{title} | {link_type}", f"{summary}\nNova atualização em {link}")

                # Adiciona o ID do anúncio à lista de IDs notificados para este feed
                notified_ids[feed_url].append(entry_id)
    except Exception as e:
        print(f"Erro ao processar o feed {feed_url}: {str(e)}")

if __name__ == "__main__":
    notified_ids = load_notified_ids()

    try:
        while True:
            for rss_url in rss_urls:
                check_for_updates(rss_url)
            save_notified_ids()
            time.sleep(300)  # Aguarda 5 minutos antes de verificar novamente
    except KeyboardInterrupt:
        save_notified_ids()
        print("\nScript interrompido. IDs notificadas salvas.")
