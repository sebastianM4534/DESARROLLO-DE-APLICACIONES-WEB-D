from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio."),
            Length(min=5, max=20, message="El número debe tener entre 5 y 20 caracteres.")
        ]
    )

    # Relación con la tabla clientes (clave foránea).
    # Las opciones (choices) se cargan dinámicamente desde la
    # base de datos en app.py antes de mostrar/validar el formulario.
    id_cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(message="Debe seleccionar un cliente.")
        ]
    )

    # DateField (no StringField): la columna "fecha" en PostgreSQL
    # es de tipo DATE, así que WTForms valida el formato antes de
    # llegar a la base de datos y entrega un objeto date real,
    # compatible con psycopg2.
    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="La fecha es obligatoria.")
        ]
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(min=0.01, message="El total debe ser mayor a 0.")
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired(message="Debe seleccionar un estado.")
        ]
    )

    submit = SubmitField("Guardar factura")