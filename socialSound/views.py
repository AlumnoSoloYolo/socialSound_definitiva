from django.shortcuts import render, redirect
from django.db.models import Sum, Q, Prefetch, Count
from .models import Usuario, Album, Cancion, Playlist, Guardado, MensajePrivado, Comentario, EstadisticasAlbum, DetalleAlbum
from django.views.defaults import page_not_found
from .forms import UsuarioModelForm, LoginForm, BusquedaAvanzadaUsuarioForm, AlbumModelForm, DetalleAlbumModelForm, BusquedaAvanzadaAlbumForm, ComentarioModelForm, BusquedaAvanzadaComentarioForm, CancionForm, DetallesCancionForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import logout
from django.db import transaction
from django.forms import formset_factory


## CRUD Usuario
 

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            usuario.set_password(raw_password)
            usuario.save()
            messages.success(request, '¡Te has registrado con éxito!', extra_tags='registro')
            return redirect('login_usuario')
        else:
            messages.error(request, 'Error en el registro de usuario')
    else:
        form = UsuarioModelForm()

    return render(request, 'CRUD_usuario/registro_usuario.html', {
        'form': form,
        'title': 'Registro de usuario'
    })


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get('nombre_usuario')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=nombre_usuario, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.nombre_usuario}', extra_tags='login')
                return redirect('perfil_usuario', nombre_usuario=user.nombre_usuario)
            else:
                messages.error(request, 'Credenciales inválidas', extra_tags='error_credencialess') 
    else:
        form = LoginForm()

    return render(request, 'CRUD_usuario/login_usuario.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_usuario')

@login_required
def actualizar_perfil(request, nombre_usuario):
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil_usuario', nombre_usuario=usuario.nombre_usuario)
    else:
        form = UsuarioModelForm(instance=usuario)
    return render(request, 'CRUD_usuario/actualizar_perfil.html', {'form': form, 'usuario': usuario})

@login_required
def eliminar_usuario(request, nombre_usuario):
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    try:
        usuario.delete()
    except:
        pass
    return redirect('login_usuario')

@login_required
def busqueda_avanzada_usuarios(request):
    form = BusquedaAvanzadaUsuarioForm(request.GET or None)
    usuarios = Usuario.objects.all();
    filtros_aplicados=[]

    if form.is_valid():

        if nombre_usuario := form.cleaned_data.get('nombre_usuario'):
            usuarios = usuarios.filter(nombre_usuario__icontains=nombre_usuario)
            filtros_aplicados.append(f"nombre: {nombre_usuario}")

        if ciudad := form.cleaned_data.get('ciudad'):
            usuarios=usuarios.filter(ciudad__icontains=ciudad)
            filtros_aplicados.append(f"Ciudad: {ciudad}")
        
        if edad_min := form.cleaned_data.get('edad_min'):
            fecha_min = date.today() - relativedelta(years=edad_min+1)
            usuarios=usuarios.filter(fecha_nac__gte=fecha_min)
            filtros_aplicados.append(f"Edad mínima: {edad_min} años")

        if edad_max := form.cleaned_data.get('edad_max'):
            fecha_min = date.today() - relativedelta(years=edad_max+1)
            usuarios = usuarios.filter(fecha_nac__gte=fecha_min)
            filtros_aplicados.append(f"Edad máxima: {edad_max} años")
        
        if bio := form.cleaned_data.get('bio_contains'):
            usuarios = usuarios.filter(bio__icontains=bio)
            filtros_aplicados.append(f"Biografía contiene: {bio}")
        
    return render(request, 'CRUD_usuario/busqueda_avanzada_usuarios.html', {
            'form': form,
            'usuarios': usuarios,
            'filtros_aplicados': filtros_aplicados
        })

@login_required
def seguir_usuario(request, usuario_id):
    usuario_a_seguir = Usuario.objects.get(id=usuario_id)
    request.user.seguir(usuario_a_seguir)
    return render(request, 'parciales/boton_seguir.html', {'usuario': usuario_a_seguir})

@login_required
def dejar_de_seguir_usuario(request, usuario_id):
    usuario_a_dejar = Usuario.objects.get(id=usuario_id)
    request.user.dejar_de_seguir(usuario_a_dejar)
    return render(request, 'parciales/boton_seguir.html', {'usuario': usuario_a_dejar})


### CRUD Álbum

