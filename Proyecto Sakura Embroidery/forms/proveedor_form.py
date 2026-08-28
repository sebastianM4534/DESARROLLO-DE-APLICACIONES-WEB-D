from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    producto = StringField(
        "Producto o servicio",
        validators=[
            DataRequired(message="El producto o servicio es obligatorio."),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=10, max=10, message="El teléfono debe tener 10 dígitos.")
        ]
    )

    submit = SubmitField("Guardar proveedor")