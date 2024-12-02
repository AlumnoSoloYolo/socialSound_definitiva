from django.urls import path, re_path
from .import views

urlpatterns = [
     path('registro/', views.registro_usuario, name='registro_usuario'),
     path('login/', views.login_usuario, name='login_usuario'),
     path('perfil/<str:nombre_usuario>/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
     path('perfil/<str:nombre_usuario>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),








     path('', views.index, name='index'),  # Página de inicio con enlaces a todas las URLs
     path('mensajes_privados/<int:emisor_id>/<int:receptor_id>/', views.mensajes_privados, name='mensajes_privados'),
     re_path(r'^perfil_usuario/(?P<nombre_usuario>[a-zA-Z0-9_]+)/$', views.perfil_usuario, name='perfil_usuario'),
     path('usuario/<str:nombre_usuario>/feed/', views.feed, name='feed'),
     path('cancion/<int:cancion_id>/detalles_cancion/', views.detalle_cancion, name='detalle_cancion'),
     path('album/<int:album_id>/detalles_album/', views.detalle_album, name='detalle_album'),
     path('album/<int:album_id>/canciones/', views.canciones_album, name='canciones_album'),
     path('canciones_guardadas/<str:nombre_usuario>/', views.canciones_guardadas, name="canciones_guardadas"),
     path('lista_albumes/<str:nombre_usuario>/', views.lista_albumes, name='lista_albumes'),
     path('album/<int:album_id>/comentarios/', views.comentarios_album, name='comentarios_album'),
     path('usuario/<str:nombre_usuario>/playlists/', views.lista_playlist, name='lista_playlist'),
     path('playlist/<int:playlist_id>/canciones/', views.canciones_playlist, name='canciones_playlist'),
     path('usuario/<str:nombre_usuario>/usuarios-que-no-sigue/', views.lista_no_sigue, name='lista_no_sigue'),
]