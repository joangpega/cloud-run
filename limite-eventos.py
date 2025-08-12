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
      `projectid.table.events_*`
    WHERE
      _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
      AND FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
    GROUP BY fecha
    ORDER BY fecha DESC
    """
    results = client.query(QUERY).result()

    fechas = []
    eventos = []
    for row in results:
        fechas.append(str(row.fecha))
        eventos.append(row.total_eventos)

    if not eventos:
        return 'No se encontraron datos'

    # Invertir para orden cronológico ascendente
    fechas.reverse()
    eventos.reverse()

    # Crear gráfico con doble eje Y
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.bar(fechas, eventos, label="Eventos diarios", color='skyblue')
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Eventos diarios", color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.set_xticklabels(fechas, rotation=45)

    ax2 = ax1.twinx()
    ax2.axhline(y=LIMITE_EVENTOS, color='red', linestyle='--', label="Límite (1M)")
    ax2.set_ylabel("Límite eventos", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, max(LIMITE_EVENTOS, max(eventos)*1.1))

    # Combinar leyendas
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title("Eventos diarios últimos 7 días")
    plt.tight_layout()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Obtener password de Secret Manager
    secret_client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/projectid/secrets/secreto/versions/latest"
    gmail_password = secret_client.access_secret_version(name=secret_name).payload.data.decode("UTF-8")

    # Preparar datos para email
    total_ultimo_dia = eventos[-1]  # Último día tras invertir, es el más reciente
    porcentaje = (total_ultimo_dia / LIMITE_EVENTOS) * 100
    
    #Podemos ajustar el umbral
    if porcentaje >= 90:
        estado = "🚨 Límite de eventos alcanzado" if total_ultimo_dia >= LIMITE_EVENTOS else "⚠️ Aproximándose al límite"

        # Construir email HTML con imagen inline
        msg = MIMEMultipart('related')
        msg['Subject'] = 'Google Cloud: límite de eventos diarios'
        msg['From'] = 'email@gmail.com'
        msg['To'] = 'email@gmail.com'
        msg['Cc'] = 'emailencopia@perezgarcia.es'

        html = f"""
        <html>
          <body>
            <p>{estado}</p>
            <p>Límite: {LIMITE_EVENTOS:,}</p>
            <p>Porcentaje del límite (último día): {porcentaje:.2f}%</p>
            <p>Eventos diarios últimos 7 días:</p>
            <p>
            El número de eventos diarios es: {total_ultimo_dia:,}<br>
            </p><br>
            <img src="cid:grafico" alt="Gráfico de eventos diarios"><br>

          </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html'))

        image = MIMEImage(img_bytes.read())
        image.add_header('Content-ID', '<grafico>')
        msg.attach(image)

        # Enviar email
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login('joangpega@gmail.com', gmail_password)
        smtp.sendmail(msg['From'], [msg['To'], msg['Cc']], msg.as_string())
        smtp.quit()

        return 'Email enviado correctamente'
    else:
        return f'No se envió email, porcentaje {porcentaje:.2f}% por debajo del umbral'
