# redSocialMusica
        # Definir en qué consistirá mi página Web:

SocialSound es una aplicación basada en una red social para amantes de la música. La plataforma permite que los usuarios hacer login en su cuenta privada; puedan añadir su propia material; o descubrir y compartir distintos discos y canciones. Un usuario puede seguir a otros usuarios y ver las publicaciones de canciones y discos que sube o comparte en su feed. 

El usuario tiene un perfil personalizable que el resto de usuarios podrá ver.

Los usuarios pueden interactuar con otros usuarios por medio de likes, comentarios en publicaciones o mensajes directos. Además, los usuarios pueden guardar distintas canciones y añadirlas a playlists personalizadas.

        #  debe especificarse en que consiste cada modelo, cada atributo y cada parámetro usado. Y el esquema de modelo entidad-relación.


1. Modelo Usuario
Descripción: Representa a los usuarios de la plataforma.
Atributos:
nombre_usuario: CharField (máx. 100 caracteres) - Nombre único del usuario.
password: CharField (máx. 100 caracteres) - Contraseña del usuario (almacenada de forma encriptada).
bio: TextField (opcional) - Biografía del usuario.
ciudad: CharField (máx. 150 caracteres) - Ciudad del usuario.
foto_perfil: ImageField (opcional) - Imagen de perfil del usuario.
fecha_nac: DateField - Fecha de nacimiento del usuario.

2. Modelo Seguidores
Descripción: Representa la relación de seguimiento entre los usuarios.
Atributos:
seguidor: ForeignKey a Usuario - Usuario que sigue a otro.
seguido: ForeignKey a Usuario - Usuario que es seguido.
fecha_inicio: DateTimeField - Fecha en que se inició el seguimiento.

3. Modelo Album
Descripción: Representa un álbum musical.
Atributos:
titulo: CharField (máx. 200 caracteres) - Título del álbum.
artista: CharField (máx. 200 caracteres) - Artista del álbum.
usuario: ForeignKey a Usuario - Usuario que crea el álbum.
fecha_lanzamiento: DateField - Fecha de lanzamiento del álbum.
portada: ImageField (opcional) - Portada del álbum.
descripcion: TextField (opcional) - Descripción del álbum.
reposts: ManyToManyField a Usuario (opcional) - Usuarios que han compartido el álbum.

4. Modelo DetalleAlbum
Descripción: Contiene información adicional sobre un álbum.
Atributos:
album: OneToOneField a Album - Álbum asociado.
productor: CharField (máx. 200 caracteres) - Productor del álbum.
estudio_grabacion: CharField (máx. 200 caracteres, opcional) - Estudio donde se grabó el álbum.
numero_pistas: PositiveIntegerField - Número de pistas en el álbum.
sello_discografico: CharField (máx. 100 caracteres, opcional) - Sello discográfico del álbum.
5. Modelo EstadisticasAlbum

Descripción: Contiene estadísticas de un álbum.
Atributos:
album: OneToOneField a Album - Álbum asociado.
reproducciones: PositiveIntegerField (valor por defecto 0) - Número de reproducciones del álbum.
likes: PositiveIntegerField (valor por defecto 0) - Número de "me gusta" del álbum.
comentarios: PositiveIntegerField (valor por defecto 0) - Número de comentarios en el álbum.

6. Modelo Cancion
Descripción: Representa una canción musical.
Atributos:
etiqueta: CharField (máx. 50 caracteres) - Categoría de la canción (ej. rock, pop).
titulo: CharField (máx. 200 caracteres) - Título de la canción.
artista: CharField (máx. 100 caracteres) - Artista de la canción.
archivo_audio: FileField - Archivo de audio de la canción.
portada: ImageField (opcional) - Portada de la canción.
fecha_subida: DateTimeField (valor por defecto: hora actual) - Fecha en que se subió la canción.
usuario: ForeignKey a Usuario - Usuario que subió la canción.
album: ForeignKey a Album (opcional) - Álbum al que pertenece la canción.
likes: ManyToManyField a Usuario (opcional) - Usuarios que le han dado "me gusta" a la canción.
reposts: ManyToManyField a Usuario (opcional) - Usuarios que han compartido la canción.

