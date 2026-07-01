"""Schlanker E-Mail-Versand über die SendGrid HTTP-API.

Warum SendGrid (Single Sender Verification): man verifiziert EINE Absender-Adresse
(z. B. ein Gmail) per Bestätigungslink — ohne eigene Domain — und kann danach an
beliebige Empfänger senden. Läuft über HTTPS (Port 443), also auch auf Render
(SMTP-Ports sind dort gesperrt).

Ohne ``SENDGRID_API_KEY``/``MAIL_FROM`` (lokale Entwicklung) wird die Mail nur ins Log
geschrieben statt versendet — so läuft die App ohne Setup. Der Versand wirft nie eine
Exception nach oben: schlägt er fehl, wird nur geloggt (z. B. bleibt eine Bewerbung
trotzdem gespeichert).
"""

import json
import urllib.error
import urllib.request

from flask import current_app

SENDGRID_ENDPOINT = "https://api.sendgrid.com/v3/mail/send"


def send_email(to, subject, html, text=None):
    """Sendet eine HTML-Mail an ``to``. True bei Versand, False bei Log-Fallback/Fehler.

    ``text`` ist eine optionale Klartext-Variante (verbessert Zustellbarkeit/Spam-Wertung).
    """
    api_key = current_app.config.get("SENDGRID_API_KEY")
    sender = current_app.config.get("MAIL_FROM")

    if not api_key or not sender:
        current_app.logger.info(
            "E-Mail (Dev-Modus, nicht versendet) → An: %s | Betreff: %s\n%s",
            to, subject, html,
        )
        return False

    # SendGrid erwartet content nach aufsteigender Präferenz: erst text/plain, dann text/html.
    content = []
    if text:
        content.append({"type": "text/plain", "value": text})
    content.append({"type": "text/html", "value": html})

    payload = json.dumps(
        {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": sender, "name": current_app.config.get("MAIL_FROM_NAME", "FlatMate")},
            "subject": subject,
            "content": content,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        SENDGRID_ENDPOINT,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10):
            return True  # SendGrid antwortet mit 202 Accepted
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        current_app.logger.warning(
            "E-Mail an %s fehlgeschlagen: HTTP %s — %s", to, exc.code, body
        )
        return False
    except Exception as exc:  # noqa: BLE001 — Mailfehler darf den Request nicht abbrechen
        current_app.logger.warning("E-Mail an %s fehlgeschlagen: %s", to, exc)
        return False
