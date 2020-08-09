import numpy as np
import pandas as pd
from recommendation import recommend
from flask import Flask, request, render_template, redirect, url_for

app = flask.Flask(__name__,template_folder='templates')

@app.route('/')
def root():
	return render_template("index.html")

@app.route("/", methods = ["GET", "POST"])
def get_movie():
	if request.method == "POST":
		default_name = "0"

		movie_name = request.form.get("movie", default_name)

		num_recommends = 10
		out_df = recommendation.recommend(movie_name, num_recommends)

		return render_template("out.html", name = "Recommended Movies", data = out_df.to_html())
