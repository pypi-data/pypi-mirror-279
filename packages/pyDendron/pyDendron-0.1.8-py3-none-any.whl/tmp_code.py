# crossdating hist
## Violin
import holoviews as hv
from holoviews import opts, dim
from pyDendron.dataname import *
hv.extension('bokeh')

data = crossdating.crossDating.concat_results(score=SCORE, threshold=None, max_rank=None)

violin = hv.Violin(data, kdims=[KEYCODE, KEYCODE_MASTER], vdims=[SCORE])
violin.opts(height=5000, width=500, invert_axes=True)

## Violin 2
import holoviews as hv
from holoviews import opts, dim
from pyDendron.dataname import *
from bokeh.palettes import turbo

hv.extension('bokeh')

data = crossdating.crossDating.concat_results(score=SCORE, threshold=None, max_rank=None)

keycodes = sorted(data[KEYCODE].unique().tolist())
colors = list(turbo(len(keycodes)))

lst = []
for keycode, df in data.groupby(KEYCODE):
    violin = hv.Violin(df, [KEYCODE_MASTER], SCORE, group='_violin')
    ddf = df[df[DATED] == True]
    point = hv.Scatter(ddf, [KEYCODE_MASTER], SCORE , group='_point')
    texts = [hv.Text(y, x, str(round(val,2)), group='Score') for x, y, val in zip(ddf[SCORE], ddf[KEYCODE_MASTER], ddf[SCORE])]
    scatter_text = point * hv.Overlay(texts)
    vp = violin * scatter_text
    vp.opts(invert_axes=True)
    lst.append(vp)
g = hv.Layout(lst).cols(1)
g.opts(
    opts.Violin('_violin', height=500, width=800,  outline_alpha=0),
    opts.Scatter('_point', size=10, color='red'),
    
)
#print(hv.help(hv.Text))

g

# SeanBorn
## Violin
import seaborn as sns

data = crossdating.crossDating.concat_results(score=SCORE, threshold=None, max_rank=None)
for keycode, df in data.groupby(KEYCODE):
    sns.catplot(
        data=df, row=KEYCODE, x=SCORE,  col=KEYCODE_MASTER, kind='violin') #split=True, palette="pastel")

# cat
import seaborn as sns

data = crossdating.crossDating.concat_results(score=SCORE, threshold=None, max_rank=None)

sns.catplot(data, row=KEYCODE, x=SCORE,  col=KEYCODE_MASTER, kind='violin') #'strip', 'swarm', 'box', 'boxen', 'violin', 'bar', 'count', 'point'

# Full wiyh annotation
import seaborn as sns
data = crossdating.crossDating.concat_results(score=SCORE, threshold=None, max_rank=None)
import matplotlib

def myplot(score, dated, date, rank, **kwargs):
    ax = sns.kdeplot(x=score, fill=True, linewidth=0, bw_adjust=.25)
    if dated.sum() > 0:
        id = dated.idxmax()
        (id, dated[id], score[id], date[id])
        x = score[id]
        date = date[id]
        r = rank[id]
        ax.axvline(x=x, color='r')
        ylim = ax.get_ylim()
        y = (ylim[1] - ylim[0]) / 2

        ax.annotate(f'Year: {date}\n{SCORE}: {round(x, 2)}\n{RANK}: {r}', 
                    xy=(x, y), xycoords='data',
                    xytext=(0.05, .75), textcoords='axes fraction',
                    fontsize=10, color='r')


g = sns.FacetGrid(data, row=KEYCODE, col=KEYCODE_MASTER, margin_keycodes=True, height=2, aspect=2, dropna=True)
g.map(myplot, SCORE, DATED, DATE_END_ESTIMATED, RANK)
g.figure.subplots_adjust(wspace=0.1, hspace=0.1)


from pyDendron.dataname import *
score = T_SCORE
#print(score)
self = crossdating.crossDating
from scipy.stats import gaussian_kde
import colorcet as cc
from bokeh.plotting import figure
from bokeh.models import RangeTool, ColumnDataSource, ColorBar, LinearColorMapper, CategoricalColorMapper, Legend, LegendItem
from bokeh.core.enums import LegendLocation
from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import brewer, d3
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show


data = self.concat_results(score=score, threshold=None, max_rank=None)
if len(data) == 0:
    raise ValueError(f'The results matrix is empty after applying the threshold and max_rank.')
a = self.param_hist.aspect
h = self.param_hist.height*100
idxs = data[IDX].unique().tolist()
master_idxs = data[IDX_MASTER].unique().tolist()

gdata = data.groupby([IDX, IDX_MASTER])

smin, smax = data[score].min() , data[score].max() 
d = (smax - smin) *.02
smin, smax = smin - d, smax + d
n = round((smax - smin) * 100)
x = np.linspace(smin, smax, n)
pdf = gaussian_kde(data[score])
y_min, y_max = 0, np.max(pdf(x))*1.1
rows = []
for j, master_idx in enumerate(master_idxs):
    row = []
    for i, idx in enumerate(idxs):
        if (idx, master_idx) in gdata.groups:
            grp = gdata.get_group((idx, master_idx))
            keycode = f'(Master) {grp.loc[grp[IDX_MASTER] == master_idx, KEYCODE_MASTER].max()} / {grp.loc[grp[IDX] == idx, KEYCODE].max()} '
            p = figure(title=keycode, width=h*a, height=h, tools='', y_range=(y_min, y_max)) #x_axis_location='above',
            p.xaxis.ticker = [0]
            p.xaxis[0].formatter = PrintfTickFormatter(format="%5.2f")
            pdf = gaussian_kde(grp[score])
            y = pdf(x)
            p.patch(x, y, color=cc.rainbow[j*15], alpha=0.3, line_color="black")
            
            ey = grp.loc[grp[DATED] == True, DATE_END_ESTIMATED].max()
            dx = grp.loc[grp[DATED] == True, score].max()
            if not np.isnan(dx):
                s = p.scatter([dx], [pdf(dx)[0]], color='red', size=2*a, legend_label=f'date: {ey}')
                p.line([dx, dx], [0, pdf(dx)[0]], color='red')
                p.legend.label_text_font_size = f'{4*a}pt'
                p.legend.label_height = round(y_max*0.05)
                p.legend.location = "top_right"
                p.legend.padding = 1
                p.legend.margin = 1
                p.legend.glyph_width = 4*a
                p.legend.glyph_height = 4*a
                p.legend.background_fill_alpha = 0.5
                p.xaxis.ticker = [dx]
                        
            p.xaxis.visible = True
            p.yaxis.visible = False
            p.keycode.text_font_size = f'{3*a}pt'
            p.xaxis.axis_label_text_font_size = f'{2*a}pt'
            p.yaxis.axis_label_text_font_size = f'{2*a}pt'
            p.ygrid.grid_line_color = None
            row.append(p)
    #row.reverse()
    rows.append(row)

grid = gridplot(rows)
show(grid)
            
