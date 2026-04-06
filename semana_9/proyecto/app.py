from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from db import init_db, configure_sqlalchemy
from models import db, ProductoORM
from inventario.inventario import Inventario
from inventario.productos import Producto
from formulario_producto import FormularioProducto, FormularioEliminar, FormularioBuscar, FormularioActualizar
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'

# Inicializar base de datos raw e Inventario (Semanas anteriores)
init_db()
inventario = Inventario()
inventario.cargar_desde_db()

# Inicializar SQLAlchemy ORM (Semana 12)
configure_sqlalchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gestion_productos')
def gestion_productos():
    return render_template('gestion_productos.html')

# SUBMENÚ DE INVENTARIO
@app.route('/inventario')
def inventario_index():
    return render_template('inventario.html')

@app.route('/inventario/mostrar')
def inventario_mostrar():
    inventario.cargar_desde_db()
    productos = inventario.listar_todos()
    return render_template('inventario_mostrar.html', productos=productos)

@app.route('/inventario/añadir', methods=['GET', 'POST'])
def inventario_añadir():
    form = FormularioProducto()
    if form.validate_on_submit():
        inventario.agregar_producto(
            form.nombre.data,
            form.cantidad.data,
            form.precio.data
        )
        flash(f'Producto "{form.nombre.data}" añadido con éxito.', 'success')
        return redirect(url_for('inventario_mostrar'))
    return render_template('productos_form.html', form=form, titulo="Añadir Producto")

@app.route('/inventario/eliminar', methods=['GET', 'POST'])
def inventario_eliminar():
    form = FormularioEliminar()
    if form.validate_on_submit():
        if inventario.eliminar_producto(form.id.data):
            flash(f'Producto ID {form.id.data} eliminado.', 'success')
            return redirect(url_for('inventario_mostrar'))
        else:
            flash(f'Error: No se encontró el producto con ID {form.id.data}.', 'danger')
    return render_template('inventario_eliminar.html', form=form)

@app.route('/inventario/actualizar', methods=['GET', 'POST'])
def inventario_actualizar():
    form = FormularioActualizar()
    if form.validate_on_submit():
        cant = form.cantidad.data
        prec = form.precio.data
        if inventario.actualizar_producto(form.id.data, nueva_cantidad=cant, nuevo_precio=prec):
            flash(f'Producto ID {form.id.data} actualizado correctamente.', 'success')
            return redirect(url_for('inventario_mostrar'))
        else:
            flash(f'Error: No se encontró el producto con ID {form.id.data}.', 'danger')
    return render_template('inventario_actualizar.html', form=form)

@app.route('/inventario/buscar', methods=['GET', 'POST'])
def inventario_buscar():
    form = FormularioBuscar()
    resultados = None
    if form.validate_on_submit():
        resultados = inventario.buscar_por_nombre(form.nombre.data)
        if not resultados:
            flash('No se encontraron productos con ese nombre.', 'info')
    return render_template('inventario_buscar.html', form=form, productos=resultados)

# NUEVAS RUTAS - SEMANA 12 (Persistencia Local y SQLAlchemy)

@app.route('/datos')
def datos():
    """Muestra los datos desde los archivos TXT, CSV y JSON"""
    txt_data = inventario.leer_txt()
    csv_data = inventario.leer_csv()
    json_data = inventario.leer_json()
    # Usando SQLAlchemy para obtener datos (REQ-S6-04)
    orm_data = ProductoORM.query.all()
    
    return render_template('datos.html', 
                           txt_data=txt_data, 
                           csv_data=csv_data, 
                           json_data=json_data,
                           orm_data=orm_data)

@app.route('/datos/exportar')
def datos_exportar():
    """Exporta el inventario activo a los tres formatos de archivo"""
    if len(inventario.productos) == 0:
        flash('El inventario está vacío, no hay datos para exportar.', 'warning')
        return redirect(url_for('inventario_index'))
    
    success_txt = inventario.guardar_txt()
    success_csv = inventario.guardar_csv()
    success_json = inventario.guardar_json()
    
    if success_txt and success_csv and success_json:
        flash('Inventario exportado exitosamente a TXT, CSV y JSON.', 'success')
    else:
        flash('Hubo un problema al exportar algunos archivos.', 'danger')
        
    return redirect(url_for('datos'))

@app.route('/datos/guardar', methods=['POST'])
def datos_guardar():
    """Guarda un producto vía ORM y actualiza archivos (Demostración)"""
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    
    if not nombre or not cantidad or not precio:
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('datos'))
    
    try:
        # Guardar en SQLite vía ORM (REQ-S6-05)
        nuevo_orm = ProductoORM(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo_orm)
        db.session.commit()
        
        # Sincronizamos el inventario en memoria para la exportación
        inventario.cargar_desde_db()
        inventario.guardar_txt()
        inventario.guardar_csv()
        inventario.guardar_json()
        
        flash(f'Producto "{nombre}" guardado vía ORM y archivos sincronizados.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar: {e}', 'danger')
        
    return redirect(url_for('datos'))

@app.route('/datos/ver/txt')
def ver_txt():
    ruta = os.path.join(os.path.dirname(__file__), 'inventario', 'data', 'datos.txt')
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            return Response(contenido, mimetype='text/plain')
    return "Archivo TXT no encontrado.", 404

@app.route('/datos/ver/json')
def ver_json():
    datos = inventario.leer_json()
    return jsonify(datos)

@app.route('/datos/ver/csv')
def ver_csv():
    ruta = os.path.join(os.path.dirname(__file__), 'inventario', 'data', 'datos.csv')
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            return Response(
                contenido, 
                mimetype='text/csv', 
                headers={"Content-Disposition": "attachment; filename=inventario.csv"}
            )
    return "Archivo CSV no encontrado.", 404

# Formulario de contacto (original)
class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired()])
    message = StringField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Mensaje enviado correctamente', 'success')
        return redirect(url_for('index'))
    return render_template('contacto.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)