7. Modelo DetalleCancion
Descripción: Contiene información adicional sobre una canción.
Atributos:
cancion: OneToOneField a Cancion - Canción asociada.
letra: TextField (opcional) - Letra de la canción.
creditos: TextField (opcional) - Créditos de la canción.
duracion: DurationField - Duración de la canción.
idioma: CharField (máx. 50 caracteres, opcional) - Idioma de la canción.

8. Modelo Playlist
Descripción: Representa una lista de reproducción de canciones.
Atributos:
nombre: CharField (máx. 100 caracteres) - Nombre de la lista de reproducción.
descripcion: TextField (máx. 255 caracteres) - Descripción de la lista de reproducción.
fecha_creacion: DateTimeField (valor por defecto: hora actual) - Fecha de creación de la lista de reproducción.
usuario: ForeignKey a Usuario - Usuario que creó la lista de reproducción.
canciones: ManyToManyField a Cancion (a través de CancionPlaylist) - Canciones en la lista de reproducción.
publica: BooleanField (valor por defecto: True) - Indica si la lista de reproducción es pública.

9. Modelo CancionPlaylist
Descripción: Tabla intermedia que relaciona Playlist y Cancion.
Atributos:
cancion: ForeignKey a Cancion - Canción en la lista de reproducción.
playlist: ForeignKey a Playlist - Lista de reproducción que contiene la canción.
orden: PositiveIntegerField (valor por defecto: 0) - Orden de la canción en la lista de reproducción.
fecha_agregada: DateTimeField (valor por defecto: hora actual) - Fecha en que se agregó la canción a la lista de reproducción.

10. Modelo Like
Descripción: Representa los "me gusta" dados a las canciones.
Atributos:
usuario: ForeignKey a Usuario - Usuario que dio "me gusta".
cancion: ForeignKey a Cancion - Canción a la que se le dio "me gusta".
fecha_like: DateTimeField (valor por defecto: hora actual) - Fecha en que se dio "me gusta".

Tipos de Atributos:
CharField: Se usa para cadenas cortas (nombres, títulos).
TextField: Se usa para cadenas más largas (biografías, letras).
DateField: Se usa para fechas.
DateTimeField: Se usa para fechas y horas.
PositiveIntegerField: Se usa para números enteros positivos (número de pistas, likes).
DurationField: Se usa para representar duraciones de tiempo.
ImageField: Se usa para cargar imágenes.
FileField: Se usa para cargar archivos (audio).
BooleanField: Se usa para valores verdadero/falso.
ManyToManyField: Se usa para relaciones de muchos a muchos.


        # Esquema de Modelo Entidad-Relación (ERD):


Relación Usuario

Relación 1 a N con Seguidores: Un usuario puede seguir a muchos otros usuarios (relación "seguidor").
Relación 1 a N con Album: Un usuario puede crear muchos álbumes.
Relación 1 a N con Cancion: Un usuario puede subir muchas canciones.
Relación N a N con Cancion a través de Like: Un usuario puede dar "me gusta" a muchas canciones, y una canción puede tener "me gusta" de muchos usuarios.
Relación N a N con Album a través de reposts: Un usuario puede repostear muchos álbumes, y un álbum puede ser reposted por muchos usuarios.
Relación N a N con Cancion a través de reposts: Un usuario puede repostear muchas canciones, y una canción puede ser reposted por muchos usuarios.
Relación 1 a N con Playlist: Un usuario puede crear muchas listas de reproducción.
Relación N a N con Cancion a través de Guardado: Un usuario puede guardar muchas canciones, y una canción puede ser guardada por muchos usuarios.


