from flask import Flask, redirect, url_for, request, send_from_directory, render_template
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sb
from time import gmtime, strftime

app = Flask(__name__)


@app.route('/buscar', methods=['POST', 'GET'])
def fechas():
    if request.method == 'POST':
        eds = request.form['eds']
        fec1 = request.form['fecini']
        fec2 = request.form['fecfin']
        if len(eds) == 0 or len(fec1) == 0 or len(fec2) == 0:
            return "Debe ingresar estacion, fecha inicial y fecha final"
        tms = strftime("%Y%m%d%H%M%S", gmtime())
        ruta_fig = "img/{}.png".format(tms)
        sql(eds, fec1, fec2, ruta_fig)
        return render_template("imagen.html", archivo="{}.png".format(tms))
    return render_template("form.html")


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory("img", filename)


def sql(eds, fec1, fec2, ruta_fig):
    engine = create_engine("mysql+mysqldb://root:your_secret_password@127.0.0.1:3306/cg")
    que = "SELECT fecha, combustible, SUM(cantidad) AS galones FROM cg_corte WHERE estacion={} AND fecha BETWEEN '{}' AND '{}' GROUP BY 1,2".format(eds,fec1,fec2)
    df = pd.read_sql_query(que, engine)
    x = df['fecha'].unique()
    plt.figure(figsize=(12,8))
    ax = sb.barplot(x='fecha', y='galones', hue='combustible', data=df)
    ax.set_xlabel(xlabel='Fecha', fontsize=16)
    ax.set_xticklabels(labels=x, fontsize=6, rotation=90)
    ax.set_ylabel(ylabel='Galones', fontsize=16)
    ax.set_title(label='Venta de combustible por dia', fontsize=20)
    plt.savefig(ruta_fig)
    plt.clf()


if __name__ == '__main__':
    app.run("0.0.0.0", "5000", debug=True)
