# Hacker News Scraper

Este proyecto es un simple scraper de Python que extrae los titulares y enlaces de la página principal de Hacker News.

## Cómo funciona

El script `scraper.py` usa las librerías `requests` y `BeautifulSoup4` para hacer una petición a la página de Hacker News y parsear el HTML para encontrar los titulares de las noticias. Los resultados se imprimen en la consola.

## Automatización con GitHub Actions

Este repositorio está configurado con un flujo de trabajo de GitHub Actions que ejecuta el scraper automáticamente todos los días a medianoche UTC. El flujo de trabajo está definido en el archivo `.github/workflows/scrape.yml`. También se puede ejecutar manualmente desde la pestaña de Acciones en GitHub.