Relación Seguidores

Relación N a 1 con Usuario (seguidor): Cada relación de seguimiento tiene un usuario que es el "seguidor".
Relación N a 1 con Usuario (seguido): Cada relación de seguimiento tiene un usuario que es "seguido".
Relación única entre los usuarios: Un usuario no puede seguir al mismo usuario más de una vez (garantizado por unique_together).


Relación Album

Relación 1 a 1 con DetalleAlbum: Cada álbum tiene detalles específicos relacionados con él.
Relación 1 a 1 con EstadisticasAlbum: Cada álbum tiene estadísticas específicas relacionadas con él.
Relación 1 a N con Cancion: Un álbum puede contener muchas canciones.
Relación N a N con Usuario a través de reposts: Un álbum puede ser reposted por muchos usuarios, y un usuario puede repostear muchos álbumes.

Relación DetalleAlbum

Relación 1 a 1 con Album: Cada detalle del álbum está vinculado a un álbum específico.
Relación EstadisticasAlbum
Relación 1 a 1 con Album: Cada estadística del álbum está vinculada a un álbum específico.
Relación Cancion
Relación N a 1 con Album: Cada canción pertenece a un álbum específico (opcional, ya que puede ser nulo).
Relación 1 a N con DetalleCancion: Cada canción puede tener detalles específicos relacionados con ella.
Relación N a N con Usuario a través de Like: Una canción puede ser "gustada" por muchos usuarios y un usuario puede gustar muchas canciones.
Relación N a N con Usuario a través de reposts: Una canción puede ser reposted por muchos usuarios y un usuario puede repostear muchas canciones.
Relación 1 a N con Comentario: Una canción puede tener muchos comentarios.


Relación DetalleCancion

Relación 1 a 1 con Cancion: Cada detalle de la canción está vinculado a una canción específica.


Relación Playlist

Relación 1 a N con Usuario: Una lista de reproducción pertenece a un usuario específico.
Relación N a N con Cancion a través de CancionPlaylist: Una lista de reproducción puede contener muchas canciones, y una canción puede estar en muchas listas de reproducción.


Relación CancionPlaylist

Relación N a 1 con Cancion: Cada entrada de la tabla intermedia se refiere a una canción específica.
Relación N a 1 con Playlist: Cada entrada de la tabla intermedia se refiere a una lista de reproducción específica.
Relación única (cancion, playlist): Una canción no puede aparecer más de una vez en la misma lista de reproducción.


Relación Like

Relación N a 1 con Usuario: Cada "me gusta" está asociado a un usuario específico.
Relación N a 1 con Cancion: Cada "me gusta" está asociado a una canción específica.
Relación única (usuario, cancion): Un usuario no puede dar "me gusta" a la misma canción más de una vez.


Relación Comentario

Relación N a 1 con Cancion: Cada comentario está asociado a una canción específica.
Relación N a 1 con Usuario: Cada comentario está asociado a un usuario específico.


Relación MensajePrivado

Relación N a 1 con Usuario (emisor): Cada mensaje privado tiene un emisor que es un usuario específico.
Relación N a 1 con Usuario (receptor): Cada mensaje privado tiene un receptor que es un usuario específico.


Relación Guardado

Relación N a 1 con Usuario: Cada canción guardada está asociada a un usuario específico.
Relación N a 1 con Cancion: Cada canción guardada está asociada a una canción específica.
Relación única (usuario, cancion): Un usuario no puede guardar la misma canción más de una vez.


______________________________________________________________________________________________________________

PARTE 2: aclaraciones y especificaciones de URLs y Vistas

## ACLARACIONES ARCHIVOS MULTIMEDIA:

NO SE SIRVEN EN MODO PRODUCCIÓN. Si quieres verlo poner DEBUG = True




## Estructura de URLs

A continuación, se detallan las URLs disponibles en la aplicación, junto con las vistas correspondientes y sus funcionalidades.