@login_required
def crear_album(request, nombre_usuario):
    # Verificar que el usuario que está creando el álbum sea el mismo que está logueado
    if request.user.nombre_usuario != nombre_usuario:
        return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)
    
    if request.method == 'POST':
        album_form = AlbumModelForm(request.POST, request.FILES)
        detalle_form = DetalleAlbumModelForm(request.POST)

      
        print("Datos recibidos para productor:", request.POST.get('productor'))
        
        if album_form.is_valid() and detalle_form.is_valid():
           
            album = album_form.save(commit=False)
            album.usuario = request.user
            album.save()

           
            estadisticas_album = EstadisticasAlbum(album=album)
            estadisticas_album.save()

          
            detalleAlbum = detalle_form.save(commit=False)
            detalleAlbum.album = album
            detalleAlbum.save()

            messages.success(request, 'Álbum creado correctamente.')
            return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)
        else:
          
            print("Errores en el formulario:", detalle_form.errors)

    else:
        album_form = AlbumModelForm()
        detalle_form = DetalleAlbumModelForm()
        
        print("Errores en el formulario:", detalle_form.errors)
    
   
    return render(request, 'CRUD_album/crear_album.html', {
        'album_form': album_form,
        'detalle_form': detalle_form,
        'title': 'Crear Nuevo Álbum',
        'operation': 'Crear'
    })



@login_required
def editar_album(request, nombre_usuario, album_id):
    
    album = Album.objects.select_related('detalle_album').get(id=album_id)
    detalle = album.detalle_album
  

    if request.method == 'POST':
       
        album_form = AlbumModelForm(request.POST, request.FILES, instance=album)
        detalle_form = DetalleAlbumModelForm(request.POST, instance=detalle)

        if album_form.is_valid() and detalle_form.is_valid():
           
            album_form.save()
            detalle_form.save()

            messages.success(request, 'Álbum actualizado correctamente')
            return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)
    else:
        album_form = AlbumModelForm(instance=album)
        detalle_form = DetalleAlbumModelForm(instance=detalle)

    return render(request, 'CRUD_album/editar_album.html', {
        'album_form': album_form,
        'detalle_form': detalle_form,
        'album': album,
        'nombre_usuario': nombre_usuario,
        'title': 'Editar Álbum',
        'operation': 'Actualizar'
    })




@login_required
def busqueda_avanzada_album(request):
    form = BusquedaAvanzadaAlbumForm(request.GET or None)
    
    # Ahora empezamos con todos los álbumes
    albums = Album.objects.all().select_related('usuario', 'detalle_album').order_by('-fecha_subida')
    filtros_aplicados = []

    if form.is_valid():
        if titulo := form.cleaned_data.get('titulo'):
            albums = albums.filter(titulo__icontains=titulo)
            filtros_aplicados.append(f"Título: {titulo}")
        
        if artista := form.cleaned_data.get('artista'):
            albums = albums.filter(artista__icontains=artista)
            filtros_aplicados.append(f"Artista: {artista}")
        
        if fecha_desde := form.cleaned_data.get('fecha_desde'):
            albums = albums.filter(fecha_subida__gte=fecha_desde)
            filtros_aplicados.append(f"fecha desde: {fecha_desde}")
        
        if fecha_hasta := form.cleaned_data.get('fecha_hasta'):
            albums = albums.filter(fecha_subida__lte=fecha_hasta)
            filtros_aplicados.append(f"fecha hasta: {fecha_hasta}")

    return render(request, "CRUD_album/busqueda_avanzada_albumes.html", {
        'form': form,
        'albums': albums,
        'filtros_aplicados': filtros_aplicados
    })





@login_required
def eliminar_album(request, album_id):
   
    album = Album.objects.get(id=album_id)
    
    if request.user != album.usuario:
        messages.error(request, 'No tienes permiso para eliminar este álbum.')
        return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)
    
    try:
        if request.method == 'POST':
           
            nombre_album = album.titulo
            album.delete()
            messages.success(request, f'El álbum "{nombre_album}" ha sido eliminado correctamente.')
    except Exception as e:
        messages.error(request, 'Hubo un error al eliminar el álbum. Por favor, inténtalo de nuevo.')
    
    return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)

