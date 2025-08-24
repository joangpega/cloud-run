# Funciones de Cloud Run para GCP

1. Límite de eventos de exportación de GA4 normal a BigQuery (limite-eventos.py)

<img width="1024" height="896" alt="image" src="https://github.com/user-attachments/assets/3bc14b51-5010-40e3-9774-aed5052717df" />

[https://github.com/joangpega/cloud-run/blob/main/limite-eventos.py
](https://github.com/joangpega/cloud-run/blob/main/limite-eventos.py
)

La exportación de GA4 hacia BigQuery de Google Cloud tiene muchísimas ventajas, sin embargo, tenemos un límite de eventos diarios que poder exportar por propiedad:

Para las propiedades de GA4 no 360, el límite es de 1 millón (1M) de eventos diarios, mientras que para las 360 el límite es de miles de millones, por lo que podemos decir que es ilimitada.

Resultado de la consulta

<img width="1632" height="1148" alt="image" src="https://github.com/user-attachments/assets/7253d245-292c-4655-b672-9003206e41a9" />


Más información en: [https://joseangel.perezgarcia.es/google-cloud/email-limite-eventos-ga4-bq/](https://joseangel.perezgarcia.es/google-cloud/email-limite-eventos-ga4-bq/
)
