from flask import *
from flask import Flask
import webbrowser
from logic import Editor
app = Flask(__name__, template_folder="templates")

editor = None


@app.route('/editor/', methods=['GET', 'POST'])
def start_editor():
    start_action = """
    <div>
    <br>
    <form action="/editor/edit/" method="post">
        <h>Введите название сборника</h>
        <input type="textarea" name="name"></input>
        <input type="submit" value="Подтвердить"></input>
        <br>
    </form>
    </div>
    """
    return render_template("editor.html", action=start_action, tasks="")


@app.route('/editor/edit/', methods=['GET', 'POST'])
def editor_main():
    global editor
    if not editor:
        name = request.form["name"]
        editor = Editor(name)
        print("editor has created")
    else:
        print("editor is already exists")
    code = f"""
    <div>
    <input type="text" value="{editor.tokens.get("title")}" style="width:300px;"></input>
    </div>
"""
    return render_template("editor_edit.html", action=code, tasks=editor.tokens["tasks"])


@app.route('/editor/edit/new_task/', methods=['GET', 'POST'])
def new_task():
    global editor
    try:
        editor.add_new_task(request.form["text_of"], request.form["answer_of"], request.form["need_solution"])
    finally:
        return redirect("/editor/edit/")


@app.route('/editor/remove/<number>', methods=['GET', 'POST'])
def remove_task(number):
    global editor
    editor.remove_task(int(number))
    return redirect("/editor/edit/")


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/editor/")
    app.run(host='0.0.0.0')