### CRUD cancion
@login_required
def crear_album_con_canciones(request, nombre_usuario):
    if request.user.nombre_usuario != nombre_usuario:
        return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)

    CancionFormSet = formset_factory(CancionForm, extra=1, can_delete=True)
    DetallesCancionFormSet = formset_factory(DetallesCancionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        album_form = AlbumModelForm(request.POST, request.FILES)
        detalle_album_form = DetalleAlbumModelForm(request.POST)
        cancion_formset = CancionFormSet(request.POST, request.FILES, prefix='canciones')
        detalles_cancion_formset = DetallesCancionFormSet(request.POST, prefix='detalles')

        if all([album_form.is_valid(), detalle_album_form.is_valid(), 
               cancion_formset.is_valid(), detalles_cancion_formset.is_valid()]):
            try:
                with transaction.atomic():
                    album = album_form.save(commit=False)
                    album.usuario = request.user
                    album.save()

                    detalle_album = detalle_album_form.save(commit=False)
                    detalle_album.album = album
                    detalle_album.save()

                    EstadisticasAlbum.objects.create(album=album)

                    for cancion_form, detalles_form in zip(cancion_formset, detalles_cancion_formset):
                        if cancion_form.cleaned_data and not cancion_form.cleaned_data.get('DELETE', False):
                            cancion = cancion_form.save(commit=False)
                            cancion.album = album
                            cancion.usuario = request.user
                            if not cancion_form.cleaned_data.get('portada'):
                                cancion.portada = album.portada
                            cancion.save()

                            detalles = detalles_form.save(commit=False)
                            detalles.cancion = cancion
                            detalles.save()

                messages.success(request, 'Álbum y canciones creados exitosamente')
                return redirect('perfil_usuario', nombre_usuario=request.user.nombre_usuario)
            except Exception as e:
                messages.error(request, f'Error al crear el álbum: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario')

    else:
        album_form = AlbumModelForm()
        detalle_album_form = DetalleAlbumModelForm()
        cancion_formset = CancionFormSet(prefix='canciones')
        detalles_cancion_formset = DetallesCancionFormSet(prefix='detalles')

    context = {
        'album_form': album_form,
        'detalle_album_form': detalle_album_form,
        'cancion_formset': cancion_formset,
        'detalles_cancion_formset': detalles_cancion_formset,
        'title': 'Crear Nuevo Álbum'
       
    }
    return render(request, 'CRUD_album/crear_album_canciones.html', context)


### CRUD Comentario
@login_required
def crear_comentario(request, album_id):

    album = Album.objects.get(id=album_id)

    if request.method == 'POST':
        form = ComentarioModelForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.album = album
            comentario.save()
            messages.success(request, 'Tu comentario se ha publicado con éxito')
            return redirect('comentarios_album', album_id=album.id)
        else:
            messages.error(request, 'Hubo un error al publicar tu comentario. Por favor, verifica los datos e inténtalo de nuevo.')
            return redirect('comentarios_album', album_id=album.id)

    else:
        form = ComentarioModelForm()

    # Obtenemos los comentarios existentes para mostrar en la página
    comentarios = Comentario.objects.filter(album=album).order_by('-fecha_publicacion')
    
    context = {
        'form': form,
        'album': album,
        'comentarios': comentarios
    }
    
    return render(request, 'CRUD_comentario/crear_comentario.html', context)


@login_required
def actualizar_comentario(request, album_id, comentario_id):
    album = Album.objects.get(id=album_id)

    comentario = Comentario.objects.get(id=comentario_id, usuario=request.user)

    if request.method == 'POST':
        form = ComentarioModelForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comentario actualizado')
            return redirect('comentarios_album', album_id=album.id)
    else:
        form = ComentarioModelForm(instance=comentario)

    context = {
        'form': form,
        'album': album,
        'comentario': comentario,
        'is_update': True
    }

    return render(request, 'CRUD_comentario/editar_comentario.html', context)
    

def busqueda_avanzada_comentarios(request, album_id):
    album = Album.objects.get(id=album_id)
    form_busqueda = BusquedaAvanzadaComentarioForm(request.GET or None)
    
    comentarios = Comentario.objects.filter(album=album).select_related('usuario')
    
    if form_busqueda.is_valid():
        contenido = form_busqueda.cleaned_data.get('contenido')
        usuario = form_busqueda.cleaned_data.get('usuario')
        fecha_desde = form_busqueda.cleaned_data.get('fecha_desde')
        fecha_hasta = form_busqueda.cleaned_data.get('fecha_hasta')
        
        if contenido:
            comentarios = comentarios.filter(contenido__icontains=contenido)
        
        if usuario:
            comentarios = comentarios.filter(usuario__nombre_usuario__icontains=usuario)
        
        if fecha_desde:
            comentarios = comentarios.filter(fecha_publicacion__date__gte=fecha_desde)
        
        if fecha_hasta:
            comentarios = comentarios.filter(fecha_publicacion__date__lte=fecha_hasta)
    
    comentarios = comentarios.order_by('-fecha_publicacion')
    
    context = {
        'album': album,
        'comentarios': comentarios,
        'form_busqueda': form_busqueda
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'comentarios/includes/lista_comentarios.html', context)
    
    return render(request, 'comentarios/includes/busqueda_avanzada.html', context)


@login_required
def eliminar_comentario(request, album_id, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id, album_id=album_id)
    if request.user == comentario.usuario:
        comentario.delete()
    return redirect('comentarios_album', album_id=album_id)


















































# 1. Página de inicio con enlaces a todas las URLs
def index(request):
    # Renderiza la plantilla principal con enlaces a las demás páginas de la aplicación
    return render(request, "index.html")


# 2. Mostrar el perfil del usuario
@login_required
def perfil_usuario(request, nombre_usuario):
    # Obtenemos el usuario por nombre de usuario
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)

    # Llamamos a los métodos de seguidos y seguidores para acceder a ellos por separado
    seguidos = usuario.obtener_seguidos()
    total_seguidos = seguidos.count()
    seguidores = usuario.obtener_seguidores()
    total_seguidores = seguidores.count()

    # Obtenemos todos los álbumes del usuario
    albumes = Album.objects.select_related('usuario').filter(usuario=usuario)
    total_albumes = albumes.count()  # Contar el total de álbumes

    # Renderizamos la plantilla con los datos del perfil y estadísticas
    return render(request, 'usuario/perfil_usuario.html', 
                  {
                      'usuario': usuario,
                      'seguidos': seguidos,
                      'seguidores': seguidores,
                      'albumes': albumes,
                      'total_seguidos': total_seguidos,
                      'total_seguidores': total_seguidores,
                      'total_albumes': total_albumes
                  })



