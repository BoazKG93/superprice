from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,  Title
from bokeh.models.glyphs import Segment
from bokeh.plotting import figure
from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
import numpy as np

from price import PriceCalculator
   

#output_file("bar_colormapped.html")
      
        
# Set up data
factor = ['stock', 'remaining days', 'demand']
values = [100, 3, 1]
max_values = [100, 10, 1]
normalized_values = [(x*1.0)/y for x, y in zip(values, max_values)]
cm = np.array(["#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"])
ix = [0, 1, 2]
colorsd = cm[ix]
#source = ColumnDataSource(data=dict(factor=factor, normalized_values=normalized_values))
source = ColumnDataSource(dict(
        x=[0.5, 1.5, 2.5],
        y=[0, 0, 0],
        xm01=[0.5, 1.5, 2.5],
        ym01=normalized_values,
        colors=["#C7E9B4", "#7FCDBB", "#41B6C4"]
    )
)

p = figure(x_range=factor, plot_height=700, plot_width=800, toolbar_location=None)
r = Segment(x0='x', y0='y', x1='xm01', y1='ym01',  line_width=150,  line_color='colors')
p.add_glyph(source, r)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 2
p.title.text_font_size = "50px"
priceCalculator = PriceCalculator('apple')
priceCalculator.update_input(values[0], values[1],  values[2])
priceCalculator.calculate_discount()
priceCalculator.calculate_price()
p.title.text = "The resulting price is ${0:.2f}".format(priceCalculator.price)
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
p.legend.label_text_font_size = "15pt"
p.add_layout(Title(text="Normal price is $1.50.", text_font_size="50px"), 'above')

# Set up widgets
stock = Slider(title="stock", value=100.0, start=0, end=200, step=1)
remaining_days = Slider(title="remaining days", value=3, start=0, end=10, step=1)
demand = Slider(title="demand", value=1.0, start=0.5, end=1.5,  step=0.1)



# Set up layouts and add to document
inputs = widgetbox(stock, remaining_days, demand)

def update_data(attr, old, new):
    s = stock.value
    re = remaining_days.value
    d = demand.value
    values = [s, re, d]
    normalized_values = [(x*1.0)/y for x, y in zip(values, max_values)]
    source.data['ym01'] = normalized_values
    #p.segment(x0=[0.5, 1.5, 2.5],  x1=[0.5, 1.5, 2.5],  y0=[0, 0, 0],  y1=normalized_values,  line_width=100)
    priceCalculator.update_input(s, re, d)
    priceCalculator.calculate_discount()
    priceCalculator.calculate_price()
    r.update(y1='ym01')
    p.title.text = "The resulting price is ${0:.2f}".format(priceCalculator.price)
    
for w in [stock, remaining_days, demand]:
    w.on_change('value', update_data)

curdoc().add_root(row(inputs, p, width=800))
