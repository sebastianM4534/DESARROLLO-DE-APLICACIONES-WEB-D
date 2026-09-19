from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import Usuario


class UsuarioForm(FlaskForm):

    usuario = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(min=4, max=50, message="El nombre de usuario debe tener entre 4 y 50 caracteres.")
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
        ]
    )

    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debe confirmar la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden.")
        ]
    )

    submit = SubmitField("Registrarse")

    def validate_usuario(self, campo):
        """
        Validador personalizado de WTForms: además del UNIQUE de la
        base de datos, comprueba antes del INSERT que el nombre de
        usuario no esté ya registrado, para mostrar un mensaje claro
        en el propio formulario.
        """

        if Usuario.existe(campo.data):
            raise ValidationError("Ese nombre de usuario ya está registrado.")