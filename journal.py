from flask import Flask, g, render_template, flash, redirect, url_for, abort

from slugify import slugify
import models
import forms


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'ajls;feijp8j8j(P*J*(PHpgeygf'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_entry', methods=('GET', 'POST'))
def new_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(user=g.user._get_current_object(),
                            title=form.title.data,
                            timestamp=form.timestamp.data,
                            time_spent=form.time_spent.data,
                            content=form.content.data.strip(),
                            resources=form.resources.data.strip())
        flash("Entry created! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/edit_entry/<slug>', methods=('GET', 'POST'))
def edit_entry(slug):
    form = forms.EditEntryForm()
    if form.validate_on_submit():
        models.Entry.update(
            title=form.title.data,
            slug=slugify(form.title.data),
            timestamp=form.timestamp.data,
            time_spent=form.time_spent.data,
            content=form.content.data,
            resources=form.resources.data)
        flash("Entry edited!", 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)


@app.route('/details/<slug>')
def details(slug):
    try:
        entry = models.Entry.get(models.Entry.slug == slug)
    except models.DoesNotExist:
        abort(404)
    return render_template('details.html', entry=entry)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)