@login_required
def feed(request):
      # Obtener los usuarios que sigue el usuario actual
    usuarios_seguidos = request.user.obtener_seguidos()
    
    # Obtener los álbumes solo de los usuarios seguidos
    albums = Album.objects.filter(
        usuario__in=usuarios_seguidos
    ).select_related('usuario', 'detalle_album').order_by('-fecha_subida')

    return render(request, "usuario/feed.html", {
        'albums': albums
    })


# 4. Listar álbumes de un usuario específico
def lista_albumes(request, nombre_usuario):
    # Primero obtenemos el usuario y sus álbumes
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    albumes = Album.objects.filter(usuario=usuario).order_by('fecha_subida').select_related('usuario', 'album').prefetch_related('canciones')

    # Renderizamos la lista de álbumes del usuario
    return render(request, 'album/lista_albumes.html', {'albumes': albumes})


# 5. Detalles de un álbum específico
def detalle_album(request, album_id):
    # Obtenemos el álbum, usuario y detalles del album por separado
    album = Album.objects.get(id=album_id)
    usuario = album.usuario
    detalles_album = album.detalle_album # Información detallada del álbum (OneToOne)
    estadisticas_album = album.estadisticasalbum  # Estadísticas del álbum (OneToOne)

    # Renderizamos plantilla con los detalles del álbum y las estadísticas
    return render(request, 'album/detalle_album.html', {
        'album': album,
        'detalles_album': detalles_album,
        'estadisticas_album': estadisticas_album,
        'usuario': usuario
    })


# 6. Listar canciones de un álbum específico
def canciones_album(request, album_id):
    # Obtenemos el álbum y sus canciones
    album = Album.objects.select_related('usuario').prefetch_related(Prefetch('canciones')).get(id=album_id)

    # Renderizamos la plantilla de canciones para el álbum
    return render(request, 'cancion/canciones_album.html', {'album': album})


# 7. Comentarios de un álbum específico
def comentarios_album(request, album_id):
    album = Album.objects.get(id=album_id)
    
    # Inicializamos el formulario con los datos de GET si existen
    form_busqueda = BusquedaAvanzadaComentarioForm(request.GET or None)
    
    # Obtenemos los comentarios base
    comentarios = Comentario.objects.filter(album=album).select_related('usuario')
    
    # Si el formulario se envía y es válido, aplicamos los filtros
    if form_busqueda.is_valid():
        contenido = form_busqueda.cleaned_data.get('contenido')
        usuario = form_busqueda.cleaned_data.get('usuario')
        fecha_desde = form_busqueda.cleaned_data.get('fecha_desde')
        fecha_hasta = form_busqueda.cleaned_data.get('fecha_hasta')
        
        if contenido:
            comentarios = comentarios.filter(contenido__icontains=contenido)
        
        if usuario:
            comentarios = comentarios.filter(usuario__nombre_usuario__icontains=usuario)
        
        if fecha_desde:
            comentarios = comentarios.filter(fecha_publicacion__date__gte=fecha_desde)
        
        if fecha_hasta:
            comentarios = comentarios.filter(fecha_publicacion__date__lte=fecha_hasta)
    
    comentarios = comentarios.order_by('-fecha_publicacion')

    return render(request, 'album/comentarios_album.html', {
        'album': album,
        'comentarios': comentarios,
        'form_busqueda': form_busqueda,
        'form': ComentarioModelForm()  # Añadimos el formulario de crear comentario
    })


