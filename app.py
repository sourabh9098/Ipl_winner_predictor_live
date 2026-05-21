# # import streamlit as st
# # import joblib
# # import plotly.express as px
# # import plotly.graph_objects as go
# # import time
# # import os  # ← add this line
# # from data_fetcher import (get_todays_match, IPL_TEAMS,
# #                           PLAYOFF_TEAMS, API_VENUE_MAP)



# # # ── Page Config ───────────────────────────────────────
# # st.set_page_config(
# #     page_title = "IPL 2026 Win Predictor",
# #     page_icon  = "🏏",
# #     layout     = "wide"
# # )

# # # ── Load Model ────────────────────────────────────────
# # @st.cache_resource
# # def load_model():
# #     model    = joblib.load("ipl_model.pkl")
# #     encoders = joblib.load("encoders.pkl")
# #     return model, encoders

# # model, encoders = load_model()

# # # ── Team Colors ───────────────────────────────────────
# # TEAM_COLORS = {
# #     'Chennai Super Kings'        : '#FFFF00',
# #     'Delhi Capitals'             : '#0078BC',
# #     'Gujarat Titans'             : '#1C1C1C',
# #     'Kolkata Knight Riders'      : '#3A225D',
# #     'Lucknow Super Giants'       : '#A0E3F0',
# #     'Mumbai Indians'             : '#004BA0',
# #     'Punjab Kings'               : "#FF010E",
# #     'Rajasthan Royals'           : '#FF69B4',
# #     'Royal Challengers Bengaluru': "#B30E13",
# #     'Sunrisers Hyderabad'        : '#FF822A',
# # }

# # # ── Predict Function ──────────────────────────────────
# # def predict_winner(team1, team2, toss_winner, toss_decision):
# #     try:
# #         t1 = encoders['team1'].transform([team1])[0]
# #         t2 = encoders['team2'].transform([team2])[0]
# #         tw = encoders['toss_winner'].transform([toss_winner])[0]
# #         td = encoders['toss_decision'].transform([toss_decision])[0]

# #         proba   = model.predict_proba([[t1, t2, tw, td]])[0]
# #         classes = encoders['match_winner'].classes_

# #         result = {}
# #         for team, prob in zip(classes, proba):
# #             if team in [team1, team2]:
# #                 result[team] = round(prob * 100, 1)

# #         # Normalize to 100%
# #         total = sum(result.values())
# #         if total > 0:
# #             result = {k: round(v/total*100, 1) for k, v in result.items()}

# #         return result
# #     except Exception as e:
# #         st.error(f"Prediction error: {e}")
# #         return None

# # # ── Header ────────────────────────────────────────────
# # st.markdown("""
# #     <h1 style='text-align:center; color:#FF6B35;'>
# #         🏏 IPL 2026 Win Probability Predictor
# #     </h1>
# #     <p style='text-align:center; color:gray;'>
# #         Powered by XGBoost | 980 Matches | Live CricBuzz API
# #     </p>
# #     <hr>
# # """, unsafe_allow_html=True)

# # # ── Tabs ──────────────────────────────────────────────
# # tab1, tab2, tab3 = st.tabs([
# #     "🏆 IPL 2026 Champion",
# #     "🔴 Today's Match",
# #     "🔮 Manual Prediction"
# # ])

# # # ════════════════════════════════════════════════════
# # # TAB 1 — IPL 2026 Champion Prediction
# # # ════════════════════════════════════════════════════
# # with tab1:
# #     st.subheader("🏆 IPL 2026 Champion Prediction")
# #     st.markdown("Based on simulating all playoff matchups using our ML model")

# #     # Current playoff teams
# #     st.markdown("**Current Playoff Contenders:**")
# #     cols = st.columns(5)
# #     for i, team in enumerate(PLAYOFF_TEAMS):
# #         with cols[i]:
# #             color = TEAM_COLORS.get(team, '#FF6B35')
# #             st.markdown(f"""
# #                 <div style='background:{color};padding:10px;
# #                 border-radius:8px;text-align:center;margin:2px;'>
# #                 <b style='color:black;font-size:11px;'>{team}</b>
# #                 </div>
# #             """, unsafe_allow_html=True)

# #     st.markdown("")

# #     if st.button("🎯 Predict IPL 2026 Champion", type="primary"):
# #         with st.spinner("Simulating playoff matchups..."):

# #             champion_probs = {}

# #             for team in PLAYOFF_TEAMS:
# #                 total_prob = 0
# #                 count      = 0

# #                 for opp in PLAYOFF_TEAMS:
# #                     if opp == team:
# #                         continue

# #                     # Simulate both toss scenarios
# #                     for toss_w in [team, opp]:
# #                         for toss_d in ['bat', 'field']:
# #                             result = predict_winner(
# #                                 team, opp, toss_w, toss_d
# #                             )
# #                             if result and team in result:
# #                                 total_prob += result[team]
# #                                 count      += 1

# #                 champion_probs[team] = round(
# #                     total_prob / count, 1
# #                 ) if count > 0 else 0

# #             # Sort
# #             champion_probs = dict(sorted(
# #                 champion_probs.items(),
# #                 key=lambda x: x[1],
# #                 reverse=True
# #             ))

# #             teams  = list(champion_probs.keys())
# #             probs  = list(champion_probs.values())
# #             colors = [TEAM_COLORS.get(t, '#FF6B35') for t in teams]

# #             # Bar chart
# #             fig_bar = go.Figure(go.Bar(
# #                 x            = teams,
# #                 y            = probs,
# #                 marker_color = colors,
# #                 text         = [f"{p}%" for p in probs],
# #                 textposition = 'outside'
# #             ))
# #             fig_bar.update_layout(
# #                 title         = "IPL 2026 Champion Win Probability",
# #                 yaxis_title   = "Win Probability (%)",
# #                 yaxis_range   = [0, max(probs) + 15],
# #                 plot_bgcolor  = "rgba(0,0,0,0)",
# #                 paper_bgcolor = "rgba(0,0,0,0)",
# #                 height        = 400,
# #             )
# #             st.plotly_chart(fig_bar, use_container_width=True)

# #             # Donut chart
# #             fig_pie = px.pie(
# #                 names  = teams,
# #                 values = probs,
# #                 color  = teams,
# #                 color_discrete_map = TEAM_COLORS,
# #                 hole   = 0.5,
# #                 title  = "Championship Share"
# #             )
# #             fig_pie.update_layout(
# #                 paper_bgcolor = "rgba(0,0,0,0)",
# #                 height        = 400
# #             )
# #             st.plotly_chart(fig_pie, use_container_width=True)

# #             # Rankings
# #             st.markdown("### 🏆 Predicted Final Rankings")
# #             medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
# #             for i, (team, prob) in enumerate(champion_probs.items()):
# #                 st.markdown(
# #                     f"{medals[i]} **{team}** "
# #                     f"— Championship probability: **{prob}%**"
# #                 )

# #             # Predicted champion
# #             champion = list(champion_probs.keys())[0]
# #             champ_prob = list(champion_probs.values())[0]
# #             st.success(
# #                 f"🏆 Predicted IPL 2026 Champion: "
# #                 f"**{champion}** with **{champ_prob}%** probability!"
# #             )

# # # ════════════════════════════════════════════════════
# # # TAB 2 — Today's Match
# # # ════════════════════════════════════════════════════
# # with tab2:
# #     st.subheader("🔴 Today's IPL Match")
# #     auto_refresh = st.toggle("Auto Refresh every 60s", value=False)

# #     with st.spinner("Loading today's match..."):
# #         match = get_todays_match()

# #     if match:
# #         team1         = match['team1']
# #         team2         = match['team2']
# #         match_type    = match.get('match_type', '')
# #         toss_winner   = match.get('toss_winner')
# #         toss_decision = match.get('toss_decision')

# #         # ← Badge AFTER toss extraction
# #         if match_type == 'LIVE':
# #             st.success("🔴 LIVE MATCH IN PROGRESS")
# #         elif match_type in ['PREVIEW', 'UPCOMING']:
# #             if toss_winner and toss_decision:
# #                 st.info("⚡ MATCH STARTING SOON — Toss Done!")
# #             else:
# #                 st.info("🕐 UPCOMING MATCH — Toss Not Announced Yet")
# #         elif match_type == 'CACHED':
# #             st.warning("📋 CACHED DATA — Limited API")
# #         else:
# #             st.warning("📋 MOST RECENT COMPLETED MATCH")

# #         # Match info
# #         st.markdown(f"### {team1} vs {team2}")
# #         st.markdown(f"**{match.get('match_desc','')}** | {match.get('venue','')}")
# #         st.markdown(f"**Status:** {match.get('status','')}")

# #         # Teams display
# #         col1, col2, col3 = st.columns([2, 1, 2])
# #         with col1:
# #             color1 = TEAM_COLORS.get(team1, '#FF6B35')
# #             st.markdown(f"""
# #                 <div style='background:{color1};padding:25px;
# #                 border-radius:12px;text-align:center;'>
# #                 <h3 style='color:black;margin:0;'>{team1}</h3>
# #                 </div>
# #             """, unsafe_allow_html=True)

# #         with col2:
# #             st.markdown("""
# #                 <div style='text-align:center;padding:25px;'>
# #                 <h2 style='margin:0;'>⚔️</h2>
# #                 <p style='margin:0;'>VS</p>
# #                 </div>
# #             """, unsafe_allow_html=True)

# #         with col3:
# #             color2 = TEAM_COLORS.get(team2, '#0078BC')
# #             st.markdown(f"""
# #                 <div style='background:{color2};padding:25px;
# #                 border-radius:12px;text-align:center;'>
# #                 <h3 style='color:white;margin:0;'>{team2}</h3>
# #                 </div>
# #             """, unsafe_allow_html=True)

# #         st.markdown("")

