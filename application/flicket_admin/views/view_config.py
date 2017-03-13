#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import (flash,
                   redirect,
                   render_template,
                   url_for)
from flask_login import login_required

from application import app, db
from application.flicket_admin.forms.form_config import ConfigForm
from application.flicket_admin.models.flicket_config import FlicketConfig

from . import admin_bp
from .view_admin import admin_permission


# Configuration view
@admin_bp.route(app.config['ADMINHOME'] + 'config/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def flicket_config():
    form = ConfigForm()

    config_details = FlicketConfig.query.first()

    if form.validate_on_submit():

        config_details.mail_server = form.mail_server.data
        config_details.mail_port = form.mail_port.data
        config_details.mail_use_tls = form.mail_use_tls.data
        config_details.mail_use_ssl = form.mail_use_ssl.data
        config_details.mail_debug = form.mail_debug.data
        config_details.mail_username = form.mail_username.data
        config_details.mail_password = form.mail_password.data
        config_details.mail_default_sender = form.mail_default_sender.data
        config_details.mail_max_emails = form.mail_max_emails.data
        config_details.mail_suppress_send = form.mail_suppress_send.data
        config_details.mail_ascii_attachments = form.mail_ascii_attachments.data

        config_details.posts_per_page = form.posts_per_page.data,
        config_details.allowed_extensions = form.allowed_extensions.data,
        config_details.ticket_upload_folder = form.ticket_upload_folder.data

        db.session.commit()
        flash('Config details updated.')
        return redirect(url_for('admin_bp.flicket_config'))

    # populate form with details from database.
    form.mail_server.data = config_details.mail_server
    form.mail_port.data = config_details.mail_port
    form.mail_use_tls.data = config_details.mail_use_tls
    form.mail_use_ssl.data = config_details.mail_use_ssl
    form.mail_debug.data = config_details.mail_debug
    form.mail_username.data = config_details.mail_username
    form.mail_password.data = config_details.mail_password
    form.mail_default_sender.data = config_details.mail_default_sender
    form.mail_max_emails.data = config_details.mail_max_emails
    form.mail_suppress_send.data = config_details.mail_suppress_send
    form.mail_ascii_attachments.data = config_details.mail_ascii_attachments

    form.posts_per_page.data = config_details.posts_per_page
    form.allowed_extensions.data = config_details.allowed_extensions
    form.ticket_upload_folder.data = config_details.ticket_upload_folder

    return render_template('admin_config.html',
                           title='Flicket Configuration',
                           form=form)