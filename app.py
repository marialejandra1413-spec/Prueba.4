import streamlit as st
import random
import time

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="🎸 Trivia Rock Peruano",
    page_icon="🎸",
    layout="centered",
)

# ── CSS custom – estética rock oscura ────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;600;700&display=swap');

  /* Fondo */
  html, body, [data-testid="stAppViewContainer"] {
      background: #0a0a0f;
      color: #e8e8e8;
  }
  [data-testid="stHeader"] { background: transparent; }

  /* Tipografía global */
  html { font-family: 'Rajdhani', sans-serif; }

  /* Título principal */
  .titulo-rock {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 3.2rem;
      letter-spacing: 4px;
      background: linear-gradient(90deg, #ff2d55, #ff9500, #ff2d55);
      background-size: 200%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: gradientShift 3s ease infinite;
      text-align: center;
      margin-bottom: 0;
  }
  .subtitulo {
      text-align: center;
      color: #888;
      font-size: 1rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-top: 0;
  }
  @keyframes gradientShift {
      0%   { background-position: 0% }
      50%  { background-position: 100% }
      100% { background-position: 0% }
  }

  /* Tarjeta de pregunta */
  .card-pregunta {
      background: linear-gradient(135deg, #12121a, #1c1c2e);
      border: 1px solid #ff2d5533;
      border-left: 4px solid #ff2d55;
      border-radius: 12px;
      padding: 24px 28px;
      margin: 16px 0 8px 0;
      font-family: 'Rajdhani', sans-serif;
      font-size: 1.25rem;
      font-weight: 600;
      color: #f0f0f0;
      box-shadow: 0 0 30px #ff2d5522;
  }
  .num-pregunta {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 0.9rem;
      letter-spacing: 3px;
      color: #ff2d55;
  }

  /* Barra de progreso custom */
  .barra-wrap { margin: 12px 0 20px 0; }
  .barra-fondo {
      background: #1c1c2e;
      border-radius: 99px;
      height: 6px;
      width: 100%;
  }
  .barra-fill {
      height: 6px;
      border-radius: 99px;
      background: linear-gradient(90deg, #ff2d55, #ff9500);
      transition: width 0.4s ease;
  }

  /* Botones de alternativas */
  div.stButton > button {
      background: #12121a;
      border: 1px solid #333;
      color: #e8e8e8;
      font-family: 'Rajdhani', sans-serif;
      font-size: 1.05rem;
      font-weight: 600;
      letter-spacing: 1px;
      border-radius: 8px;
      padding: 12px 20px;
      width: 100%;
      text-align: left;
      transition: all 0.2s ease;
      margin-bottom: 2px;
  }
  div.stButton > button:hover {
      background: #1e1e30;
      border-color: #ff2d55;
      color: #ff2d55;
      transform: translateX(4px);
      box-shadow: 0 0 12px #ff2d5544;
  }

  /* Feedback correcto / incorrecto */
  .fb-correcto {
      background: #0d2b1a;
      border: 1px solid #2ecc71;
      border-radius: 8px;
      padding: 14px 18px;
      color: #2ecc71;
      font-size: 1.1rem;
      font-weight: 700;
      margin: 8px 0;
  }
  .fb-incorrecto {
      background: #2b0d12;
      border: 1px solid #e74c3c;
      border-radius: 8px;
      padding: 14px 18px;
      color: #e74c3c;
      font-size: 1.1rem;
      font-weight: 700;
      margin: 8px 0;
  }

  /* Marcador */
  .marcador {
      background: #12121a;
      border: 1px solid #ff9500;
      border-radius: 10px;
      padding: 10px 18px;
      display: inline-block;
      font-family: 'Bebas Neue', sans-serif;
      font-size: 1.4rem;
      color: #ff9500;
      letter-spacing: 2px;
  }

  /* Pantalla final */
  .pantalla-final {
      text-align: center;
      padding: 30px 10px;
  }
  .score-grande {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 5rem;
      color: #ff2d55;
      line-height: 1;
  }
  .mensaje-final {
      font-size: 1.3rem;
      color: #aaa;
      margin: 10px 0 24px 0;
  }

  /* Animación confetti simulada */
  .confetti-container {
      font-size: 2.5rem;
      animation: bounce 0.6s ease infinite alternate;
      display: block;
      text-align: center;
  }
  @keyframes bounce {
      from { transform: translateY(0px) rotate(-5deg); }
      to   { transform: translateY(-14px) rotate(5deg); }
  }
  .fuego { animation: fuego 0.8s ease infinite alternate; }
  @keyframes fuego {
      from { filter: brightness(1); }
      to   { filter: brightness(1.6) drop-shadow(0 0 12px #ff2d55); }
  }

  /* Botón reiniciar */
  .stButton.reiniciar > button {
      background: linear-gradient(90deg, #ff2d55, #ff9500);
      color: #fff;
      border: none;
      font-size: 1.1rem;
      font-weight: 700;
  }
</style>
""", unsafe_allow_html=True)


# ── Banco de preguntas ────────────────────────────────────────────────────────
TODAS_LAS_PREGUNTAS = [
    {
        "pregunta": "¿Quién es el vocalista de Líbido, una de las bandas más exitosas del rock peruano de los 90s?",
        "correcta": "Salim Vera",
        "opciones": ["Salim Vera", "Pedro Suárez-Vértiz", "Daniel F", "Rafo Quispe"],
        "dato": "💡 Salim Vera lideró Líbido desde su formación en 1996 en Lima.",
    },
    {
        "pregunta": "¿Quién fue el carismático vocalista de Arena Hash, banda pionera del rock peruano mainstream?",
        "correcta": "Pedro Suárez-Vértiz",
        "opciones": ["Pedro Suárez-Vértiz", "Salim Vera", "Fredy Ortiz", "Erwin Flores"],
        "dato": "💡 Pedro Suárez-Vértiz fundó Arena Hash en 1990 antes de iniciar su exitosa carrera solista.",
    },
    {
        "pregunta": "¿Quién es el vocalista de Uchpa, la banda que fusiona el rock con el quechua?",
        "correcta": "Fredy Ortiz",
        "opciones": ["Fredy Ortiz", "Toño Jara", "Rafo Quispe", "Daniel F"],
        "dato": "💡 Fredy Ortiz es guitarrista y vocalista de Uchpa, banda que canta íntegramente en quechua.",
    },
    {
        "pregunta": "¿Quién es el vocalista y fundador de Leusemia, banda emblemática del punk rock peruano?",
        "correcta": "Daniel F",
        "opciones": ["Daniel F", "Salim Vera", "Pedro Suárez-Vértiz", "Erwin Flores"],
        "dato": "💡 Daniel F (Daniel Funes) fundó Leusemia en 1982, considerada la primera banda punk del Perú.",
    },
    {
        "pregunta": "¿Quién fue el vocalista de Los Saicos, precursores mundiales del punk nacidos en Lima en los 60s?",
        "correcta": "Erwin Flores",
        "opciones": ["Erwin Flores", "Rafo Quispe", "Daniel F", "Fredy Ortiz"],
        "dato": "💡 Los Saicos (1964) son reconocidos internacionalmente como uno de los primeros grupos punk del mundo.",
    },
    {
        "pregunta": "¿Quién es la vocalista de Mar de Copas, banda de rock alternativo que marcó los 90s en el Perú?",
        "correcta": "Marisse Delgado",
        "opciones": ["Marisse Delgado", "Sandra Muente", "Daniela Darcourt", "Sara Van"],
        "dato": "💡 Marisse Delgado es la voz y alma de Mar de Copas, banda formada en Lima en 1993.",
    },
    {
        "pregunta": "¿Quién es el vocalista de La Sarita, la banda que mezcla rock con música afroperuana?",
        "correcta": "Toño Jara",
        "opciones": ["Toño Jara", "Salim Vera", "Fredy Ortiz", "Pedro Suárez-Vértiz"],
        "dato": "💡 La Sarita es conocida por su fusión única de rock, ska y ritmos afroperuanos.",
    },
    {
        "pregunta": "¿Cuál de estos cantantes perteneció a la banda de rock psicodélico Traffic Sound en los 70s?",
        "correcta": "Percy Gibson",
        "opciones": ["Percy Gibson", "Daniel F", "Erwin Flores", "Rafo Quispe"],
        "dato": "💡 Traffic Sound fue una pionera del rock psicodélico latinoamericano grabando en inglés.",
    },
]


# ── Estado de sesión ──────────────────────────────────────────────────────────
def init_state():
    if "iniciado" not in st.session_state:
        st.session_state.iniciado = False
    if "preguntas" not in st.session_state:
        st.session_state.preguntas = []
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "respondida" not in st.session_state:
        st.session_state.respondida = False
    if "ultima_respuesta" not in st.session_state:
        st.session_state.ultima_respuesta = None
    if "terminado" not in st.session_state:
        st.session_state.terminado = False
    if "opciones_mezcladas" not in st.session_state:
        st.session_state.opciones_mezcladas = []


def iniciar_juego():
    seleccionadas = random.sample(TODAS_LAS_PREGUNTAS, 5)
    for p in seleccionadas:
        mezclada = p["opciones"][:]
        random.shuffle(mezclada)
        p["_mezcladas"] = mezclada
    st.session_state.preguntas = seleccionadas
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.respondida = False
    st.session_state.ultima_respuesta = None
    st.session_state.terminado = False
    st.session_state.iniciado = True


def responder(opcion):
    if st.session_state.respondida:
        return
    p = st.session_state.preguntas[st.session_state.idx]
    es_correcta = opcion == p["correcta"]
    if es_correcta:
        st.session_state.score += 1
    st.session_state.ultima_respuesta = {
        "opcion": opcion,
        "correcta": es_correcta,
        "correcta_texto": p["correcta"],
        "dato": p["dato"],
    }
    st.session_state.respondida = True


def siguiente_pregunta():
    st.session_state.idx += 1
    st.session_state.respondida = False
    st.session_state.ultima_respuesta = None
    if st.session_state.idx >= 5:
        st.session_state.terminado = True


# ── RENDER ────────────────────────────────────────────────────────────────────
init_state()

st.markdown('<p class="titulo-rock">🎸 TRIVIA ROCK PERUANO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">¿Conoces a los vocalistas del rock nacional?</p>', unsafe_allow_html=True)
st.markdown("---")

# ── PANTALLA DE INICIO ───────────────────────────────────────────────────────
if not st.session_state.iniciado:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <p style="font-size:1.15rem; color:#aaa; line-height:1.8;">
            5 preguntas sobre los <strong style="color:#ff2d55">vocalistas</strong> de las bandas más icónicas<br>
            del <strong style="color:#ff9500">rock peruano</strong>. Alternativas en orden aleatorio.<br><br>
            🎤 Los Saicos · Líbido · Leusemia · Uchpa · y más...
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ INICIAR TRIVIA", use_container_width=True):
            iniciar_juego()
            st.rerun()

# ── PANTALLA FINAL ───────────────────────────────────────────────────────────
elif st.session_state.terminado:
    score = st.session_state.score
    total = 5

    if score == total:
        # ── ANIMACIÓN PERFECTA ────────────────────────────────────────────────
        st.markdown("""
        <div class="pantalla-final">
            <span class="confetti-container fuego">🔥🎸🤘🎸🔥</span>
            <div class="score-grande">5 / 5</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2rem; 
                        background:linear-gradient(90deg,#ff2d55,#ff9500);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        letter-spacing:3px; margin: 8px 0;">
                ¡LEYENDA DEL ROCK PERUANO!
            </div>
            <div class="mensaje-final">
                ¡Acertaste todo! Eres un verdadero conocedor del rock nacional 🤘
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Animación con balloons de Streamlit
        st.balloons()
        time.sleep(0.5)

        # Letras animadas con efecto
        cols = st.columns(5)
        emojis = ["🎸", "🤘", "🎤", "⚡", "🥁"]
        labels = ["Líbido", "Leusemia", "Los Saicos", "Uchpa", "Arena Hash"]
        for i, (col, emo, lab) in enumerate(zip(cols, emojis, labels)):
            with col:
                st.markdown(
                    f"<div style='text-align:center;font-size:2rem;animation:bounce 0.6s {i*0.1:.1f}s ease infinite alternate;'>{emo}</div>"
                    f"<div style='text-align:center;font-size:0.7rem;color:#888;'>{lab}</div>",
                    unsafe_allow_html=True,
                )

    elif score >= 3:
        st.markdown(f"""
        <div class="pantalla-final">
            <span style="font-size:3rem;">🤘</span>
            <div class="score-grande">{score} / {total}</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#ff9500; letter-spacing:2px;">
                ¡Buen nivel, rockero!
            </div>
            <div class="mensaje-final">Casi lo tienes — vuelve a intentarlo y llega al 5/5.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pantalla-final">
            <span style="font-size:3rem;">🎵</span>
            <div class="score-grande">{score} / {total}</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:#888; letter-spacing:2px;">
                ¡Sigue escuchando rock peruano!
            </div>
            <div class="mensaje-final">Hay mucho por descubrir en la escena nacional.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 JUGAR DE NUEVO", use_container_width=True):
            iniciar_juego()
            st.rerun()

# ── PANTALLA DE JUEGO ────────────────────────────────────────────────────────
else:
    idx = st.session_state.idx
    p = st.session_state.preguntas[idx]
    opciones = p["_mezcladas"]

    # Progreso
    progreso_pct = int((idx / 5) * 100)
    st.markdown(
        f'<div class="barra-wrap">'
        f'<div class="barra-fondo"><div class="barra-fill" style="width:{progreso_pct}%"></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(
            f'<span class="num-pregunta">PREGUNTA {idx + 1} DE 5</span>',
            unsafe_allow_html=True,
        )
    with col_r:
        st.markdown(
            f'<div class="marcador">🎯 {st.session_state.score} pts</div>',
            unsafe_allow_html=True,
        )

    # Tarjeta de pregunta
    st.markdown(
        f'<div class="card-pregunta">{p["pregunta"]}</div>',
        unsafe_allow_html=True,
    )

    # Alternativas
    if not st.session_state.respondida:
        letras = ["A", "B", "C", "D"]
        for i, op in enumerate(opciones):
            if st.button(f"  {letras[i]})  {op}", key=f"btn_{idx}_{i}", use_container_width=True):
                responder(op)
                st.rerun()
    else:
        res = st.session_state.ultima_respuesta
        letras = ["A", "B", "C", "D"]

        # Mostrar opciones con marcado visual
        for i, op in enumerate(opciones):
            if op == res["correcta_texto"]:
                st.markdown(
                    f'<div class="fb-correcto">✅  {letras[i]})  {op}  ← CORRECTA</div>',
                    unsafe_allow_html=True,
                )
            elif op == res["opcion"] and not res["correcta"]:
                st.markdown(
                    f'<div class="fb-incorrecto">❌  {letras[i]})  {op}  ← Tu respuesta</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="padding:12px 18px; color:#555; font-size:1rem;">'
                    f'{letras[i]})  {op}</div>',
                    unsafe_allow_html=True,
                )

        # Dato curioso
        st.markdown(
            f'<div style="background:#12121a; border-left:3px solid #ff9500; '
            f'border-radius:6px; padding:12px 16px; margin:12px 0; color:#ccc; font-size:0.95rem;">'
            f'{res["dato"]}</div>',
            unsafe_allow_html=True,
        )

        # Botón siguiente
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            label = "🏁 VER RESULTADO" if idx == 4 else "➡️ SIGUIENTE PREGUNTA"
            if st.button(label, use_container_width=True):
                siguiente_pregunta()
                st.rerun()