# #         if toss_winner and toss_decision:
# #             st.markdown(f"🎯 **Toss:** {toss_winner} won and chose to **{toss_decision}**")

# #             result = predict_winner(team1, team2, toss_winner, toss_decision)

# #             if result:
# #                 st.markdown("---")
# #                 st.subheader("Win Probability")

# #                 teams  = list(result.keys())
# #                 probs  = list(result.values())
# #                 colors = [TEAM_COLORS.get(t, '#FF6B35') for t in teams]

# #                 fig = go.Figure(go.Bar(
# #                     x            = probs,
# #                     y            = teams,
# #                     orientation  = 'h',
# #                     marker_color = colors,
# #                     text         = [f"{p}%" for p in probs],
# #                     textposition = 'outside'
# #                 ))
# #                 fig.update_layout(
# #                     xaxis_range   = [0, 110],
# #                     xaxis_title   = "Win Probability (%)",
# #                     plot_bgcolor  = "rgba(0,0,0,0)",
# #                     paper_bgcolor = "rgba(0,0,0,0)",
# #                     height        = 220,
# #                     margin        = dict(l=0, r=50, t=0, b=0)
# #                 )
# #                 st.plotly_chart(fig, use_container_width=True)

# #                 predicted_winner = max(result, key=result.get)
# #                 win_prob         = result[predicted_winner]
# #                 st.success(
# #                     f"🏆 Predicted Winner: **{predicted_winner}** "
# #                     f"with **{win_prob}%** probability"
# #                 )

# #         else:
# #             st.warning("⏳ Toss not done yet — prediction will appear after toss!")
# #             st.markdown("Refresh the page after toss is announced.")

# #         # Auto refresh explanation
# #         if auto_refresh:
# #             st.info("🔄 Auto refresh is ON — page will reload every 60s to check for toss/live updates")
# #             time.sleep(60)
# #             st.rerun()
        
# #         if st.button("🔄 Refresh Match Data"):
# #             # Delete cache to force fresh API call
# #             if os.path.exists("match_cache.json"):
# #                 os.remove("match_cache.json")
# #             st.rerun()

# #     else:
# #         st.error("Could not fetch match data. Check API connection.")
# # # ════════════════════════════════════════════════════
# # # TAB 3 — Manual Prediction
# # # ════════════════════════════════════════════════════
# # with tab3:
# #     st.subheader("🔮 Predict Any Match Manually")
# #     st.markdown("Select any two IPL teams to predict win probability")

# #     col1, col2 = st.columns(2)
# #     with col1:
# #         team1 = st.selectbox("Select Team 1", IPL_TEAMS, index=0)
# #     with col2:
# #         remaining = [t for t in IPL_TEAMS if t != team1]
# #         team2     = st.selectbox("Select Team 2", remaining, index=0)

# #     col3, col4 = st.columns(2)
# #     with col3:
# #         toss_winner   = st.selectbox("Toss Winner", [team1, team2])
# #     with col4:
# #         toss_decision = st.selectbox("Toss Decision", ["bat", "field"])

# #     if st.button("🎯 Predict Winner", type="primary"):
# #         result = predict_winner(team1, team2, toss_winner, toss_decision)

# #         if result:
# #             st.markdown("---")

# #             col1, col2 = st.columns(2)

# #             with col1:
# #                 # Donut chart
# #                 fig_pie = px.pie(
# #                     names  = list(result.keys()),
# #                     values = list(result.values()),
# #                     color  = list(result.keys()),
# #                     color_discrete_map = TEAM_COLORS,
# #                     hole   = 0.5,
# #                     title  = "Win Probability"
# #                 )
# #                 fig_pie.update_layout(
# #                     paper_bgcolor = "rgba(0,0,0,0)",
# #                     height        = 350
# #                 )
# #                 st.plotly_chart(fig_pie, use_container_width=True)

# #             with col2:
# #                 st.markdown("### Match Summary")
# #                 st.markdown(f"**{team1}** vs **{team2}**")
# #                 st.markdown(f"Toss: **{toss_winner}** chose to **{toss_decision}**")
# #                 st.markdown("---")

# #                 for team, prob in result.items():
# #                     color = TEAM_COLORS.get(team, '#FF6B35')
# #                     st.markdown(f"""
# #                         <div style='background:{color};padding:12px;
# #                         border-radius:8px;margin:8px 0;
# #                         text-align:center;'>
# #                         <b style='color:black;'>{team}: {prob}%</b>
# #                         </div>
# #                     """, unsafe_allow_html=True)

# #             predicted_winner = max(result, key=result.get)
# #             win_prob         = result[predicted_winner]
# #             st.success(
# #                 f"🏆 Predicted Winner: **{predicted_winner}** "
# #                 f"with **{win_prob}%** probability"
# #             )

# # # ── Footer ────────────────────────────────────────────
# # st.markdown("---")
# # st.markdown("""
# #     <p style='text-align:center;color:gray;font-size:12px;'>
# #     Built with ❤️ | XGBoost + Streamlit + CricBuzz API |
# #     IPL 2008-2026 | 980 Matches 
# #     </p>
# # """, unsafe_allow_html=True)








































# import streamlit as st
# import joblib
# import plotly.express as px
# import plotly.graph_objects as go
# import time
# import os
# from data_fetcher import (get_todays_match, IPL_TEAMS,
#                           PLAYOFF_TEAMS, API_VENUE_MAP)

# # ── Page Config ───────────────────────────────────────
# st.set_page_config(
#     page_title = "IPL 2026 Analytics",
#     page_icon  = "🏏",
#     layout     = "wide",
#     initial_sidebar_state = "collapsed"
# )

# # ── Custom CSS ────────────────────────────────────────
# st.markdown("""
# <style>
# /* Main background */
# .stApp {
#     background: linear-gradient(135deg, #0a1f0a 0%, #0d2b0d 50%, #0a1a1a 100%);
#     color: #e8f5e9;
# }

# /* Hide default streamlit elements */
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}

# /* Metric cards */
# .metric-card {
#     background: linear-gradient(145deg, #1a3d1a, #0f2d0f);
#     border: 1px solid #2d5a2d;
#     border-radius: 16px;
#     padding: 20px;
#     text-align: center;
#     box-shadow: 0 4px 15px rgba(0,200,0,0.1);
#     margin: 8px 0;
# }

# .metric-value {
#     font-size: 32px;
#     font-weight: 700;
#     color: #00e676;
#     margin: 0;
# }

# .metric-label {
#     font-size: 13px;
#     color: #81c784;
#     margin: 4px 0 0 0;
#     text-transform: uppercase;
#     letter-spacing: 1px;
# }

# /* Team cards */
# .team-card {
#     border-radius: 16px;
#     padding: 24px;
#     text-align: center;
#     box-shadow: 0 8px 32px rgba(0,0,0,0.3);
#     transition: transform 0.2s;
# }

# /* Live badge */
# .live-badge {
#     background: linear-gradient(90deg, #ff1744, #ff6b6b);
#     color: white;
#     padding: 6px 16px;
#     border-radius: 20px;
#     font-size: 13px;
#     font-weight: 600;
#     display: inline-block;
#     animation: pulse 1.5s infinite;
# }

# @keyframes pulse {
#     0% { opacity: 1; }
#     50% { opacity: 0.7; }
#     100% { opacity: 1; }
# }

# /* Section headers */
# .section-header {
#     color: #00e676;
#     font-size: 22px;
#     font-weight: 600;
#     border-left: 4px solid #00e676;
#     padding-left: 12px;
#     margin: 24px 0 16px 0;
# }

# /* Probability bar container */
# .prob-container {
#     background: #1a3d1a;
#     border-radius: 12px;
#     padding: 20px;
#     border: 1px solid #2d5a2d;
#     margin: 12px 0;
# }

# /* Tab styling */
# .stTabs [data-baseweb="tab-list"] {
#     background: #0f2d0f;
#     border-radius: 12px;
#     padding: 4px;
#     gap: 4px;
# }

# .stTabs [data-baseweb="tab"] {
#     background: transparent;
#     color: #81c784;
#     border-radius: 8px;
#     padding: 8px 20px;
#     font-weight: 500;
# }

# .stTabs [aria-selected="true"] {
#     background: #00e676 !important;
#     color: #0a1f0a !important;
# }

# /* Button styling */
# .stButton > button {
#     background: linear-gradient(135deg, #00c853, #00e676);
#     color: #0a1f0a;
#     border: none;
#     border-radius: 10px;
#     font-weight: 600;
#     padding: 10px 24px;
#     width: 100%;
#     transition: all 0.3s;
# }

# .stButton > button:hover {
#     background: linear-gradient(135deg, #00e676, #69f0ae);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 15px rgba(0,230,118,0.3);
# }

# /* Selectbox */
# .stSelectbox > div > div {
#     background: #1a3d1a;
#     border: 1px solid #2d5a2d;
#     border-radius: 10px;
#     color: #e8f5e9;
# }

# /* Info/Success/Warning boxes */
# .stSuccess {
#     background: #1a3d1a;
#     border: 1px solid #00e676;
#     border-radius: 12px;
# }

# /* Divider */
# .green-divider {
#     border: none;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, #00e676, transparent);
#     margin: 20px 0;
# }

# /* Winner card */
# .winner-card {
#     background: linear-gradient(135deg, #00c853, #00e676);
#     border-radius: 16px;
#     padding: 24px;
#     text-align: center;
#     color: #0a1f0a;
#     font-weight: 700;
#     font-size: 20px;
#     box-shadow: 0 8px 32px rgba(0,200,83,0.3);
#     margin: 16px 0;
# }

# /* Spinner */
# .stSpinner > div {
#     border-top-color: #00e676 !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # ── Load Model ────────────────────────────────────────
# @st.cache_resource
# def load_model():
#     model    = joblib.load("ipl_model.pkl")
#     encoders = joblib.load("encoders.pkl")
#     return model, encoders

