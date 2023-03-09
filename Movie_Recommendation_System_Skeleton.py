import requests
import json
import pandas as pd


url = "https://api.themoviedb.org/3/movie/popular?api_key=YOUR_API_KEY&language=en-US&page=1"
response = requests.get(url)
data = json.loads(response.text)


movies_df = pd.DataFrame(data['results'])



import matplotlib.pyplot as plt
import seaborn as sns



from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
