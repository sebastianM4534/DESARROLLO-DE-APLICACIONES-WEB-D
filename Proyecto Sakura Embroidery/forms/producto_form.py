from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Uniformes", "Uniformes"),
            ("Gorras", "Gorras"),
            ("Camisetas", "Camisetas"),
            ("Otros", "Otros")
        ],
        validators=[
            DataRequired(message="Debe seleccionar una categoría.")
        ]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0.")
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(min=0, message="El stock no puede ser negativo.")
        ]
    )

    # Relación con la tabla proveedores (clave foránea).
    # Las opciones (choices) se cargan dinámicamente desde la
    # base de datos en app.py antes de mostrar/validar el formulario.
    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(message="Debe seleccionar un proveedor.")
        ]
    )

    submit = SubmitField("Guardar producto")