# model, encoders = load_model()

# # ── Team Colors ───────────────────────────────────────
# TEAM_COLORS = {
#     'Chennai Super Kings'        : '#FFCA28',
#     'Delhi Capitals'             : '#1565C0',
#     'Gujarat Titans'             : '#37474F',
#     'Kolkata Knight Riders'      : '#6A1B9A',
#     'Lucknow Super Giants'       : '#00ACC1',
#     'Mumbai Indians'             : '#1565C0',
#     'Punjab Kings'               : '#C62828',
#     'Rajasthan Royals'           : '#AD1457',
#     'Royal Challengers Bengaluru': '#B71C1C',
#     'Sunrisers Hyderabad'        : '#E65100',
# }

# # ── Predict Function ──────────────────────────────────
# def predict_winner(team1, team2, toss_winner, toss_decision):
#     try:
#         t1 = encoders['team1'].transform([team1])[0]
#         t2 = encoders['team2'].transform([team2])[0]
#         tw = encoders['toss_winner'].transform([toss_winner])[0]
#         td = encoders['toss_decision'].transform([toss_decision])[0]

#         proba   = model.predict_proba([[t1, t2, tw, td]])[0]
#         classes = encoders['match_winner'].classes_

#         result = {}
#         for team, prob in zip(classes, proba):
#             if team in [team1, team2]:
#                 result[team] = round(prob * 100, 1)

#         total = sum(result.values())
#         if total > 0:
#             result = {k: round(v/total*100, 1) for k, v in result.items()}

#         return result
#     except Exception as e:
#         st.error(f"Prediction error: {e}")
#         return None

# # ── Header ────────────────────────────────────────────
# st.markdown("""
# <div style='text-align:center; padding: 20px 0 10px 0;'>
#     <h1 style='color:#00e676; font-size:42px; font-weight:800;
#     letter-spacing:2px; margin:0;'>
#     🏏 IPL 2026 ANALYTICS
#     </h1>
#     <p style='color:#81c784; font-size:15px; margin:8px 0 0 0;
#     letter-spacing:3px; text-transform:uppercase;'>
#     AI-Powered Match Prediction Dashboard
#     </p>
# </div>
# <div class='green-divider'></div>
# """, unsafe_allow_html=True)

# # ── Top Metrics Bar ───────────────────────────────────
# m1, m2, m3, m4 = st.columns(4)

# with m1:
#     st.markdown("""
#     <div class='metric-card'>
#         <p class='metric-value'>980</p>
#         <p class='metric-label'>Matches Trained</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m2:
#     st.markdown("""
#     <div class='metric-card'>
#         <p class='metric-value'>58%</p>
#         <p class='metric-label'>Model Accuracy</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m3:
#     st.markdown("""
#     <div class='metric-card'>
#         <p class='metric-value'>2008-26</p>
#         <p class='metric-label'>Data Range</p>
#     </div>
#     """, unsafe_allow_html=True)

# with m4:
#     st.markdown("""
#     <div class='metric-card'>
#         <p class='metric-value'>XGBoost</p>
#         <p class='metric-label'>Algorithm</p>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# # ── Tabs ──────────────────────────────────────────────
# tab1, tab2, tab3 = st.tabs([
#     "🔴  Today's Match",
#     "🏆  IPL 2026 Champion",
#     "🔮  Manual Prediction"
# ])

# # ════════════════════════════════════════════════════
# # TAB 1 — Today's Match (First tab now!)
# # ════════════════════════════════════════════════════
# with tab1:

#     # Auto load match
#     with st.spinner(""):
#         match = get_todays_match()

#     if match:
#         team1         = match['team1']
#         team2         = match['team2']
#         match_type    = match.get('match_type', '')
#         toss_winner   = match.get('toss_winner')
#         toss_decision = match.get('toss_decision')

#         # ── Status Badge ──
#         col_badge, col_refresh = st.columns([3, 1])

#         with col_badge:
#             if match_type == 'LIVE':
#                 st.markdown("""
#                 <span class='live-badge'>🔴 LIVE NOW</span>
#                 """, unsafe_allow_html=True)
#             elif match_type in ['PREVIEW', 'UPCOMING']:
#                 if toss_winner:
#                     st.info("⚡ Match Starting Soon — Toss Complete!")
#                 else:
#                     st.info("🕐 Upcoming Match — Toss Not Announced")
#             else:
#                 st.warning("📋 Most Recent Match Result")

#         with col_refresh:
#             if st.button("🔄 Refresh"):
#                 if os.path.exists("match_cache.json"):
#                     os.remove("match_cache.json")
#                 st.rerun()

#         st.markdown("")

#         # ── Match Header ──
#         st.markdown(f"""
#         <div style='text-align:center; margin: 10px 0;'>
#             <span style='color:#81c784; font-size:14px;
#             text-transform:uppercase; letter-spacing:2px;'>
#             {match.get('match_desc','')} •
#             {match.get('venue','')}
#             </span>
#         </div>
#         """, unsafe_allow_html=True)

#         # ── Team Cards ──
#         col1, col2, col3 = st.columns([5, 2, 5])

#         with col1:
#             color1 = TEAM_COLORS.get(team1, '#00e676')
#             st.markdown(f"""
#             <div class='team-card' style='background:
#             linear-gradient(135deg, {color1}22, {color1}44);
#             border: 2px solid {color1};'>
#                 <div style='font-size:40px;'>🏏</div>
#                 <h2 style='color:{color1}; margin:8px 0 0 0;
#                 font-size:20px;'>{team1}</h2>
#             </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown("""
#             <div style='text-align:center; padding:30px 0;'>
#                 <div style='color:#00e676; font-size:28px;
#                 font-weight:800;'>VS</div>
#             </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             color2 = TEAM_COLORS.get(team2, '#ff6b35')
#             st.markdown(f"""
#             <div class='team-card' style='background:
#             linear-gradient(135deg, {color2}22, {color2}44);
#             border: 2px solid {color2};'>
#                 <div style='font-size:40px;'>🏏</div>
#                 <h2 style='color:{color2}; margin:8px 0 0 0;
#                 font-size:20px;'>{team2}</h2>
#             </div>
#             """, unsafe_allow_html=True)

#         st.markdown("<div class='green-divider'></div>",
#                     unsafe_allow_html=True)

#         # ── Prediction Section ──
#         if toss_winner and toss_decision:

#             # Toss info
#             st.markdown(f"""
#             <div style='background:#1a3d1a; border-radius:12px;
#             padding:14px 20px; border:1px solid #2d5a2d;
#             margin-bottom:16px;'>
#             🎯 <b style='color:#00e676;'>Toss:</b>
#             <span style='color:#e8f5e9;'>{toss_winner}</span>
#             won and elected to
#             <span style='color:#00e676; font-weight:600;'>
#             {toss_decision}</span>
#             </div>
#             """, unsafe_allow_html=True)

#             result = predict_winner(
#                 team1, team2, toss_winner, toss_decision
#             )

#             if result:
#                 teams  = list(result.keys())
#                 probs  = list(result.values())
#                 colors = [TEAM_COLORS.get(t, '#00e676') for t in teams]

#                 # ── Big Probability Display ──
#                 p_col1, p_col2 = st.columns(2)

#                 for i, (team, prob) in enumerate(result.items()):
#                     col = p_col1 if i == 0 else p_col2
#                     color = TEAM_COLORS.get(team, '#00e676')

#                     with col:
#                         st.markdown(f"""
#                         <div style='background:linear-gradient(135deg,
#                         {color}15, {color}30);
#                         border:2px solid {color};
#                         border-radius:16px; padding:24px;
#                         text-align:center;'>
#                             <div style='font-size:52px; font-weight:800;
#                             color:{color};'>{prob}%</div>
#                             <div style='color:#e8f5e9; font-size:16px;
#                             margin-top:8px;'>{team}</div>
#                             <div style='color:#81c784; font-size:13px;'>
#                             Win Probability</div>
#                         </div>
#                         """, unsafe_allow_html=True)

#                 st.markdown("")

#                 # ── Horizontal Bar Chart ──
#                 fig = go.Figure()

#                 for i, (team, prob) in enumerate(result.items()):
#                     color = TEAM_COLORS.get(team, '#00e676')
#                     fig.add_trace(go.Bar(
#                         name         = team,
#                         x            = [prob],
#                         y            = [team],
#                         orientation  = 'h',
#                         marker_color = color,
#                         text         = f"{prob}%",
#                         textposition = 'inside',
#                         textfont     = dict(
#                             size  = 18,
#                             color = 'white'
#                         ),
#                         hovertemplate = f"<b>{team}</b><br>"
#                                        f"Win Probability: {prob}%"
#                                        f"<extra></extra>"
#                     ))

#                 fig.update_layout(
#                     plot_bgcolor  = "rgba(0,0,0,0)",
#                     paper_bgcolor = "rgba(0,0,0,0)",
#                     font_color    = "#e8f5e9",
#                     height        = 160,
#                     margin        = dict(l=0, r=20, t=10, b=10),
#                     showlegend    = False,
#                     xaxis = dict(
#                         range      = [0, 100],
#                         showgrid   = False,
#                         showticklabels = False,
#                         zeroline   = False,
#                     ),
#                     yaxis = dict(
#                         showgrid   = False,
#                         zeroline   = False,
#                         tickfont   = dict(size=14)
#                     ),
#                     bargap = 0.3
#                 )
#                 st.plotly_chart(fig, use_container_width=True)

