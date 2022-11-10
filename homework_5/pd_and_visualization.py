# importing the libraries needed for this task

import pandas as pd
import numpy as np
import re # i need it for the task 2
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


# task 1: create two functions for reading .gff and .bed formats

def read_gff(path_to_gff):
    """ function to read the .gff file """
    column_names=["chromosome","source","type","start","end","score","strand","phase","attributes"] # set the column names
    gff_data = pd.read_csv(path_to_gff, sep='\t', names=column_names) # read the file
    gff_data = gff_data[gff_data.chromosome.str.startswith("#") == False] # skip the commented lines
    gff_data = gff_data.astype({'start': 'int', 'end': 'int'}) # set the int type for start and end
    return gff_data.reset_index(drop=True) # reset index so that after commentaries skipping indexation will be ok


def read_bed6(path_to_bed6):
    """ function to read the .bed file """
    column_names = ["chromosome", "start", "end", "name", "score", "strand"] # set the column names
    bed_data = pd.read_csv(path_to_bed, sep = "\t", names=column_names) # read the file
    return bed_data


# test of the read_gff function from task 1

path_to_gff = "./rrna_annotation.gff"
gff_df = read_gff(path_to_gff)
gff_df

# test of the read_bed6 function from task 1

path_to_bed = "./alignment.bed" # in physical world my own path to bed is the best part of my day (just joking)
bed_df = read_bed6(path_to_bed)
bed_df

# task 2: shorten the information in the attributes column

pattern = r'.*=(.*)_.*' # regexp with the needed information in the first group
gff_df["attributes"] = gff_df["attributes"].apply(lambda x: re.sub(pattern, r'\1', x)) 

# task 3.1: for each chromosome count the number of each rRNAs types (table)

# I renamed the columns so that their names would correspond to the reference barplot
chromosome_rRNA_count = gff_df\
    .groupby(['chromosome', 'attributes'])\
    .agg({'attributes': 'count'})\
    .rename(columns={'attributes': 'Count'})\
    .reset_index()\
    .rename(columns={'chromosome': 'Sequence', 'attributes': 'RNA type'}) # that's the table for the plot
chromosome_rRNA_count

# task 3.2: for each chromosome count the number of each rRNAs types (barplot)

count_rRNA = sns.barplot(data=chromosome_rRNA_count, x="Sequence", y="Count", hue="RNA type")
sns.move_legend(count_rRNA, "upper right")
plt.xticks(rotation=90);

# task 4: create something like bedtools intersect

gff_for_intersect = gff_df\
    .rename(columns={
        'start': 'start_x', 
        'end': 'end_x'
        }) # renamed columns
bed_for_intersect = bed_df\
    .rename(columns={
        'start': 'start_y', 
        'end': 'end_y'
        }) # renamed columns

""" 
Now I want to merge two tebles; using usual merge parameters I will get a giant table with all possible combinations 
of contigs that share the same chromosome number. I will then use query to leave the contigs that are intersected only.
"""

gff_bed_intersect = gff_for_intersect\
    .merge(bed_for_intersect, left_on='chromosome', right_on='chromosome') # merged, now there are all combinations

gff_bed_intersect = gff_bed_intersect\
    .query('start_x > start_y and end_x < end_y') # selected only contigs that intersect with annotation

# let's have a look at the final table

gff_bed_intersect 

# task 5: volcano plot 
# part 1: preparing

diffexpr = pd.read_csv('diffexpr_data.tsv.gz', sep='\t') # first download the data

# then modify the data: i added two columns on significance and direction of change and then combined them together
diffexpr['sign_non_sign'] = diffexpr.apply(lambda x: 'Significantly' if x['pval_corr'] < 0.05 else 'Non-significantly', axis=1)
diffexpr['up_down'] = diffexpr.apply(lambda x: 'downregulated' if x['logFC'] < 0 else 'upregulated', axis=1)
diffexpr['sector'] = diffexpr['sign_non_sign'] + ' ' + diffexpr['up_down'] # here finally i get the column needed
diffexpr = diffexpr.sort_values(by=['sign_non_sign', 'up_down'], ascending=[False, True]) # sorted just to please my eyes

# now i have to get some values for plot tuning
# first one: i need the approximate log_pval value that corresponds to pval_corr=0.05 for a horizontal line
print(diffexpr[diffexpr['pval_corr'] > 0.05][diffexpr['pval_corr'] < 0.0508]) # finding log_pval for pval_corr = 0.05
# from this table i choose 1.297575

# secondly, to customize the x axis length i need the maximum and minimum values on the x scale
print(min(diffexpr['logFC'])) # minimum = -10.661092815248146
print(max(diffexpr['logFC'])) # maximum = 10.092524279930334
# okay then i will make the x axis from -11.5 to 11.5

