# Funciones de Cloud Run para GCP

1. Límite de eventos de exportación de GA4 normal a BigQuery:

[https://github.com/joangpega/cloud-run/blob/main/limite-eventos.py
](https://github.com/joangpega/cloud-run/blob/main/limite-eventos.py
)

La exportación de GA4 hacia BigQuery de Google Cloud tiene muchísimas ventajas, sin embargo, tenemos un límite de eventos diarios que poder exportar por propiedad:

Para las propiedades de GA4 no 360, el límite es de 1 millón (1M) de eventos diarios, mientras que para las 360 el límite es de miles de millones, por lo que podemos decir que es ilimitada.

Más información en: [https://joseangel.perezgarcia.es/google-cloud/email-limite-eventos-ga4-bq/](https://joseangel.perezgarcia.es/google-cloud/email-limite-eventos-ga4-bq/
)