### 1. Página de inicio

- URL: `/`
- Vista: `index`
- Descripción: Página principal con enlaces a todas las otras vistas de la aplicación.
- Requisito cumplido:
      -  index donde aaceder a todas las urls

### 2. Perfil del usuario

- URL: `/perfil_usuario/<nombre_usuario>/`
- Vista: `perfil_usuario`
- Descripción: Muestra el perfil del usuario especificado, incluyendo seguidos, seguidores y álbumes creados.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Relaciones ManyToMany (seguidores y seguidos).
  - Parámetros str
  - Uso de re_path en la url
  
### 3. Feed del usuario

- URL: `/usuario/<nombre_usuario>/feed/`
- Vista: `feed`
- Descripción: Muestra los álbumes subidos por los usuarios que el usuario especificado sigue.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Aggregates para calcular el total de likes en los álbumes.
  - Uso de limit
  - Parámetros str
  - Uso de order_by

### 4. Lista de álbumes

- URL: `/lista_albumes/<nombre_usuario>/`
- Vista: `lista_albumes`
- Descripción: Muestra una lista de todos los álbumes creados por el usuario especificado.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Relaciones OneToMany (álbumes del usuario).
  - Parámetros str
  - order_by

### 5. Detalles de un álbum

- URL: `/album/<int:album_id>/detalles_album/`
- Vista: `detalle_album`
- Descripción: Muestra los detalles de un álbum específico, incluyendo estadísticas.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Relaciones OneToOne (detalles y estadísticas del álbum).
  - Parámetros enteros

### 6. Listar canciones de un álbum

- URL: `/album/<int:album_id>/canciones/`
- Vista: `canciones_album`
- Descripción: Muestra todas las canciones que pertenecen a un álbum específico.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros enteros

### 7. Comentarios de un álbum

- URL: `/album/<int:album_id>/comentarios/`
- Vista: `comentarios_album`
- Descripción: Muestra todos los comentarios realizados en un álbum específico.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Relaciones OneToMany (comentarios del álbum).
  - Parámetros enteros
  - uso order_by

### 8. Detalles de una canción

- URL: `/cancion/<int:cancion_id>/detalles_cancion/`
- Vista: `detalle_cancion`
- Descripción: Muestra los detalles de una canción específica.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros enteros

### 9. Lista de playlists de un usuario

- URL: `/usuario/<nombre_usuario>/playlists/`
- Vista: `lista_playlist`
- Descripción: Muestra todas las playlists creadas por el usuario especificado.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros str

### 10. Contenido de una playlist

- URL: `/playlist/<int:playlist_id>/canciones/`
- Vista: `canciones_playlist`
- Descripción: Muestra todas las canciones que pertenecen a una playlist específica.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros enteros

### 11. Canciones guardadas por el usuario

- URL: `/canciones_guardadas/<nombre_usuario>/`
- Vista: `canciones_guardadas`
- Descripción: Muestra una lista de todas las canciones que el usuario ha guardado.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros str

### 12. Mensajes privados entre dos usuarios

- URL: `/mensajes_privados/<int:emisor_id>/<int:receptor_id>/`
- Vista: `mensajes_privados`
- Descripción: Muestra la interfaz de mensajes privados entre dos usuarios.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros enteros
  - filtros con OR y AND
  - Uso order_by


### 13. URL: Usuarios que un usuario específico no sigue
- Vista: `lista_no_sigue`
- Descripción: Muestra una lista de usuarios que el usuario actual no sigue.
- Requisitos cumplidos:
  - Uso de QuerySet, optimización y comentarios explicando funcionamiento de las vistas.
  - Parámetros str
  - Filtro con `None`: Se aplica un filtro que utiliza `None` en la tabla intermedia para determinar la relación de seguimiento.

## Requisitos cumplidos

