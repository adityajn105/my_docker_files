python configure_notebook.py
PASSWORD=$PASSWORD ./code-server/code-server --host 0.0.0.0 --port 5000&
jupyter notebook --allow-root --ip=0.0.0.0