# 8. Detalles de una canción específica
def detalle_cancion(request, cancion_id):
    # Obtenemos la canción, sus detalles y su álbum
    cancion = Cancion.objects.get(id=cancion_id)
    detalles_cancion = cancion.detalles  # Detalles adicionales (OneToOne)
    album = cancion.album  # Álbum al que pertenece la canción

    # Rnederizamos la plantilla con los detalles de la canción
    return render(request, 'cancion/detalle_cancion.html', 
                  { 
                      'cancion': cancion,
                      'detalles': detalles_cancion, 
                      'album': album,
                  })


# 9. Listar las playlists creadas por un usuario
def lista_playlist(request, nombre_usuario):
    # Obtenemos el usuario ysus playlists
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    playlists = Playlist.objects.filter(usuario=usuario)

    # Renderizamos la plantilla con la lista de playlists del usuario
    return render(request, 'playlist/lista_playlist.html', {'playlists': playlists, 'usuario': usuario})


# 10. Contenido de una playlist específica
def canciones_playlist(request, playlist_id):
    # Obtenemos la playlist y sus canciones, además de los likes por cada canción
    playlist = Playlist.objects.select_related('usuario').prefetch_related('canciones').prefetch_related('canciones__like_set__usuario').get(id=playlist_id)

    # Renderizamos la plantilla con las canciones de la playlist
    return render(request, 'cancion/canciones_playlist.html', {
        'playlist': playlist,
    })


# 11. Lista de canciones guardadas por el usuario
def canciones_guardadas(request, nombre_usuario):
    # Obtenemos el usuario y las canciones guardadas
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    lista_canciones = Guardado.objects.filter(usuario=usuario).select_related('cancion', 'cancion__usuario')

    # Renderizamos la plantilla con las canciones guardadas
    return render(request, 'cancion/canciones_guardadas.html', {
        'usuario': usuario,
        'lista_canciones': lista_canciones,
    })


# 12. Interfaz de mensajes privados entre dos usuarios
def mensajes_privados(request, emisor_id, receptor_id):
    # Los primero que he hecho ha sido obtener los usuarios que participan en la conversación
    emisor = Usuario.objects.get(id=emisor_id)
    receptor = Usuario.objects.get(id=receptor_id)

    # Filtramos mensajes entre el emisor y el receptor
    mensajes = MensajePrivado.objects.filter(
        Q(emisor_id=emisor_id, receptor_id=receptor_id) | 
        Q(emisor_id=receptor_id, receptor_id=emisor_id)
    ).select_related('emisor', 'receptor').order_by('fecha_envio')

    # Si se envía un nuevo mensaje 
    if request.method == "POST":
        contenido = request.POST.get('contenido')
        if contenido: 
            nuevo_mensaje = MensajePrivado(
                emisor=emisor,
                receptor=receptor,
                contenido=contenido
            )
            nuevo_mensaje.save()  # Guardamos el nuevo mensaje en la base de datos
            return redirect('mensajes_privados', emisor_id=emisor_id, receptor_id=receptor_id)

    # Renderizamos la plantilla con los mensajes entre los dos usuarios
    return render(request, 'usuario/mensajes_privados.html', {
        'mensajes': mensajes,
        'emisor': emisor,
        'receptor': receptor
    })


# 13 listar usuarios que un usuario específico no sigue
def lista_no_sigue(request, nombre_usuario):
    # Obtenemos el usuario actual
    usuario_actual = Usuario.objects.get(nombre_usuario=nombre_usuario)
    # Obtener todos los usuarios que no son el actual
    todos_usuarios = Usuario.objects.exclude(id=usuario_actual.id)
    
    # Filtramos usuarios que no están en la relación 'seguidores' del usuario actual
    # Aplicamos el filtro para obtener usuarios que el usuario actual NO sigue.
    usuarios_no_seguidos = todos_usuarios.filter(seguidores__isnull=True)

    return render(request, 'usuario/lista_no_sigue.html', {
        'usuarios_no_seguidos': usuarios_no_seguidos
    })


def lista_seguidos(request):
    usuario_actual = request.user
    usuarios_seguidos = usuario_actual.obtener_seguidos()
    return render(request, 'usuario/usuarios_seguidos.html', {'usuarios_seguidos': usuarios_seguidos})

#Vistas de error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