1. 10 URLs con vistas correspondientes.
2. Uso de funciones vistas en clase y QuerySet para obtener datos entre tablas.
3. Comentarios en cada vista explicando su funcionalidad.
4. Manejo de relaciones ManyToMany, OneToOne y OneToMany.
5. Página de error personalizada para los cuatro tipos de errores.
6. Optimización de queries.
7. Uso de `re_path`, parámetros enteros y `str`.
8. Filtros con AND y OR, aggregate, relación reversa, `order_by`, limit y filtro con `None`.
9. Existencia de un índice desde donde se puede acceder a todas las URLs.



## Uso de templates tags (al menos 5)

 {% include 'header.html' %} en 'principal.html'
 {% block contenido %} {% endblock %} en 'principal.html'
 {% for %} {% endfor %} en 'album.html'
 {% empty %} en 'album.html'
 {% if %} {% else %} {% endif %} en 'album.html'

Son frecuentes en todo el proyecto, pero aquí especifico un ejemplo que muestra el uso de cada uno de ellos.


 ## Uso de al menos cinco operadores distintos
 {% if album.album.numero_pistas > 0 %} en 'album.html'
 {% if comentario.usuario.ciudad == None or comentario.usuario.ciudad != "" %} en 'comentario.html'
 {% if album.usuario and album.usuario.nombre_usuario %} en 'comentarios_album.html'
 {% if estadisticas_album.comentarios == 0 %} en 'detalle_album.html


 ## uso de distintos template filters
  <p>Estudio de Grabación: {{ album.album.estudio_grabacion|default:"Desconocido" }}</p> en 'album.html'
  <p>Ciudad: {{ comentario.usuario.ciudad|upper }}</p> en 'comentario.html'
  <p>Género: {{ album.descripcion|lower }}</p> en 'comentario.html'
  <p>{{ comentario.fecha_publicacion|date:"d/m/Y" }}</p> en 'comentario.html'
  <p>{{ comentario.contenido|linebreaks }}</p> en 'comentario.html'
  {% if comentarios|length > 0 %} en 'comentarios-album.html
  <p>Género: {{ album.descripcion|lower }}</p> en 'comentario.html'

Estoy especificando ejemplos de los distintos filtros que he utilizado, los cuales repito en el proyecto sumando más de 10. 
      

Lo primero que tienes que hacer para probar los CRUDS es logearte. Una vez logueado te redirijirá a la página principal donde
encontrarás distintas listas con todos los CRUDS.

# CRUD USUARIO


# CREATE - UsuarioModelForm

    - Validación del Email
    
    Reglas

    Campo obligatorio (no puede estar vacío)
    Debe coincidir con el patrón de email: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

    Mensajes de Error

    Si está vacío: "Este campo es requerido."
    Si formato inválido: "Introduce un correo electrónico válido."

    Ejemplos
    usuario@dominio.com
  
    - Validación de nombre de usuario 

    Reglas

    Campo obligatorio (no puede estar vacío)
    Solo permite letras, números y guiones bajos: ^[a-zA-Z0-9_]+$
    Debe ser único en el sistema

    Mensajes de Error

    Si está vacío: "Este campo es requerido."
    Si formato inválido: "El nombre de usuario solo puede contener letras, números y guiones bajos"
    Si ya existe: "Nombre de usuario en uso"

    Ejemplos
    ✓ usuario123
    ✗ usuario@123
    ✗ usuario espacio
    ✗ usuario#especial


    - Validación de la Contraseña

    Reglas

    Campo obligatorio (no puede estar vacío)
    Debe cumplir con el patrón: ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
    
    [Mínimo 8 caracteres
    Al menos una mayúscula
    Al menos una minúscula
    Al menos un número
    Al menos un carácter especial (@$!%*?&)]

    Mensajes de Error

    Si está vacío: "Este campo es requerido."
    Si formato inválido: "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial (@$!%*?&)"

    Ejemplos
    Copy✓ Ejemplo1@
    ✓ Password123$
    ✗ password
    ✗ Password
    ✗ Password1
    ✗ pass

