#Author: Raúl Santiago Castellanos Guzmán 

#importing packages 
import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

#importing functions from other files 
from happy_app.analysis.hhs_visits import plot_hhs_visits
from happy_app.analysis.covid_cases import plot_covid_cases
from happy_app.analysis.social_referrals import get_social_referral_frequency
from happy_app.analysis.domain_visits import plot_domain_visits
from happy_app.analysis.traffic_sources import plot_traffic_sources
from happy_app.analysis.domain_visits import plot_domain_visits
from happy_app.analysis.cdc_visits import plot_cdc_visits


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
"""
Creates a Dash application and adds it to a Flask server.
"""
def generate_title_container(title_text, subtitle_text, scrolldown_text):
    """
    This function generates a container containing a title and subtitle.

    Inputs: 
    - title_text: (str)
        The text to be used for the main title.
    - subtitle_text: (str)
        The text to be used for the subtitle.

    Returns: 
    - dbc.Container
        A Dash container that will be the title. 
    """
    title_container = dbc.Container(
        fluid=True,
        style={
            "height": "100vh",
            "background-color": "#005aae",
            "color": "white",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center"
        },
        children=[
            html.H1(title_text, style={"font-size": "8rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.H2(subtitle_text, style={"font-size": "2rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H3(scrolldown_text, style={"font-size": "1rem", "text-align": "center"}),
            html.Img(src='https://cdn3.iconfinder.com/data/icons/faticons/32/arrow-down-01-512.png', className="white-arrow", style={"width": "50px", "margin-left": "10px"}),
            html.Br(),
        ],
        className="title-container"
    )
    return title_container




def generate_subtitle_container(subtitle_text, background_color, text_color):
    """
    This function generates containers that are subtitles 

    Inputs: 
    - subtitle_text: (str)
        The text to be used for the subtitle.
    - background_color: (str)
        The background color to be used for the subtitle container.
    - text_color: (str)
        The color to be used for the subtitle text.

    Returns: 
    - dbc.Container
        A Dash container that will be the subtitles of the app. 
    """
    subtitle_container = dbc.Container(
        fluid=True,
        style={
            "height": "20vh",
            "background-color": background_color,
            "color": text_color,
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "flex-start"
        },
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(subtitle_text, style={"font-size": "3rem", "color": "white"}),
                    width=12,
                    style={"display": "flex", "justify-content": "center", "align-items": "center"}
                )
            )
        ]
    )
    return subtitle_container


def generate_graph_container_one(title_text, 
                                 paragraph_text,
                                 graph_component, 
                                 graph_title, 
                                title_color):
    """
    This function generates a graph container with only one static graph. 

    Inputs: 
    - title_text: (str)
        The text to be used for the title of the graph component. 
    - paragraph_text: (str)
        The text to be used for the paragraph.
    - graph_component: imported graph 
        A graph imported as a dcc object 
    - title_color : str
        The color to be used for the title text.

    Returns: 
    - dbc.Container
        A Dash container that will be used to display and give context for one graph

    """
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=3),
                dbc.Col([
                    html.H2(graph_title, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    graph_component, 
                ], width=9)
            ])
        ]
    )
    return graph_container






def generate_graph_container_two(title_text, paragraph_text, graph_component, 
                                 graph_component_2, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    graph_component, 
                    graph_component_2
                ], width=8)
            ])
        ]
    )
    return graph_container




