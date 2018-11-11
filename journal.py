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
    entries = models.Entry.select()
    return render_template('index.html', entries=entries)


@app.route('/new_entry', methods=('GET', 'POST'))
def new_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(title=form.title.data,
                            timestamp=form.timestamp.data,
                            time_spent=form.time_spent.data,
                            content=form.content.data.strip(),
                            resources=form.resources.data.strip())
        flash("Entry created! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)



@app.route('/edit_entry/<title>', methods=('GET', 'POST'))
def edit_entry(title):
    try:
        entry = models.Entry.get(models.Entry.title==title)
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.EditEntryForm(obj=entry)
        if form.validate_on_submit():
            models.Entry.update(
                title = form.title.data,
                timestamp = form.timestamp.data,
                time_spent = form.time_spent.data,
                content = form.content.data.strip(),
                resources = form.resources.data.strip()
            ).where(models.Entry.slug == entry.slug).execute()
            flash("Entry updated!", "success")
            return redirect(url_for('index'))
        return render_template('edit.html', form=form, entry=entry)


@app.route('/details/<title>')
def details(title):
    try:
        entry = models.Entry.get(models.Entry.title == title)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/delete/<title>')
def delete(title):
    try:
        entry = models.Entry.get(models.Entry.title == title)
    except models.DoesNotExist:
        abort(404)
    else:
        entry.delete_instance()
        flash("Entry deleted!", "success")
        return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)