import pandas as pd
import altair as alt

# Data prep
df = pd.read_csv("country_economics_data.csv")
df.rename(columns={
    'GDP': 'GDP (Billions USD)',
    'GDP Growth': 'GDP Growth (%)',
    'Interest Rate': 'Interest Rate (%)',
    'Debt/GDP': 'Debt to GDP Ratio (%)',
    'Jobless Rate': 'Unemployment Rate (%)'
}, inplace=True)

df_viz = df[['Name', 'Region', 'GDP (Billions USD)', 'GDP Growth (%)',
             'Interest Rate (%)', 'Debt to GDP Ratio (%)', 'Unemployment Rate (%)']].copy()

metrics_for_pcp = ['GDP Growth (%)', 'Interest Rate (%)', 'Debt to GDP Ratio (%)']
df_clean_pcp = df_viz.dropna(subset=metrics_for_pcp)

df_long = df_clean_pcp.melt(
    id_vars=['Name', 'Region'],
    value_vars=metrics_for_pcp,
    var_name='Metric',
    value_name='Value'
)

selector_country = alt.selection_point(
    fields=['Name'],
    empty='none',
    name='CountrySelect'
)

selector_region = alt.selection_interval(
    encodings=['x'],
    name='RegionFilter'
)

region_color_scale = alt.Scale(scheme='tableau10')
highlight_color = '#007bff'  # bright blue


# View 1: Top 20 GDP ranking
top_20_df = df_viz.nlargest(20, 'GDP (Billions USD)')

ranking_chart = alt.Chart(top_20_df).mark_bar().encode(
    y=alt.Y('Name:N', sort='-x', title='Country (Top 20 GDP)'),
    x=alt.X('GDP (Billions USD):Q', title='GDP (Billion USD)'),

    color=alt.condition(
        selector_country,
        alt.value(highlight_color),
        alt.Color('Region:N', scale=region_color_scale, title='Region')
    ),
    opacity=alt.condition(
        selector_country,
        alt.value(1.0),
        alt.value(0.25)
    ),

    tooltip=[
        alt.Tooltip('Name:N'),
        alt.Tooltip('Region:N'),
        alt.Tooltip('GDP (Billions USD):Q', format='$,.0f')
    ]
).properties(
    title='View 1: Top 20 Global Economies (GDP Ranking)',
    width=350,
    height=350
).add_params(
    selector_country
).transform_filter(
    selector_region
)

# View 2: Avg unemployment by region
df_clean_unemp = df_viz.dropna(subset=['Unemployment Rate (%)'])

bar_chart = alt.Chart(df_clean_unemp).mark_bar().encode(
    x=alt.X('Region:N', title='Region', axis=alt.Axis(labelAngle=-45, titleY=30)),
    y=alt.Y('mean(Unemployment Rate (%)):Q', title='Avg. Unemployment Rate (%)'),
    color=alt.Color('Region:N', scale=region_color_scale, legend=alt.Legend(title='Region')),
    opacity=alt.condition(selector_region, alt.value(0.9), alt.value(0.3)),
    tooltip=[
        alt.Tooltip('Region:N'),
        alt.Tooltip('mean(Unemployment Rate (%)):Q', format='.2f', title='Avg. Rate')
    ]
).properties(
    title='View 2: Avg. Unemployment by Region',
    width=350,
    height=350
).add_params(
    selector_region
)


# View 3: Parallel Coordinates Plot
pcp_lines = alt.Chart(df_long).mark_line().encode(
    x=alt.X('Metric:N', axis=alt.Axis(title='Economic Metric', labelAngle=0)),
    y=alt.Y('Value:Q', title='Standardized Metric Value'),
    detail='Name:N',

    color=alt.condition(
        selector_country,
        alt.value(highlight_color),
        alt.Color('Region:N', scale=region_color_scale, legend=alt.Legend(title='Region'))
    ),
    opacity=alt.condition(
        selector_country,
        alt.value(1.0),   
        alt.value(0.25)   
    ),
    size=alt.condition(
        selector_country,
        alt.value(3.5),   
        alt.value(0.8)    
    ),

    tooltip=['Name:N', 'Metric:N', alt.Tooltip('Value:Q', format='.2f')]
).transform_filter(
    selector_region
)

