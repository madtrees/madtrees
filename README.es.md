# 🌳 Mapa Interactivo de Árboles - Tutorial

Crea un mapa web interactivo para visualizar los árboles de tu ciudad usando datos abiertos. Este proyecto se construyó originalmente para los ~790,000 árboles de Madrid, pero puedes adaptarlo para cualquier ciudad.

## 📋 Lo Que Necesitarás

- Un archivo GeoJSON con las ubicaciones de árboles del portal de datos abiertos de tu ciudad
- Python 3 instalado en tu computadora
- Git instalado
- Una cuenta de GitHub (gratuita)
- Conocimientos básicos de línea de comandos

## 🚀 Tutorial Paso a Paso

### Paso 1: Clonar Este Proyecto

Abre tu terminal y ejecuta:

```bash
git clone https://github.com/TU_USUARIO/madtrees.git
cd madtrees
```

O descarga y extrae el archivo ZIP desde GitHub.

### Paso 2: Obtener los Datos de Árboles de Tu Ciudad

1. Encuentra el portal de datos abiertos de tu ciudad
2. Busca conjuntos de datos sobre "árboles", "arbolado urbano" o "espacios verdes"
3. Descarga los datos en **formato GeoJSON** (o conviértelos desde CSV/Shapefile)
4. Coloca el archivo en la carpeta del proyecto y nómbralo `trees.geojson`

**Ejemplos de portales de datos:**
- Madrid: https://datos.madrid.es/
- Barcelona: https://opendata-ajuntament.barcelona.cat/
- Nueva York: https://opendata.cityofnewyork.us/
- Londres: https://data.london.gov.uk/

### Paso 3: Optimizar Tus Datos

Los archivos GeoJSON grandes (>100 MB) no funcionarán en GitHub. Usa el script de optimización:

**Windows (PowerShell):**
```powershell
python optimize-geojson.py
```

**Linux/Mac:**
```bash
python3 optimize-geojson.py
```

Este script:
- Eliminará campos innecesarios
- Reducirá significativamente el tamaño del archivo
- Creará `trees-data.geojson`

```

**Alternativa: Dividir por distritos**

Para conjuntos de datos muy grandes (>200k árboles), divídelos en archivos más pequeños por distrito:

```bash
python split-by-district.py
```

Esto crea un archivo por distrito en la carpeta `data/districts/`.

**Luego comprime los archivos de distrito:**

```bash
python compress-districts.py
```

Esto elimina campos redundantes y acorta nombres de propiedades, reduciendo el tamaño de los archivos en ~18%. Al desplegar, GitHub Pages aplica automáticamente compresión gzip (reducción adicional del ~88%), por lo que los usuarios descargan solo **~22 MB** en lugar de 184 MB.

### Paso 4: Reemplazar el Archivo Original

Después de optimizar, reemplaza el archivo original:

**Windows (PowerShell):**
```powershell
Remove-Item trees.geojson
Rename-Item trees-data.geojson trees.geojson
```

**Linux/Mac:**
```bash
rm trees.geojson
mv trees-data.geojson trees.geojson
```

### Paso 5: Probar Localmente

Antes de subir, prueba el mapa en tu computadora desde la carpeta local del proyecto:

**Windows (PowerShell):**
```powershell
python -m http.server 8000
```

**Linux/Mac:**
```bash
python3 -m http.server 8000
```

Abre tu navegador y ve a: http://localhost:8000

¡Deberías ver tu mapa de árboles! Presiona `Ctrl+C` en la terminal para detener el servidor.

### Paso 6: Inicializar Repositorio Git

```bash
git init
git add .
git commit -m "Commit inicial: Mapa de árboles de la ciudad"
```

### Paso 7: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: elige un nombre (ej., `barcelona-arboles`, `madrid-arboles`)
3. Hazlo **Público** (requerido para GitHub Pages gratuito)
4. **NO** marques "Initialize with README" (ya tienes uno)
5. Haz clic en **Create repository**

### Paso 8: Subir a GitHub

Reemplaza `TU_USUARIO` y `nombre-de-tu-repo` con tus valores:

```bash
git remote add origin https://github.com/TU_USUARIO/nombre-de-tu-repo.git
git branch -M main
git push -u origin main
```

**Si el archivo es demasiado grande para GitHub:**

Usa Git LFS (Large File Storage):

```bash
git lfs install
git lfs track "*.geojson"
git add .gitattributes
git add .
git commit -m "Agregar archivos grandes con LFS"
git push -u origin main
```

### Paso 9: Habilitar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** (arriba a la derecha)
3. Desplázate hacia abajo y haz clic en **Pages** (barra lateral izquierda)
4. En **Source**, selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
5. Haz clic en **Save**
6. Espera 2-3 minutos para el despliegue

### Paso 10: ¡Ver Tu Mapa!

Tu mapa estará disponible en:

```
https://TU_USUARIO.github.io/nombre-de-tu-repo/
```

¡Comparte esta URL con quien quieras!

## 🎨 Personalizar Tu Mapa

### Cambiar el Nombre y Centro de la Ciudad

Edita `map.js` línea 1:

```javascript
// Cambia las coordenadas [latitud, longitud] y el nivel de zoom para centrar tu ciudad
const map = L.map('map').setView([40.4168, -3.7038], 12);
```

Encuentra las coordenadas de tu ciudad en Google Maps (clic derecho > coordenadas).

### Cambiar el Título de la Página

Edita `index.html` línea 7:

```html
<title>Árboles de Tu Ciudad - Mapa Interactivo</title>
```

### Ajustar Campos de Datos de Árboles

Si tus datos tienen nombres de campo diferentes, edita `map.js` alrededor de las líneas 120-125:

```javascript
const species = props.species || props."NOMBRE_DE_TU_CAMPO" || "Desconocido";
```

## 📦 Estructura del Proyecto

```
tu-proyecto/
├── index.html              # Página web principal
├── map.js                  # Lógica e interactividad del mapa
├── trees.geojson           # Tus datos de árboles (optimizados)
├── optimize-geojson.py     # Script para reducir tamaño de archivo
├── split-by-district.py    # Script para dividir datos por distritos
└── README.md               # Este archivo
```

## 🛠️ Referencia de Scripts

### optimize-geojson.py

Optimiza archivos GeoJSON eliminando campos innecesarios y reduciendo el tamaño.

**Uso básico:**
```bash
python optimize-geojson.py
```

**Opciones:**
```bash
--input <archivo>          Archivo GeoJSON de entrada (predeterminado: trees.geojson)
--output <archivo>         Archivo de salida (predeterminado: trees-data.geojson)
--keep-ratio <0.0-1.0>     Porcentaje de árboles a mantener (1.0=100%, 0.5=50%)
```

**Ejemplos:**
```bash
# Mantener todos los árboles, solo optimizar campos
python optimize-geojson.py