def generate_numbers_container(title_text, paragraph_text, number1, explanation1, number2, explanation2, number3, explanation3, title_color='black', number_color='black'):
    container = dbc.Container(
        fluid=True,
        style={'height': '50vh'},
        children=[ dbc.Row(
        [dbc.Col([html.H1(title_text, 
                          style={"color": title_color, "font-size": "2rem"}),
                                     html.P(paragraph_text)],
                        width=4,
                        style={'height': '40vh', 'display': 'flex',
                                'flex-direction': 'column', 
                                'justify-content': 'center'}
                    ),
                    dbc.Col(
                        [dbc.Row(
                            [dbc.Col([html.H1(f"{number1}%", style={'text-align': 'center',
                                                                     'font-size': '6rem', 
                                                                     'color': number_color}),                                            html.P(explanation1, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex',
                                                'flex-direction': 'column', 
                                                'justify-content': 'center'}
                                    ),
                                    dbc.Col(
                                        [html.H1(f"{number2}%", style={'text-align': 'center', 
                                                                       'font-size': '6rem',
                                                                         'color': number_color}),                                            html.P(explanation2, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex',
                                                'flex-direction': 'column',
                                                  'justify-content': 'center'}
                                    ),
                                    dbc.Col(
                                        [html.H1(f"{number3}%", style={'text-align': 'center', 
                                                                       'font-size': '6rem',
                                                                         'color': number_color}),                                            html.P(explanation3, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex',
                                                'flex-direction': 'column', 
                                                'justify-content': 'center'}
                                    ),
                                ],
                                style={'height': '50%'}
                            )
                        ],
                        width=8,
                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'space-between'}
                    )
                ],
                style={'height': '100%'}
            )
        ]
    )
    return container


def generate_conclusion_container(title_text, list_items, bg_color):
    container = dbc.Container(
        fluid=True,
        style={'height': '100vh', 'background-color': bg_color},
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(title_text, style={'color': 'white', 'font-size': '5rem', 'margin-bottom': '2rem', 'text-align': 'center'}),
                            html.Ul(
                                [html.Li(item, style={'color': 'white', 'font-size': '2rem', 'text-align': 'center'}) for item in list_items],
                                style={'list-style-type': 'none', 'padding-left': '0', 'margin-top': '2rem', 'text-align': 'center'}
                            )
                        ],
                        width=12,
                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'}
                    )
                ],
                style={'height': '100%'}
            )
        ]
    )
    return container

def generate_graph_container_interactive(title_text, paragraph_text, graph_component_1, graph_component_2, graph_component_3, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    dcc.Dropdown(
                        id='graph-dropdown-2',
                        options=[
                            {'label': 'Graph 1', 'value': 'graph1'},
                            {'label': 'Graph 2', 'value': 'graph2'},
                            {'label': 'Graph 3', 'value': 'graph3'}
                        ],
                        value='graph1'
                    ),
                    html.Div(
                        id='graph-container-2',
                        children=graph_component_1
                    )
                ], width=8)
            ])
        ]
    )
    return graph_container

def generate_graph_container_interactive_two(title_text, paragraph_text,
                                              graph_component_1, graph_component_2, 
                                              graph_component_3, graph_component_4,
                                                graph_component_5, graph_component_6,
                                                  title_color, graph_title, 
                                                  first_label, 
                                                  second_label, 
                                                  third_label):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=3),
                dbc.Col([
                    html.H2(graph_title, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    dcc.Dropdown(
                        id='graph-dropdown-1',
                        options=[
                            {'label': first_label, 'value': 'graph1'},
                            {'label': second_label, 'value': 'graph2'},
                            {'label': third_label, 'value': 'graph3'}
                        ],
                        value='graph1'
                    ),
                    html.Div(
                        id='graph-container-1',
                        children=[graph_component_1, graph_component_2]
                    )
                ], width=9)
            ])
        ]
    )
    return graph_container



##############
# Fake data 
#############

# Bar plot
data = {'fruit': ['apple', 'orange', 'banana'], 'quantity': [10, 5, 20]}
df = pd.DataFrame(data)
fig_bar = go.Figure(data=[go.Bar(x=df['fruit'], y=df['quantity'])])
graph_component_bar = dcc.Graph(figure=fig_bar)

# Line plot
data = {'year': [2010, 2011, 2012, 2013, 2014, 2015, 2016],
        'sales': [100, 150, 200, 250, 300, 350, 400]}
df = pd.DataFrame(data)
fig_line = go.Figure(data=[go.Scatter(x=df['year'], y=df['sales'], mode='lines')])
graph_component_line = dcc.Graph(figure=fig_line)

# Treemap
data = px.data.gapminder().query("year == 2007").query("continent == 'Asia'")
fig_treemap = px.treemap(data, path=['continent', 'country'], values='pop',
                         color='lifeExp', hover_data=['iso_alpha'])
graph_component_treemap = dcc.Graph(figure=fig_treemap)

#import graphs visits to cdc by year 
graph_2019_2020 = plot_hhs_visits(2020)
graph_2019_2021 = plot_hhs_visits(2021)
graph_2019_2022 = plot_hhs_visits(2022)