#                 # ── Donut Chart ──
#                 fig_donut = go.Figure(go.Pie(
#                     labels    = teams,
#                     values    = probs,
#                     hole      = 0.65,
#                     marker    = dict(
#                         colors = colors,
#                         line   = dict(
#                             color = '#0a1f0a',
#                             width = 3
#                         )
#                     ),
#                     textinfo      = 'label+percent',
#                     textfont_size = 14,
#                     textfont_color= ['white', 'white'],
#                     hovertemplate = "<b>%{label}</b><br>"
#                                    "Win Probability: %{value}%"
#                                    "<extra></extra>"
#                 ))

#                 # Center annotation
#                 predicted_winner = max(result, key=result.get)
#                 win_prob         = result[predicted_winner]

#                 fig_donut.update_layout(
#                     plot_bgcolor  = "rgba(0,0,0,0)",
#                     paper_bgcolor = "rgba(0,0,0,0)",
#                     font_color    = "#e8f5e9",
#                     height        = 320,
#                     margin        = dict(l=0, r=0, t=20, b=0),
#                     showlegend    = False,
#                     annotations   = [dict(
#                         text      = f"<b>{win_prob}%</b>",
#                         x         = 0.5,
#                         y         = 0.5,
#                         font_size = 28,
#                         font_color= "#00e676",
#                         showarrow = False
#                     )]
#                 )
#                 st.plotly_chart(fig_donut, use_container_width=True)

#                 # ── Winner Banner ──
#                 st.markdown(f"""
#                 <div class='winner-card'>
#                     🏆 Predicted Winner: {predicted_winner}
#                     &nbsp;|&nbsp; {win_prob}% Win Probability
#                 </div>
#                 """, unsafe_allow_html=True)

#         else:
#             st.markdown("""
#             <div style='background:#1a3d1a; border:1px solid #2d5a2d;
#             border-radius:12px; padding:30px; text-align:center;'>
#                 <div style='font-size:48px;'>⏳</div>
#                 <h3 style='color:#00e676;'>Waiting for Toss</h3>
#                 <p style='color:#81c784;'>
#                 Prediction will appear automatically after toss
#                 is announced. Enable auto-refresh below.
#                 </p>
#             </div>
#             """, unsafe_allow_html=True)

#         # ── Auto Refresh ──
#         st.markdown("")
#         auto_refresh = st.toggle("🔄 Auto Refresh every 60s", value=False)
#         if auto_refresh:
#             st.markdown("""
#             <div style='color:#81c784; font-size:13px;
#             text-align:center;'>
#             ✅ Auto refresh active —
#             checking for toss/live updates every 60s
#             </div>
#             """, unsafe_allow_html=True)
#             time.sleep(60)
#             st.rerun()

#     else:
#         st.markdown("""
#         <div style='text-align:center; padding:60px 20px;'>
#             <div style='font-size:64px;'>🏏</div>
#             <h2 style='color:#00e676;'>No Match Data Available</h2>
#             <p style='color:#81c784;'>
#             API connection issue. Check your API key.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

# # ════════════════════════════════════════════════════
# # TAB 2 — IPL 2026 Champion
# # ════════════════════════════════════════════════════
# with tab2:
#     st.markdown("""
#     <div class='section-header'>IPL 2026 Playoff Contenders</div>
#     """, unsafe_allow_html=True)

#     # Playoff teams display
#     cols = st.columns(5)
#     for i, team in enumerate(PLAYOFF_TEAMS):
#         with cols[i]:
#             color = TEAM_COLORS.get(team, '#00e676')
#             st.markdown(f"""
#             <div style='background:linear-gradient(135deg,
#             {color}22, {color}44);
#             border:1px solid {color};
#             border-radius:12px; padding:14px;
#             text-align:center; margin:4px 0;'>
#                 <div style='color:{color}; font-weight:700;
#                 font-size:13px;'>{team}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("<div class='green-divider'></div>",
#                 unsafe_allow_html=True)

#     if st.button("🎯 Predict IPL 2026 Champion", type="primary"):
#         with st.spinner("Simulating all playoff matchups..."):

#             champion_probs = {}

#             for team in PLAYOFF_TEAMS:
#                 total_prob = 0
#                 count      = 0

#                 for opp in PLAYOFF_TEAMS:
#                     if opp == team:
#                         continue
#                     for toss_w in [team, opp]:
#                         for toss_d in ['bat', 'field']:
#                             result = predict_winner(
#                                 team, opp, toss_w, toss_d
#                             )
#                             if result and team in result:
#                                 total_prob += result[team]
#                                 count      += 1

#                 champion_probs[team] = round(
#                     total_prob/count, 1
#                 ) if count > 0 else 0

#             # Sort
#             champion_probs = dict(sorted(
#                 champion_probs.items(),
#                 key   = lambda x: x[1],
#                 reverse = True
#             ))

#             teams  = list(champion_probs.keys())
#             probs  = list(champion_probs.values())
#             colors = [TEAM_COLORS.get(t, '#00e676') for t in teams]

#             # ── Ranking Cards ──
#             st.markdown("""
#             <div class='section-header'>Championship Rankings</div>
#             """, unsafe_allow_html=True)

#             medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
#             for i, (team, prob) in enumerate(
#                 champion_probs.items()
#             ):
#                 color = TEAM_COLORS.get(team, '#00e676')
#                 bar_width = int(prob * 2)

#                 st.markdown(f"""
#                 <div style='background:linear-gradient(135deg,
#                 {color}15, {color}25);
#                 border:1px solid {color}66;
#                 border-radius:12px; padding:16px 20px;
#                 margin:8px 0; display:flex;
#                 align-items:center; gap:16px;'>
#                     <span style='font-size:24px;'>{medals[i]}</span>
#                     <div style='flex:1;'>
#                         <div style='color:#e8f5e9; font-weight:600;
#                         font-size:16px;'>{team}</div>
#                         <div style='background:#0a1f0a;
#                         border-radius:4px; height:8px;
#                         margin-top:8px; overflow:hidden;'>
#                             <div style='background:{color};
#                             height:100%; width:{bar_width}%;
#                             border-radius:4px;'></div>
#                         </div>
#                     </div>
#                     <span style='color:{color}; font-size:24px;
#                     font-weight:800;'>{prob}%</span>
#                 </div>
#                 """, unsafe_allow_html=True)

#             st.markdown("")

#             # ── Bar Chart ──
#             fig_bar = go.Figure(go.Bar(
#                 x            = teams,
#                 y            = probs,
#                 marker_color = colors,
#                 text         = [f"{p}%" for p in probs],
#                 textposition = 'outside',
#                 textfont     = dict(
#                     color = '#00e676',
#                     size  = 14
#                 ),
#                 hovertemplate = "<b>%{x}</b><br>"
#                                "Championship Prob: %{y}%"
#                                "<extra></extra>"
#             ))

#             fig_bar.update_layout(
#                 plot_bgcolor  = "rgba(0,0,0,0)",
#                 paper_bgcolor = "rgba(0,0,0,0)",
#                 font_color    = "#e8f5e9",
#                 height        = 380,
#                 yaxis_range   = [0, max(probs) + 15],
#                 yaxis = dict(
#                     showgrid    = True,
#                     gridcolor   = "#1a3d1a",
#                     title       = "Win Probability (%)"
#                 ),
#                 xaxis = dict(
#                     showgrid    = False,
#                     tickangle   = -15
#                 ),
#                 margin = dict(l=0, r=0, t=40, b=0),
#             )
#             st.plotly_chart(fig_bar, use_container_width=True)

#             # ── Donut Chart ──
#             fig_pie = go.Figure(go.Pie(
#                 labels    = teams,
#                 values    = probs,
#                 hole      = 0.5,
#                 marker    = dict(
#                     colors = colors,
#                     line   = dict(color='#0a1f0a', width=3)
#                 ),
#                 textinfo      = 'label+percent',
#                 textfont_size = 13,
#                 hovertemplate = "<b>%{label}</b><br>"
#                                "Championship Share: %{value}%"
#                                "<extra></extra>"
#             ))

#             champion     = teams[0]
#             champ_prob   = probs[0]
#             champ_color  = TEAM_COLORS.get(champion, '#00e676')

#             fig_pie.update_layout(
#                 plot_bgcolor  = "rgba(0,0,0,0)",
#                 paper_bgcolor = "rgba(0,0,0,0)",
#                 font_color    = "#e8f5e9",
#                 height        = 380,
#                 showlegend    = True,
#                 legend        = dict(
#                     bgcolor    = "rgba(0,0,0,0)",
#                     font_color = "#e8f5e9"
#                 ),
#                 margin     = dict(l=0, r=0, t=20, b=0),
#                 annotations = [dict(
#                     text      = f"<b>{champ_prob}%</b>",
#                     font_size = 26,
#                     font_color= champ_color,
#                     showarrow = False
#                 )]
#             )
#             st.plotly_chart(fig_pie, use_container_width=True)

#             # ── Champion Banner ──
#             st.markdown(f"""
#             <div class='winner-card' style='font-size:22px;'>
#                 🏆 Predicted IPL 2026 Champion:
#                 {champion} — {champ_prob}%
#             </div>
#             """, unsafe_allow_html=True)

# # ════════════════════════════════════════════════════
# # TAB 3 — Manual Prediction
# # ════════════════════════════════════════════════════
# with tab3:
#     st.markdown("""
#     <div class='section-header'>Match Simulator</div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         team1 = st.selectbox(
#             "🏏 Select Team 1", IPL_TEAMS, index=0
#         )
#     with col2:
#         remaining = [t for t in IPL_TEAMS if t != team1]
#         team2     = st.selectbox(
#             "🏏 Select Team 2", remaining, index=0
#         )

#     col3, col4 = st.columns(2)
#     with col3:
#         toss_winner = st.selectbox(
#             "🪙 Toss Winner", [team1, team2]
#         )
#     with col4:
#         toss_decision = st.selectbox(
#             "⚡ Toss Decision", ["bat", "field"]
#         )

#     st.markdown("")