# Mantener 50% de los árboles
python optimize-geojson.py --keep-ratio 0.5

# Archivos de entrada/salida personalizados
python optimize-geojson.py --input misdatos.geojson --output optimizado.geojson
```

### split-by-district.py

Divide archivos GeoJSON grandes en archivos más pequeños por distrito para mejor rendimiento.

**Uso básico:**
```bash
python split-by-district.py
```

**Opciones:**
```bash
--input <archivo>       Archivo GeoJSON de entrada (predeterminado: trees.geojson)
--output <carpeta>      Carpeta de salida (predeterminado: data/districts)
```

**Ejemplo:**
```bash
python split-by-district.py --input trees.geojson --output data/districts
```

Esto crea:
- Un archivo `.geojson` por distrito
- `districts_index.json` con metadatos

**Nota:** Si usas división por distritos, necesitas modificar `map.js` para cargar distritos dinámicamente (código ya incluido en la versión actual).

### compress-districts.py

Después de dividir, comprime los archivos de distrito para reducir el tamaño de descarga eliminando campos redundantes y acortando nombres de propiedades.

**Uso básico:**
```bash
python compress-districts.py
```

Este script:
- Elimina campos internos (ASSETNUM, NUM_DTO, NUM_BARRIO)
- Acorta nombres de propiedades (ej., "Nombre científico" → "sn")
- Reduce el tamaño del archivo en ~18%
- Los archivos se comprimen más con gzip al servirse (GitHub Pages aplica automáticamente ~88% de compresión)

**Resultados de ejemplo:**
- Sin comprimir en disco: 184 MB → Usuario descarga con gzip: **~22 MB**

**Cuándo usar:** Después de ejecutar `split-by-district.py`, siempre ejecuta `compress-districts.py` antes de desplegar para optimizar velocidades de descarga.

## 🐛 Solución de Problemas

### "Límite de tamaño de archivo de GitHub excedido"

**Solución:** Tu archivo es demasiado grande (>100 MB).

1. Ejecuta el optimizador:
   ```bash
   python optimize-geojson.py
   ```
2. O usa Git LFS (ver Paso 8)
3. O divide por distritos (ver `split-by-district.py`)

### El mapa no carga / página en blanco

**Solución:**

1. Revisa la consola del navegador (F12) para errores
2. Verifica que `trees.geojson` exista en la raíz del proyecto
3. Asegúrate de que el GeoJSON sea válido (usa https://geojson.io/ para verificar)
4. Prueba primero localmente con `python -m http.server`

### "Error CORS" al probar localmente

**Solución:** No abras `index.html` directamente (file://).

Siempre usa un servidor local:
```bash
python -m http.server 8000
```

### El mapa es muy lento

**Solución:** Demasiados árboles para el navegador.

Divide por distritos para carga dinámica

### Los árboles no aparecen en el mapa

**Solución:** Los nombres de los campos pueden ser diferentes.

1. Abre tu `trees.geojson` en un editor de texto
2. Mira la sección "properties" de la primera característica
3. Actualiza los nombres de campo en `map.js` (líneas 120-140)

## 📊 Consejos de Rendimiento

**Tamaños de archivo recomendados:**
- Ciudades pequeñas (<50,000 árboles): < 50 MB
- Ciudades medianas (50k-200k árboles): 50-100 MB
- Ciudades grandes (>200k árboles): Usar división por distritos

**Tiempos de carga esperados:**
- Archivo de 20 MB: 2-5 segundos
- Archivo de 50 MB: 5-10 segundos
- Archivo de 100 MB: 10-30 segundos

## 🔄 Actualizar Tus Datos

Cuando tengas datos nuevos:

1. Reemplaza `trees.geojson` con el nuevo archivo
2. Optimízalo:
   ```bash
   python optimize-geojson.py
   rm trees.geojson
   mv trees-data.geojson trees.geojson
   ```
3. Haz commit y push:
   ```bash
   git add trees.geojson
   git commit -m "Actualizar datos de árboles"
   git push
   ```
4. Espera 1-2 minutos para que GitHub Pages se actualice

## 📄 Licencia

Este proyecto es de código abierto. Los datos de árboles pertenecen a la comunidad.

## 🤝 ¿Necesitas Ayuda?

- Abre un issue en GitHub
- Revisa los issues existentes para soluciones
- Lee los comentarios del código en `map.js` e `index.html`

## 🌍 Ejemplos

Proyectos usando esta plantilla:
- Árboles de Madrid: https://github.com/TU_USUARIO/madtrees
- (¡Agrega tu ciudad aquí!)

---

## Toque Final
Cambia el favicon por uno que represente tu ciudad

**¡Feliz mapeo! 🗺️🌳**
