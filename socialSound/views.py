from django.shortcuts import render, redirect
from django.db.models import Sum, Q, Prefetch, Count
from .models import Usuario, Album, Cancion, Playlist, Guardado, MensajePrivado, Comentario
from django.views.defaults import page_not_found
from .forms import UsuarioModelForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate


## CRUD Usuario
 

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            usuario.set_password(raw_password)
            usuario.save()
            messages.success(request, 'registro existoso')
            return redirect('login_usuario')
        else:
            messages.error(request, 'Error en el registro de usuario')
    else:
        form = UsuarioModelForm()

    return render(request, 'CRUD_usuario/registro_usuario.html', {
        'form': form,
        'title': 'Registro d usuario'
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
                messages.success(request, f'Bienvenido {user.nombre_usuario}')
                return redirect('perfil_usuario', nombre_usuario=user.nombre_usuario)
            else:
                messages.error(request, 'Credenciales inválidas') 
    else:
        form = LoginForm()

    return render(request, 'CRUD_usuario/login_usuario.html', {'form': form})


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


def eliminar_usuario(request, nombre_usuario):
    usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
    try:
        usuario.delete()
    except:
        pass
    return redirect('registro_usuario')

       
    























































# 1. Página de inicio con enlaces a todas las URLs
def index(request):
    # Renderiza la plantilla principal con enlaces a las demás páginas de la aplicación
    return render(request, "index.html")


# 2. Mostrar el perfil del usuario
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


# 3. Feed que muestra los álbumes subidos por los usuarios seguidos
def feed(request, nombre_usuario):
    # Primero obtenemos el usuario actual y los usuarios que sigue
    usuario_actual = Usuario.objects.get(nombre_usuario=nombre_usuario)
    usuarios_seguidos = usuario_actual.obtener_seguidos()

    # Ahora los álbumes de los usuarios seguidos, ordenados por fecha de subida
    albumes_feed = Album.objects.select_related('usuario').filter(usuario__in=usuarios_seguidos).order_by('-fecha_subida')[:5] #uso de limit

    # Calculamos el total de likes en los álbumes del feed
    total_likes = albumes_feed.aggregate(total_likes=Sum('estadisticasalbum__likes'))['total_likes'] or 0

    # Renderizammos el feed con los álbumes y el total de likes
    return render(request, 'usuario/feed.html', {
        'albumes_feed': albumes_feed,
        'usuario_actual': usuario_actual,
        'total_likes': total_likes,
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
    detalles_album = album.album  # Información detallada del álbum (OneToOne)
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
    # Obtenemos el álbum y sus comentarios, ordenados por fecha de publicación (uso de prefetch y queryset)
    album = Album.objects.prefetch_related(
        Prefetch(
            'comentario_set',
            queryset=Comentario.objects.select_related('usuario').order_by('-fecha_publicacion'),
            to_attr='comentarios'
        )
    ).get(id=album_id)

    # Renderizamos la plantilla con los comentarios del álbum
    return render(request, 'album/comentarios_album.html', {
        'album': album,
        'comentarios': album.comentarios
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


#Vistas de error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