#     if st.button("🎯 Predict Match Winner", type="primary"):
#         result = predict_winner(
#             team1, team2, toss_winner, toss_decision
#         )

#         if result:
#             st.markdown("<div class='green-divider'></div>",
#                         unsafe_allow_html=True)

#             # ── Probability Cards ──
#             p1, p2 = st.columns(2)
#             for i, (team, prob) in enumerate(result.items()):
#                 col  = p1 if i == 0 else p2
#                 color = TEAM_COLORS.get(team, '#00e676')
#                 with col:
#                     st.markdown(f"""
#                     <div style='background:linear-gradient(135deg,
#                     {color}15, {color}35);
#                     border:2px solid {color};
#                     border-radius:16px; padding:28px;
#                     text-align:center;'>
#                         <div style='font-size:56px; font-weight:800;
#                         color:{color};'>{prob}%</div>
#                         <div style='color:#e8f5e9; font-size:17px;
#                         margin-top:8px; font-weight:500;'>{team}</div>
#                     </div>
#                     """, unsafe_allow_html=True)

#             st.markdown("")

#             # ── Charts side by side ──
#             ch1, ch2 = st.columns(2)

#             teams  = list(result.keys())
#             probs  = list(result.values())
#             colors = [TEAM_COLORS.get(t, '#00e676') for t in teams]

#             with ch1:
#                 # Bar chart
#                 fig_bar = go.Figure(go.Bar(
#                     x            = probs,
#                     y            = teams,
#                     orientation  = 'h',
#                     marker_color = colors,
#                     text         = [f"{p}%" for p in probs],
#                     textposition = 'inside',
#                     textfont     = dict(size=16, color='white'),
#                 ))
#                 fig_bar.update_layout(
#                     plot_bgcolor  = "rgba(0,0,0,0)",
#                     paper_bgcolor = "rgba(0,0,0,0)",
#                     font_color    = "#e8f5e9",
#                     height        = 220,
#                     xaxis = dict(
#                         range    = [0, 100],
#                         showgrid = False,
#                         showticklabels = False
#                     ),
#                     yaxis  = dict(showgrid=False),
#                     margin = dict(l=0, r=20, t=10, b=10),
#                     showlegend = False,
#                     bargap = 0.3
#                 )
#                 st.plotly_chart(fig_bar, use_container_width=True)

#             with ch2:
#                 # Donut
#                 predicted_winner = max(result, key=result.get)
#                 win_prob         = result[predicted_winner]

#                 fig_donut = go.Figure(go.Pie(
#                     labels    = teams,
#                     values    = probs,
#                     hole      = 0.6,
#                     marker    = dict(
#                         colors = colors,
#                         line   = dict(color='#0a1f0a', width=3)
#                     ),
#                     textinfo      = 'percent',
#                     textfont_size = 14,
#                 ))
#                 fig_donut.update_layout(
#                     plot_bgcolor  = "rgba(0,0,0,0)",
#                     paper_bgcolor = "rgba(0,0,0,0)",
#                     font_color    = "#e8f5e9",
#                     height        = 220,
#                     showlegend    = False,
#                     margin        = dict(l=0, r=0, t=10, b=10),
#                     annotations   = [dict(
#                         text       = f"<b>{win_prob}%</b>",
#                         font_size  = 22,
#                         font_color = "#00e676",
#                         showarrow  = False
#                     )]
#                 )
#                 st.plotly_chart(
#                     fig_donut, use_container_width=True
#                 )

#             # ── Winner Banner ──
#             st.markdown(f"""
#             <div class='winner-card'>
#                 🏆 Predicted Winner: {predicted_winner}
#                 &nbsp;|&nbsp; {win_prob}% Probability
#             </div>
#             """, unsafe_allow_html=True)

# # ── Footer ────────────────────────────────────────────
# st.markdown("<div class='green-divider'></div>",
#             unsafe_allow_html=True)
# st.markdown("""
# <div style='text-align:center; padding:16px 0;'>
#     <p style='color:#2d5a2d; font-size:13px; margin:0;'>
#     Built with ❤️ &nbsp;|&nbsp;
#     XGBoost + Streamlit + CricBuzz API &nbsp;|&nbsp;
#     IPL 2008–2026 &nbsp;|&nbsp; 980 Matches &nbsp;|&nbsp;
#     58% Accuracy
#     </p>
# </div>
# """, unsafe_allow_html=True)





































import streamlit as st
import joblib
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from data_fetcher import (get_todays_match, IPL_TEAMS,
                          PLAYOFF_TEAMS, API_VENUE_MAP)

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="IPL 2026 Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# # ── Team Data: Colors + Logos + Short Names ───────────
# TEAM_DATA = {
#     'Chennai Super Kings': {
#         'color': '#F5A800',
#         'secondary': '#1A237E',
#         'short': 'CSK',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/2/2b/Chennai_Super_Kings_Logo.svg',
#     },
#     'Delhi Capitals': {
#         'color': '#004C97',
#         'secondary': '#EF1C25',
#         'short': 'DC',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/c/c2/Delhi_Capitals_Logo.svg',
#     },
#     'Gujarat Titans': {
#         'color': '#1C1C4A',
#         'secondary': '#A5ACAF',
#         'short': 'GT',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg',
#     },
#     'Kolkata Knight Riders': {
#         'color': '#3A225D',
#         'secondary': '#F5A800',
#         'short': 'KKR',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg',
#     },
#     'Lucknow Super Giants': {
#         'color': '#A4DDED',
#         'secondary': '#2596BE',
#         'short': 'LSG',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/a/a6/Lucknow_Super_Giants_Logo.svg',
#     },
#     'Mumbai Indians': {
#         'color': '#004BA0',
#         'secondary': '#D1AB3E',
#         'short': 'MI',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg',
#     },
#     'Punjab Kings': {
#         'color': '#ED1B24',
#         'secondary': '#A7A9AC',
#         'short': 'PBKS',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg',
#     },
#     'Rajasthan Royals': {
#         'color': '#E73B6D',
#         'secondary': '#2D4EA2',
#         'short': 'RR',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/6/60/Rajasthan_Royals_Logo.svg',
#     },
#     'Royal Challengers Bengaluru': {
#         'color': '#EC1C24',
#         'secondary': '#2E0A16',
#         'short': 'RCB',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/2/2a/Royal_Challengers_Bangalore_2020.svg',
#     },
#     'Sunrisers Hyderabad': {
#         'color': '#F7A721',
#         'secondary': '#E2541A',
#         'short': 'SRH',
#         'logo': 'https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg',
#     },
# }


TEAM_DATA = {
    'Chennai Super Kings': {
        'color': '#F5A800',
        'secondary': '#1A237E',
        'short': 'CSK',
        'logo': 'https://documents.iplt20.com/ipl/CSK/Logos/Logooutline/CSKoutline.png',
    },

    'Delhi Capitals': {
        'color': '#004C97',
        'secondary': '#EF1C25',
        'short': 'DC',
        'logo': 'https://documents.iplt20.com/ipl/DC/Logos/LogoOutline/DCoutline.png',
    },

    'Gujarat Titans': {
        'color': '#1C1C4A',
        'secondary': '#A5ACAF',
        'short': 'GT',
        'logo': 'https://documents.iplt20.com/ipl/GT/Logos/Logooutline/GToutline.png',
    },

    'Kolkata Knight Riders': {
        'color': '#3A225D',
        'secondary': '#F5A800',
        'short': 'KKR',
        'logo': 'https://documents.iplt20.com/ipl/KKR/Logos/Logooutline/KKRoutline.png',
    },

    'Lucknow Super Giants': {
        'color': '#A4DDED',
        'secondary': '#2596BE',
        'short': 'LSG',
        'logo': 'https://documents.iplt20.com/ipl/LSG/Logos/Logooutline/LSGoutline.png',
    },

    'Mumbai Indians': {
        'color': '#004BA0',
        'secondary': '#D1AB3E',
        'short': 'MI',
        'logo': 'https://documents.iplt20.com/ipl/MI/Logos/Logooutline/MIoutline.png',
    },

    'Punjab Kings': {
        'color': '#ED1B24',
        'secondary': '#A7A9AC',
        'short': 'PBKS',
        'logo': 'https://documents.iplt20.com/ipl/PBKS/Logos/Logooutline/PBKSoutline.png',
    },

    'Rajasthan Royals': {
        'color': '#E73B6D',
        'secondary': '#2D4EA2',
        'short': 'RR',
        'logo': 'https://documents.iplt20.com/ipl/RR/Logos/Logooutline/RRoutline.png',
    },

    'Royal Challengers Bengaluru': {
        'color': '#EC1C24',
        'secondary': '#2E0A16',
        'short': 'RCB',
        'logo': 'https://documents.iplt20.com/ipl/RCB/Logos/Logooutline/RCBoutline.png',
    },

    'Sunrisers Hyderabad': {
        'color': '#F7A721',
        'secondary': '#E2541A',
        'short': 'SRH',
        'logo': 'https://documents.iplt20.com/ipl/SRH/Logos/Logooutline/SRHoutline.png',
    },
}







def get_color(team):
    return TEAM_DATA.get(team, {}).get('color', '#00e676')

def get_short(team):
    return TEAM_DATA.get(team, {}).get('short', team[:3].upper())

def get_logo(team):
    return TEAM_DATA.get(team, {}).get('logo', '')

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Barlow+Condensed:wght@400;600;700;800&display=swap');

* { font-family: 'Barlow Condensed', sans-serif; }

