from django.shortcuts import render
from myapp.plot import (
    hist,
    bar,
    line,
    line_5y,
    line_10y,
    density,
    choloropeth1,
    choloropeth2,
    choloropeth3,
    index_map,
)
import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup
import random

rank_df = pd.read_csv("static/data/flood_rank.csv")


def index(request):
    context = {}
    data_table = rank_df[
        ["loc", "Average Severity Level", "Total Human Fatalities", "Rank"]
    ].head(3)
    # make a list of lists
    fig1 = index_map()
    chart1 = fig1.to_html()
    context["map"] = chart1
    data_table = data_table.values.tolist()
    context["data_table"] = data_table

    return render(request, "index2.html", context)


def flood_data(request):
    context = {}
    data = pd.read_csv("static/data/final.csv")
    data = data.drop(["Unnamed: 0"], axis=1)
    geojson = gpd.read_file(
        "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    )
    st = data["loc"].unique()
    context["st"] = st
    center = dict(lat=20.5937, lon=78.9629)
    zoom = 3

    if request.method == "POST":
        choice = request.POST.get("choice")
        if choice != "India":
            geojson = geojson[geojson["ST_NM"] == choice].reset_index(drop=True)
            data = data[data["loc"] == choice].reset_index(drop=True)
            centroid = geojson["geometry"][0].centroid
            center = dict(lat=centroid.y, lon=centroid.x)
            zoom = 4
            flood_relief_num = random.randint(9800000000, 9999999999)
            flood_relief_name = f"{choice} Floor Relief Center"
            context["flood_relief_num"] = flood_relief_num
            context["flood_relief_name"] = flood_relief_name
            context["per"] = (
                rank_df[rank_df["loc"] == choice]["Historical Flooding Probability (%)"]
                .values[0]
                .round(2)
            )
            input_str = choice.lower()
            input_str = input_str.replace(" ", "-")
            URL = f"https://www.timeanddate.com/weather/india/{input_str}"
            headers = {"user-agent": "Mozilla/5.0"}
            p1 = requests.get(URL)
            soup = BeautifulSoup(p1.content, "html5lib")
            soup1 = soup.find("div", class_="bk-focus__qlook")
            soup2 = soup1.findAll("p")
            soup3 = soup.find("img", id="cur-weather")
            img = soup3["src"]
            arr = []
            for i in range(len(soup2)):
                if i == 2:
                    string = soup2[i].text
                    string = string.replace("Feels Like:", "\nFeels Like:")
                    string = string.replace("Forecast:", "\nForecast:")
                    string = string.replace("Wind:", "\nWind:")
                    arr.append(string)
                else:
                    arr.append(soup2[i].text)
            arr.append(img)
            forecast = arr[2].split("\n")[1:4]
            forecast = [f.replace("\xa0", " ") for f in forecast]
            context["img"] = img
            # Update the list with the extracted information
            arr[2] = forecast[0]
            arr[3] = forecast[1]
            arr.append(forecast[2])
            arr.pop()
            arr[0] = input_str
            context["temp"] = arr

        context["choice"] = choice
    ###################################
    den_w = density(data, center, zoom)
    dens_w = den_w.to_html()
    context["dens_w"] = dens_w
    ##################################
    cl1_w = choloropeth1(data.groupby("loc")["Severity"].mean().reset_index(), geojson)
    cl1_w = cl1_w.to_html()
    context["cl1_w"] = cl1_w
    #################################
    cl3_w_data = data.groupby("loc")["Human fatality"].sum().reset_index()
    cl3_w = choloropeth3(cl3_w_data, geojson)
    cl3_w = cl3_w.to_html()
    context["cl3_w"] = cl3_w
    ################################
    fig3 = line()
    chart3 = fig3.to_html()
    context["chart3"] = chart3
    fig_5y = line_5y()
    chart_5y = fig_5y.to_html()
    context["chart_5y"] = chart_5y
    fig_10y = line_10y()
    chart_10y = fig_10y.to_html()
    context["chart_10y"] = chart_10y
    #################################
    return render(request, "countrychoice.html", context)
