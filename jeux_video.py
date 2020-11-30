# filename = 'dash-01.py'

#
# Imports
#

import plotly_express as px
import pandas as pd
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

#
# Data
#


df = pd.read_csv('vgsales.csv', index_col = 0)
#Nettoyage du dataset
index_with_nan = df.index[df.isnull().any(axis=1)] #Suppression des lignes avec des valeurs nulles ou manquantes (NA)
df.drop(index_with_nan,0, inplace=True)
df['Year'] = df['Year'].astype(int)
df['Year'] = df['Year'].astype(str)
df['Platform'] = df['Platform'].astype(str)
Year = df['Year']
Genre = df['Genre']
Name = df['Name']
Platforme = df['Platform']
USA = df['NA_Sales']
EU = df['EU_Sales']
JP = df['JP_Sales']
Global = df['Global_Sales']


#filtration de data pour fig1
x = Genre.value_counts()
x = pd.DataFrame(x).reset_index()
x = x.rename(columns={"index" : "Genre","Genre":"Nb Vente"})
#y = [2346,886,1249,1488,582,1739,1310,867,3316,848,1286,681]

#filtration de data pour fig2
dfplatform = df.groupby('Platform') #Créer des groupes en fonction des plateformes 
dfplatmin = pd.DataFrame(dfplatform.Year.min()).reset_index() #Création d'un dataFrame avec l'année minimum de chaque plateforme
dfplatmax = pd.DataFrame(dfplatform.Year.max()).reset_index() #Création d'un dataFrame avec l'année maximum de chaque plateforme
dfplatmax = dfplatmax.rename(columns = {'Year': 'YearMax'}) #On renome les colonnes des deux dataFrames
dfplatmin = dfplatmin.rename(columns = {'Year' : 'YearMin'})
dfnew = pd.merge(dfplatmin,dfplatmax) #On concataine les deux dataFrames


#filtration de data pour fig8
df2 = pd.read_csv("vgsales.csv") #Nous avons rechargé un autre dataFrame par souci de simplicité
index_with_nan = df2.index[df2.isnull().any(axis=1)]
df2.drop(index_with_nan,0,inplace = True)
df2['Year'] = df2['Year'].astype(int)
df2.drop('Name',1,inplace=True) #Suppression des colonnes dont nous nous servons pas 
df2.drop('Publisher',1,inplace=True)
df2.drop('NA_Sales',1,inplace=True)
df2.drop('JP_Sales',1,inplace=True)
df2.drop('Other_Sales',1,inplace=True)
df2.drop('EU_Sales',1,inplace=True)
df2.drop('Genre',1,inplace=True)
Console = df2.groupby(['Platform']).sum().reset_index() #Permet de faire la somme des ventes globales de chaque plateforme

#filtration de data pour fig9
Global = Console['Global_Sales']
Console2 = Console[Global > 150]

#filtration de data pour fig10
Annes2 = df2.groupby(['Platform','Year']).sum().reset_index() #Permet de faire la somme des ventes globales pour toutes les années pour chaque plateforme

#filtration de data pour fig11
Globalesales = df.groupby(['Year']).sum().reset_index()


#filtration de data pour fig15
df4 = pd.read_csv("vgsales.csv")
df4.drop('Name',1,inplace=True)
df4.drop('Other_Sales',1,inplace=True)
df4.drop('NA_Sales',1,inplace=True)
df4.drop('JP_Sales',1,inplace=True)
df4.drop('EU_Sales',1,inplace=True)
df4.drop('Genre',1,inplace=True)
df4.drop('Platform',1,inplace=True)
df4.drop('Year',1,inplace=True)
Publish = df4.groupby(['Publisher']).sum().reset_index()
Globale = Publish["Global_Sales"]
Publish = Publish[Globale>100]





#
# Main
# Création de toutes nos figures pour pouvoir ensuite les afficher dans le dashboard
#

