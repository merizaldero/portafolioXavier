# XPD Texturas Tazas

**Plugin para WordPress v0.6**  
Autor: **Xavier Merizalde**

## Descripción

XPD Texturas Tazas es un plugin para WordPress que permite diseñar y gestionar texturas de sublimación para tazas. Define un tipo personalizado de contenido `xtt_TexturaSublimado` con un editor SVG integrado estilo Inkscape para la creación de gráficos vectoriales, que al ser aprobados se convierten automáticamente a PNG con canal alfa para su publicación.

Los usuarios autenticados pueden crear, editar y eliminar sus texturas directamente desde el frontend del sitio, sin necesidad de acceder a `wp-admin`.

## Características

- **Tipo de contenido personalizado** (`xtt_texturasublimado`) con soporte para título, editor y revisiones
- **Taxonomía jerárquica** (`xtt_categoria_textura`) para clasificar texturas por tipo de taza
- **Editor SVG integrado** basado en SVG.js + svg.draw.js con herramientas de dibujo vectorial
- **Herramientas de diseño**:
  - Selección y movimiento de objetos
  - Rectángulo, Círculo, Elipse, Línea, Polígono
  - Texto personalizado
  - Dibujo libre (path)
- **Controles de estilo**:
  - Color de relleno y borde
  - Grosor de borde ajustable
  - Opacidad configurable
- **Panel de usuario en el frontend** (`/mis-texturas/`):
  - Dashboard con lista paginada de texturas del usuario
  - Filtrado por categorías jerárquicas
  - Crear, editar y eliminar texturas sin acceder a wp-admin
  - Editor SVG completo integrado en el frontend
- **Flujo de aprobación** (exclusivo en wp-admin):
  - Estados personalizados: Borrador, Pendiente, Aprobado
  - Conversión automática SVG → PNG al aprobar
  - PNG con canal alfa para transparencia
- **Canvas redimensionable** (ancho y alto personalizables)
- **Vista previa** del PNG generado
- **Historial de deshacer** (hasta 20 acciones)
- **Seguridad**: Nonces, sanitización, verificación de permisos y autoría
- **Frontend público**: Función PHP y shortcode para mostrar texturas aprobadas

## Requisitos

- WordPress 5.8 o superior
- PHP 7.4 o superior
- Navegador moderno con soporte para Canvas API y SVG

## Instalación

1. Descarga o clona este repositorio
2. Sube la carpeta `xpd_texturas_tazas` a `wp-content/plugins/`
3. Activa el plugin desde el panel de administración de WordPress (Plugins > Plugins instalados)
4. Comienza a crear texturas desde el menú **Texturas Tazas** (wp-admin) o desde **Mis Texturas** (frontend)

## Uso

### Desde wp-admin (Administradores/Editores)

1. Ve a **Texturas Tazas > Nueva Textura**
2. Ingresa un título para la textura
3. Usa el editor SVG para diseñar tu textura
4. Guarda como borrador para continuar editando después

#### Aprobar y publicar

1. Cambia el estado a **Aprobado** en el panel de publicación
2. Al actualizar, el plugin convertirá automáticamente el SVG a PNG con canal alfa
3. Publica la textura

### Desde el Frontend (Usuarios autenticados)

#### Dashboard de Texturas

Accede a `/mis-texturas/` desde el navegador o desde el menú **Mis Texturas**.

- Verás una tabla con todas tus texturas (paginada: 10 por página)
- Usa el filtro lateral para filtrar por categoría
- Acciones disponibles: **Nueva Textura**, **Editar**, **Eliminar**

#### Crear una Nueva Textura

1. Haz clic en **+ Nueva Textura**
2. Ingresa título, descripción y selecciona categoría
3. Diseña tu textura con el editor SVG integrado
4. Haz clic en **Crear Textura** para guardar como borrador

#### Editar una Textura Existente

1. Haz clic en **Editar** junto a la textura deseada
2. Modifica título, descripción, categoría o estado
3. Edita el diseño en el editor SVG
4. Haz clic en **Guardar Cambios**

#### Eliminar una Textura

1. Haz clic en **Eliminar** junto a la textura deseada
2. Confirma la eliminación en la pantalla de confirmación
3. La textura será eliminada permanentemente

### Mostrar texturas en el sitio público

**Usando la función PHP:**
```php
echo xtt_render_png( $post_id );
```

**Usando el shortcode:**
```
[xtt_textura id="123"]
```

## Estructura del Plugin

