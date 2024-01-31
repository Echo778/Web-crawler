# Creator: QI NIU
# This file is to visualize the data from Zillow.com(Zillow.csv) in order to help people find a place to live.

from pyecharts import options as opts
from pyecharts.charts import Pie
import pandas as pd


df = pd.read_csv('Zillow.csv')
info = df['Type'].value_counts().index.to_list() 
num = df['Type'].value_counts().to_list()
c = (
    Pie()
    .add(
        "",
        [
            list(z)
            for z in zip(info, num)
        ],
        center=["40%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Distruibution of Apartment Type"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("Zillow-type.html")
)



avg_salary = df.groupby('Type')['Price'].mean()
CityType = avg_salary.index.tolist()
CityNum = [int(a) for a in avg_salary.values.tolist()]
from pyecharts.charts import Bar
c = (
    Bar()
    .add_xaxis(CityType)
    .add_yaxis("", CityNum)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Average Price In Different Apartment Type"),
        visualmap_opts=opts.VisualMapOpts(
            dimension=1,
            pos_right="5%",
            max_=30,
            is_inverse=True,
        ),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="min", name="Min price"),
                opts.MarkLineItem(type_="max", name="Max price"),
                opts.MarkLineItem(type_="average", name="Avearage price"),
            ]
        ),
    )
    .render("Zillow-price.html")
)