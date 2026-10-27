"""
Perfect Store — Análisis Gerencial del Cierre Q4 vs. Q3 2026
MARS Petcare Colombia
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd

# ─── DIRECTORIO BASE Y CARGA DEL HTML EJECUTIVO ──────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"

if HTML_FILE.exists():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        HTML_CONTENT = f.read()
else:
    HTML_CONTENT = ""

# ─── CONFIGURACIÓN DE PÁGINA STREAMLIT ───────────────────────────────────────
st.set_page_config(
    page_title="Perfect Store — Análisis Gerencial Q4 vs Q3 2026",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── ESTILOS GLOBALES CORPORATIVOS (DARK SLATE) ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Tarjetas KPI ── */
.kpi-card {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(51, 65, 85, 0.8);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
.kpi-card .label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #94a3b8;
}
.kpi-card .value {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.1;
    margin: 6px 0;
}
.kpi-card .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
}
.badge-red    { background: rgba(239,68,68,.15); color:#f87171; border:1px solid rgba(239,68,68,.3); }
.badge-green  { background: rgba(16,185,129,.15); color:#34d399; border:1px solid rgba(16,185,129,.3); }
.badge-amber  { background: rgba(245,158,11,.15); color:#fbbf24; border:1px solid rgba(245,158,11,.3); }
.badge-blue   { background: rgba(59,130,246,.15); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.badge-indigo { background: rgba(99,102,241,.15); color:#a5b4fc; border:1px solid rgba(99,102,241,.3); }
.badge-purple { background: rgba(139,92,246,.15); color:#c4b5fd; border:1px solid rgba(139,92,246,.3); }

/* ── Cabeceras de Slide ── */
.slide-header {
    border-left: 4px solid;
    padding-left: 16px;
    margin-bottom: 20px;
}
.slide-header .eyebrow {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
}
.slide-header h2 {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    margin: 4px 0 2px 0;
}
.slide-header p {
    font-size: 13px;
    color: #94a3b8;
}

/* ── Cajas de Información ── */
.info-box {
    background: rgba(30,41,59,.6);
    border: 1px solid rgba(51,65,85,.6);
    border-radius: 14px;
    padding: 18px 22px;
    font-size: 14px;
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 20px;
}

/* ── Tarjetas de Drivers ── */
.driver-card {
    background: rgba(15,23,42,.85);
    border-radius: 14px;
    padding: 20px;
    border: 1px solid rgba(51,65,85,.7);
    margin-bottom: 14px;
}

/* ── Tarjetas de Ejecutivos ── */
.exec-card {
    background: rgba(15,23,42,.9);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    border: 1px solid rgba(51,65,85,.7);
}

/* ── Banner de Cierre ── */
.closing-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e1b4b 50%, #0f172a 100%);
    border: 2px solid rgba(99,102,241,.5);
    border-radius: 18px;
    padding: 32px;
    text-align: center;
}
.closing-banner h3 {
    font-size: 19px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.6;
}

/* ── Ocultar elementos predeterminados de Streamlit para aspecto profesional ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── TEMAS PLOTLY REUTILIZABLES ──────────────────────────────────────────────
PLOT_BG  = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_CLR = "#94a3b8"
GRID_CLR = "rgba(51,65,85,0.35)"
FONT_FAM = "Plus Jakarta Sans, sans-serif"

def base_layout(**kwargs) -> dict:
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=FONT_CLR, size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(font=dict(color=FONT_CLR, size=11), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR)),
        **kwargs,
    )

# ─── BARRA LATERAL (SIDEBAR) ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;">
      <div style="width:44px;height:44px;border-radius:12px;
                  background:linear-gradient(135deg,#3b82f6,#6366f1);
                  display:flex;align-items:center;justify-content:center;
                  font-size:22px;font-weight:900;color:white;box-shadow:0 4px 12px rgba(59,130,246,0.3);">M</div>
      <div>
        <div style="font-weight:800;color:#f8fafc;font-size:15px;line-height:1.2;">MARS | Perfect Store</div>
        <div style="font-size:11px;color:#94a3b8;">Cierre Q4 vs Q3 2026</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="badge badge-red" style="font-size:12px;display:block;text-align:center;padding:6px;">⚠️ Canal Total: -0,2 p.p. (637 PDV)</span>', unsafe_allow_html=True)
    st.markdown("---")

    modo_vista = st.radio(
        "Modo de Visualización:",
        [
            "🌐 Presentación Ejecutiva (HTML)",
            "📊 Dashboard Interactivo (Streamlit)"
        ],
        index=0
    )

    if modo_vista == "📊 Dashboard Interactivo (Streamlit)":
        st.markdown("---")
        slide = st.radio(
            "Navegación de Slides:",
            options=[
                "📊 1. Resultado General",
                "📉 2. Drivers por KPI",
                "👤 3. Zoom Responsables",
                "🎯 4. Conclusiones y Plan",
            ],
        )

    st.markdown("---")
    if HTML_CONTENT:
        st.download_button(
            label="📥 Descargar Informe HTML",
            data=HTML_CONTENT,
            file_name="Informe_Perfect_Store_Q4_vs_Q3_2026.html",
            mime="text/html",
            use_container_width=True
        )

    st.caption("MARS Petcare Colombia\nAnálisis Gerencial Perfect Store Q4 vs. Q3 2026")


# ════════════════════════════════════════════════════════════════════════════
# MODO 1: PRESENTACIÓN EJECUTIVA COMPLETA (TAILWIND + CHART.JS)
# ════════════════════════════════════════════════════════════════════════════
if modo_vista == "🌐 Presentación Ejecutiva (HTML)":

    st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 1rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100% !important;
            border: none !important;
            min-height: 94vh !important;
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    if HTML_CONTENT:
        components.html(HTML_CONTENT, height=940, scrolling=True)
    else:
        st.error("No se encontró el archivo HTML index.html en la carpeta.")


# ════════════════════════════════════════════════════════════════════════════
# MODO 2: DASHBOARD INTERACTIVO NATIVO EN STREAMLIT
# ════════════════════════════════════════════════════════════════════════════
else:

    # DATOS MAESTROS DE RESPONSABLES Q4 vs Q3
    df_rank = pd.DataFrame({
        "Responsable Mars": ["Jhon Gómez", "Karol Rojas", "Sebastián Ceballos", "Total canal"],
        "PDV válidos": ["308 (48,4%)", "63 (9,9%)", "266 (41,8%)", "637 (100%)"],
        "Surtido": ["-1,7 p.p.", "-0,7 p.p.", "+0,2 p.p.", "-0,5 p.p."],
        "Visibilidad": ["-0,4 p.p.", "+1,7 p.p.", "+0,7 p.p.", "+0,3 p.p."],
        "Exhibición secundaria": ["+0,40 p.p.", "+0,26 p.p.", "+0,57 p.p.", "+0,47 p.p."],
        "Perfect Store": ["-2,3 p.p.", "+1,2 p.p.", "+1,3 p.p.", "-0,2 p.p."],
    })

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 1 — RESULTADO GENERAL
    # ────────────────────────────────────────────────────────────────────────
    if slide == "📊 1. Resultado General":

        st.markdown("""
        <div class="slide-header" style="border-color:#3b82f6;">
          <div class="eyebrow" style="color:#60a5fa;">Slide 01 — Visión Ejecutiva Consolidada</div>
          <h2>ANÁLISIS GERENCIAL DEL CIERRE PERFECT STORE — Q4 VS. Q3 2026</h2>
          <p>Resultado general del canal, distribución por responsable y variación por KPI</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Lectura Gerencial:</strong> Para lo que va del Q4, comparándolo con el Q3, la tabla general evidencia 
          una variación de <strong style="color:#f87171;">-0,2 p.p.</strong> en <strong>Perfect Store</strong>, sobre una base de <strong>637 PDV válidos</strong>. 
          <strong>Surtido</strong> registra una caída de <strong style="color:#f87171;">-0,5 p.p.</strong>, mientras que 
          <strong>Visibilidad</strong> crece <strong style="color:#34d399;">+0,3 p.p.</strong> y 
          <strong>Exhibición Secundaria</strong> <strong style="color:#c4b5fd;">+0,47 p.p.</strong> Aunque estos dos últimos indicadores presentan avances, 
          el resultado general continúa en terreno negativo.<br><br>
          La distribución por responsable muestra que <strong>Jhon Gómez</strong> presenta el mayor retroceso, con 
          <span style="color:#f87171;font-weight:700;">-2,3 p.p.</span>; <strong>Sebastián Ceballos</strong> lidera el crecimiento con 
          <span style="color:#34d399;font-weight:700;">+1,3 p.p.</span>, seguido muy de cerca por <strong>Karol Rojas</strong>, con 
          <span style="color:#34d399;font-weight:700;">+1,2 p.p.</span>
        </div>
        """, unsafe_allow_html=True)

        # Tarjetas Métricas
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
            <div class="kpi-card" style="border-color:rgba(239,68,68,.4);">
              <div class="label">Perfect Store Q4 vs Q3</div>
              <div class="value" style="color:#f87171;">-0,2 p.p.</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Base: 637 PDV válidos</div>
              <span class="badge badge-red">⚠️ Terreno Negativo</span>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="kpi-card" style="border-color:rgba(245,158,11,.4);">
              <div class="label">KPI Surtido</div>
              <div class="value" style="color:#fbbf24;">-0,5 p.p.</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Principal Freno del Canal</div>
              <span class="badge badge-amber">📦 Factor de Deterioro</span>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="kpi-card" style="border-color:rgba(6,182,212,.4);">
              <div class="label">KPI Visibilidad</div>
              <div class="value" style="color:#60a5fa;">+0,3 p.p.</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Reto en Multicaras (-0,5 pp)</div>
              <span class="badge badge-blue">👁️ Crecimiento Moderado</span>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown("""
            <div class="kpi-card" style="border-color:rgba(168,85,247,.4);">
              <div class="label">KPI Exhibición Secundaria</div>
              <div class="value" style="color:#c4b5fd;">+0,47 p.p.</div>
              <div style="font-size:12px;color:#94a3b8;margin-bottom:8px;">Avance Positivo en los 3</div>
              <span class="badge badge-purple">⚡ Motor del Trimestre</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col_tbl, col_cht = st.columns([7, 5])

        with col_tbl:
            st.markdown("#### 🏅 Tabla General de Responsables MARS")
            st.caption("Variaciones Q4 vs. Q3 por KPI y resultado consolidado")

            def color_format(val):
                if isinstance(val, str):
                    if val.startswith("+"):
                        return "color: #34d399; font-weight:700"
                    elif val.startswith("-"):
                        return "color: #f87171; font-weight:700"
                return ""

            styled_df = df_rank.style.applymap(color_format, subset=["Surtido", "Visibilidad", "Exhibición secundaria", "Perfect Store"])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            st.caption("Nota: Estas cifras corresponden a variaciones Q4 vs. Q3, no a niveles absolutos de cumplimiento. Las variaciones de los KPI no deben sumarse directamente para reconstruir Perfect Store, porque intervienen ponderaciones y reglas de cálculo.")

            h1, h2, h3 = st.columns(3)
            with h1:
                st.markdown('<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#f87171;">🚨 Mayor Retroceso</span><br><strong style="color:#f8fafc;">Jhon — -2,3 p.p.</strong><br><span style="font-size:10px;color:#94a3b8;">308 PDV (48,4%)</span></div>', unsafe_allow_html=True)
            with h2:
                st.markdown('<div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#60a5fa;">🥈 2° Mejor Resultado</span><br><strong style="color:#f8fafc;">Karol — +1,2 p.p.</strong><br><span style="font-size:10px;color:#94a3b8;">63 PDV (9,9%)</span></div>', unsafe_allow_html=True)
            with h3:
                st.markdown('<div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:10px;padding:10px;"><span style="font-size:11px;font-weight:700;color:#34d399;">🏆 Mayor Crecimiento</span><br><strong style="color:#f8fafc;">Sebastián — +1,3 p.p.</strong><br><span style="font-size:10px;color:#94a3b8;">266 PDV (41,8%)</span></div>', unsafe_allow_html=True)

        with col_cht:
            st.markdown("#### 📊 Aporte por KPI a la Variación Q4 vs Q3")
            st.caption("Barras: Pilares clave | Línea: Perfect Store (p.p.)")

            names = ["Jhon Gómez", "Karol Rojas", "Sebastián C.", "Total Canal"]
            fig_s1 = go.Figure()
            fig_s1.add_trace(go.Bar(
                name="Surtido",
                x=names, y=[-1.7, -0.7, 0.2, -0.5],
                marker_color="#f59e0b",
                text=["-1,7", "-0,7", "+0,2", "-0,5"],
                textposition="outside",
            ))
            fig_s1.add_trace(go.Bar(
                name="Visibilidad",
                x=names, y=[-0.4, 1.7, 0.7, 0.3],
                marker_color="#06b6d4",
                text=["-0,4", "+1,7", "+0,7", "+0,3"],
                textposition="outside",
            ))
            fig_s1.add_trace(go.Bar(
                name="Exhibición Sec.",
                x=names, y=[0.40, 0.26, 0.57, 0.47],
                marker_color="#a855f7",
                text=["+0,40", "+0,26", "+0,57", "+0,47"],
                textposition="outside",
            ))
            fig_s1.add_trace(go.Scatter(
                name="Perfect Store",
                x=names, y=[-2.3, 1.2, 1.3, -0.2],
                mode="lines+markers",
                line=dict(color="#ef4444", width=3),
                marker=dict(color="#ef4444", size=8),
            ))
            fig_s1.update_layout(
                **base_layout(yaxis=dict(range=[-3, 2.5], gridcolor=GRID_CLR, tickfont=dict(color=FONT_CLR))),
                barmode="group",
                height=350,
            )
            st.plotly_chart(fig_s1, use_container_width=True)

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 2 — DRIVERS POR KPI
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "📉 2. Drivers por KPI":

        st.markdown("""
        <div class="slide-header" style="border-color:#f59e0b;">
          <div class="eyebrow" style="color:#fbbf24;">Slide 02 — Diagnóstico por Indicadores</div>
          <h2>DRIVERS DEL AVANCE Y RETROCESO Q4 VS. Q3</h2>
          <p>Comportamiento táctico en Surtido, Visibilidad y Exhibición Secundaria</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Diagnóstico de Drivers:</strong> Aunque <strong>Exhibición Secundaria (+0,47 p.p.)</strong> y 
          <strong>Visibilidad (+0,3 p.p.)</strong> avanzan en el consolidado, la caída en 
          <strong style="color:#fbbf24;">Surtido (-0,5 p.p.)</strong> es el principal freno que mantiene el Perfect Store en terreno negativo (-0,2 p.p.). 
          La caída en Surtido se concentra en Olímpica Costa y Occidente, con desplomes severos en la categoría <em>Perro Wet (-8,0 p.p.)</em>, 
          mientras que Visibilidad se ve presionada por el retroceso de <em>Multicaras (-0,5 p.p.)</em> en Jhon Gómez.
        </div>
        """, unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3)

        with d1:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(245,158,11,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-amber">Principal Presión</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Surtido</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:24px;font-weight:800;color:#f8fafc;">SURTIDO</div>
                <div style="font-size:20px;font-weight:900;color:#fbbf24;">-0,5 p.p.</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;line-height:1.7;">
                🚨 <strong>Occidente Jhon (-4,3 p.p.):</strong> Perro Wet cae <strong>-8,0 p.p.</strong> Desplomes en <em>Pancita Saludable Pavo y Zanahoria (-13,7 p.p.)</em> y <em>Pollo y Camote (-12,1 p.p.)</em>.<br><br>
                ⚠️ <strong>Costa Jhon (-2,0 p.p.):</strong> Afectación en Olímpica (170 PDV).<br><br>
                🚨 <strong>Karol Occidente (-2,8 p.p.):</strong> Metro cae -5,4 p.p. (4 PDV); Eje Cafetero (-2,4 p.p.).<br><br>
                ✔ <strong>Sebastián (+0,2 p.p.):</strong> Consistencia positiva, salvo Super Inter Eje (-2,9 p.p.).
              </div>
            </div>
            """, unsafe_allow_html=True)

        with d2:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(6,182,212,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-blue">Avance Dispar</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Visibilidad</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:24px;font-weight:800;color:#f8fafc;">VISIBILIDAD</div>
                <div style="font-size:20px;font-weight:900;color:#60a5fa;">+0,3 p.p.</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;line-height:1.7;">
                🚀 <strong>Karol Líder (+1,7 p.p.):</strong> Participación (+0,8 p.p.) y Multicaras (+0,5 p.p.). Antioquia (+4,9 p.p.) y Costa (+3,0 p.p.).<br><br>
                🚨 <strong>Jhon Multicaras (-0,5 p.p.):</strong> Pese a Bloque (+0,1) y Participación (+0,6), Multicaras hunde el KPI a -0,4 p.p. Centro cae -0,7 p.p. y Costa -0,2 p.p.<br><br>
                🚨 <strong>Super Inter Eje (Sebastián):</strong> Caída severa de -4,7 p.p. en visibilidad en 9 PDV.
              </div>
            </div>
            """, unsafe_allow_html=True)

        with d3:
            st.markdown("""
            <div class="driver-card" style="border:1px solid rgba(168,85,247,.4);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge badge-purple">Motor de Avance</span>
                <span style="font-size:11px;color:#94a3b8;">KPI Exhibición Sec.</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:24px;font-weight:800;color:#f8fafc;">EXHIBICIÓN SEC.</div>
                <div style="font-size:20px;font-weight:900;color:#c4b5fd;">+0,47 p.p.</div>
              </div>
              <hr style="border-color:rgba(51,65,85,.6);margin:14px 0;">
              <div style="font-size:12px;color:#cbd5e1;line-height:1.7;">
                🚀 <strong>Sebastián Líder (+0,57 p.p.):</strong> Costa (+1,48 p.p.) y Antioquia (+0,86 p.p.).<br><br>
                🚀 <strong>Jhon Costa (+0,83 p.p.):</strong> Principal fortaleza, aunque Centro (-0,17) y Occidente (-0,08) caen.<br><br>
                🚨 <strong>Alerta Karol Costa (-0,92 p.p.):</strong> Hipermercados caen -1,37 p.p. por menor implementación de <strong>chimeneas e islas</strong>.
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 3 — ZOOM DETALLADO POR RESPONSABLE
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "👤 3. Zoom Responsables":

        st.markdown("""
        <div class="slide-header" style="border-color:#6366f1;">
          <div class="eyebrow" style="color:#a5b4fc;">Slide 03 — Zoom Operativo e Interactivo</div>
          <h2>ANÁLISIS DETALLADO POR RESPONSABLE MARS</h2>
          <p>Diagnóstico por ejecutivo, causa raíz por región, cadena y categoría</p>
        </div>
        """, unsafe_allow_html=True)

        exec_sel = st.selectbox(
            "Selecciona un Responsable:",
            [
                "📊 Vista Consolidada (3 Responsables)",
                "🔴 Jhon Gómez (-2,3 p.p. | 308 PDV)",
                "🟢 Karol Rojas (+1,2 p.p. | 63 PDV)",
                "🏆 Sebastián Ceballos (+1,3 p.p. | 266 PDV)"
            ]
        )

        if "Vista Consolidada" in exec_sel:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #ef4444;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🔴 JHON GÓMEZ</div>
                  <div style="font-size:26px;font-weight:900;color:#f87171;margin:6px 0;">-2,3 p.p. <span style="font-size:12px;color:#94a3b8;">(308 PDV - 48,4%)</span></div>
                  <p style="font-size:12px;color:#cbd5e1;line-height:1.6;">
                    Mayor caída del canal. Surtido cae -1,7 p.p. (Occidente -4,3 p.p., Costa -2,0 p.p. en Olímpica). Perro Wet -8,0 p.p. Multicaras retrocede -0,5 p.p.
                  </p>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #10b981;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🟢 KAROL ROJAS</div>
                  <div style="font-size:26px;font-weight:900;color:#34d399;margin:6px 0;">+1,2 p.p. <span style="font-size:12px;color:#94a3b8;">(63 PDV - 9,9%)</span></div>
                  <p style="font-size:12px;color:#cbd5e1;line-height:1.6;">
                    Líder en Visibilidad (+1,7 p.p.) y avance en Antioquia (+8,5 p.p. en Jumbo). Alerta prioritaria: Exhibición Costa cae -0,92 p.p. (chimeneas e islas).
                  </p>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown("""
                <div class="exec-card" style="border-top:4px solid #10b981;">
                  <div style="font-weight:800;color:#f8fafc;font-size:16px;">🏆 SEBASTIÁN CEBALLOS</div>
                  <div style="font-size:26px;font-weight:900;color:#34d399;margin:6px 0;">+1,3 p.p. <span style="font-size:12px;color:#94a3b8;">(266 PDV - 41,8%)</span></div>
                  <p style="font-size:12px;color:#cbd5e1;line-height:1.6;">
                    Mayor crecimiento y balance positivo 3/3 (Surtido +0,2, Visi +0,7, Exhi +0,57). Alerta puntual: Super Inter Eje Cafetero cae -6,8 p.p. (9 PDV).
                  </p>
                </div>
                """, unsafe_allow_html=True)

        elif "Jhon Gómez" in exec_sel:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(239,68,68,.5);">
              <span class="badge badge-red">🔴 RESPONSABLE CON MAYOR RETROCESO</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">JHON GÓMEZ</h3>
              <p style="font-size:12px;color:#94a3b8;">Base: 308 PDVs válidos (48,4% de la base analizada)</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Perfect Store: <strong style="color:#f87171;font-size:18px;">-2,3 p.p.</strong></span>
                <span>Surtido: <strong style="color:#f87171;">-1,7 p.p.</strong></span>
                <span>Visibilidad: <strong style="color:#f87171;">-0,4 p.p.</strong></span>
                <span>Exhibición: <strong style="color:#c4b5fd;">+0,40 p.p.</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(239,68,68,.4);">
                  <strong style="color:#f87171;font-size:13px;">1. SURTIDO (-1,7 p.p.) & SKUs CRÍTICOS</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Occidente retrocede <strong>-4,3 p.p.</strong> y Costa <strong>-2,0 p.p.</strong>
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Perro Wet Occidente:</strong> -8,0 p.p.<br>
                    • <strong>Pancita Saludable Pavo y Zanahoria:</strong> <span style="color:#f87171;font-weight:700;">-13,7 p.p.</span><br>
                    • <strong>Pancita Saludable Pollo y Camote:</strong> <span style="color:#f87171;font-weight:700;">-12,1 p.p.</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(59,130,246,.4);">
                  <strong style="color:#60a5fa;font-size:13px;">2. VISIBILIDAD & MULTICARAS</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Pese a Bloque de Marca (+0,1) y Participación (+0,6), Visibilidad cae -0,4 p.p. por <strong>Multicaras (-0,5 p.p.)</strong>.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Centro Visibilidad:</strong> -0,7 p.p.<br>
                    • <strong>Costa Visibilidad:</strong> -0,2 p.p.<br>
                    • <strong>Freno:</strong> Pérdida de frentes en góndola (multicaras).
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(168,85,247,.4);">
                  <strong style="color:#c4b5fd;font-size:13px;">3. EXHIBICIÓN & REGIONES</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Exhibición sube +0,40 p.p. gracias a <strong>Costa (+0,83 p.p.)</strong>, pero Centro cae -0,17 p.p. y Occidente -0,08 p.p.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Costa (170 PDV):</strong> Olímpica -3,4 p.p. vs Megatiendas +6,0 p.p.<br>
                    • <strong>Occidente:</strong> -5,2 p.p. en Perfect Store.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:12px;font-size:12px;color:#f87171;"><strong>Prioridad Operativa:</strong> Recuperar Surtido en Olímpica (Costa y Occidente), reponer los SKUs de Pancita Saludable y corregir Multicaras sin ceder el avance de exhibición en Costa.</div>', unsafe_allow_html=True)

        elif "Karol Rojas" in exec_sel:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(16,185,129,.5);">
              <span class="badge badge-green">🟢 SEGUNDO MEJOR RESULTADO</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">KAROL ROJAS</h3>
              <p style="font-size:12px;color:#94a3b8;">Base: 63 PDVs válidos (9,9% de la base)</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Perfect Store: <strong style="color:#34d399;font-size:18px;">+1,2 p.p.</strong></span>
                <span>Visibilidad: <strong style="color:#34d399;">+1,7 p.p. 🏆</strong></span>
                <span>Exhibición: <strong style="color:#c4b5fd;">+0,26 p.p.</strong></span>
                <span>Surtido: <strong style="color:#fbbf24;">-0,7 p.p.</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(16,185,129,.4);">
                  <strong style="color:#34d399;font-size:13px;">1. VISIBILIDAD LÍDER (+1,7 p.p.)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Mejor crecimiento en Visibilidad del canal. Participación sube +0,8 p.p. y Multicaras +0,5 p.p.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Antioquia Visibilidad:</strong> +4,9 p.p.<br>
                    • <strong>Costa Visibilidad:</strong> +3,0 p.p.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(245,158,11,.4);">
                  <strong style="color:#fbbf24;font-size:13px;">2. SURTIDO & METRO OCCIDENTE</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Surtido cae -0,7 p.p., con alertas en <strong>Occidente (-2,8 p.p.)</strong> y <strong>Eje Cafetero (-2,4 p.p.)</strong>.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Metro Occidente:</strong> cae <span style="color:#f87171;font-weight:700;">-5,4 p.p.</span> en 4 PDV.<br>
                    • Contrasta con Antioquia (+1,8 p.p. en surtido).
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(239,68,68,.4);">
                  <strong style="color:#f87171;font-size:13px;">3. ALERTA EXHIBICIÓN COSTA (-0,92 p.p.)</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Exhibición en Costa cae -0,92 p.p., con mayor afectación en <strong>hipermercados (-1,37 p.p.)</strong>.
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Causa raíz:</strong> Menor implementación de <strong>chimeneas e islas</strong>.<br>
                    • Debe tratarse como prioridad operativa inmediata.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:10px;padding:12px;font-size:12px;color:#34d399;"><strong>Conclusión:</strong> Mantener el liderazgo en Visibilidad, recuperar Surtido en Metro Occidente y corregir con urgencia el montaje de chimeneas e islas en Costa.</div>', unsafe_allow_html=True)

        elif "Sebastián Ceballos" in exec_sel:
            st.markdown("""
            <div class="exec-card" style="border:2px solid rgba(16,185,129,.5);">
              <span class="badge badge-green">🏆 RESPONSABLE CON MAYOR CRECIMIENTO</span>
              <h3 style="font-size:28px;font-weight:800;color:#f8fafc;margin:8px 0 2px;">SEBASTIÁN CEBALLOS</h3>
              <p style="font-size:12px;color:#94a3b8;">Base: 266 PDVs válidos (41,8% de la base)</p>
              <div style="display:flex;gap:20px;margin-top:10px;font-size:13px;">
                <span>Perfect Store: <strong style="color:#34d399;font-size:18px;">+1,3 p.p.</strong></span>
                <span>Surtido: <strong style="color:#34d399;">+0,2 p.p.</strong></span>
                <span>Visibilidad: <strong style="color:#34d399;">+0,7 p.p.</strong></span>
                <span>Exhibición: <strong style="color:#c4b5fd;">+0,57 p.p. 🏆</strong></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(16,185,129,.4);">
                  <strong style="color:#34d399;font-size:13px;">1. MOTORES DE CRECIMIENTO</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Único con los 3 KPI en positivo. Crecimientos regionales destacados:
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Oriente:</strong> <span style="color:#34d399;font-weight:700;">+5,9 p.p.</span> (Éxito Hiper +14,3 p.p.)<br>
                    • <strong>Antioquia:</strong> +3,5 p.p. (Éxito +4,3, Carulla +2,9, Euro +2,2)<br>
                    • <strong>Costa:</strong> +2,5 p.p. (Éxito +5,5, Euro +5,4)
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(239,68,68,.4);">
                  <strong style="color:#f87171;font-size:13px;">2. ALERTA SUPER INTER EJE</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    La principal alerta se ubica en <strong>Eje Cafetero (-1,1 p.p. en PS)</strong>:
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Super Inter:</strong> <span style="color:#f87171;font-weight:700;">-6,8 p.p. en 9 PDV</span><br>
                    • Caída de Surtido: <strong>-2,9 p.p.</strong><br>
                    • Caída de Visibilidad: <strong>-4,7 p.p.</strong><br>
                    • Exhibición (+0,60) no compensa.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown("""
                <div class="driver-card" style="border:1px solid rgba(168,85,247,.4);">
                  <strong style="color:#c4b5fd;font-size:13px;">3. FORTALEZA EN EXHIBICIÓN</strong>
                  <p style="font-size:12px;color:#cbd5e1;margin-top:6px;">
                    Exhibición Secundaria muestra un avance altamente consistente:
                  </p>
                  <div style="background:rgba(15,23,42,.7);padding:8px;border-radius:8px;font-size:11px;color:#cbd5e1;line-height:1.6;">
                    • <strong>Consolidado:</strong> +0,57 p.p.<br>
                    • <strong>Costa:</strong> +1,48 p.p.<br>
                    • <strong>Antioquia:</strong> +0,86 p.p.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:10px;padding:12px;font-size:12px;color:#34d399;"><strong>Conclusión:</strong> Sebastián lidera el crecimiento y muestra la mayor consistencia. La prioridad es contener la caída puntual de Super Inter en el Eje Cafetero y sostener las buenas prácticas en las demás zonas.</div>', unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────────────
    # SLIDE 4 — CONCLUSIONES Y PLAN DE ACCIÓN
    # ────────────────────────────────────────────────────────────────────────
    elif slide == "🎯 4. Conclusiones y Plan":

        st.markdown("""
        <div class="slide-header" style="border-color:#10b981;">
          <div class="eyebrow" style="color:#34d399;">Slide 04 — Estrategia de Cierre y Frentes de Acción</div>
          <h2>CONCLUSIÓN GERENCIAL Y PLAN DE ACCIÓN</h2>
          <p>Tres frentes de intervención inmediata para recuperar el resultado general del canal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong style="color:#f1f5f9;">Conclusión para Presentar a la Gerencia:</strong> El cierre de Perfect Store Q4 frente a Q3 
          presenta una variación total de <strong style="color:#f87171;">-0,2 p.p.</strong> sobre <strong>637 PDV</strong>. El principal factor de presión es 
          <strong style="color:#fbbf24;">Surtido (-0,5 p.p.)</strong>, mientras que 
          <strong style="color:#60a5fa;">Visibilidad (+0,3 p.p.)</strong> y 
          <strong style="color:#c4b5fd;">Exhibición Secundaria (+0,47 p.p.)</strong> muestran avances.<br><br>
          La distribución por responsable evidencia que <strong>Jhon Gómez concentra el mayor retroceso (-2,3 p.p.)</strong>, especialmente por Surtido en Olímpica Costa y Occidente y por el deterioro de Multicaras. 
          <strong>Karol Rojas crece +1,2 p.p.</strong> impulsada por Visibilidad, pero requiere recuperar la implementación de chimeneas e islas en Costa. 
          <strong>Sebastián Ceballos lidera el crecimiento (+1,3 p.p.)</strong> con avances en los tres KPI, aunque Super Inter en Eje Cafetero continúa como una alerta prioritaria.
        </div>
        """, unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)

        with p1:
            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #ef4444;border-radius:0 14px 14px 0;padding:22px;height:100%;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(239,68,68,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#f87171;">1</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">SURTIDO EN OLÍMPICA</div>
                  <div style="font-size:11px;color:#f87171;">Prioridad: Jhon Gómez (308 PDV)</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Reposición Inmediata:</strong> Recuperar Surtido en Olímpica Costa (170 PDV) y Occidente (-4,3 p.p.).</li>
                <li><strong>Plan de Choque Wet:</strong> Reabastecer Pancita Saludable Pavo y Zanahoria (-13,7%) y Pollo y Camote (-12,1%).</li>
                <li><strong>Ajuste de Multicaras:</strong> Revertir la caída de -0,5 p.p. en Centro (-0,7) y Costa (-0,2) para frenar la pérdida en Visibilidad.</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        with p2:
            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #f59e0b;border-radius:0 14px 14px 0;padding:22px;height:100%;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(245,158,11,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#fbbf24;">2</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">EXHIBICIÓN COSTA & METRO</div>
                  <div style="font-size:11px;color:#fbbf24;">Prioridad: Karol Rojas (63 PDV)</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Chimeneas e Islas:</strong> Corregir de inmediato la caída de -1,37 p.p. en Hipermercados Costa por menor implementación.</li>
                <li><strong>Surtido Metro Occidente:</strong> Recuperar la caída de -5,4 p.p. en los 4 PDV de Metro.</li>
                <li><strong>Sostener Visibilidad:</strong> Proteger el liderazgo de +1,7 p.p. consolidado en Antioquia y Costa.</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        with p3:
            st.markdown("""
            <div style="background:rgba(30,41,59,.9);border-left:4px solid #10b981;border-radius:0 14px 14px 0;padding:22px;height:100%;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="width:36px;height:36px;border-radius:10px;background:rgba(16,185,129,.2);
                             display:flex;align-items:center;justify-content:center;font-weight:900;color:#34d399;">3</span>
                <div>
                  <div style="font-weight:800;color:#f8fafc;font-size:15px;">PLAN SUPER INTER EJE</div>
                  <div style="font-size:11px;color:#34d399;">Prioridad: Sebastián Ceballos (266 PDV)</div>
                </div>
              </div>
              <ul style="font-size:12px;color:#cbd5e1;line-height:1.9;padding-left:14px;margin:0;">
                <li><strong>Intervención Focalizada:</strong> Plan de contingencia urgente en los 9 PDV de Super Inter (-6,8 p.p. en Perfect Store).</li>
                <li><strong>Frenar Fugas:</strong> Recuperar la caída de Surtido (-2,9 p.p.) y Visibilidad (-4,7 p.p.).</li>
                <li><strong>Sostener Consistencia:</strong> Replicar y mantener las fortalezas de Costa (+1,48 en exhibición), Antioquia y Oriente.</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div class="closing-banner">
          <span class="badge badge-indigo" style="margin-bottom:14px;display:inline-block;">
            Compromiso de Gestión Gerencial — Q4 2026
          </span>
          <h3>
            “De cara al siguiente periodo, la gestión debe concentrarse en tres frentes: <span style="color:#f87171;">recuperar Surtido en Olímpica para Jhon</span>, 
            <span style="color:#fbbf24;">mejorar la ejecución de Exhibición Secundaria en Costa para Karol</span> y 
            <span style="color:#34d399;">corregir las caídas de Surtido y Visibilidad en Super Inter para Sebastián</span>. 
            El objetivo es convertir los avances individuales y regionales en una <span style="color:#c4b5fd;">mejora sostenible del resultado general del canal</span>.”
          </h3>
        </div>
        """, unsafe_allow_html=True)
