from flask import (
    render_template, url_for, request,
    flash,
    jsonify,
    send_file,
    redirect,
)
from UserResearch import app
import UserResearch.blueprints

from UserResearch.util import (
    accounts_forbidden,
)

"""
ROUTING
"""

# @app.route('/', methods=['GET','POST'])
# @accounts_forbidden([1, 2])
# def index(forms, dbvalues):
#     if request.method == 'GET':
#         form_from_db_fields(dbvalues['current_notes'], forms['note_form'])
#     elif bulk_validate(forms): # pragma: no branch
#         forms['note_form'].populate_obj(dbvalues['current_notes'])
#         try:
#             db.session.commit()
#             flash("Updated Note has been saved", "success")
#         except Exception as e: # pragma: no cover
#             flash("not saved", "danger")
#     patient_times = patient_time_calculate(dbvalues['time_to_mtf'])
#     return render_template(
#         'home.html',
#         title='Home',
#         **forms,
#         mtf_statuses=dbvalues['mtf_statuses'],
#         asset_statuses=dbvalues['asset_statuses'],
#         time_to_mtf=patient_times,
#     )

@app.route('/download')
@accounts_forbidden([1])
def download():
    import zipfile
    import io
    mem_file = io.BytesIO()
    with zipfile.ZipFile(mem_file, 'w') as zf:
        for table in TABLES_TO_SAVE:
            filename = table.__name__ + '.csv'
            file = io.StringIO()
            table_to_csv_file(table, file)
            zf.writestr(filename, file.getvalue())
    mem_file.seek(0)
    return send_file(
        mem_file,
        attachment_filename='RAPID-data.zip',
        as_attachment=True,
    )

@app.route('/upload', methods=['GET','POST'])
@accounts_forbidden([1, 2])
def upload(forms):
    import io
    if request.method == 'GET':
        pass
    elif bulk_validate(forms): # pragma: no branch
        f = forms['upload_form'].file.data
        filename = f.filename
        table = TABLE_DICT.get(filename, False)
        if table:
            f = io.StringIO(f.read().decode('utf-8'))
            csv_file_to_table(table, f)
            flash(f'Imported data from "{filename}"', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Unknown table "{filename}"', 'danger')
    return render_template(
        'upload.html',
        title='Upload CSV data',
        **forms,
    )

"""Must be done after adding routes to bp"""
app.register_blueprint(UserResearch.blueprints.users)
app.register_blueprint(UserResearch.blueprints.posts)
app.register_blueprint(UserResearch.blueprints.main)
app.register_blueprint(UserResearch.blueprints.errors)
app.register_blueprint(UserResearch.blueprints.projects)
app.register_blueprint(UserResearch.blueprints.personas)
app.register_blueprint(UserResearch.blueprints.stories)
