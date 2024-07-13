from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, PasswordField, IntegerField, TextAreaField, FileField, MultipleFileField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class FeedbackForm(FlaskForm):
    # name = StringField('Имя пользователя', validators=[DataRequired()])
    rating = IntegerField('Оценка', validators=[DataRequired()])
    review = TextAreaField('Отзыв')
    submit = SubmitField('Оставить отзыв')
    images = FileField('Изображения')


    # def validate_images(self, images):
    #     for file in images.data:
       
    #         extension = file.filename.lower().split('.')[-1]
    #         print('File extension: ', extension)
    #         if extension not in images.extensions:
    #             raise ValidationError('Добавлять можно только картинки')