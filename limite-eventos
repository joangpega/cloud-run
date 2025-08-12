from google.cloud import bigquery, secretmanager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
import io

LIMITE_EVENTOS = 1_000_000

def enviar_eventos_diarios(request):
    client = bigquery.Client()

    QUERY = """
    SELECT
      event_date AS fecha,
      COUNT(*) AS total_eventos
    FROM
      `projectid.tableid.events_*`
    WHERE
      _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
      AND FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
    GROUP BY fecha
    ORDER BY fecha desc
    """
    results = client.query(QUERY).result()

    fechas = []
    eventos = []
    for row in results:
        fechas.append(str(row.fecha))
        eventos.append(row.total_eventos)

    if not eventos:
        return 'No se encontraron datos'

    # Crear gráfico
    plt.figure(figsize=(8, 5))
    plt.bar(fechas, eventos, label="Eventos diarios", color='skyblue')
    plt.axhline(y=LIMITE_EVENTOS, color='red', linestyle='--', label="Límite (1M)")
    plt.xlabel("Fecha")
    plt.ylabel("Eventos")
    plt.title("Eventos diarios últimos 7 días")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Obtener secreto desde Secret Manager
    secret_client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/project_id/secrets/secreto/versions/latest"
    gmail_password = secret_client.access_secret_version(name=secret_name).payload.data.decode("UTF-8")

    # Construir email con imagen
    msg = MIMEMultipart()
    total_ultimo_dia = eventos[0]
    porcentaje = (total_ultimo_dia / LIMITE_EVENTOS) * 100
    if total_ultimo_dia >= LIMITE_EVENTOS:
        estado = "🚨 Límite de eventos alcanzado"
    else:
        estado = "✅ Límite no alcanzado"

    texto = f"""
    {estado}

    El número de eventos diarios es: {total_ultimo_dia:,}
    Límite: {LIMITE_EVENTOS:,}
    Porcentaje del límite: {porcentaje:.2f}%
    """

    msg.attach(MIMEText(texto, 'plain'))
    msg['Subject'] = 'Google Cloud: límite de eventos diarios'
    msg['From'] = '--@gmail.com'
    msg['To'] = '--@gmail.com'
    msg['Cc'] = '--@perezgarcia.es'

    # Adjuntar imagen
    image = MIMEImage(img_bytes.read())
    image.add_header('Content-ID', '<grafico>')
    msg.attach(image)

    # Enviar email
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login('joangpega@gmail.com', gmail_password)
    smtp.sendmail(msg['From'], [msg['To'], msg['Cc']], msg.as_string())
    smtp.quit()

    return 'Email enviado correctamente'
