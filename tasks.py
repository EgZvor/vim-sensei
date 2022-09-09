from invoke import task

@task
def ipynb_to_py(c):
    c.run("python ipynb-to-py.py sensei.ipynb sensei.py")