# finally i really need to know top-2 significantly upregulated and significantly downregulated genes
top_genes = [] # in this list i will put the lists of dots coordinates and gene names
top_down = diffexpr.query('pval_corr < 0.05').sort_values(by='logFC').iloc[0:2] # top-2 downregulated genes
top_up = diffexpr.query('pval_corr < 0.05').sort_values(by='logFC', ascending=False).iloc[0:2] # top-2 upregulated genes
for i in range(2):
    top_genes.append([top_up.iloc[i].logFC, top_up.iloc[i].log_pval, top_up.iloc[i].Sample])
    top_genes.append([top_down.iloc[i].logFC, top_down.iloc[i].log_pval, top_down.iloc[i].Sample])

# task 5: volcano plot 
# part 2: action

plt.rcParams["figure.figsize"] = (8, 5) # figure size
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.bf'] = 'Verdana:italic:bold'

# the plot itself
res = sns.scatterplot(
    data=diffexpr, 
    x='logFC', 
    y='log_pval', 
    hue='sector', # for different colors
    s=4, # dot size
    linewidth=0 # no white dot lineage
    ) 

res.axhline(1.297575, c='grey', lw=1, ls='--') # horizontal line
res.axvline(0, c='grey', lw=1, ls='--') #vertical line
plt.text(8, 1.7, 'p value = 0.05', size=6, color='grey', weight='semibold') # label for p-value

plt.xlabel(r'$\bf{log_2}$(fold change)', size=10, weight='bold', style='italic') # label for x axis
plt.ylabel(r'-$\bf{log_{10}}$(p value corrected)', size=10, weight='bold', style='italic') # label for y axis

plt.title('Volcano plot', size=13, weight='bold', style='italic') # title
plt.tick_params(axis='both', which='major', labelsize=8) # ticks

res.xaxis.set_minor_locator(MultipleLocator(1)) # smaller ticks for x axis
res.yaxis.set_minor_locator(MultipleLocator(5)) # smaller ticks for y axis

plt.xlim([-11.5, 11.5]) # x axis scale

for axis in ['top','bottom','left','right']:
    res.spines[axis].set_linewidth(1) # a little more wide plot borders

l = res.legend(title=None, shadow=True, facecolor='white', fontsize=7, markerscale=0.75) # legend settings

for i in range(4):
    plt.text( # add gene name to the plot
        x=top_genes[i][0],
        y=top_genes[i][1] + 10, 
        s=top_genes[i][2], 
        size=5, 
        style='italic', 
        weight='bold'
        )
    plt.arrow( # add an arrow
        x=top_genes[i][0] + 0.4, 
        y=top_genes[i][1] + 8, 
        dx=-0.3, 
        dy=-6, 
        width=0.15, 
        fill=True, 
        edgecolor='black', 
        facecolor='red', 
        linewidth=0.3
        )
;
# plt.savefig('volcano_plot', bbox_inches='tight', dpi=800)


# task 6: Pie chart

from matplotlib.patches import ConnectionPatch
from matplotlib.collections import PatchCollection

# synthesis of data

names = []
for i in range(1, 17):
    names.append(f'Group_{i}')
names.append('Other')
masses = [8.5, 8.5, 3.8, 2.46, 6.26, 6.94, 8.95, 1.12, 6.94, 1.34, 2.46, 2.24, 3.13, 0.22, 3.36, 2.24, 31.54]
other = [27, 19, 8, 7, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
expl = [0.01] * 16
expl.append(0.05)

# some data and labels

pie_data = []
bar_data = []
labels = []
for i in range(len(names)):
    pie_data.append((names[i], masses[i]))
    labels.append(f'{names[i]}\n{masses[i]}%')
for i in range(len(other)):
    bar_data.append((other[i], other[i]))

# make the plot omg i don't understand why it works 
# one of its versions looked like spider and i got scared

# it is actually two plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 15), subplot_kw=dict(aspect="equal"), gridspec_kw={'width_ratios': [3, 1]})


palette_color = sns.color_palette()

# put others sector on its place
vals_sum = sum(masses)
others_prop = sum(other) / vals_sum # other to the right
start_angle = 45 * others_prop



# lines between the piechart and barplot omg i nearly died
con1 = ConnectionPatch(xyA=(0.55, -0.9),
                       xyB=(-4, -0),
                       coordsA=ax1.transData,
                       coordsB=ax2.transData,
                       axesA=ax2,
                       axesB=ax1,
                       color="black",
                       zorder=999)
con2 = ConnectionPatch(xyA=(0.7, 0.78),
                       xyB=(-4, 113),
                       coordsA=ax1.transData,
                       coordsB=ax2.transData,
                       axesA=ax2,
                       axesB=ax1,
                       color="black",
                       zorder=999)

ax2.add_artist(con1)
ax2.add_artist(con2)

wedges, texts, _ = ax1.pie(masses,
                           labels=None,
                           colors=palette_color,
                           explode=expl, 
                           startangle=start_angle, 
                           autopct='%.1f%%',
                           wedgeprops=dict(width=1),
                           labeldistance=None)

bbox_props = dict(boxstyle="square,pad=0.3", edgecolor="k", facecolor="white", lw=1) # labels in boxes settings
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props,
          zorder=1,
          va="center")

