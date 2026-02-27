# ckanext/mma/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from ckan.plugins import toolkit
from ckan.lib.mailer import mail_recipient
from sqlalchemy import text
from ckan import model


def get_top_datasets(period='all'):

    session = model.Session

    if period == '24h':
        query = text("""
            SELECT p.id,
                   p.title,
                   SUM(ts.count) AS total
            FROM tracking_summary ts
            JOIN package p ON p.id = ts.package_id
            WHERE ts.tracking_date >= NOW() - INTERVAL '24 hours'
            GROUP BY p.id, p.title
            ORDER BY total DESC
            LIMIT 3
        """)
    else:
        query = text("""
            SELECT p.id,
                   p.title,
                   SUM(ts.count) AS total
            FROM tracking_summary ts
            JOIN package p ON p.id = ts.package_id
            GROUP BY p.id, p.title
            ORDER BY total DESC
            LIMIT 3
        """)

    return session.execute(query).fetchall()

mma_blueprint = Blueprint(
    'mma',
    __name__,
    url_prefix='/mma'
)

@mma_blueprint.route('/retc')
def retc():
    return toolkit.render('mma/retc.html')

@mma_blueprint.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            toolkit.h.flash_error('Todos los campos son obligatorios')
            return toolkit.redirect_to('mma.contact')

        subject = f'Formulario MMA - {name}'
        body = f"""
Nombre: {name}
Email: {email}

Mensaje:
{message}
"""

        try:
            recipient = toolkit.config.get('ckan.mail_to')
            mail_recipient(subject, recipient, recipient, body)
            toolkit.h.flash_success('Mensaje enviado correctamente')
        except Exception as e:
            toolkit.h.flash_error(f'Error enviando correo: {str(e)}')

        return toolkit.redirect_to('mma.contact')

    return toolkit.render('mma/contact.html')

@mma_blueprint.route('/oirs', methods=['GET', 'POST'])
def oirs():

    if request.method == 'POST':

        nombre = request.form.get('nombre')
        email = request.form.get('email')
        descripcion = request.form.get('descripcion')

        if not nombre or not email or not descripcion:
            toolkit.h.flash_error('Todos los campos son obligatorios')
            return toolkit.redirect_to('mma.oirs')

        subject = f'Solicitud MMA - {email}'
        body = f"""
Nombre: {name}
Email: {email}

Descripción:
{descripcion}
"""

        try:
            recipient = toolkit.config.get('ckan.mail_to')
            mail_recipient(subject, recipient, recipient, body)
            toolkit.h.flash_success('Solicitud enviada correctamente')
        except Exception as e:
            toolkit.h.flash_error(f'Error enviando correo: {str(e)}')

        return toolkit.redirect_to('mma.oirs')

    return toolkit.render('mma/oirs.html')