if __name__ == '__main__':

    app = dash.Dash(__name__) 

    fig = px.histogram(x,x = "Genre", y="Nb Vente", title = 'Histogramme du nombre de jeux développé en fonction de leur genre',labels = {"sum of Nb Vente":"Ventes globales (en millions)"})
    
    fig2 = px.timeline(dfnew, x_start='YearMin', x_end='YearMax', y = 'Platform', title = 'Timeline de ventes de jeux sur chaque platforme',labels = {"Platform": "Plateformes", "Year":"Années"})
    
    
    fig8 = px.bar(Console,x = "Platform",y ="Global_Sales",color = "Global_Sales",title = "Histogramme des plateformes avec le plus grand nombre de ventes selon le continent",labels = {"Name": "Consoles", "Global_Sales":"Ventes Globales (en millions)"})

    fig9 = px.pie(Console2, values='Global_Sales', names='Platform', title='Camembert des consoles de jeu avec le plus grand nombre de ventes',hover_data=['Global_Sales'],labels={'Platform':'Console de jeu','Global_Sales':'Ventes Globales (en millions)'})

    fig10 = px.line(Annes2,x = 'Year',y = "Global_Sales",color = "Platform",title = "Évolution du nombre de ventes des jeux au fil des années pour chaque plateforme",labels = {"Year": "Année", "Global_Sales":"Ventes Globales (en millions)"})

    fig15 = px.bar(Publish,x = 'Publisher',y = "Global_Sales",color = "Global_Sales",title = "Graphique du nombre de ventes des jeux selon l'éditeur",labels = {"Publisher": "Éditeur", "Global_Sales": "Ventes Globales (en millions)"})

    fig16 = px.pie(Publish, values='Global_Sales', names='Publisher', title="Évolution du nombre de ventes des jeux au fil des années selon l'éditeur",hover_data=['Global_Sales'],labels={'Publisher':'Éditeur','Global_Sales':'Ventes Globales (en millions)'})



#Création de la mise en page du dashboard, c'est ici que nous organisons 
#notre dashboard et l'odre dans lequel nous voulons faire
#apparaitre chaque graphique avec son commentaire