.stApp {
    background: #050D18;
    color: #E8EDF5;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── IPL Header Bar ── */
.ipl-header {
    background: linear-gradient(90deg, #0D1B2E 0%, #162035 50%, #0D1B2E 100%);
    border-bottom: 3px solid #D4AF37;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.ipl-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #D4AF37, #F5D978, #D4AF37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-transform: uppercase;
    margin: 0;
}

.ipl-subtitle {
    color: #8899BB;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 4px 0 0 0;
}

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(145deg, #0F1E35, #0A1626);
    border: 1px solid #1E3A5F;
    border-top: 3px solid #D4AF37;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #D4AF37;
    letter-spacing: 1px;
    margin: 0;
}

.metric-label {
    font-size: 11px;
    color: #5577AA;
    margin: 4px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── Team Card ── */
.team-card {
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

/* ── Live Badge ── */
.live-badge {
    background: linear-gradient(90deg, #C0392B, #E74C3C);
    color: white;
    padding: 5px 14px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: inline-block;
    animation: blink 1.2s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.6; }
}

/* ── Section Header ── */
.section-header {
    color: #D4AF37;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-left: 4px solid #D4AF37;
    padding-left: 14px;
    margin: 24px 0 16px 0;
}

/* ── Gold Divider ── */
.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #D4AF37 30%, #D4AF37 70%, transparent);
    margin: 20px 0;
    opacity: 0.5;
}

/* ── Winner Card ── */
.winner-card {
    background: linear-gradient(135deg, #1A0A00, #2D1500);
    border: 2px solid #D4AF37;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    color: #D4AF37;
    font-weight: 800;
    font-size: 22px;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow: 0 0 40px rgba(212,175,55,0.2);
    margin: 16px 0;
}

/* ── Key Insight Box ── */
.insight-box {
    background: linear-gradient(135deg, #071A0A, #0A2210);
    border: 1px solid #1E5C2A;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
}

.insight-title {
    color: #2ECC71;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.insight-text {
    color: #A8C8B0;
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
}

/* ── Probability Box ── */
.prob-box {
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    border: 2px solid;
}

.prob-percent {
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1;
}

.prob-team {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 8px;
    color: #E8EDF5;
}

.prob-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
    color: #8899BB;
}

/* ── Pre-toss Input Box ── */
.pretoss-box {
    background: linear-gradient(135deg, #0F1E35, #0A1626);
    border: 1px solid #1E3A5F;
    border-radius: 14px;
    padding: 24px;
    margin: 16px 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0A1626;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E3A5F;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #5577AA;
    border-radius: 8px;
    padding: 8px 22px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #D4AF37, #F5D978) !important;
    color: #050D18 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #C9A227, #D4AF37, #E8C84A);
    color: #050D18;
    border: none;
    border-radius: 8px;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 12px 28px;
    width: 100%;
    transition: all 0.3s;
    font-family: 'Barlow Condensed', sans-serif;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #E8C84A, #F5D978);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(212,175,55,0.35);
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0F1E35;
    border: 1px solid #1E3A5F;
    border-radius: 8px;
    color: #E8EDF5;
    font-family: 'Barlow Condensed', sans-serif;
}

.stSelectbox label {
    color: #8899BB !important;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Toggle ── */
.stToggle label {
    color: #8899BB !important;
    font-size: 13px;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #D4AF37 !important;
}

/* ── Info/Warning boxes ── */
.stAlert {
    background: #0F1E35 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
}

/* ── Points Table ── */
.pts-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 15px;
}

.pts-table th {
    background: #0A1626;
    color: #D4AF37;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 12px 10px;
    border-bottom: 2px solid #D4AF37;
    text-align: center;
}

.pts-table td {
    padding: 11px 10px;
    border-bottom: 1px solid #0F1E35;
    text-align: center;
    color: #C8D8E8;
}

.pts-table tr:hover td { background: #0F1E35; }

.pts-table .qualify-yes { color: #2ECC71; font-size: 18px; }
.pts-table .qualify-no  { color: #E74C3C; font-size: 18px; }
.pts-table .rank-gold   { color: #D4AF37; font-weight: 800; }

.pts-table .team-logo-sm {
    width: 28px;
    height: 28px;
    object-fit: contain;
    vertical-align: middle;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────
@st.cache_resource
def load_model():
    model    = joblib.load("ipl_model.pkl")
    encoders = joblib.load("encoders.pkl")
    return model, encoders

model, encoders = load_model()

# ── Predict Function (accepts None toss for pre-toss avg) ─────
def predict_winner(team1, team2, toss_winner=None, toss_decision=None):
    """
    If toss_winner / toss_decision are None, averages all 4 toss scenarios
    to give a pre-toss prediction.
    """
    try:
        if toss_winner and toss_decision:
            scenarios = [(toss_winner, toss_decision)]
        else:
            # Average over all 4 scenarios
            scenarios = [
                (team1, 'bat'), (team1, 'field'),
                (team2, 'bat'), (team2, 'field'),
            ]

        cumulative = {team1: 0.0, team2: 0.0}
        count = 0

        for tw, td in scenarios:
            t1 = encoders['team1'].transform([team1])[0]
            t2 = encoders['team2'].transform([team2])[0]
            tw_enc = encoders['toss_winner'].transform([tw])[0]
            td_enc = encoders['toss_decision'].transform([td])[0]

            proba   = model.predict_proba([[t1, t2, tw_enc, td_enc]])[0]
            classes = encoders['match_winner'].classes_

            for team, prob in zip(classes, proba):
                if team in [team1, team2]:
                    cumulative[team] += prob
            count += 1

        result = {k: round(v / count * 100) for k, v in cumulative.items()}

        # Normalise to sum to 100
        total = sum(result.values())
        if total > 0:
            result = {k: round(v / total * 100) for k, v in result.items()}

        return result
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# ════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════
st.markdown("""
<div class='ipl-header'>
    <div>
        <p class='ipl-title'>🏏 IPL 2026 Analytics</p>
        <p class='ipl-subtitle'>AI-Powered Match Prediction Dashboard</p>
    </div>
    <div style='text-align:right;'>
        <p style='color:#D4AF37; font-size:13px; letter-spacing:2px;
        text-transform:uppercase; margin:0;'>XGBoost Model</p>
        <p style='color:#5577AA; font-size:12px; margin:4px 0 0 0;'>
        2008 – 2026 · 980 Matches</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top Metrics ───────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
for col, val, label in zip(
    [m1, m2, m3, m4],
    [ "IPL 2026","980", "2008–26", "XGBoost"],
    [ "Live Match Prediction","Matches Trained", "Data Range", "Algorithm"]
):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <p class='metric-value'>{val}</p>
            <p class='metric-label'>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔴  Today's Match",
    "🏆  IPL 2026 Champion",
    "🔮  Manual Prediction",
])

# ════════════════════════════════════════════════════
# TAB 1 — Today's Match
# ════════════════════════════════════════════════════
with tab1:
    with st.spinner("Fetching today's match..."):
        match = get_todays_match()

    if match:
        team1         = match['team1']
        team2         = match['team2']
        match_type    = match.get('match_type', '')
        toss_winner   = match.get('toss_winner')
        toss_decision = match.get('toss_decision')

        c_badge, c_refresh = st.columns([4, 1])
        with c_badge:
            if match_type == 'LIVE':
                st.markdown("<span class='live-badge'>🔴 LIVE NOW</span>",
                            unsafe_allow_html=True)
            elif match_type in ['PREVIEW', 'UPCOMING']:
                if toss_winner:
                    st.info("⚡ Match Starting Soon — Toss Complete!")
                else:
                    st.info("🕐 Upcoming Match — Toss Not Yet Announced")
            else:
                st.warning("📋 Most Recent Match Result")

        with c_refresh:
            if st.button("🔄 Refresh"):
                if os.path.exists("match_cache.json"):
                    os.remove("match_cache.json")
                st.rerun()

        # ── Match Desc ──
        st.markdown(f"""
        <div style='text-align:center; margin:14px 0 6px 0;'>
            <span style='color:#5577AA; font-size:13px;
            text-transform:uppercase; letter-spacing:3px;'>
            {match.get('match_desc','')} &nbsp;·&nbsp; {match.get('venue','')}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── Team Cards with Logos ──
        col1, col2, col3 = st.columns([5, 2, 5])

        c1  = get_color(team1)
        c2  = get_color(team2)
        l1  = get_logo(team1)
        l2  = get_logo(team2)
        s1  = get_short(team1)
        s2  = get_short(team2)

        with col1:
            st.markdown(f"""
            <div class='team-card' style='background:linear-gradient(135deg,
            {c1}18, {c1}30); border-color:{c1};'>
                <img src='{l1}' width='90' height='90'
                style='object-fit:contain; margin-bottom:10px;'
                onerror="this.style.display='none'">
                <div style='font-size:32px; font-weight:800;
                color:{c1}; letter-spacing:2px;'>{s1}</div>
                <div style='font-size:14px; color:#8899BB;
                margin-top:4px;'>{team1}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='text-align:center; padding:40px 0;'>
                <div style='color:#D4AF37; font-size:32px;
                font-weight:800; letter-spacing:3px;'>VS</div>
                <div style='width:40px; height:2px;
                background:#D4AF37; margin:8px auto;
                opacity:0.5;'></div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='team-card' style='background:linear-gradient(135deg,
            {c2}18, {c2}30); border-color:{c2};'>
                <img src='{l2}' width='90' height='90'
                style='object-fit:contain; margin-bottom:10px;'
                onerror="this.style.display='none'">
                <div style='font-size:32px; font-weight:800;
                color:{c2}; letter-spacing:2px;'>{s2}</div>
                <div style='font-size:14px; color:#8899BB;
                margin-top:4px;'>{team2}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

        # ── PRE-TOSS PREDICTION (always show) ──
        st.markdown("<div class='section-header'>Pre-Toss Prediction</div>",
                    unsafe_allow_html=True)

        pretoss_result = predict_winner(team1, team2)

        if pretoss_result:
            pt1, pt2 = st.columns(2)
            for i, (team, prob) in enumerate(pretoss_result.items()):
                col  = pt1 if i == 0 else pt2
                clr  = c1 if i == 0 else c2
                logo = l1 if i == 0 else l2
                srt  = s1 if i == 0 else s2

                with col:
                    st.markdown(f"""
                    <div class='prob-box' style='background:linear-gradient(135deg,
                    {clr}12, {clr}28); border-color:{clr};'>
                        <img src='{logo}' width='60' height='60'
                        style='object-fit:contain; margin-bottom:10px;'
                        onerror="this.style.display='none'">
                        <div class='prob-percent' style='color:{clr};'>{prob}%</div>
                        <div class='prob-team'>{srt}</div>
                        <div class='prob-label'>Win Probability</div>
                    </div>
                    """, unsafe_allow_html=True)

            pretoss_winner = max(pretoss_result, key=pretoss_result.get)
            pretoss_prob   = pretoss_result[pretoss_winner]
            loser          = [t for t in pretoss_result if t != pretoss_winner][0]

            st.markdown(f"""
            <div class='insight-box' style='margin-top:16px;'>
                <div class='insight-title'>🔍 Key Insight</div>
                <p class='insight-text'>
                {get_short(pretoss_winner)} has a higher probability to win based on our
                machine learning model and historical simulation across all toss scenarios.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Donut chart
            fig_pre = go.Figure(go.Pie(
                labels    = [get_short(t) for t in pretoss_result.keys()],
                values    = list(pretoss_result.values()),
                hole      = 0.65,
                marker    = dict(
                    colors = [c1, c2],
                    line   = dict(color='#050D18', width=3)
                ),
                textinfo      = 'label+percent',
                textfont_size = 15,
                textfont      = dict(color=['white', 'white']),
                hovertemplate = "<b>%{label}</b><br>Win Probability: %{value}%<extra></extra>"
            ))
            fig_pre.update_layout(
                plot_bgcolor  = "rgba(0,0,0,0)",
                paper_bgcolor = "rgba(0,0,0,0)",
                font_color    = "#E8EDF5",
                height        = 280,
                margin        = dict(l=0, r=0, t=20, b=0),
                showlegend    = False,
                annotations   = [dict(
                    text      = f"<b>{pretoss_prob}%</b>",
                    x=0.5, y=0.5,
                    font_size = 28,
                    font_color= c1 if pretoss_winner == team1 else c2,
                    showarrow = False
                )]
            )
            st.plotly_chart(fig_pre, use_container_width=True)

        st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

        # ── POST-TOSS PREDICTION ──
        if toss_winner and toss_decision:
            st.markdown("<div class='section-header'>Post-Toss Prediction</div>",
                        unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background:#0F1E35; border-radius:10px;
            padding:12px 18px; border:1px solid #1E3A5F;
            margin-bottom:16px;'>
            🪙 <b style='color:#D4AF37;'>Toss:</b>
            <span style='color:#E8EDF5;'>{toss_winner}</span>
            elected to
            <span style='color:#D4AF37; font-weight:700;'>
            {toss_decision}</span>
            </div>
            """, unsafe_allow_html=True)

            result = predict_winner(team1, team2, toss_winner, toss_decision)

            if result:
                p1, p2 = st.columns(2)
                for i, (team, prob) in enumerate(result.items()):
                    col  = p1 if i == 0 else p2
                    clr  = c1 if i == 0 else c2
                    logo = l1 if i == 0 else l2
                    srt  = s1 if i == 0 else s2

                    with col:
                        st.markdown(f"""
                        <div class='prob-box' style='background:linear-gradient(135deg,
                        {clr}12, {clr}28); border-color:{clr};'>
                            <img src='{logo}' width='60' height='60'
                            style='object-fit:contain; margin-bottom:10px;'
                            onerror="this.style.display='none'">
                            <div class='prob-percent' style='color:{clr};'>{prob}%</div>
                            <div class='prob-team'>{srt}</div>
                            <div class='prob-label'>Win Probability</div>
                        </div>
                        """, unsafe_allow_html=True)

                predicted_winner = max(result, key=result.get)
                win_prob         = result[predicted_winner]
                pw_color = c1 if predicted_winner == team1 else c2

                st.markdown(f"""
                <div class='winner-card' style='border-color:{pw_color};
                color:{pw_color};'>
                    🏆 Predicted Winner: {get_short(predicted_winner)}
                    &nbsp;·&nbsp; {win_prob}% Win Probability
                </div>
                """, unsafe_allow_html=True)

        else:
            # Allow manual toss input for pre-prediction
            st.markdown("<div class='section-header'>Simulate Toss Outcome</div>",
                        unsafe_allow_html=True)

            st.markdown("""
            <div class='pretoss-box'>
                <p style='color:#8899BB; font-size:13px;
                letter-spacing:2px; text-transform:uppercase;
                margin-bottom:16px;'>
                Enter toss details to refine prediction
                </p>
            </div>
            """, unsafe_allow_html=True)

            tc1, tc2 = st.columns(2)
            with tc1:
                sim_toss_winner = st.selectbox(
                    "🪙 Toss Winner", [team1, team2],
                    key="sim_toss_winner"
                )
            with tc2:
                sim_toss_decision = st.selectbox(
                    "⚡ Elected To", ["bat", "field"],
                    key="sim_toss_decision"
                )

            if st.button("🎯 Run Toss Prediction", key="run_toss"):
                result = predict_winner(
                    team1, team2, sim_toss_winner, sim_toss_decision
                )
                if result:
                    tp1, tp2 = st.columns(2)
                    for i, (team, prob) in enumerate(result.items()):
                        col  = tp1 if i == 0 else tp2
                        clr  = c1 if i == 0 else c2
                        logo = l1 if i == 0 else l2
                        srt  = s1 if i == 0 else s2

                        with col:
                            st.markdown(f"""
                            <div class='prob-box' style='background:linear-gradient(135deg,
                            {clr}12, {clr}28); border-color:{clr};'>
                                <img src='{logo}' width='60' height='60'
                                style='object-fit:contain; margin-bottom:10px;'
                                onerror="this.style.display='none'">
                                <div class='prob-percent' style='color:{clr};'>{prob}%</div>
                                <div class='prob-team'>{srt}</div>
                                <div class='prob-label'>Win Probability</div>
                            </div>
                            """, unsafe_allow_html=True)

                    pw    = max(result, key=result.get)
                    pwp   = result[pw]
                    pwclr = c1 if pw == team1 else c2

                    st.markdown(f"""
                    <div class='winner-card' style='border-color:{pwclr};
                    color:{pwclr};'>
                        🏆 Predicted Winner: {get_short(pw)} · {pwp}%
                    </div>
                    """, unsafe_allow_html=True)

        # ── Auto Refresh ──
        st.markdown("")
        auto_refresh = st.toggle("🔄 Auto Refresh every 60s", value=False)
        if auto_refresh:
            st.markdown("""
            <div style='color:#5577AA; font-size:13px; text-align:center;'>
            ✅ Auto-refresh active — checking live updates every 60s
            </div>
            """, unsafe_allow_html=True)
            time.sleep(60)
            st.rerun()

    else:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px;'>
            <div style='font-size:64px;'>🏏</div>
            <h2 style='color:#D4AF37;'>No Match Data Available</h2>
            <p style='color:#5577AA;'>API connection issue. Check your API key.</p>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# TAB 2 — IPL 2026 Champion
# ════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>IPL 2026 Playoff Contenders</div>",
                unsafe_allow_html=True)

    # Playoff teams grid
    cols = st.columns(5)
    for i, team in enumerate(PLAYOFF_TEAMS):
        with cols[i]:
            clr  = get_color(team)
            logo = get_logo(team)
            srt  = get_short(team)
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, {clr}18, {clr}30);
            border:1px solid {clr}66; border-radius:12px;
            padding:16px 10px; text-align:center; margin:4px 0;'>
                <img src='{logo}' width='56' height='56'
                style='object-fit:contain; margin-bottom:8px;'
                onerror="this.style.display='none'">
                <div style='color:{clr}; font-weight:800;
                font-size:16px; letter-spacing:1px;'>{srt}</div>
                <div style='color:#5577AA; font-size:11px;
                margin-top:3px;'>{team}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    if st.button("🎯 Predict IPL 2026 Champion", type="primary"):
        with st.spinner("Simulating all playoff matchups..."):
            champion_probs = {}

            for team in PLAYOFF_TEAMS:
                total_prob = 0
                count      = 0
                for opp in PLAYOFF_TEAMS:
                    if opp == team:
                        continue
                    for toss_w in [team, opp]:
                        for toss_d in ['bat', 'field']:
                            result = predict_winner(
                                team, opp, toss_w, toss_d
                            )
                            if result and team in result:
                                total_prob += result[team]
                                count += 1

                champion_probs[team] = round(
                    total_prob / count
                ) if count > 0 else 0

            # Sort descending
            champion_probs = dict(sorted(
                champion_probs.items(),
                key=lambda x: x[1], reverse=True
            ))

            teams  = list(champion_probs.keys())
            probs  = list(champion_probs.values())
            colors = [get_color(t) for t in teams]
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

            st.markdown("<div class='section-header'>Championship Rankings</div>",
                        unsafe_allow_html=True)

            for i, (team, prob) in enumerate(champion_probs.items()):
                clr  = get_color(team)
                logo = get_logo(team)
                srt  = get_short(team)
                bar  = min(int(prob * 1.8), 100)

                st.markdown(f"""
                <div style='background:linear-gradient(135deg, {clr}12, {clr}22);
                border:1px solid {clr}55; border-radius:12px;
                padding:14px 20px; margin:8px 0;
                display:flex; align-items:center; gap:14px;'>
                    <span style='font-size:22px; min-width:30px;'>{medals[i]}</span>
                    <img src='{logo}' width='44' height='44'
                    style='object-fit:contain;'
                    onerror="this.style.display='none'">
                    <div style='flex:1;'>
                        <div style='color:#E8EDF5; font-weight:700;
                        font-size:18px; letter-spacing:1px;'>
                        {srt}
                        <span style='color:#5577AA; font-size:13px;
                        font-weight:400; margin-left:8px;'>{team}</span>
                        </div>
                        <div style='background:#050D18; border-radius:4px;
                        height:6px; margin-top:8px; overflow:hidden;'>
                            <div style='background:{clr}; height:100%;
                            width:{bar}%; border-radius:4px;
                            transition:width 0.8s;'></div>
                        </div>
                    </div>
                    <span style='color:{clr}; font-size:28px;
                    font-weight:800; min-width:60px;
                    text-align:right;'>{prob}%</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")

            # Bar Chart
            fig_bar = go.Figure(go.Bar(
                x            = [get_short(t) for t in teams],
                y            = probs,
                marker_color = colors,
                text         = [f"{p}%" for p in probs],
                textposition = 'outside',
                textfont     = dict(color='#D4AF37', size=14),
                hovertemplate = "<b>%{x}</b><br>Championship Prob: %{y}%<extra></extra>"
            ))
            fig_bar.update_layout(
                plot_bgcolor  = "rgba(0,0,0,0)",
                paper_bgcolor = "rgba(0,0,0,0)",
                font_color    = "#E8EDF5",
                height        = 360,
                yaxis_range   = [0, max(probs) + 12],
                yaxis = dict(showgrid=True, gridcolor="#0F1E35",
                             title="Win Probability (%)"),
                xaxis = dict(showgrid=False),
                margin = dict(l=0, r=0, t=40, b=0),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # Champion Banner
            champion   = teams[0]
            champ_prob = probs[0]
            champ_clr  = get_color(champion)
            champ_logo = get_logo(champion)
            champ_srt  = get_short(champion)

            st.markdown(f"""
            <div class='winner-card' style='border-color:{champ_clr};'>
                <img src='{champ_logo}' width='72' height='72'
                style='object-fit:contain; margin-bottom:12px;'
                onerror="this.style.display='none'"><br>
                <span style='color:{champ_clr};'>
                🏆 Predicted IPL 2026 Champion: {champ_srt} — {champ_prob}%
                </span>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# TAB 3 — Manual Prediction
# ════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Match Simulator</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        team1_m = st.selectbox("🏏 Select Team 1", IPL_TEAMS, index=0,
                               key="manual_t1")
    with col2:
        remaining = [t for t in IPL_TEAMS if t != team1_m]
        team2_m   = st.selectbox("🏏 Select Team 2", remaining, index=0,
                                 key="manual_t2")

    # Live team preview cards
    mc1, mc2 = st.columns(2)
    for col, team in zip([mc1, mc2], [team1_m, team2_m]):
        clr  = get_color(team)
        logo = get_logo(team)
        srt  = get_short(team)
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, {clr}15, {clr}28);
            border:1px solid {clr}55; border-radius:12px;
            padding:16px; text-align:center; margin:8px 0;'>
                <img src='{logo}' width='70' height='70'
                style='object-fit:contain; margin-bottom:8px;'
                onerror="this.style.display='none'">
                <div style='color:{clr}; font-size:24px;
                font-weight:800; letter-spacing:2px;'>{srt}</div>
                <div style='color:#5577AA; font-size:12px;
                margin-top:3px;'>{team}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Pre-toss prediction auto-show
    st.markdown("<div class='section-header'>Pre-Toss Prediction</div>",
                unsafe_allow_html=True)

    pretoss_m = predict_winner(team1_m, team2_m)
    if pretoss_m:
        pc1, pc2 = st.columns(2)
        for i, (team, prob) in enumerate(pretoss_m.items()):
            col  = pc1 if i == 0 else pc2
            clr  = get_color(team)
            logo = get_logo(team)
            srt  = get_short(team)
            with col:
                st.markdown(f"""
                <div class='prob-box' style='background:linear-gradient(135deg,
                {clr}12, {clr}28); border-color:{clr};'>
                    <img src='{logo}' width='60' height='60'
                    style='object-fit:contain; margin-bottom:10px;'
                    onerror="this.style.display='none'">
                    <div class='prob-percent' style='color:{clr};'>{prob}%</div>
                    <div class='prob-team'>{srt}</div>
                    <div class='prob-label'>Pre-Toss Win Probability</div>
                </div>
                """, unsafe_allow_html=True)

        pw_pre = max(pretoss_m, key=pretoss_m.get)
        st.markdown(f"""
        <div class='insight-box' style='margin-top:16px;'>
            <div class='insight-title'>🔍 Key Insight</div>
            <p class='insight-text'>
            {get_short(pw_pre)} has a higher historical win probability based on our
            XGBoost model trained on 980 IPL matches (2008–2026).
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Toss simulation
    st.markdown("<div class='section-header'>Post-Toss Simulation</div>",
                unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        toss_winner_m   = st.selectbox("🪙 Toss Winner",
                                       [team1_m, team2_m], key="manual_tw")
    with col4:
        toss_decision_m = st.selectbox("⚡ Elected To",
                                       ["bat", "field"], key="manual_td")

    st.markdown("")

    if st.button("🎯 Predict Match Winner", type="primary"):
        result = predict_winner(
            team1_m, team2_m, toss_winner_m, toss_decision_m
        )

        if result:
            st.markdown("<div class='gold-divider'></div>",
                        unsafe_allow_html=True)

            p1, p2 = st.columns(2)
            for i, (team, prob) in enumerate(result.items()):
                col  = p1 if i == 0 else p2
                clr  = get_color(team)
                logo = get_logo(team)
                srt  = get_short(team)
                with col:
                    st.markdown(f"""
                    <div class='prob-box' style='background:linear-gradient(135deg,
                    {clr}12, {clr}28); border-color:{clr};'>
                        <img src='{logo}' width='70' height='70'
                        style='object-fit:contain; margin-bottom:10px;'
                        onerror="this.style.display='none'">
                        <div class='prob-percent' style='color:{clr};'>{prob}%</div>
                        <div class='prob-team'>{srt}</div>
                        <div class='prob-label'>Win Probability</div>
                    </div>
                    """, unsafe_allow_html=True)

            predicted_winner = max(result, key=result.get)
            win_prob         = result[predicted_winner]
            pw_color         = get_color(predicted_winner)
            pw_logo          = get_logo(predicted_winner)

            st.markdown("")

            # Side-by-side charts
            ch1, ch2 = st.columns(2)
            teams_r  = list(result.keys())
            probs_r  = list(result.values())
            colors_r = [get_color(t) for t in teams_r]

            with ch1:
                fig_bar = go.Figure(go.Bar(
                    x            = probs_r,
                    y            = [get_short(t) for t in teams_r],
                    orientation  = 'h',
                    marker_color = colors_r,
                    text         = [f"{p}%" for p in probs_r],
                    textposition = 'inside',
                    textfont     = dict(size=16, color='white'),
                ))
                fig_bar.update_layout(
                    plot_bgcolor  = "rgba(0,0,0,0)",
                    paper_bgcolor = "rgba(0,0,0,0)",
                    font_color    = "#E8EDF5",
                    height        = 220,
                    xaxis = dict(range=[0, 100], showgrid=False,
                                 showticklabels=False),
                    yaxis = dict(showgrid=False,
                                 tickfont=dict(size=16, color="#E8EDF5")),
                    margin     = dict(l=0, r=20, t=10, b=10),
                    showlegend = False,
                    bargap     = 0.35
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with ch2:
                fig_donut = go.Figure(go.Pie(
                    labels    = [get_short(t) for t in teams_r],
                    values    = probs_r,
                    hole      = 0.62,
                    marker    = dict(
                        colors = colors_r,
                        line   = dict(color='#050D18', width=3)
                    ),
                    textinfo      = 'percent',
                    textfont_size = 14,
                ))
                fig_donut.update_layout(
                    plot_bgcolor  = "rgba(0,0,0,0)",
                    paper_bgcolor = "rgba(0,0,0,0)",
                    font_color    = "#E8EDF5",
                    height        = 220,
                    showlegend    = False,
                    margin        = dict(l=0, r=0, t=10, b=10),
                    annotations   = [dict(
                        text       = f"<b>{win_prob}%</b>",
                        font_size  = 24,
                        font_color = pw_color,
                        showarrow  = False
                    )]
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            # Winner Banner
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, #0A0500, #1A0E00);
            border:2px solid {pw_color}; border-radius:16px;
            padding:24px; text-align:center; margin:12px 0;
            box-shadow: 0 0 40px {pw_color}33;'>
                <div style='display:flex; align-items:center;
                justify-content:center; gap:24px; flex-wrap:wrap;'>
                    <div>
                        <p style='color:#8899BB; font-size:12px;
                        letter-spacing:3px; margin:0;'>PREDICTED WINNER</p>
                        <p style='color:{pw_color}; font-size:32px;
                        font-weight:800; letter-spacing:3px; margin:4px 0;'>
                        {get_short(predicted_winner)}</p>
                    </div>
                    <div style='border-left:1px solid {pw_color}55;
                    padding-left:24px;'>
                        <p style='color:#8899BB; font-size:12px;
                        letter-spacing:3px; margin:0;'>WIN PROBABILITY</p>
                        <p style='color:{pw_color}; font-size:32px;
                        font-weight:800; margin:4px 0;'>{win_prob}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────
st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding:14px 0;'>
    <p style='color:#1E3A5F; font-size:13px; letter-spacing:2px;
    text-transform:uppercase; margin:0;'>
    IPL 2026 Analytics · XGBoost · CricBuzz API · 980 Matches · 2008–2026
    </p>
</div>
""", unsafe_allow_html=True)