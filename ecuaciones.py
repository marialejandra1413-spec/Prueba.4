import streamlit as st
import random
import time

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="📐 Trivia Ecuaciones",
    page_icon="📐",
    layout="centered",
)

# ── CSS custom – estética matemática moderna ─────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');

  html, body, [data-testid="stAppViewContainer"] {
      background: #05080f;
      color: #e2e8f0;
      font-family: 'DM Sans', sans-serif;
  }
  [data-testid="stHeader"] { background: transparent; }

  /* ── Título ── */
  .titulo-mat {
      font-family: 'Space Mono', monospace;
      font-size: 2.4rem;
      font-weight: 700;
      letter-spacing: 2px;
      background: linear-gradient(135deg, #38bdf8, #818cf8, #38bdf8);
      background-size: 200%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: gradientFlow 4s ease infinite;
      text-align: center;
      margin-bottom: 0;
  }
  .subtitulo {
      text-align: center;
      color: #475569;
      font-size: 0.9rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-top: 4px;
  }
  @keyframes gradientFlow {
      0%   { background-position: 0% }
      50%  { background-position: 100% }
      100% { background-position: 0% }
  }

  /* ── Tarjeta de pregunta ── */
  .card-pregunta {
      background: linear-gradient(135deg, #0f172a, #1e293b);
      border: 1px solid #1e40af44;
      border-top: 3px solid #38bdf8;
      border-radius: 14px;
      padding: 28px 32px;
      margin: 16px 0 10px 0;
      font-family: 'Space Mono', monospace;
      font-size: 1.15rem;
      color: #f1f5f9;
      box-shadow: 0 0 40px #38bdf81a;
      line-height: 1.7;
  }
  .label-pregunta {
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
      letter-spacing: 3px;
      color: #38bdf8;
      text-transform: uppercase;
      margin-bottom: 6px;
  }

  /* ── Barra de progreso ── */
  .barra-fondo {
      background: #1e293b;
      border-radius: 99px;
      height: 5px;
      margin: 12px 0 18px 0;
  }
  .barra-fill {
      height: 5px;
      border-radius: 99px;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      transition: width 0.5s ease;
  }

  /* ── Botones de alternativas ── */
  div.stButton > button {
      background: #0f172a;
      border: 1px solid #1e293b;
      color: #cbd5e1;
      font-family: 'Space Mono', monospace;
      font-size: 0.95rem;
      border-radius: 10px;
      padding: 14px 20px;
      width: 100%;
      text-align: left;
      transition: all 0.2s ease;
  }
  div.stButton > button:hover {
      background: #1e293b;
      border-color: #38bdf8;
      color: #38bdf8;
      transform: translateX(5px);
      box-shadow: 0 0 16px #38bdf822;
  }

  /* ── Resolución paso a paso ── */
  .resolucion {
      background: #0f172a;
      border: 1px solid #1e40af55;
      border-left: 4px solid #818cf8;
      border-radius: 10px;
      padding: 20px 24px;
      margin: 14px 0;
      font-family: 'Space Mono', monospace;
      font-size: 0.88rem;
      line-height: 2;
      color: #94a3b8;
  }
  .resolucion h4 {
      color: #818cf8;
      font-size: 0.8rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin: 0 0 12px 0;
  }
  .paso {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      margin: 6px 0;
  }
  .paso-num {
      background: #1e293b;
      border: 1px solid #38bdf844;
      color: #38bdf8;
      border-radius: 50%;
      width: 22px;
      height: 22px;
      min-width: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.7rem;
      font-weight: 700;
      margin-top: 2px;
  }
  .paso-texto { color: #cbd5e1; }
  .resultado-final {
      background: #1e293b;
      border-radius: 8px;
      padding: 10px 16px;
      margin-top: 12px;
      color: #38bdf8;
      font-weight: 700;
      font-size: 1rem;
  }

  /* ── Feedback correcto ── */
  .fb-correcto {
      background: #052e16;
      border: 1px solid #166534;
      border-radius: 10px;
      padding: 14px 20px;
      color: #4ade80;
      font-weight: 700;
      font-size: 1rem;
      margin: 8px 0;
  }
  .fb-incorrecto {
      background: #2d1515;
      border: 1px solid #7f1d1d;
      border-radius: 10px;
      padding: 14px 20px;
      color: #f87171;
      font-weight: 700;
      font-size: 1rem;
      margin: 8px 0;
  }
  .opcion-correcta-highlight {
      background: #052e16;
      border: 1px solid #166534;
      border-radius: 8px;
      padding: 12px 18px;
      color: #4ade80;
      margin: 3px 0;
      font-family: 'Space Mono', monospace;
      font-size: 0.92rem;
  }
  .opcion-incorrecta-highlight {
      background: #2d1515;
      border: 1px solid #7f1d1d;
      border-radius: 8px;
      padding: 12px 18px;
      color: #f87171;
      margin: 3px 0;
      font-family: 'Space Mono', monospace;
      font-size: 0.92rem;
  }
  .opcion-neutra {
      padding: 12px 18px;
      color: #334155;
      margin: 3px 0;
      font-family: 'Space Mono', monospace;
      font-size: 0.92rem;
  }

  /* ── Animaciones fin ── */
  .anim-correcto {
      text-align: center;
      animation: popIn 0.5s cubic-bezier(0.175,0.885,0.32,1.275);
  }
  .anim-incorrecto {
      text-align: center;
      animation: shake 0.5s ease;
  }
  @keyframes popIn {
      0%   { transform: scale(0.5); opacity: 0; }
      100% { transform: scale(1);   opacity: 1; }
  }
  @keyframes shake {
      0%,100% { transform: translateX(0); }
      20%      { transform: translateX(-8px); }
      40%      { transform: translateX(8px); }
      60%      { transform: translateX(-5px); }
      80%      { transform: translateX(5px); }
  }

  /* ── Marcador ── */
  .marcador {
      background: #0f172a;
      border: 1px solid #38bdf855;
      border-radius: 8px;
      padding: 8px 16px;
      font-family: 'Space Mono', monospace;
      font-size: 1rem;
      color: #38bdf8;
      display: inline-block;
      float: right;
  }

  /* ── Pantalla final ── */
  .pantalla-final { text-align: center; padding: 20px 0; }
  .score-final {
      font-family: 'Space Mono', monospace;
      font-size: 4.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1;
  }
  .mensaje-final { color: #64748b; font-size: 1.1rem; margin: 10px 0 24px 0; }

  /* ── Estrellas animadas en victorias ── */
  .estrella-anim {
      display: inline-block;
      animation: orbit 1.5s ease infinite alternate;
      font-size: 2.5rem;
  }
  @keyframes orbit {
      0%   { transform: translateY(0) rotate(-10deg); }
      100% { transform: translateY(-12px) rotate(10deg); }
  }

  /* Intro info box */
  .info-box {
      background: #0f172a;
      border: 1px solid #1e40af44;
      border-radius: 12px;
      padding: 20px 24px;
      margin: 16px 0;
      color: #94a3b8;
      font-size: 1rem;
      line-height: 1.8;
  }
  .info-box strong { color: #38bdf8; }
</style>
""", unsafe_allow_html=True)


# ── Banco de preguntas con resolución paso a paso ────────────────────────────
BANCO = [
    {
        "enunciado": "Resuelve:   2x + 5 = 13",
        "correcta": "x = 4",
        "opciones": ["x = 4", "x = 9", "x = 3", "x = 6"],
        "pasos": [
            ("Ecuación original", "2x + 5 = 13"),
            ("Restamos 5 en ambos lados", "2x + 5 − 5 = 13 − 5  →  2x = 8"),
            ("Dividimos ambos lados entre 2", "2x ÷ 2 = 8 ÷ 2"),
        ],
        "resultado": "x = 4",
        "verificacion": "Verificación: 2(4) + 5 = 8 + 5 = 13 ✔",
    },
    {
        "enunciado": "Resuelve:   3x − 7 = 11",
        "correcta": "x = 6",
        "opciones": ["x = 6", "x = 4", "x = 8", "x = 3"],
        "pasos": [
            ("Ecuación original", "3x − 7 = 11"),
            ("Sumamos 7 en ambos lados", "3x − 7 + 7 = 11 + 7  →  3x = 18"),
            ("Dividimos ambos lados entre 3", "3x ÷ 3 = 18 ÷ 3"),
        ],
        "resultado": "x = 6",
        "verificacion": "Verificación: 3(6) − 7 = 18 − 7 = 11 ✔",
    },
    {
        "enunciado": "Resuelve:   5x + 3 = 3x + 11",
        "correcta": "x = 4",
        "opciones": ["x = 4", "x = 7", "x = 2", "x = 5"],
        "pasos": [
            ("Ecuación original", "5x + 3 = 3x + 11"),
            ("Restamos 3x en ambos lados", "5x − 3x + 3 = 11  →  2x + 3 = 11"),
            ("Restamos 3 en ambos lados", "2x = 11 − 3  →  2x = 8"),
            ("Dividimos entre 2", "x = 8 ÷ 2"),
        ],
        "resultado": "x = 4",
        "verificacion": "Verificación: 5(4)+3 = 23 = 3(4)+11 = 23 ✔",
    },
    {
        "enunciado": "Resuelve:   (x + 6) / 2 = 5",
        "correcta": "x = 4",
        "opciones": ["x = 4", "x = 16", "x = 1", "x = 7"],
        "pasos": [
            ("Ecuación original", "(x + 6) / 2 = 5"),
            ("Multiplicamos ambos lados por 2", "(x + 6) = 5 × 2  →  x + 6 = 10"),
            ("Restamos 6 en ambos lados", "x = 10 − 6"),
        ],
        "resultado": "x = 4",
        "verificacion": "Verificación: (4 + 6)/2 = 10/2 = 5 ✔",
    },
    {
        "enunciado": "Resuelve:   4(x − 2) = 12",
        "correcta": "x = 5",
        "opciones": ["x = 5", "x = 2", "x = 7", "x = 3"],
        "pasos": [
            ("Ecuación original", "4(x − 2) = 12"),
            ("Dividimos ambos lados entre 4", "(x − 2) = 12 ÷ 4  →  x − 2 = 3"),
            ("Sumamos 2 en ambos lados", "x = 3 + 2"),
        ],
        "resultado": "x = 5",
        "verificacion": "Verificación: 4(5 − 2) = 4(3) = 12 ✔",
    },
    {
        "enunciado": "Resuelve:   7x − 4 = 2x + 16",
        "correcta": "x = 4",
        "opciones": ["x = 4", "x = 6", "x = 2", "x = 12"],
        "pasos": [
            ("Ecuación original", "7x − 4 = 2x + 16"),
            ("Restamos 2x en ambos lados", "5x − 4 = 16"),
            ("Sumamos 4 en ambos lados", "5x = 20"),
            ("Dividimos entre 5", "x = 20 ÷ 5"),
        ],
        "resultado": "x = 4",
        "verificacion": "Verificación: 7(4)−4 = 24 = 2(4)+16 = 24 ✔",
    },
    {
        "enunciado": "Resuelve:   −3x + 9 = 0",
        "correcta": "x = 3",
        "opciones": ["x = 3", "x = −3", "x = 9", "x = −9"],
        "pasos": [
            ("Ecuación original", "−3x + 9 = 0"),
            ("Restamos 9 en ambos lados", "−3x = 0 − 9  →  −3x = −9"),
            ("Dividimos entre −3 (cambia el signo)", "x = −9 ÷ −3"),
        ],
        "resultado": "x = 3",
        "verificacion": "Verificación: −3(3) + 9 = −9 + 9 = 0 ✔",
    },
    {
        "enunciado": "Resuelve:   2(3x + 1) = 20",
        "correcta": "x = 3",
        "opciones": ["x = 3", "x = 4", "x = 9", "x = 1"],
        "pasos": [
            ("Ecuación original", "2(3x + 1) = 20"),
            ("Dividimos ambos lados entre 2", "3x + 1 = 10"),
            ("Restamos 1 en ambos lados", "3x = 9"),
            ("Dividimos entre 3", "x = 9 ÷ 3"),
        ],
        "resultado": "x = 3",
        "verificacion": "Verificación: 2(3·3 + 1) = 2(10) = 20 ✔",
    },
]


# ── Estado de sesión ──────────────────────────────────────────────────────────
def init():
    defaults = {
        "iniciado": False,
        "preguntas": [],
        "idx": 0,
        "score": 0,
        "respondida": False,
        "ultima": None,
        "terminado": False,
        "historial": [],   # lista de True/False por pregunta
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def iniciar():
    sel = random.sample(BANCO, 5)
    for p in sel:
        p["_mix"] = random.sample(p["opciones"], len(p["opciones"]))
    st.session_state.preguntas = sel
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.respondida = False
    st.session_state.ultima = None
    st.session_state.terminado = False
    st.session_state.historial = []
    st.session_state.iniciado = True


def responder(opcion):
    if st.session_state.respondida:
        return
    p = st.session_state.preguntas[st.session_state.idx]
    ok = opcion == p["correcta"]
    if ok:
        st.session_state.score += 1
    st.session_state.ultima = {
        "opcion": opcion,
        "ok": ok,
        "correcta": p["correcta"],
    }
    st.session_state.historial.append(ok)
    st.session_state.respondida = True


def siguiente():
    st.session_state.idx += 1
    st.session_state.respondida = False
    st.session_state.ultima = None
    if st.session_state.idx >= 5:
        st.session_state.terminado = True


# ── Render ────────────────────────────────────────────────────────────────────
init()

st.markdown('<p class="titulo-mat">📐 TRIVIA · ECUACIONES</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Primer Grado · Despeja la incógnita</p>', unsafe_allow_html=True)
st.markdown("---")


# ════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INICIO
# ════════════════════════════════════════════════════════════════════════
if not st.session_state.iniciado:
    st.markdown("""
    <div class="info-box">
        🎯 <strong>5 preguntas</strong> sobre ecuaciones de primer grado<br>
        📋 Alternativas en <strong>orden aleatorio</strong> en cada partida<br>
        🔍 Verás la <strong>resolución paso a paso</strong> después de cada respuesta<br>
        🎉 Recibirás una <strong>animación</strong> por cada acierto (¡o ánimo si te equivocas!)
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶  INICIAR TRIVIA", use_container_width=True):
            iniciar()
            st.rerun()


# ════════════════════════════════════════════════════════════════════════
#  PANTALLA FINAL
# ════════════════════════════════════════════════════════════════════════
elif st.session_state.terminado:
    score = st.session_state.score
    hist  = st.session_state.historial

    # Emojis por pregunta
    hist_str = "  ".join(["✅" if h else "❌" for h in hist])

    if score == 5:
        st.markdown("""
        <div class="pantalla-final">
            <div style="font-size:3rem; animation: orbit 1s ease infinite alternate; display:inline-block;">🏆</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.8rem; letter-spacing:4px;
                        color:#38bdf8; text-transform:uppercase; margin:8px 0;">¡Puntaje perfecto!</div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        st.markdown(f'<div class="score-final">5 / 5</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-size:1.5rem; margin:4px 0;">{hist_str}</div>', unsafe_allow_html=True)
        st.markdown('<div class="mensaje-final">¡Dominas las ecuaciones de primer grado! Eres un crack de las matemáticas. 🧠⚡</div>', unsafe_allow_html=True)

    elif score >= 3:
        st.markdown(f'<div class="score-final">{score} / 5</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-size:1.5rem; margin:4px 0;">{hist_str}</div>', unsafe_allow_html=True)
        st.markdown('<div class="mensaje-final">¡Buen trabajo! Estás casi listo — repasa los pasos que fallaste y lo lograrás. 💪</div>', unsafe_allow_html=True)

    elif score >= 1:
        st.markdown(f'<div class="score-final">{score} / 5</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-size:1.5rem; margin:4px 0;">{hist_str}</div>', unsafe_allow_html=True)
        st.markdown('<div class="mensaje-final">¡Sigue practicando! Lee las resoluciones con calma y vuelve a intentarlo. 📚</div>', unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="score-final">0 / 5</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; font-size:1.5rem; margin:4px 0;">{hist_str}</div>', unsafe_allow_html=True)
        st.markdown('<div class="mensaje-final">No te rindas — las matemáticas se aprenden con práctica. ¡Revisa los pasos y vuelve! 🚀</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 JUGAR DE NUEVO", use_container_width=True):
            iniciar()
            st.rerun()


# ════════════════════════════════════════════════════════════════════════
#  PANTALLA DE JUEGO
# ════════════════════════════════════════════════════════════════════════
else:
    idx = st.session_state.idx
    p   = st.session_state.preguntas[idx]
    mix = p["_mix"]

    # ── Barra de progreso ──
    pct = int((idx / 5) * 100)
    st.markdown(
        f'<div class="barra-fondo"><div class="barra-fill" style="width:{pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    # ── Cabecera ──
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f'<div class="label-pregunta">Pregunta {idx + 1} de 5</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="marcador">🎯 {st.session_state.score} pts</div>', unsafe_allow_html=True)

    # ── Tarjeta de pregunta ──
    st.markdown(f'<div class="card-pregunta">{p["enunciado"]}</div>', unsafe_allow_html=True)

    letras = ["A", "B", "C", "D"]

    # ── ESTADO: SIN RESPONDER ──
    if not st.session_state.respondida:
        for i, op in enumerate(mix):
            if st.button(f"  {letras[i]})  {op}", key=f"op_{idx}_{i}", use_container_width=True):
                responder(op)
                st.rerun()

    # ── ESTADO: YA RESPONDIDA ──
    else:
        res = st.session_state.ultima

        # ── Animación de feedback ──
        if res["ok"]:
            st.markdown("""
            <div class="anim-correcto">
              <span style="font-size:3rem;">🎉✨🎊</span><br>
              <span style="font-family:'Space Mono',monospace; color:#4ade80;
                           font-size:1rem; letter-spacing:2px;">¡CORRECTO! ¡Excelente!</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="anim-incorrecto">
              <span style="font-size:2.8rem;">📚💡🔁</span><br>
              <span style="font-family:'Space Mono',monospace; color:#fbbf24;
                           font-size:0.95rem; letter-spacing:2px;">¡Sigue practicando! Mira la solución abajo.</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Alternativas marcadas ──
        for i, op in enumerate(mix):
            if op == res["correcta"]:
                st.markdown(
                    f'<div class="opcion-correcta-highlight">✅  {letras[i]})  {op}  ← Correcta</div>',
                    unsafe_allow_html=True,
                )
            elif op == res["opcion"] and not res["ok"]:
                st.markdown(
                    f'<div class="opcion-incorrecta-highlight">❌  {letras[i]})  {op}  ← Tu respuesta</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="opcion-neutra">{letras[i]})  {op}</div>',
                    unsafe_allow_html=True,
                )

        # ── Resolución paso a paso ──
        st.markdown("<br>", unsafe_allow_html=True)

        pasos_html = ""
        for n, (desc, expr) in enumerate(p["pasos"], 1):
            pasos_html += f"""
            <div class="paso">
              <div class="paso-num">{n}</div>
              <div class="paso-texto">
                <span style="color:#64748b; font-size:0.8rem;">{desc}</span><br>
                <code style="color:#e2e8f0; background:transparent; font-size:0.95rem;">{expr}</code>
              </div>
            </div>
            """

        st.markdown(f"""
        <div class="resolucion">
          <h4>📋 Resolución paso a paso</h4>
          {pasos_html}
          <div class="resultado-final">
            ➜ &nbsp; {p["resultado"]}
          </div>
          <div style="margin-top:10px; color:#475569; font-size:0.8rem;">
            {p["verificacion"]}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Botón siguiente ──
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            label = "🏁 VER RESULTADO FINAL" if idx == 4 else "➡️ SIGUIENTE PREGUNTA"
            if st.button(label, use_container_width=True):
                siguiente()
                st.rerun()
