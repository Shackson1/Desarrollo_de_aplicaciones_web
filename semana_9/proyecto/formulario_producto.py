from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class FormularioProducto(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres")
    ])
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria"),
        NumberRange(min=0, max=1000000, message="La cantidad debe ser mayor o igual a 0")
    ])
    precio = FloatField('Precio', validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0, max=1000000, message="El precio debe ser mayor o igual a 0")
    ])
    submit = SubmitField('Guardar Producto')

class FormularioEliminar(FlaskForm):
    id = IntegerField('ID del Producto a eliminar', validators=[
        DataRequired(message="El ID es necesario")
    ])
    submit = SubmitField('Eliminar Producto')

class FormularioBuscar(FlaskForm):
    nombre = StringField('Buscar por Nombre', validators=[
        DataRequired(message="Escribe un nombre para buscar"),
        Length(min=1, max=50)
    ])
    submit = SubmitField('Buscar')

class FormularioActualizar(FlaskForm):
    id = IntegerField('ID del Producto', validators=[
        DataRequired(message="El ID es obligatorio")
    ])
    cantidad = IntegerField('Nueva Cantidad', validators=[
        NumberRange(min=0, max=1000000)
    ], render_kw={"placeholder": "Opcional (Dejar vacío para no cambiar)"})
    precio = FloatField('Nuevo Precio', validators=[
        NumberRange(min=0, max=1000000)
    ], render_kw={"placeholder": "Opcional (Dejar vacío para no cambiar)"})
    submit = SubmitField('Actualizar')
