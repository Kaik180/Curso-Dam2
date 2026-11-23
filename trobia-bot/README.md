# 🍊 Bot de trobia

Bot de Discord con economía, minijuegos, casino, logros, cajas de botín y personalización de perfil.

## Arrancar
Doble clic en **`iniciar.bat`** (instala dependencias, arranca el bot y lo reinicia si se cae).
Funciona mientras la ventana esté abierta y el ordenador encendido.

**Que arranque solo al encender el PC:** `Win + R` → `shell:startup` → crea ahí un acceso directo a `iniciar.bat`.

## Configuración
- `.env` → token, ID del servidor e ID de la aplicación (**nunca lo subas a GitHub**; ya está en `.gitignore`).
- `config.py` → recompensas, tiempos de espera, límites de apuesta.
- `data/items.py` → objetos, precios y probabilidades de las cajas.
- `data/achievements.py` → logros.
- `data/trivia.py` → preguntas de trivia.
- `data/trobia.db` → base de datos (se crea sola; haz copia de seguridad de vez en cuando).

## Comandos
| Categoría | Comandos |
|---|---|
| Economía | `/saldo` `/diario` `/trabajar` `/pagar` `/ranking` |
| Perfil | `/perfil` `/logros` `/personalizar bio/color/titulo/insignia` |
| Tienda | `/tienda` `/comprar` `/inventario` `/usar` `/cajas` `/abrir` |
| Casino | `/moneda` `/dados` `/tragaperras` `/blackjack` `/ppt` `/duelo` |
| Gratis | `/trivia` `/adivina` `/ppt` |
| Admin | `/admin monedas` `/admin objeto` `/admin evento` |
| Ayuda | `/ayuda` |