app.layout = html.Div(children=[

                            html.H1(children=f'Étude des jeux vidéo dans le monde de 1980 à 2016',    
                                        style={'textAlign': 'center', 'color': 'black'}), # Zone où le titre du dashboard va être

                            html.Br(),
                            
                            html.H4(children=f'''Ce Dashboard constitue une étude des jeux vidéo dans le monde de 1980 à 2016. Nous avons fait le choix de ce sujet car nous sommes tous deux de grands adeptes de jeux vidéo. 
                            À travers les différents graphiques et interprétations, nous allons mettre en évidence les genres de jeux vidéo les plus prisés, les jeux les plus vendus selon la zone géographique ou encore les 
                            plateformes les plus rentables de ces dernières années. Nous avons fait le choix de créer 3 onglets dans lesquels se mêlent différents types de données sous différentes formes''',
                                        style={'textAlign': 'center', 'color': 'black'}), # Zone pour l'introduction

                            html.Br(),

                            html.H4(children=f"""Ventes Globales""",
                                        style={'textAlign': 'center', 'color': 'black'}),

                            
                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), #Créer une zone pour afficher un graphique, nous passons en paramètre un id pour identifier cette zone et une figure pour afficher la figure que nous souhaitons dans cette zone
                            

                            html.Div(children=f'''
                                Cette histogramme nous montre les catégories de jeux qui ont été le plus developpé par les éditeurs depuis 1980.
                                On remarque que la plupart des jeux developpés sont des jeux d'actions et de sports. Il est intérressant de voir que ces deux catégories ressortent le plus et cette étude à sûrement dû 
                                aider les éditeurs de jeux pour cibler quels genres plaisaient le plus aux gamers et pour developper des jeux en fonction. Personnellement nous pensions que le genre Shooter pesait beaucoup
                                plus sachant qu'aujourd'hui la plupart des jeunes jouent à des jeux de guerre comme Call of duty, Fortnite etc...
                                mais il ne faut pas oublier que notre dataset remonte les jeux depuis 1980 et qu'en 1980 on ne jouait pas aux même jeux qu'aujourd'hui.
                                Vous pouvez survolez le graphique pour voir en detail le nombre de jeux créés dans chaque catégorie.
                            ''',style={'textAlign': 'center'}), #Créer une zone pour afficher du texte, c'est ici que nous mettons le commentaire du graphique en question

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                        

                            html.Label('Continent :',style={'color': 'black', 'fontSize': 20,'font-weight': 'bold'}),
                            dcc.Dropdown(
                            id="year-dropdow",
                            options=[
                                {'label': 'Monde', 'value': 'Global_Sales'},
                                {'label': 'Europe', 'value': 'EU_Sales'},
                                {'label': 'Etats-Unis', 'value': 'NA_Sales'},
                                {'label': 'Japon', 'value': 'JP_Sales'},
                                
                            ],
                            value='Global_Sales',
                            ),    #Création d'une zone pour selectionner differentes variables qui vont nous permettre de changer les données d'un graphique et de le rendre interactif

                            dcc.Graph(
                                id='graph4',
                              
                            ),

                        
                            

                            html.Div(children=f'''
                                Ces 4 histogrammes permettent de montrer les jeux vidéo ayant le plus grand nombre de ventes en fonction de 4 zones géographiques différentes, les États-Unis, le Japon, l'Europe ainsi que le monde entier. 
                                Nous pouvons observer que les jeux sont assez différents en fonction du continent. Le jeu « Wii Sports » est par exemple le jeu le plus vendus aux États-Unis et en Europe mais ne fait pas partie du top 10 des jeux les plus vendus au Japon. 
                                Ce graphique constitué de 4 histogrammes permet de mettre en évidence le choix assez différents des jeux choisis par la population en fonction des continents.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            dcc.Graph(
                                id='graph15',
                                figure=fig15
                            ),
                            
                             

                            html.Div(children=f'''
                            Cet histogramme permet de mettre en évidence les éditeurs avec le plus grand nombre de ventes de jeux vidéo. 
                            Nous pouvons observer que Nintendo est très largement en tête avec plus de 1780 millions de ventes de jeux depuis sa création.
                            Nintendo est l’éditeur à l’origine de jeux comme « Mario » qui connaissent un succès assez important dans les principaux pays du monde. 
                            C’est une entreprise très ancienne datant de 1889 et à l’origine de la création de plus de milliers de jeux ainsi que la création de nombreuses consoles de jeux. 
                            Les éditeurs Electronics Arts et Activision occupent quant à eux la deuxième et troisième place avec respectivement 1130 et 727 millions de jeux vendus.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            dcc.Graph(
                                id='graph16',
                                figure=fig16
                            ),
                            
                             

                            html.Div(children=f'''
                            Ce camembert nous offre une vision différente de l'histogramme précédent. 
                            Nous pouvons observer que Nintendo, Electronic Arts, Activison et Sony Computer Entertainment ont vendus à eux 4 environ 60% des jeux depuis 1980. 
                            À eux seuls les 4 éditeurs réalisent un plus grand nombre de ventes que plus de 15 éditeurs réunis. 
                            Nous pouvons aussi noter que Nintendo réalise environ un quart de toutes les ventes depuis 1980. 
                            Cela peut s’expliquer car les budgets ne sont pas les mêmes pour tout le monde, certaines firmes ne sortent ou ont sorti que très peu de jeux depuis leurs créations.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            html.H4(children=f"""Plateformes""",
                                        style={'textAlign': 'center', 'color': 'black'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),          

                            dcc.Graph(
                                id='graph8',
                                figure=fig8,
                                
                            ),
                            
               

                            html.Div(children=f'''
                                Cet histogramme permet de montrer les plateformes de jeux avec le plus grand nombre de ventes. 
                                Ici, nous pouvons observer que la PS2 est la console qui a vendu le plus de jeux avec plus de 1255 millions de ventes. 
                                Nous pouvons observer que les consoles de salon Playstation de la marque Sony sont toutes présentes dans le top 6. 
                                La somme de la vente des 3 consoles est égal a plus de 2900 millions. 
                                Ce qui fait de Sony l’éditeur ayant vendu le plus de consoles de jeux.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            dcc.Graph(
                                id='graph9',
                                figure=fig9
                            ),
                            


                            html.Div(children=f'''
                            Ce camembert est une vision différente de la figure précédente, il permet d'afficher sous la forme d'un camembert les plateformes ayant vendu le plus de jeux. 
                            La PS2, la XBOX 360, La PS3 et la WII sont les plateformes constituant plus de 50% de la vente des jeux vidéo. 
                            Nous pouvons observer que 6 plateformes se détachent en nombre de ventes des autres. 
                            À elles 6, elles constituent environ 70% de la ventes de consoles de jeux. 
                            La Wii et la DS sont deux consoles créées par Nintendo et elles représentent 20% des ventes. 
                            Sony Computer Entertainment réalise 34% des ventes.
                            ''',style={'textAlign': 'center'}),


                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            dcc.Graph(
                               id='graph10',
                               figure=fig10
                            ),

                            dcc.Graph(
                                id='graph2',
                                figure=fig2
                            ),

                            html.Div(children=f'''
                                Les deux graphiques ci-dessus ont un lien et c'est pour cela que l'on va les étudier ensemble. 
                     Le deuxième graphique reprensente en réalité la durée de commercialisation des jeux vidéo pour chaque plateforme et donc logiquement la durée de vie de toutes les plateformes.
                     Si les éditeurs ont décidé de ne plus sortir de jeux vidéo pour telle plateforme c'est que cette plateforme devenait obsolete et qu'elle n'interressait plus personne.
                     On peut donc se rendre facilement compte grace au graphique les plateformes qui ont réussi à s'imposer dans la durée. Nous pouvons que constater l'impressionnante domination de la DS
                     et du PC dans le temps. IL est vrai que la DS et le PC ont connu des évolutions logiciel mais pas au niveau du nom contrairement à la PS2 qui est devenu la PS3 par exemple.
                     Le premier graphique represente les ventes globales des jeux vidéo en fonction des années pour chaque plateforme. Si on regarde le second graphique on a accès aux dates de sorties de chaque plateforme
                     car logiquement l'année où le premier jeu video est sorti sur une plateforme correspond à la date de sortie de la pateforme elle même. Donc si on regarde la date de sortie de la Wii par exemple (2006)
                     et qu'on la reporte sur le premier graphique, nous obsevons que 137 millions de jeux vidéo se sont vendus pour la Wii la premiere année. La PS2 arrive en deuxième position avec 39 millions de jeux 
                     video vendus la premiere année. L'ecart est très conséquent et on se rend compte de l'impact de la Wii l'année de son lancement. Il est vrai que de nos jours la Wii est une console qui a touché toutes les générations.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                            html.H4(children=f"""Vision Globale""",
                                        style={'textAlign': 'center', 'color': 'black'}),

                            html.Br(),
                            html.Br(),
                            html.Br(),
                             
                            
                            html.Label('Continent :',style={'color': 'black', 'fontSize': 20,'font-weight': 'bold'}),
                            dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {'label': 'Monde', 'value': 'Global_Sales'},
                                {'label': 'Europe', 'value': 'EU_Sales'},
                                {'label': 'Etats-Unis', 'value': 'NA_Sales'},
                                {'label': 'Japon', 'value': 'JP_Sales'},
                                
                            ],
                            
                            value='Global_Sales',
                            ),
                           
                           
                            dcc.Graph(
                                id='graph11',
                                
                            ),
                            html.Div(children=f'''
                                Cette histogramme nous offre une vision globale de l'importance des jeux vidéo au niveau mondial et pour differents continents dans le monde.
                     Dans le monde on peut voir que les jeux vidéo n'ont cessé de se democratimer jusqu'en 2008 où l'on a atteint le pique. Depuis 2008 il y a une baisse considerable d'années en années.
                     Au États-Unis, on retrouve cette même tendence avec une democratisation jusqu'en 2008 puis une baisse à partir de cette date. On remarque qu'en Europe les jeux ont eu beaucoup de mal à se democratiser
                     au debut entre 1980 à 1995. Après cette date cela s'est vite democratisé jusqu'en 2009 et il y a eu ensuite une baise importante jusqu'en 2016. On constate que l'Europe était donc legèrement en retard
                     par rapport aux États-Unis à propos des jeux vidéo. Enfin pour le Japon on constate que les jeux vidéos se sont democratisés beaucoup plus vite qu'au USA et qu'en Europe. Le pique a eu lieu en 2006 ce qui 
                     témoigne de leur avance.
                     Pour tous les continents on peut peut etre expliquer une baisse de vente des jeux vidéos à partir des années 2006-2009 par la hausse des prix des consoles et des jeux vidéos. Il est vrai qu'aujourd'hui jouer au jeux vidéos est devenue un privilège
                     et qu'il faut debourser beaucoup d'argents dans du matériels pour pouvoir jouer.
                            ''',style={'textAlign': 'center'}),

                            html.Br(),

                            html.H4(children=f"""Conclusion""",
                                        style={'textAlign': 'center', 'color': 'black'}),

                            html.H4(children=f"""Nous pouvons tirer les conclusions suivantes de cette étude :
                       - Depuis 1980 jusqu'a 2016, les catégories qui ont vendu le plus sont les jeux d'action et de sport
                       - Nintendo, Electronic Arts et Activison ont vendu à eux 3 environ 50% des jeux depuis 1980
                       - La PS2 et la XBOX sont les deux consoles qui ont vendus le plus de jeux vidéo mais il faut noter que la WII a connu un succès fulgurant lors de sa sortie avec 137 millions de vente la première année
                       - Les jeux vidéos étaient à leur apogée dans les années 2006 à 2009 puis sont moins important aujourd'hui surement grâce à la hausse des prix des consoles et à la democratisation des jeux sur smartphone.""",
                                        style={'textAlign': 'center', 'color': 'black'}),
                            

                            


                            

    ]
    )

    #Création des callback qui vont nous permettre de récuperer les input créés dans les Dropdown et modifier les graphiques en fonction de la variable choisie.
    #Ce sont les dropdown et les callback qui nous permette de créer des graphiques interactifs 

@app.callback(
    Output('graph11','figure'), 
    [Input('year-dropdown','value')] 
)
def cont(conti):
        fig200 = px.scatter(Globalesales,
                  x = 'Year',
                  y = conti,
                  color = conti,
                  size = conti,
                  title = "Evolution du nombre de ventes des jeux au fil des années selon la zone géographique",
                  log_x=True, size_max=40, range_x=[1980,2018],
                  labels = {"Year": "Année", "Global_sales":"Ventes Globales (en millions)","JP_Sales":"Ventes Globales au Japon (en millions)","EU_Sales":"Ventes Globales en Europe (en millions)","NA_Sales":"Ventes Globales au Etats-Unis (en millions)"})
        return fig200

@app.callback(
    Output('graph4','figure'), 
    [Input('year-dropdow','value')] 
)   
def top_jeux(cont):
        dfNew = df.sort_values(by=[cont],ascending=False)
        fig50 = px.bar(dfNew[0:10],cont,'Name',color = 'Platform',title="Histogramme des jeux les plus vendus selon le continent",labels = {"Name": "Nom des jeux", "Global_Sales":"Ventes Globales (en millions)","JP_Sales":"Ventes Globales au Japon (en millions)","EU_Sales":"Ventes Globales en Europe (en millions)","NA_Sales":"Ventes Globales au Etats-Unis (en millions)"})
        return fig50

    #
    # RUN APP
    #


app.run_server(debug=True) 