#import grpahs of covid cases by year 
graph_covid_2020 = plot_covid_cases(2020)
graph_covid_2021 = plot_covid_cases(2021)
graph_covid_2022 = plot_covid_cases(2022)

#import numbers of social referals
fb_number = get_social_referral_frequency("Facebook")
tw_number = get_social_referral_frequency("Twitter")
ig_number = get_social_referral_frequency("Instagram")


from happy_app.analysis.domain_visits import plot_domain_visits
from happy_app.analysis.cdc_visits import plot_cdc_visits


#import sites 
key_sites = ['vaccines.gov', 'vacunas.gov', 'covid.cdc.gov', 'covid.gov', 'covidtests.gov']
cdc_data_graph = plot_domain_visits(key_sites)
non_cdc_data_graph = plot_cdc_visits()

#import 
graph_traffic_sources = plot_traffic_sources()



title_container = generate_title_container(
   title_text = "COVID-19 Online:", 
   subtitle_text =  "How were people interacting with COVID-19 goverment pages during the crisis?", 
   scrolldown_text = "Scroll down.")



subtitle_container_goverment_pages = generate_subtitle_container(
    subtitle_text = "Web Traffic Surged Alongside COVID-19",
 background_color = "#005aae", 
   text_color = "white"
     )


graph_container_cdc_data = generate_graph_container_two(
 title_text =   "CDC Data",
 paragraph_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc.",
  graph_component = graph_component_bar, 
  graph_component_2 = graph_component_line, 
  title_color = "#808080")


subtitle_container_forms_of_accesing = generate_subtitle_container(
  subtitle_text =  "FROM WHERE WERE PEOPLE ACCESING GOV. WEBSITES?",
 background_color = "#005aae", 
 text_color = "white")



graph_container_language = generate_graph_container_one(
title_text = "Language", 
paragraph_text =  "During the COVID-19 pandemic, users visited government websites in more than 68 languages. Government sites were most viewed in English (74.2%), Spanish (13%), Chinese (3.8%) or French (1%)." , 
graph_component = graph_component_bar, 
title_color = "#808080", 
graph_title = "This is a title")

graph_container_cdc_visits = generate_graph_container_one(
title_text = "A Digital Response to the Pandemic", 
paragraph_text =  "In looking at traffic to cdc.gov alone, we see a significant uptick in the number of total visits surrounding the date when COVID-19 was declared a national emergency (March 11, 2020). In looking at traffic over 2019-2022, that was the only significant increase of traffic, suggesting that other sites might have absorbed more of the fluctuation of web traffic during the course of the COVID-19 pandemic." , 
graph_component = cdc_data_graph, 
title_color = "#808080", 
graph_title = "Cumulative Visits to CDC.gov from 2019-2022")

graph_container_non_cdc_visits = generate_graph_container_one(
title_text = "Websites Born out of the Pandemic", 
paragraph_text =  "Likely in response to the uptick of traffic on government websites, the Biden administration increased efforts to offer digital tools related to the pandemic launching two new sites specific to COVID-19: CovidTests.gov and Covid.gov. In part due to the Omicron wave, CovidTests.gov drew visitors almost instantly, achieving similar traffic numbers to longer-standing sites like Vaccines.gov within weeks. Traffic to CovidTests.gov plateaus after the launch of Covid.gov in March 2020, which aggregated information on the pandemic to one website. Like CovidTests.gov, Covid.gov quickly amassed visitors post-launch offering further evidence of people’s increased reliance on digital services as a result of the pandemic." , 
graph_component = non_cdc_data_graph, 
title_color = "#808080", 
graph_title = "Cumulative Visits to Other Pandemic-Related Websites from 2019-2022")

social_numbers_container = generate_numbers_container(
    title_text = "Traffic Driven by Social Networks",
    paragraph_text = "Some of the government website traffic during the pandemic was driven by links shared by friends on social media. However, the proportion of traffic driven by friends differed across social media platforms. In the two months around the three largest spikes of COVID cases, Twitter was the most “contagious” in terms of sharing government website links (99% of traffic was due to social referrals), while only 4 in 10 Facebook visits were driven by social referrals. Instragram traffic was driven the least by social referrals, as only 14% of all traffic from the platform were driven by this type of interaction.", 
    number1 = fb_number, 
    explanation1 = "from Facebook", 
    number2 = tw_number, 
    explanation2 = "from Twitter", 
    number3 = ig_number, 
    explanation3 = "from Instagram", 
    title_color= "#808080", 
    number_color= "#005aae")