# labels around piechart
for i, p in enumerate(wedges):
    ang = ((p.theta2 - p.theta1) / 2) + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))

    connectionstyle = f"angle,angleA=0,angleB={ang}"
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    x_text_coord = 1.7 * np.sign(x)
    y_text_coord = 1.2 * y 

    ax1.annotate(labels[i],
                 xy=(x, y),
                 xytext=(x_text_coord, y_text_coord),
                 horizontalalignment="center",
                 **kw)

### horizontal barplot
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)

def font_size(shift):
    if shift > 0.01:
        return 12
    elif shift > 0.05:
        return 10
    else:
        return 8

# Create vertical barplot
# Actually, a sequence of barplots on top of each other
prev_sum = 0
for i in bar_data:
    val = i[0]
    ax2.bar(1, val, width=10, bottom=prev_sum, edgecolor="black")
    prev_sum += val
    shift = val / 2
    label_num = i[0]
    if shift > 1:
        fontsize = font_size(shift)
        ax2.annotate(label_num, xy=(1, prev_sum), xytext=(1.03, prev_sum - shift), horizontalalignment="left", fontsize=fontsize)

plt.show()

# task 7: covid data eda

covid = pd.read_csv("owid-covid-data.csv")

covid.head()

covid.info()

covid.describe()

print(covid.nunique())

covid.columns # very useful for query

covid.isnull().sum()

covid.dropna(subset='continent').isnull().sum()

covid_continents = covid\
    .groupby(['continent', 'date'])\
    .agg({'total_cases': 'sum', 'new_cases': 'sum'})\
    .reset_index()\
    .sort_values('date')
covid_continents

total_cases_plot = sns.lineplot(covid_continents.query('continent == "Europe" or continent == "Asia"'), x='date', y='new_cases', hue='continent', alpha=0.5)
plt.xticks(ticks=range(0, 1100, 100), rotation=90)
plt.ylabel('new cases per day')
plt.legend(loc='upper right')

total_cases_plot

# well okay why so little new cases between 10/13/2021 and 2/17/2021?
# new strain? lack of information? lack of tests?

sns.heatmap(covid.corr(), xticklabels=True, yticklabels=True)
plt.tick_params(axis='both', which='major', labelsize=3) # ticks

# plt.savefig('covid correlations', bbox_inches='tight', dpi=800)

covid_without_repeat = covid[[
       'location', 
       'total_cases_per_million',
       'new_cases_per_million', 
       'total_deaths_per_million', 
       'new_deaths_per_million',
       'reproduction_rate',
       'icu_patients_per_million',
       'hosp_patients_per_million', 
       'weekly_icu_admissions_per_million',
       'weekly_hosp_admissions_per_million',
       'total_tests_per_thousand', 'new_tests_per_thousand',
       'positive_rate', 'tests_per_case', 'tests_units', 
       'new_vaccinations', 
       'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
       'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
       'stringency_index',
       'population', 'population_density', 'median_age', 'aged_65_older',
       'aged_70_older', 'gdp_per_capita', 'extreme_poverty',
       'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
       'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
       'life_expectancy', 'human_development_index',
       'excess_mortality_cumulative_absolute', 'excess_mortality_cumulative',
       'excess_mortality', 'excess_mortality_cumulative_per_million']]

sns.heatmap(covid_without_repeat.corr(), xticklabels=True, yticklabels=True)
plt.tick_params(axis='both', which='major', labelsize=6) # ticks

# i want a carpet like this or a poncho maybe

sns.scatterplot(data=covid, x='extreme_poverty', y='life_expectancy', hue='continent')
# less poor is the country, more life expectancy? maybe, not so clear

smokers = covid.query('female_smokers > 0 and male_smokers > 0').sort_values('continent')

female_smok = sns.scatterplot(data=smokers, x='female_smokers', y='location', hue='continent')
female_smok.set(yticklabels=[]);
# mostly women smoke in Europe

male_smok = sns.scatterplot(data=smokers, x='male_smokers', y='location', hue='continent')
male_smok.set(yticklabels=[]);
# number of smoking men has bigger variety on all continents

smok = sns.scatterplot(data=smokers, x='female_smokers', y='male_smokers', hue='continent')
plt.plot([0, 50], [0, 50], 'k-', lw=2)

# we see that most countries with the almost same number of smoking men and women are in Europe
# is it because of feminism? 
# or is it just the number of stressed women and men the same?
# i don't have an answer to this question

sns.lineplot(data=covid\
    .query('location == "Germany" or location == "France" or location == "Italy"'), 
    x='total_vaccinations_per_hundred', 
    y='icu_patients_per_million', 
    hue='location')

# this is funny, from some point of vaccinated people the number of ICU patients rises
# perhaps because they think that they are invincible due to vaccination
# or because the rules became not so strict 

sns.heatmap(covid_without_repeat.query('location == "France"').corr(), xticklabels=True, yticklabels=True)
plt.tick_params(axis='both', which='major', labelsize=6) # ticks

sns.lineplot(data=covid\
    .query('location == "Germany" or location == "France" or location == "Italy"'), 
    y='total_vaccinations_per_hundred', 
    x='total_cases_per_million', 
    hue='location')

# wow! maybe the more cases the more people are motivated to vaccinate?