```
xpd_texturas_tazas/
├── xpd_texturas_tazas.php          # Plugin principal
├── includes/
│   ├── xtt-post-type.php           # Definición del CPT y estados
│   ├── xtt-taxonomy.php            # Taxonomía xtt_categoria_textura
│   ├── xtt-metabox.php             # Metabox del editor SVG (admin)
│   ├── xtt-ajax.php                # Handlers AJAX
│   ├── xtt-render.php              # Renderizado frontend público
│   ├── xtt-frontend.php            # Rewrite rules, routing, templates
│   └── xtt-frontend-actions.php    # Handlers POST (crear, editar, eliminar)
├── templates/
│   └── frontend/
│       ├── dashboard.php           # Lista paginada + filtro categorías
│       ├── form.php                # Formulario crear/editar + editor
│       └── delete-confirm.php      # Confirmación eliminación
├── assets/
│   ├── js/
│   │   ├── xtt-editor.js           # Lógica del editor (admin)
│   │   ├── xtt-converter.js        # Conversión SVG → PNG
│   │   └── xtt-frontend-editor.js  # Lógica del editor (frontend)
│   └── css/
│       ├── xtt-editor.css          # Estilos del editor (admin)
│       └── xtt-frontend.css        # Estilos panel frontend
└── vendor/
    ├── svg.min.js                  # SVG.js v2.7.1
    └── svg.draw.js                 # svg.draw.js v2.0.4
```

## Prefijo de código

Todas las variables, clases y funciones del plugin utilizan el prefijo `xtt_` para evitar conflictos con otros plugins o temas.

## Convenciones de nombrado

| Tipo | Prefijo | Ejemplo |
|------|---------|---------|
| Funciones PHP | `xtt_` | `xtt_register_post_type()` |
| Variables PHP | `$xtt_` | `$xtt_svg_content` |
| Meta keys | `_xtt_` | `_xtt_svg_content`, `_xtt_png_data` |
| Funciones JS | `xtt_` | `xtt_init_editor()` |
| Variables JS | `xtt_` | `xtt_current_tool` |
| IDs HTML | `xtt-` | `xtt-drawing-area`, `xtt-toolbar` |
| Clases CSS | `.xtt-` | `.xtt-toolbar`, `.xtt-tool-btn` |

## Estados personalizados

| Estado | Slug | Descripción |
|--------|------|-------------|
| Borrador | `draft` | En edición, no visible públicamente |
| Pendiente | `xtt_pendiente` | Revisión pendiente |
| Aprobado | `xtt_aprobado` | Aprobado, visible públicamente, PNG generado |
| Publicado | `publish` | Publicado directamente |

## URLs del Frontend

| URL | Función |
|-----|---------|
| `/mis-texturas/` | Dashboard con lista de texturas del usuario |
| `/mis-texturas/nueva/` | Formulario de creación con editor SVG |
| `/mis-texturas/editar/{id}/` | Formulario de edición con editor SVG |
| `/mis-texturas/eliminar/{id}/` | Confirmación de eliminación |

## Hooks y Acciones

### Acciones disponibles

| Hook | Descripción |
|------|-------------|
| `xtt_on_approve` | Se ejecuta cuando una textura cambia a estado "Aprobado" |

### Meta datos almacenados

| Meta Key | Tipo | Descripción |
|----------|------|-------------|
| `_xtt_svg_content` | string | Contenido SVG del diseño |
| `_xtt_png_data` | string | Data URL del PNG generado |
| `_xtt_canvas_width` | int | Ancho del canvas en píxeles |
| `_xtt_canvas_height` | int | Alto del canvas en píxeles |
| `_xtt_needs_png` | bool | Flag para indicar conversión pendiente |

## Licencia

GPL v2 o posterior. Ver [LICENSE](LICENSE) para más detalles.

## Changelog

### v0.6 (2026-05-02)
- Panel de usuario en el frontend (`/mis-texturas/`)
- Dashboard paginado con filtrado por categorías
- Crear, editar y eliminar texturas sin acceder a wp-admin
- Taxonomía jerárquica `xtt_categoria_textura`
- Editor SVG integrado en formularios frontend
- Confirmación de eliminación con verificación de autoría
- Item de menú "Mis Texturas" en navegación principal

### v0.5 (2026-05-02)
- Versión inicial
- Custom Post Type `xtt_texturasublimado`
- Editor SVG integrado con SVG.js
- Conversión automática SVG → PNG con Canvas API
- Estados personalizados de flujo de aprobación
- Función y shortcode para renderizado frontend