subtitle_container_language = generate_subtitle_container(
  subtitle_text =  "DID USER LANGUAGE PLAYED A ROLE?",
 background_color = "#005aae", 
 text_color = "white")

graph_container_accesing = generate_graph_container_interactive(
    title_text = "Traffic Source", 
    paragraph_text = "In the first wave of the pandemic (March/April 2020), 63% of traffic to government websites came from search engines, followed by direct links (15%). Only 0.7% of traffic to government websites came from social media websites during this time period. These trends remained true during the peak of COVID cases in December 2020/January 2021 as well as in December 2021/January 2022.", 
    graph_component_1 = graph_traffic_sources, 
    graph_component_2 = graph_component_line, 
    graph_component_3 = graph_component_bar, 
    title_color = "#808080")

subtitle_container_most_visited_pages = generate_subtitle_container(
  subtitle_text =  "KEY SITES", 
 background_color = "#005aae", 
 text_color = "white" )

conclusion_container = generate_conclusion_container(
        title_text="Conclusion",
        list_items=[
            "1. This is our first conclusion.",
            "2. This is our second conclusion.",
            "3. This is our third conclusion."
        ],
        bg_color="#005aae"
    )





interactive_cdc_covid_container = generate_graph_container_interactive_two(
    title_text = "Spikes in Health and Human Services Web Usage", 
    paragraph_text = "In tandem with the pandemic’s initial surge during March 2020, visits to Department of Health and Human Services websites increased sharply, rising 155 million more than traffic in 2019. When COVID- 19 was declared a national emergency and lockdowns begun traffic reached number, some amount higher then. 234 million (max visits per week) As the pandemic stretched on throughout 2020 into 2021, HHS website traffic remained consistently higher than what was witnessed during 2019, suggesting the presence of the pandemic increased the likelihood people turned to government sources for information regarding health and safety.Traffic remained steady until January 2022, when visits peaked coinciding with the Omicron wave of the pandemic and the launch of new HHS websites, like CovidTests.gov.", 
    graph_component_1 = graph_2019_2020 , 
    graph_component_2 = graph_covid_2020, 
    graph_component_3 = graph_2019_2021, 
    graph_component_4 = graph_covid_2021, 
    graph_component_5 = graph_2019_2022, 
    graph_component_6 = graph_covid_2022, 
    title_color = "#808080", 
    graph_title = "Visits to the Health and Human Services Websites by Week (compared to a base year)", 
    first_label = 2020, 
    second_label = 2021, 
    third_label = 2022) 
   

app.layout = html.Div(children=[
    title_container,
    subtitle_container_goverment_pages,
    interactive_cdc_covid_container,
    subtitle_container_forms_of_accesing, 
    graph_container_accesing, 
    social_numbers_container, 
    subtitle_container_language, 
    graph_container_language, 
    subtitle_container_most_visited_pages, 
    graph_container_cdc_visits,
    graph_container_non_cdc_visits,  
    conclusion_container

])


@app.callback(
    [dash.dependencies.Output('graph-container-1', 'children'),
     dash.dependencies.Output('graph-container-2', 'children')],
    [dash.dependencies.Input('graph-dropdown-1', 'value'),
     dash.dependencies.Input('graph-dropdown-2', 'value')]
)

def update_graph_container(value1, value2):
    if value1 == 'graph1':
        graph_container_1 = [graph_2019_2020, graph_covid_2020]
    elif value1 == 'graph2':
        graph_container_1 = [graph_2019_2021, graph_covid_2021]
    elif value1 == 'graph3':
        graph_container_1 = [graph_2019_2022, graph_covid_2022]
    
    if value2 == 'graph1':
        graph_container_2 = graph_traffic_sources
    elif value2 == 'graph2':
        graph_container_2 = graph_component_line
    elif value2 == 'graph3':
        graph_container_2 = graph_component_treemap
    
    return graph_container_1, graph_container_2





# Run app
if __name__=='__main__':
    app.run_server(port=8052)