# UPDATE - UsuarioUpdateForm

    - Validación del Email

    Reglas

    Campo obligatorio (no puede estar vacío)
    Debe coincidir con el patrón: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

    Mensajes de Error

    Si está vacío: "Este campo es requerido."
    Si formato inválido: "Introduce un correo electrónico válido."

    Ejemplos
    ✓ usuario@dominio.com
    ✓ nombre.apellido@empresa.es
    ✗ usuario@
    ✗ @dominio.com


    - Validación del Nombre de Usuario

    Reglas

    Campo obligatorio (no puede estar vacío)
    Solo permite letras, números y guiones bajos: ^[a-zA-Z0-9_]+$
    Debe ser único en el sistema
    Verifica si es el mismo usuario antes de validar unicidad

    Mensajes de Error

    Si está vacío: "Este campo es requerido."
    Si formato inválido: "El nombre de usuario solo puede contener letras, números y guiones bajos"
    Si ya existe: "Nombre de usuario en uso"

    Ejemplos
    ✓ usuario123
    ✓ nombre_usuario
    ✗ usuario@123
    ✗ usuario espacio


# READ - BusquedaavanzadaUsuarioForm

    Reglas

    Al menos un campo debe contener un valor
    No se permiten todos los campos vacíos

    Mensajes de Error

    Si todos están vacíos: "Debes especificar al menos un criterio de búsqueda"

    Ejemplos
    ✓ Solo nombre_usuario con valor
    ✓ Solo ciudad con valor
    ✓ Cualquier combinación de campos
    ✗ Todos los campos vacíos


    - Validación de Edades
    
    Reglas

    Rango permitido: 1-120 años
    Si solo hay edad_min, edad_max = edad_min
    Si solo hay edad_max, edad_min = edad_max
    edad_min no puede ser mayor que edad_max
    Se convierten automáticamente a fechas:

    fecha_max = fecha_actual - edad_min
    fecha_min = fecha_actual - (edad_max + 1)

    Mensajes de Error

    Si edad_min > edad_max: "La edad mínima no puede ser mayor que la edad máxima"

    Ejemplos
    ✓ edad_min: 18, edad_max: 25
    ✓ edad_min: 30 (automáticamente edad_max = 30)
    ✓ edad_max: 50 (automáticamente edad_min = 50)
    ✗ edad_min: 40, edad_max: 30
    ✗ edad_min: 150 (fuera de rango)



# CRUD ALBUM


# CREATE - AlbumModelForm

    - Validación del Título
    
    Reglas

    Campo obligatorio
    Longitud máxima: 200 caracteres
    Debe ser único en combinación con el artista

    Mensajes de Error

    Si está vacío: "El título es obligatorio"
    Si excede longitud: "El título no puede exceder los 200 caracteres"
    Si duplicado: "Ya existe un álbum con este título y artista"

    Ejemplos
    ✓ "Dark Side of the Moon"
    ✓ "Abbey Road"
    ✗ "" (vacío)
    ✗ "Lorem ipsum..." (más de 200 caracteres)
    ✗ Título duplicado del mismo artista


    - Validación del Artista

    Reglas

    Campo obligatorio
    Longitud máxima: 200 caracteres

    Mensajes de Error

    Si está vacío: "El artista es obligatorio"
    Si excede longitud: "El nombre del artista no puede exceder los 200 caracteres"

    Ejemplos
    ✓ "Pink Floyd"
    ✓ "The Beatles"
    ✗ "" (vacío)
    ✗ "Lorem ipsum..." (más de 200 caracteres)

    Validación de Unicidad Compuesta

    Reglas

    La combinación título-artista debe ser única
    Se excluye el álbum actual en actualizaciones
    Se verifica en la base de datos

# READ - BusquedaAvanzadaAlbumForm

    





