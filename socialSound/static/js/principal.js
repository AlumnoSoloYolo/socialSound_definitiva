function eliminar_usuario() {
    let x = confirm('¿Está seguro que desea eliminar su cuenta?');
    if (x)
        return true;
    else
        return false;

};