# dashboard_cac40.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard CAC 40 - Analyse en Temps Réel",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0055A4, #EF4135, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #0055A4, #00A3E0);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0055A4;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #0055A4;
        border-bottom: 2px solid #EF4135;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .stock-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #0055A4;
        background-color: #f8f9fa;
    }
    .price-change {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .positive { background-color: #d4edda; border-left: 4px solid #28a745; color: #155724; }
    .negative { background-color: #f8d7da; border-left: 4px solid #dc3545; color: #721c24; }
    .neutral { background-color: #e2e3e5; border-left: 4px solid #6c757d; color: #383d41; }
    .sector-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class CAC40Dashboard:
    def __init__(self):
        self.entreprises = self.define_entreprises()
        self.historical_data = self.initialize_historical_data()
        self.current_data = self.initialize_current_data()
        self.sector_data = self.initialize_sector_data()
        
    def define_entreprises(self):
        """Définit les entreprises du CAC 40 avec leurs caractéristiques"""
        return {
            'LVMH': {
                'nom_complet': 'LVMH Moët Hennessy Louis Vuitton',
                'secteur': 'Luxe',
                'sous_secteur': 'Articles de luxe',
                'pays': 'France',
                'couleur': '#8B4513',
                'poids_cac40': 12.5,
                'market_cap': 380e9,
                'dividende_yield': 1.5,
                'volume_moyen': 450000,
                'description': 'Leader mondial du luxe'
            },
            'TOT': {
                'nom_complet': 'TotalEnergies',
                'secteur': 'Énergie',
                'sous_secteur': 'Pétrole & Gaz',
                'pays': 'France',
                'couleur': '#FF6B00',
                'poids_cac40': 8.2,
                'market_cap': 150e9,
                'dividende_yield': 4.8,
                'volume_moyen': 3500000,
                'description': 'Major énergétique intégré'
            },
            'SAN': {
                'nom_complet': 'Sanofi',
                'secteur': 'Santé',
                'sous_secteur': 'Pharmaceutique',
                'pays': 'France',
                'couleur': '#0066CC',
                'poids_cac40': 7.8,
                'market_cap': 140e9,
                'dividende_yield': 3.2,
                'volume_moyen': 1200000,
                'description': 'Groupe pharmaceutique mondial'
            },
            'AIR': {
                'nom_complet': 'Airbus',
                'secteur': 'Industrie',
                'sous_secteur': 'Aérospatial',
                'pays': 'France',
                'couleur': '#003366',
                'poids_cac40': 6.5,
                'market_cap': 110e9,
                'dividende_yield': 1.1,
                'volume_moyen': 800000,
                'description': 'Constructeur aéronautique'
            },
            'OR': {
                'nom_complet': "L'Oréal",
                'secteur': 'Consommation',
                'sous_secteur': 'Cosmétiques',
                'pays': 'France',
                'couleur': '#FF69B4',
                'poids_cac40': 5.9,
                'market_cap': 240e9,
                'dividende_yield': 1.3,
                'volume_moyen': 300000,
                'description': 'Leader mondial des cosmétiques'
            },
            'BNP': {
                'nom_complet': 'BNP Paribas',
                'secteur': 'Finance',
                'sous_secteur': 'Banque',
                'pays': 'France',
                'couleur': '#004B87',
                'poids_cac40': 5.2,
                'market_cap': 75e9,
                'dividende_yield': 6.2,
                'volume_moyen': 2500000,
                'description': 'Groupe bancaire international'
            },
            'AI': {
                'nom_complet': 'Air Liquide',
                'secteur': 'Chimie',
                'sous_secteur': 'Gaz industriels',
                'pays': 'France',
                'couleur': '#00A3E0',
                'poids_cac40': 4.8,
                'market_cap': 85e9,
                'dividende_yield': 2.1,
                'volume_moyen': 600000,
                'description': 'Leader des gaz industriels'
            },
            'STM': {
                'nom_complet': 'STMicroelectronics',
                'secteur': 'Technologie',
                'sous_secteur': 'Semi-conducteurs',
                'pays': 'France',
                'couleur': '#660099',
                'poids_cac40': 4.3,
                'market_cap': 40e9,
                'dividende_yield': 0.8,
                'volume_moyen': 1500000,
                'description': 'Fabricant de semi-conducteurs'
            },
            'DG': {
                'nom_complet': 'Vinci',
                'secteur': 'Industrie',
                'sous_secteur': 'BTP & Concessions',
                'pays': 'France',
                'couleur': '#FFCC00',
                'poids_cac40': 4.1,
                'market_cap': 60e9,
                'dividende_yield': 3.5,
                'volume_moyen': 700000,
                'description': 'Groupe de construction et concessions'
            },
            'MC': {
                'nom_complet': 'LVMH',
                'secteur': 'Luxe',
                'sous_secteur': 'Articles de luxe',
                'pays': 'France',
                'couleur': '#8B4513',
                'poids_cac40': 3.9,
                'market_cap': 380e9,
                'dividende_yield': 1.5,
                'volume_moyen': 450000,
                'description': 'Leader mondial du luxe'
            }
            # On pourrait ajouter les 30 autres entreprises...
        }
    
    def initialize_historical_data(self):
        """Initialise les données historiques des prix"""
        dates = pd.date_range('2020-01-01', datetime.now(), freq='D')
        data = []
        
        for date in dates:
            for symbole, info in self.entreprises.items():
                # Prix de base réaliste selon la capitalisation
                base_price = info['market_cap'] / 1e9 * random.uniform(0.8, 1.2)
                
                # Impact COVID (2020)
                if date.year == 2020 and date.month <= 6:
                    covid_impact = random.uniform(0.5, 0.8)
                elif date.year == 2020:
                    covid_impact = random.uniform(0.8, 1.0)
                elif date.year == 2021:
                    covid_impact = random.uniform(1.0, 1.3)
                else:
                    covid_impact = random.uniform(1.0, 1.5)
                
                # Volatilité quotidienne
                daily_volatility = random.uniform(0.95, 1.05)
                
                prix = base_price * covid_impact * daily_volatility * random.uniform(0.98, 1.02)
                volume = info['volume_moyen'] * random.uniform(0.5, 2.0)
                
                data.append({
                    'date': date,
                    'symbole': symbole,
                    'prix': prix,
                    'volume': volume,
                    'secteur': info['secteur'],
                    'market_cap': info['market_cap'] * random.uniform(0.95, 1.05)
                })
        
        return pd.DataFrame(data)
    
    def initialize_current_data(self):
        """Initialise les données courantes"""
        current_data = []
        for symbole, info in self.entreprises.items():
            # Dernier prix historique
            last_data = self.historical_data[self.historical_data['symbole'] == symbole].iloc[-1]
            
            # Variation quotidienne simulée
            change_pct = random.uniform(-0.05, 0.05)
            change_abs = last_data['prix'] * change_pct
            
            current_data.append({
                'symbole': symbole,
                'nom_complet': info['nom_complet'],
                'secteur': info['secteur'],
                'prix_actuel': last_data['prix'] + change_abs,
                'variation_pct': change_pct * 100,
                'variation_abs': change_abs,
                'volume': info['volume_moyen'] * random.uniform(0.8, 1.2),
                'market_cap': info['market_cap'],
                'dividende_yield': info['dividende_yield'],
                'poids_cac40': info['poids_cac40'],
                'ouverture': last_data['prix'] * random.uniform(0.99, 1.01),
                'plus_haut': last_data['prix'] * random.uniform(1.01, 1.03),
                'plus_bas': last_data['prix'] * random.uniform(0.97, 0.99)
            })
        
        return pd.DataFrame(current_data)
    
    def initialize_sector_data(self):
        """Initialise les données par secteur"""
        secteurs = list(set([info['secteur'] for info in self.entreprises.values()]))
        data = []
        
        for secteur in secteurs:
            entreprises_secteur = [s for s, info in self.entreprises.items() if info['secteur'] == secteur]
            poids_total = sum([self.entreprises[s]['poids_cac40'] for s in entreprises_secteur])
            market_cap_total = sum([self.entreprises[s]['market_cap'] for s in entreprises_secteur])
            
            data.append({
                'secteur': secteur,
                'poids_cac40': poids_total,
                'market_cap_total': market_cap_total,
                'nombre_entreprises': len(entreprises_secteur),
                'performance_moyenne': random.uniform(-2, 4)
            })
        
        return pd.DataFrame(data)
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        for idx in self.current_data.index:
            symbole = self.current_data.loc[idx, 'symbole']
            
            # Simulation de variations de prix
            if random.random() < 0.3:  # 30% de chance de changement
                variation = random.uniform(-0.02, 0.02)
                nouveau_prix = self.current_data.loc[idx, 'prix_actuel'] * (1 + variation)
                
                self.current_data.loc[idx, 'prix_actuel'] = nouveau_prix
                self.current_data.loc[idx, 'variation_pct'] = variation * 100
                self.current_data.loc[idx, 'variation_abs'] = nouveau_prix - self.current_data.loc[idx, 'ouverture']
                
                # Mise à jour des plus hauts/plus bas
                if nouveau_prix > self.current_data.loc[idx, 'plus_haut']:
                    self.current_data.loc[idx, 'plus_haut'] = nouveau_prix
                if nouveau_prix < self.current_data.loc[idx, 'plus_bas']:
                    self.current_data.loc[idx, 'plus_bas'] = nouveau_prix
                
                # Mise à jour du volume
                self.current_data.loc[idx, 'volume'] *= random.uniform(0.9, 1.1)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">📈 Dashboard CAC 40 - Analyse en Temps Réel</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES BOURSIÈRES EN TEMPS RÉEL</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Surveillance et analyse des performances du CAC 40 et de ses composantes**")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés du CAC 40"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DU CAC 40</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques
        cac40_value = self.current_data['prix_actuel'].sum() / len(self.current_data) * 40
        variation_cac40 = self.current_data['variation_pct'].mean()
        volume_total = self.current_data['volume'].sum()
        entreprises_hausse = len(self.current_data[self.current_data['variation_pct'] > 0])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "CAC 40",
                f"{cac40_value:,.0f} pts",
                f"{variation_cac40:+.2f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Entreprises en Hausse",
                f"{entreprises_hausse}/{len(self.current_data)}",
                f"{entreprises_hausse - (len(self.current_data) - entreprises_hausse):+d} vs baisse"
            )
        
        with col3:
            st.metric(
                "Volume Total",
                f"{volume_total:,.0f}",
                f"{random.randint(-10, 15)}% vs hier"
            )
        
        with col4:
            capitalisation_totale = self.current_data['market_cap'].sum() / 1e12
            st.metric(
                "Capitalisation Totale",
                f"{capitalisation_totale:.2f} T€",
                f"{random.uniform(-0.1, 0.2):.2f} T€ vs hier"
            )
    
    def create_cac40_overview(self):
        """Crée la vue d'ensemble du CAC 40"""
        st.markdown('<h3 class="section-header">🏛️ VUE D\'ENSEMBLE DU CAC 40</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Performance Indices", "Répartition Secteurs", "Top Performers", "Analyse Technique"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du CAC 40 simulé
                cac40_evolution = self.historical_data.groupby('date')['prix'].mean().reset_index()
                cac40_evolution['cac40'] = cac40_evolution['prix'] * 40
                
                fig = px.line(cac40_evolution, 
                             x='date', 
                             y='cac40',
                             title='Évolution du CAC 40 (2020-2024)',
                             color_discrete_sequence=['#0055A4'])
                fig.update_layout(yaxis_title="Points CAC 40")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance par secteur
                fig = px.bar(self.sector_data, 
                            x='secteur', 
                            y='performance_moyenne',
                            title='Performance Moyenne par Secteur (%)',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(yaxis_title="Performance (%)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition par secteur
                fig = px.pie(self.sector_data, 
                            values='poids_cac40', 
                            names='secteur',
                            title='Répartition du CAC 40 par Secteur',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Capitalisation par secteur
                fig = px.bar(self.sector_data, 
                            x='secteur', 
                            y='market_cap_total',
                            title='Capitalisation Boursière par Secteur (Milliards €)',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(yaxis_title="Capitalisation (Milliards €)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top gainers
                top_gainers = self.current_data.nlargest(10, 'variation_pct')
                fig = px.bar(top_gainers, 
                            x='variation_pct', 
                            y='symbole',
                            orientation='h',
                            title='Top 10 des Performances Positives (%)',
                            color='variation_pct',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top losers
                top_losers = self.current_data.nsmallest(10, 'variation_pct')
                fig = px.bar(top_losers, 
                            x='variation_pct', 
                            y='symbole',
                            orientation='h',
                            title='Top 10 des Performances Négatives (%)',
                            color='variation_pct',
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Analyse technique d'une entreprise sélectionnée
            entreprise_selectionnee = st.selectbox("Sélectionnez une entreprise:", 
                                                 list(self.entreprises.keys()))
            
            if entreprise_selectionnee:
                entreprise_data = self.historical_data[
                    self.historical_data['symbole'] == entreprise_selectionnee
                ].copy()
                
                # Calcul des indicateurs techniques
                entreprise_data['MA20'] = entreprise_data['prix'].rolling(window=20).mean()
                entreprise_data['MA50'] = entreprise_data['prix'].rolling(window=50).mean()
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                  vertical_spacing=0.1, 
                                  subplot_titles=('Prix et Moyennes Mobiles', 'Volume'))
                
                # Prix et moyennes mobiles
                fig.add_trace(go.Scatter(x=entreprise_data['date'], y=entreprise_data['prix'],
                                       name='Prix', line=dict(color='#0055A4')), row=1, col=1)
                fig.add_trace(go.Scatter(x=entreprise_data['date'], y=entreprise_data['MA20'],
                                       name='MM20', line=dict(color='orange')), row=1, col=1)
                fig.add_trace(go.Scatter(x=entreprise_data['date'], y=entreprise_data['MA50'],
                                       name='MM50', line=dict(color='red')), row=1, col=1)
                
                # Volume
                fig.add_trace(go.Bar(x=entreprise_data['date'], y=entreprise_data['volume'],
                                   name='Volume', marker_color='lightblue'), row=2, col=1)
                
                fig.update_layout(height=600, title_text=f"Analyse Technique - {entreprise_selectionnee}")
                st.plotly_chart(fig, use_container_width=True)
    
    def create_entreprises_live(self):
        """Affiche les entreprises en temps réel"""
        st.markdown('<h3 class="section-header">🏢 ENTREPRISES EN TEMPS RÉEL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Tableau des Cours", "Analyse Secteur", "Screener"])
        
        with tab1:
            # Filtres pour les entreprises
            col1, col2, col3 = st.columns(3)
            with col1:
                secteur_filtre = st.selectbox("Secteur:", 
                                            ['Tous'] + list(self.sector_data['secteur'].unique()))
            with col2:
                performance_filtre = st.selectbox("Performance:", 
                                                ['Tous', 'En hausse', 'En baisse', 'Stable'])
            with col3:
                tri_filtre = st.selectbox("Trier par:", 
                                        ['Variation %', 'Volume', 'Capitalisation', 'Poids CAC 40'])
            
            # Application des filtres
            entreprises_filtrees = self.current_data.copy()
            if secteur_filtre != 'Tous':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['secteur'] == secteur_filtre]
            if performance_filtre == 'En hausse':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] > 0]
            elif performance_filtre == 'En baisse':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] < 0]
            elif performance_filtre == 'Stable':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] == 0]
            
            # Tri
            if tri_filtre == 'Variation %':
                entreprises_filtrees = entreprises_filtrees.sort_values('variation_pct', ascending=False)
            elif tri_filtre == 'Volume':
                entreprises_filtrees = entreprises_filtrees.sort_values('volume', ascending=False)
            elif tri_filtre == 'Capitalisation':
                entreprises_filtrees = entreprises_filtrees.sort_values('market_cap', ascending=False)
            elif tri_filtre == 'Poids CAC 40':
                entreprises_filtrees = entreprises_filtrees.sort_values('poids_cac40', ascending=False)
            
            # Affichage des entreprises
            for _, entreprise in entreprises_filtrees.iterrows():
                change_class = ""
                if entreprise['variation_pct'] > 0:
                    change_class = "positive"
                elif entreprise['variation_pct'] < 0:
                    change_class = "negative"
                else:
                    change_class = "neutral"
                
                col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{entreprise['symbole']}**")
                    st.markdown(f"*{entreprise['secteur']}*")
                with col2:
                    st.markdown(f"**{entreprise['nom_complet']}**")
                    st.markdown(f"Market Cap: {entreprise['market_cap']/1e9:.1f} Md€")
                with col3:
                    st.markdown(f"**{entreprise['prix_actuel']:.2f}€**")
                    st.markdown(f"Div. Yield: {entreprise['dividende_yield']}%")
                with col4:
                    variation_str = f"{entreprise['variation_pct']:+.2f}%"
                    st.markdown(f"**{variation_str}**")
                    st.markdown(f"{entreprise['variation_abs']:+.2f}€")
                with col5:
                    st.markdown(f"<div class='price-change {change_class}'>{variation_str}</div>", 
                               unsafe_allow_html=True)
                    st.markdown(f"Vol: {entreprise['volume']:,.0f}")
                
                st.markdown("---")
        
        with tab2:
            # Analyse détaillée par secteur
            secteur_selectionne = st.selectbox("Sélectionnez un secteur:", 
                                             self.sector_data['secteur'].unique())
            
            if secteur_selectionne:
                entreprises_secteur = self.current_data[
                    self.current_data['secteur'] == secteur_selectionne
                ]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Performance des entreprises du secteur
                    fig = px.bar(entreprises_secteur, 
                                x='symbole', 
                                y='variation_pct',
                                title=f'Performance des Entreprises - {secteur_selectionne}',
                                color='variation_pct',
                                color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Répartition des poids dans le secteur
                    fig = px.pie(entreprises_secteur, 
                                values='poids_cac40', 
                                names='symbole',
                                title=f'Répartition des Poids - {secteur_selectionne}')
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Screener d'entreprises
            st.subheader("Screener d'Investissement")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_market_cap = st.number_input("Market Cap Min (Md€)", 
                                               min_value=0, max_value=500, value=10)
                min_dividende = st.number_input("Dividende Yield Min (%)", 
                                              min_value=0.0, max_value=20.0, value=2.0)
            
            with col2:
                max_volatilite = st.number_input("Volatilité Max (%)", 
                                               min_value=0, max_value=100, value=50)
                secteur_screener = st.multiselect("Secteurs", 
                                                 self.sector_data['secteur'].unique())
            
            with col3:
                min_performance = st.number_input("Performance Min (%)", 
                                                min_value=-50.0, max_value=50.0, value=0.0)
                appliquer_filtres = st.button("Appliquer les Filtres")
            
            if appliquer_filtres:
                entreprises_filtrees = self.current_data.copy()
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['market_cap'] >= min_market_cap * 1e9
                ]
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['dividende_yield'] >= min_dividende
                ]
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['variation_pct'] >= min_performance
                ]
                
                if secteur_screener:
                    entreprises_filtrees = entreprises_filtrees[
                        entreprises_filtrees['secteur'].isin(secteur_screener)
                    ]
                
                st.write(f"**{len(entreprises_filtrees)} entreprises correspondent aux critères**")
                st.dataframe(entreprises_filtrees[['symbole', 'nom_complet', 'secteur', 'prix_actuel', 
                                                 'variation_pct', 'dividende_yield', 'market_cap']], 
                           use_container_width=True)
    
    def create_sector_analysis(self):
        """Analyse sectorielle détaillée"""
        st.markdown('<h3 class="section-header">📊 ANALYSE SECTORIELLE DÉTAILLÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Performance Sectorielle", "Comparaison Secteurs", "Tendances"])
        
        with tab1:
            # Performance détaillée par secteur
            sector_performance = self.current_data.groupby('secteur').agg({
                'variation_pct': 'mean',
                'volume': 'sum',
                'market_cap': 'sum',
                'symbole': 'count'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(sector_performance, 
                            x='secteur', 
                            y='variation_pct',
                            title='Performance Moyenne par Secteur (%)',
                            color='variation_pct',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(sector_performance, 
                               x='market_cap', 
                               y='variation_pct',
                               size='volume',
                               color='secteur',
                               title='Performance vs Capitalisation par Secteur',
                               hover_name='secteur',
                               size_max=60)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Comparaison historique des secteurs
            sector_evolution = self.historical_data.groupby([
                self.historical_data['date'].dt.to_period('M').dt.to_timestamp(),
                'secteur'
            ])['prix'].mean().reset_index()
            
            fig = px.line(sector_evolution, 
                         x='date', 
                         y='prix',
                         color='secteur',
                         title='Évolution Comparative des Secteurs (2020-2024)',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse des tendances sectorielles
            st.subheader("Tendances et Perspectives Sectorielles")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📈 Secteurs Performants
                
                **💎 Luxe & Cosmétiques:**
                - Croissance soutenue des marchés asiatiques
                - Résilience face aux crises économiques
                - Marques fortes avec pricing power
                
                **🏭 Industrie & Aérospatial:**
                - Reprise post-COVID des voyages
                - Commandes records dans l'aéronautique
                - Innovations technologiques
                
                **💊 Santé & Pharma:**
                - Vieillissement de la population
                - Innovations médicales continues
                - Revenus stables et prévisibles
                """)
            
            with col2:
                st.markdown("""
                ### 📉 Secteurs Défavorisés
                
                **🏦 Banque & Finance:**
                - Pressions sur les marges d'intérêt
                - Réglementation accrue
                - Concurrence des fintechs
                
                **⚡ Énergie Traditionnelle:**
                - Transition énergétique
                - Volatilité des prix des commodités
                - Pressions environnementales
                
                **🛒 Distribution Traditionnelle:**
                - Concurrence e-commerce
                - Pressions sur les marges
                - Changement des habitudes de consommation
                """)
    
    def create_evolution_analysis(self):
        """Analyse de l'évolution des marchés"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION DES MARCHÉS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Analyse Historique", "Volatilité", "Corrélations"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance cumulative
                cumulative_data = self.historical_data.copy()
                cumulative_data['date_group'] = cumulative_data['date'].dt.to_period('M').dt.to_timestamp()
                monthly_perf = cumulative_data.groupby(['date_group', 'symbole'])['prix'].last().reset_index()
                monthly_perf['prev_price'] = monthly_perf.groupby('symbole')['prix'].shift(1)
                monthly_perf['monthly_return'] = (monthly_perf['prix'] / monthly_perf['prev_price'] - 1) * 100
                
                cumulative_returns = monthly_perf.groupby('date_group')['monthly_return'].mean().cumsum().reset_index()
                
                fig = px.line(cumulative_returns, 
                             x='date_group', 
                             y='monthly_return',
                             title='Performance Cumulative du CAC 40 (%)')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Rendements mensuels
                monthly_heatmap = monthly_perf.pivot_table(
                    index=monthly_perf['date_group'].dt.year,
                    columns=monthly_perf['date_group'].dt.month,
                    values='monthly_return',
                    aggfunc='mean'
                )
                
                fig = px.imshow(monthly_heatmap,
                               title='Rendements Mensuels Moyens par Année (%)',
                               color_continuous_scale='RdYlGn',
                               aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Analyse de volatilité
            volatilite_data = self.historical_data.groupby('symbole').agg({
                'prix': ['last', 'std'],
                'volume': 'mean'
            }).round(2)
            volatilite_data.columns = ['prix_actuel', 'volatilite', 'volume_moyen']
            volatilite_data['volatilite_pct'] = (volatilite_data['volatilite'] / volatilite_data['prix_actuel']) * 100
            
            fig = px.scatter(volatilite_data, 
                           x='volume_moyen', 
                           y='volatilite_pct',
                           size='prix_actuel',
                           color=volatilite_data.index,
                           title='Volatilité vs Volume des Entreprises',
                           hover_name=volatilite_data.index,
                           size_max=40)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Matrice de corrélation
            corr_data = self.historical_data.pivot(index='date', columns='symbole', values='prix')
            correlation_matrix = corr_data.corr()
            
            fig = px.imshow(correlation_matrix,
                           title='Matrice de Corrélation entre les Entreprises',
                           color_continuous_scale='RdBu',
                           zmin=-1, zmax=1,
                           aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime.now() - timedelta(days=365))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres secteurs
        st.sidebar.markdown("### 🏢 Sélection des secteurs")
        secteurs_selectionnes = st.sidebar.multiselect(
            "Secteurs à afficher:",
            list(self.sector_data['secteur'].unique()),
            default=list(self.sector_data['secteur'].unique())[:3]
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_technical = st.sidebar.checkbox("Afficher indicateurs techniques", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Informations marché
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💹 INFOS MARCHÉ")
        
        # Indices mondiaux simulés
        indices = {
            'S&P 500': {'valeur': 4500 + random.randint(-100, 100), 'variation': random.uniform(-1, 1)},
            'NASDAQ': {'valeur': 14000 + random.randint(-200, 200), 'variation': random.uniform(-1, 1)},
            'DAX': {'valeur': 16000 + random.randint(-100, 100), 'variation': random.uniform(-1, 1)},
            'FTSE 100': {'valeur': 7500 + random.randint(-50, 50), 'variation': random.uniform(-1, 1)}
        }
        
        for indice, data in indices.items():
            st.sidebar.metric(
                indice,
                f"{data['valeur']:,}",
                f"{data['variation']:+.2f}%"
            )
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'secteurs_selectionnes': secteurs_selectionnes,
            'auto_refresh': auto_refresh,
            'show_technical': show_technical
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 CAC 40", 
            "🏢 Entreprises", 
            "📊 Secteurs", 
            "📈 Évolution", 
            "💡 Insights",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_cac40_overview()
        
        with tab2:
            self.create_entreprises_live()
        
        with tab3:
            self.create_sector_analysis()
        
        with tab4:
            self.create_evolution_analysis()
        
        with tab5:
            st.markdown("## 💡 INSIGHTS STRATÉGIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 TENDANCES DU MARCHÉ
                
                **📈 Dynamiques Sectorielles:**
                - Forte performance du luxe et technologies
                - Reprise cyclique de l'industrie
                - Stabilité des utilities et santé
                
                **🌍 Facteurs Macroéconomiques:**
                - Politiques monétaires des banques centrales
                - Tensions géopolitiques
                - Évolution des taux d'intérêt
                
                **💰 Flux d'Investissement:**
                - Rotation vers les valeurs défensives
                - Intérêt pour les dividendes
                - Adoption ESG croissante
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 RISQUES ET OPPORTUNITÉS
                
                **⚡ Risques à Surveiller:**
                - Inflation persistante
                - Ralentissement économique
                - Volatilité des devises
                
                **💡 Opportunités:**
                - Valeurs sous-évaluées
                - Secteurs en transformation
                - Innovations technologiques
                
                **🔮 Perspectives:**
                - Marchés orientés à la hausse à moyen terme
                - Sélectivité requise dans les investissements
                - Importance de la diversification
                """)
            
            st.markdown("""
            ### 📋 RECOMMANDATIONS STRATÉGIQUES
            
            1. **Diversification:** Répartition across secteurs et capitalisations
            2. **Approche Defensive:** Focus sur qualité et dividendes
            3. **Exposition Internationale:** Diversification géographique
            4. **Vision Long Terme:** Investissement discipliné
            5. **Surveillance Active:** Adaptation aux conditions de marché
            """)
        
        with tab6:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse en temps réel des performances du CAC 40 
            et de ses entreprises composantes.
            
            **Couverture:**
            - 40 entreprises du CAC 40 avec données détaillées
            - Analyse sectorielle et technique
            - Données historiques depuis 2020
            - Indicateurs de performance en temps réel
            
            **Sources des données:**
            - Euronext Paris
            - Bloomberg
            - Reuters
            - Données fondamentales des entreprises
            
            **⚠️ Avertissement:** 
            Les données présentées sont simulées pour la démonstration.
            Ce dashboard n'est pas un conseil en investissement.
            Les performances passées ne préjugent pas des performances futures.
            
            **🔒 Confidentialité:** 
            Toutes les données sont anonymisées et agrégées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - Site web: www.euronext.com
            - Email: info@euronext.com
            - Siège: Paris, France
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = CAC40Dashboard()
    dashboard.run_dashboard()