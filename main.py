import json
import os
import random
import shutil

from fileinput import filename

from werkzeug.utils import secure_filename
from flask import *
from flask import Flask

from logic import *

import webbrowser


from cryptographer import Cryptographer


app = Flask(__name__, template_folder="templates")


"""
template of user data {"fname": "", "lname": "", "role": ""}
"""

# Global variables for interactive between functions
# Be good if rewrite this in OOP-style
editor = None
user = None
solution = None

UPLOAD_FOLDER = os.path.join('tasks')
ALLOWED_EXTENSIONS = ["json"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


cryptographer = Cryptographer(b'pbBf8hbN2YybfvP_ieCQmZf7ZDdg9934mY7bA_b4rUM=')


@app.route('/insolve/', methods=['GET', 'POST'])
def front_page():
    shutil.rmtree("files")
    shutil.rmtree("tasks")
    os.mkdir("files")
    os.mkdir("tasks")
    jsn = None
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = f.read()
        # print(f"data {data}")
        jsn = json.loads(data)
    if jsn["role"] == "" or jsn["fname"] == "" or jsn["lname"] == "":
        return redirect("/insolve/regiester/")
    else:
        global user
        user = str(User(jsn["role"], jsn["fname"], jsn["lname"]))
        role = json.loads(data)["role"]
        if role == "student":
            return redirect("/solver/")
        elif role == "teacher":
            return redirect("/editor/")
        else:
            return redirect("/insolve/regiester/")


@app.route('/insolve/regiester/')
def regiester():
    return render_template("regiester.html")


@app.route('/insolve/regiester/done/', methods=['GET', 'POST'])
def regiester_done():
    role = request.form["role"].strip()
    fname = request.form["fname"].strip()
    lname = request.form["lname"].strip()
    if role == "" or fname == "" or lname == "":
        return redirect("/insolve/regiester/")
    else:
        with open("data/data.json", "w", encoding='utf-8') as f:
            json.dump(User(role, fname, lname).__dict__, f, ensure_ascii=False)
            f.close()
        return redirect("/insolve/")


@app.route('/editor/', methods=['GET', 'POST'])
def start_editor():
    global user
    code = """
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
    return render_template("editor.html", user=user, action=code)


@app.route('/editor/edit/', methods=['GET', 'POST'])
def editor_main():
    global editor, user

    if not editor:
        name = request.form["name"]
        editor = Editor(name)
        print("editor has created")
    else:
        print("editor is already exists")
        try:
            editor.tokens["title"] = request.form["name"]
        except:
            pass
    return render_template("editor_edit.html", user=user, action=editor.tokens.get("title"),
                           tasks=editor.tokens["tasks"])


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


@app.route('/editor/edit/finish/', methods=['GET', 'POST'])
def finish():
    global editor, user
    with open(f"files/{editor.tokens['title']}.json", "wb") as f:
        jsn = cryptographer.encrypt(json.dumps(editor.tokens))
        f.write((jsn))
    fl = f"files/{editor.tokens['title']}.json"
    return render_template("finish.html", user=user)


@app.route("/editor/edit/finish/download/", methods=['GET', 'POST'])
def download():
    return send_file(f"files/{editor.tokens['title']}.json", as_attachment=True)


@app.route("/checking/", methods=['GET', 'POST'])
def checking():
    global user
    code = '''<div class="task_widget" style="font-family: 'Roboto', sans-serif;">
        <br>
        <form action="/checking/view_solution/" enctype="multipart/form-data" method="post">
            <p1>Выберите файл с решением,</p1>
            <p2>чтоб приступить к проверке</p2>
            <br>
            <input type="file" name="file">
            <br>
            <br>
            <input type="submit" value="Начать проверку">
            <br>
        </form>
        <br>
    </div>'''
    return render_template("checking.html", user=user, code=code)


@app.route("/checking/view_solution/", methods=['GET', 'POST'])
def checking_view():
    global user
    code = ""
    if request.method == 'POST':
        file = request.files.get("file")
        if file:
            try:
                flname = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], flname))
                solution = open(f"tasks/{flname}", "r")
                solution_value = json.loads(cryptographer.decrypt(solution.read()))
                code = ""
                code += f"""<br><div><label>{solution_value["title"]}</label></div>"""
                code += f"""<br><div><label>{solution_value["name"]}</label></div>"""
                code += f"""<br><div><label>Процент правильных решений: {solution_value["right_percent"]}</label></div>"""
                for solution_ in solution_value['solutions']:
                    code += """<br><div class="task_widget"><br>"""
                    code += f"""<label style="border-radius: 5px">Текст задания: {solution_["text"]}
                    </label><br>"""
                    if solution_["solution"] != "none":
                        code += f"""<label style="border-radius: 5px">Решение учечащегося: {solution_["solution"]}
                        </label><br>"""
                    code += f"""<label style="border-radius: 5px">Ответ учащегося: {solution_["answer"]}
                    </label><br><br></div>"""
                solution.close()
            except:
                return redirect("/checking/view_solution/")
        return render_template("checking.html", user=user, code=code)


@app.route('/overload/')
def overload():
    global editor, solution
    editor.remove_json()
    editor = None
    solution = None
    return redirect("/insolve/")


@app.route("/solver/", methods=['GET', 'POST'])
def solver():
    global user
    return render_template("solver_start.html", user=user)


@app.route("/solver/task/", methods=['GET', 'POST'])
def solver_task():
    global user, solution
    code = ""
    if request.method == 'POST':
        file = request.files.get("file")
        if file:
            try:
                flname = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], flname))
                with open(f"tasks/{flname}", "rb") as task:
                    text = cryptographer.decrypt(task.read())
                    data = json.loads(text)
                    for number, task in enumerate(data["tasks"]):
                        code += """<br>"""
                        code += """<div class="task_widget">"""
                        code += f"""<br><div><label>Задача {number+1}. {task["text"]}</label></div>"""
                        if task["solution"] == "true":
                            solution_name = "solution-"+str(number+1)
                            code += f"""<div>Ваше решение: <textarea name="{solution_name}" style="min-height:100px;
                            min-width:550px"></textarea></div>"""
                        answer_name = "answer-"+str(number+1)
                        code += f"""<div>Ответ: <input name="{answer_name}"></div>"""
                        code += "<br></div>"
                    solution = Solution()
                    solution.data = data
                os.remove(f"tasks/{flname}")
            except:
                return redirect("/solver/task/")
            return render_template("solver_task.html", content=code, user=user, title=data["title"])
        else:
            return redirect("/solver/")


@app.route("/solver/task/done/", methods=["GET", "POST"])
def solver_done():
    global solution, user
    right_answers = []
    total_answers = []
    solution.set_title(solution.data["title"])
    for idx, element in enumerate(solution.data["tasks"]):
        text = element["text"]
        if element["solution"] == "true":
            solution_ = request.form[f"solution-{idx+1}"]
        else:
            solution_ = "none"
        answer = request.form[f"answer-{idx+1}"]
        solution.add_new_solution(text, solution_, answer)
        if solution.data["tasks"][idx]["answer"] == answer:
            total_answers.append(answer)
            right_answers.append(answer)
        else:
            total_answers.append(answer)
    right_percent = f"{round(len(right_answers)/len(total_answers)*100)}"
    solution.set_result(right_percent)
    solution.set_name(user)
    base = SolutionsBase()
    elo = Elo(len(total_answers), int(right_percent)).__repr__()
    base.add_solution(solution.tokens["title"], int(elo))
    print("добавление в main отработало")
    return render_template("solver_done.html", user=user, percent=right_percent)


@app.route("/solver/task/download/", methods=["GET", "POST"])
def solution_download():
    global solution
    jsn = json.dumps(solution.tokens)

    name = f"{random.randint(1, 10**10)}.json"
    with open(f"files/{name}", "wb") as f:
        f.write(cryptographer.encrypt(jsn))
    solution = None
    return send_file(f"files/{name}", as_attachment=True)


@app.route("/stats/")
def profile_view():
    global user
    rank = Statistic().rank
    common_elo = Statistic().elo
    try:
        base = SolutionsBase().__repr__()
        return render_template("stats.html", user=user, rank=rank, common_elo=common_elo, base=base)
    except:
        return render_template("stats.html", user=user, rank=rank, common_elo=common_elo)


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/insolve/")
    app.run(host='0.0.0.0', debug=True)