pcp_points = alt.Chart(df_long).mark_point(
    filled=True,
    size=80
).encode(
    x='Metric:N',
    y='Value:Q',
    detail='Name:N',
    color=alt.value(highlight_color),
    tooltip=['Name:N', 'Metric:N', alt.Tooltip('Value:Q', format='.2f')],
    opacity=alt.condition(
        "!length(data('CountrySelect_store'))",
        alt.value(0),   
        alt.value(1)    
    )
).transform_filter(
    selector_region & selector_country
)

pcp = (pcp_lines + pcp_points).properties(
    title='View 3: Comparison Across Multiple Attributes (Parallel Coordinates Plot)',
    height=400,
    width=910
).add_params(
    selector_country
)


# View 4: Summary Card
base_summary = alt.Chart(df_viz).transform_filter(selector_country).properties(
    title='View 4: Selected Country Key Metrics',
    width=280,
    height=350
)

country_box = base_summary.transform_aggregate(
    count='count()'
).mark_rect(
    stroke='lightgray', strokeWidth=1, fill='white'
).encode(
    x=alt.value(10), x2=alt.value(270),
    y=alt.value(40), y2=alt.value(90)
)

growth_box = base_summary.transform_aggregate(
    count='count()'
).mark_rect(
    stroke='lightgray', strokeWidth=1, fill='white'
).encode(
    x=alt.value(10), x2=alt.value(270),
    y=alt.value(100), y2=alt.value(150)
)

debt_box = base_summary.transform_aggregate(
    count='count()'
).mark_rect(
    stroke='lightgray', strokeWidth=1, fill='white'
).encode(
    x=alt.value(10), x2=alt.value(270),
    y=alt.value(160), y2=alt.value(210)
)

country_label = base_summary.mark_text(
    fontSize=11, color='gray', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(55),
    text=alt.value('COUNTRY NAME')
)

growth_label = base_summary.mark_text(
    fontSize=11, color='gray', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(115),
    text=alt.value('GDP GROWTH RATE')
)

debt_label = base_summary.mark_text(
    fontSize=11, color='gray', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(175),
    text=alt.value('DEBT / GDP RATIO')
)

name_text = base_summary.mark_text(
    fontSize=16, fontWeight='bold', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(80),
    text='Name:N'
)

growth_value = base_summary.mark_text(
    fontSize=22, color='darkgreen', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(140),
    text=alt.Text('GDP Growth (%):Q', format="+.1f")
)

growth_unit = base_summary.mark_text(
    fontSize=16, color='darkgreen', align='left'
).encode(
    x=alt.value(90),
    y=alt.value(140),
    text=alt.value('%')
)

debt_value = base_summary.mark_text(
    fontSize=22, color='darkred', align='left'
).encode(
    x=alt.value(20),
    y=alt.value(200),
    text=alt.Text('Debt to GDP Ratio (%):Q', format=".1f")
)

debt_unit = base_summary.mark_text(
    fontSize=16, color='darkred', align='left'
).encode(
    x=alt.value(95),
    y=alt.value(200),
    text=alt.value('%')
)

prompt_text = alt.Chart(
    pd.DataFrame({'text': ['Select a Country for Detail']})
).mark_text(
    color='gray',
    fontSize=18,
    fontStyle='italic'
).encode(
    text='text:N',
    opacity=alt.condition(
        "!length(data('CountrySelect_store'))",
        alt.value(1),
        alt.value(0)
    )
).properties(width=280, height=350)

active_summary_layers = (
    country_box + growth_box + debt_box +
    country_label + growth_label + debt_label +
    name_text + growth_value + growth_unit +
    debt_value + debt_unit
)

summary_card = (prompt_text + active_summary_layers).properties(
    title='View 4: Selected Country Key Metrics',
    width=280,
    height=350
)

# Combine views into dashboard
top_row = ranking_chart | bar_chart | summary_card

final_dashboard = (top_row & pcp).properties(
    title='Global Economic Country Data for the General Public - 4 Coordinated Views'
).configure_title(
    fontSize=20,
    anchor='start'
)

final_dashboard.save('final_dashboard.html')
