import streamlit as st
import numpy as np

st.set_page_config(page_title="Encuesta", page_icon="📋", layout="centered")

# ---------- Estado y helpers de navegación ----------
if "page" not in st.session_state:
    st.session_state.page = "demo"   # página inicial

def go_to(page_name: str):
    st.session_state.page = page_name

def go_to_and_rerun(page_name: str):
    st.session_state.page = page_name
    st.rerun()

# (Opcional) ver página actual en sidebar para depurar
st.sidebar.markdown(f"**Página actual:** `{st.session_state.page}`")


# ---------- Paso 1: Demográficos ----------
def render_demograficos():
    st.title("Encuesta — Datos demográficos")

    with st.form("form_demo"):

        st.radio(
            "Rango de edad",
            ["18–24","25–34","35–44","45–54","55–64","65+"],
            index=None, key="edad"
        )

        st.radio(
            "Género",
            ["Femenino","Masculino","Otro / Prefiero no decir"],
            index=None, key="genero"
        )

        st.radio(
            "Nivel educativo",
            ["Secundaria o menos","Técnico",
             "Universitario incompleto","Universitario completo","Posgrado"],
            index=None, key="edu"
        )

        st.radio(
            "Situación familiar actual",
            ["Soltero/a sin hijos","Pareja/convivencia sin hijos",
             "Familia con hijos menores de 10","Familia con hijos de 10+",
             "Nido vacío (hijos no viven en casa)","Otro"],
            index=None, key="fam"
        )

        st.radio(
            "Ingreso familiar mensual",
            ["< 1,500","1,500 – 3,000","3,000 – 6,000","6,000 – 10,000","> 10,000","Prefiero no decir"],
            index=None, key="ingreso"
        )
        st.caption("Considera el ingreso sumado de todos los miembros del hogar que trabajan.")

        st.radio(
            "Tipo de vivienda",
            ["Propia","Alquilada","Vivo en casa de familiares","Otro"],
            index=None, key="vivienda"
        )

        submitted = st.form_submit_button("Continuar")

    if submitted:
        if None in (st.session_state.edad,
                    st.session_state.genero,
                    st.session_state.edu,
                    st.session_state.fam,
                    st.session_state.ingreso,
                    st.session_state.vivienda):
            st.error("Por favor responde todas las preguntas antes de continuar.")
        else:
            st.success("Datos demográficos registrados.")
            go_to_and_rerun("pvq")  # navega a PVQ


# ---------- Paso 2: PVQ-40 ----------
def render_pvq():
    st.title("Sección 2 — PVQ-40 (Portrait Values Questionnaire)")

    st.info(
        "A continuación se describen brevemente distintas personas. "
        "Piensa cuánto se parece esa descripción a ti. "
        "Responde con una escala de 1 a 6 donde: "
        "1 = Nada parecido a mí, 2 = Poco parecido, 3 = Un poco parecido, "
        "4 = Algo parecido, 5 = Parecido, 6 = Muy parecido a mí."
    )

    items = [
        "1) Valora pensar ideas nuevas y ser creativo/a; le gusta hacer las cosas a su manera.",
        "2) Le importa ser rico/a; desea tener mucho dinero y cosas caras.",
        "3) Cree que todas las personas deben ser tratadas por igual; todos deberían tener las mismas oportunidades.",
        "4) Le importa mostrar sus capacidades; quiere que la gente admire lo que hace.",
        "5) Valora vivir en entornos seguros; evita lo que pueda poner en peligro su seguridad.",
        "6) Cree que es importante hacer muchas cosas distintas en la vida; siempre busca probar cosas nuevas.",
        "7) Piensa que las personas deben hacer lo que se les pide; seguir reglas incluso cuando nadie mira.",
        "8) Le importa escuchar a quienes son diferentes; aunque no esté de acuerdo, busca comprenderlos.",
        "9) Cree que no hay que pedir más de lo que se tiene; es mejor estar satisfecho/a con lo que uno tiene.",
        "10) Busca cada oportunidad para divertirse; le importa hacer cosas que le den placer.",
        "11) Le importa decidir por sí mismo/a lo que hace; le gusta planear y elegir sus actividades.",
        "12) Es muy importante ayudar a las personas alrededor; quiere cuidar su bienestar.",
        "13) Ser muy exitoso/a es importante; le gusta impresionar a los demás.",
        "14) Le importa que su país sea seguro; el Estado debe vigilar amenazas internas y externas.",
        "15) Le gusta tomar riesgos; siempre está buscando aventuras.",
        "16) Le importa comportarse correctamente; evita hacer algo que otros podrían decir que está mal.",
        "17) Le importa tener el mando y decir a otros qué hacer; quiere que la gente haga lo que dice.",
        "18) Ser leal a sus amistades es importante; quiere dedicarse a la gente cercana.",
        "19) Cree firmemente que hay que cuidar la naturaleza.",
        "20) La religión es importante; se esfuerza por cumplir lo que su religión exige.",
        "21) Le importa que todo esté ordenado y limpio; no le gusta el desorden.",
        "22) Cree que es importante interesarse por las cosas; le gusta la curiosidad y entender de todo.",
        "23) Cree que todas las personas del mundo deben vivir en armonía; promover la paz entre grupos es importante.",
        "24) Considera importante ser ambicioso/a; quiere demostrar de lo que es capaz.",
        "25) Piensa que es mejor hacer las cosas a la manera tradicional; mantener las costumbres aprendidas.",
        "26) Disfrutar los placeres de la vida es importante; le gusta darse gustos.",
        "27) Le importa responder a las necesidades de otros; intenta apoyar a quienes conoce.",
        "28) Cree que siempre se debe respetar a los padres y a las personas mayores; ser obediente es importante.",
        "29) Quiere que todos sean tratados con justicia, incluso quienes no conoce; proteger a los más débiles es importante.",
        "30) Le gustan las sorpresas; tener una vida emocionante es importante.",
        "31) Se esfuerza por no enfermarse; mantenerse saludable es muy importante.",
        "32) Progresar en la vida es importante; se esfuerza por hacerlo mejor que los demás.",
        "33) Perdonar a quienes le han hecho daño es importante; intenta ver lo bueno en ellos y no guardar rencor.",
        "34) Ser independiente es importante; le gusta depender de sí mismo/a.",
        "35) Tener un gobierno estable es importante; le preocupa que el orden social se proteja.",
        "36) Le importa ser siempre amable con otras personas; intenta no molestar ni irritar a los demás.",
        "37) Realmente quiere disfrutar la vida; pasarlo bien es muy importante.",
        "38) Ser humilde y modesto/a es importante; intenta no llamar la atención.",
        "39) Siempre quiere ser quien toma las decisiones; le gusta ser líder.",
        "40) Le importa adaptarse a la naturaleza y encajar en ella; cree que las personas no deben cambiar la naturaleza."
    ]

    value_map = {
        "Universalismo":  [3, 8, 19, 23, 29, 40],
        "Benevolencia":   [12, 18, 27, 33],
        "Tradición":      [9, 20, 25, 38],
        "Conformidad":    [7, 16, 28, 36],
        "Seguridad":      [5, 14, 21, 31, 35],
        "Poder":          [2, 17, 39],
        "Logro":          [4, 13, 24, 32],
        "Hedonismo":      [10, 26, 37],
        "Estimulación":   [6, 15, 30],
        "Autodirección":  [1, 11, 22, 34],
    }

    labels = [
        "1 – Nada parecido a mí",
        "2",
        "3",
        "4",
        "5",
        "6 – Muy parecido a mí"
    ]

    with st.form("form_pvq"):
        st.caption("Escala: 1 = Nada parecido a mí ··· 6 = Muy parecido a mí")

        for idx, texto in enumerate(items, start=1):
            st.radio(
                label=texto,
                options=labels,
                index=None,
                key=f"pvq_choice_{idx}",
                horizontal=True
            )

        col1, col2 = st.columns([1,1], gap="small")
        guardar = col1.form_submit_button("Guardar y calcular puntajes")
        volver  = col2.form_submit_button("Volver a demográficos")

    if volver:
        go_to_and_rerun("demo")
        return

    if guardar:
        # Validación
        missing = [i for i in range(1, 41) if st.session_state.get(f"pvq_choice_{i}") is None]
        if missing:
            st.error("Por favor responde **todos** los ítems antes de continuar.")
            return

        # helper: "1 – ..." -> 1 ; "3" -> 3
        def label_to_int(lbl: str) -> int:
            return int(lbl.split("–")[0].strip().split()[0])

        pvq_vals = {i: label_to_int(st.session_state[f"pvq_choice_{i}"]) for i in range(1, 41)}

        # Puntajes por valor
        value_scores, all_scores = {}, []
        for val_name, item_ids in value_map.items():
            vals = [pvq_vals[i] for i in item_ids]
            value_scores[val_name] = float(np.mean(vals))
            all_scores.extend(vals)

        overall_mean = float(np.mean(all_scores))
        adjusted = {k: round(v - overall_mean, 3) for k, v in value_scores.items()}

        macro = {
            "Autotrascendencia":  np.mean([value_scores["Universalismo"], value_scores["Benevolencia"]]),
            "Autopromoción":      np.mean([value_scores["Logro"], value_scores["Poder"]]),
            "Apertura al cambio": np.mean([value_scores["Hedonismo"], value_scores["Autodirección"], value_scores["Estimulación"]]),
            "Conservación":       np.mean([value_scores["Conformidad"], value_scores["Tradición"], value_scores["Seguridad"]]),
        }

        st.success("¡Respuestas registradas! Aquí tienes tus puntajes.")
        st.subheader("Puntajes por valor (promedio 1–6)")
        st.json({k: round(v, 3) for k, v in value_scores.items()})

        st.subheader("Puntajes ajustados (valor − media global)")
        st.json(adjusted)

        st.subheader("Macro-dimensiones (promedio de valores relacionados)")
        st.json({k: round(float(v), 3) for k, v in macro.items()})

        st.caption("Referencia: escala 1–6 del PVQ-40 y agrupación por valores/macro-dimensiones.")

    # Botón fuera del form con callback
    st.button("Continuar a CFC-14", key="btn_cfc",
              on_click=go_to_and_rerun, args=("cfc",))


# ---------- Paso 3: CFC-14 ----------
def render_cfc():
    st.title("Sección 3 — CFC-14 (Consideration of Future Consequences)")

    st.info(
        "Indica cuánto estás de acuerdo con cada afirmación. Escala de 1 a 7:\n"
        "1 = Muy en desacuerdo ··· 7 = Muy de acuerdo."
    )

    cfc_items = {
        1: ("Considera cómo podrían ser las cosas en el futuro y trata de influir en ese resultado con sus acciones cotidianas.", "F"),
        2: ("Toma en serio advertencias sobre consecuencias negativas aunque ocurran dentro de muchos años.", "F"),
        3: ("Prefiere realizar conductas con consecuencias importantes a largo plazo aunque los beneficios tarden en llegar.", "F"),
        4: ("Piensa en las consecuencias futuras de sus decisiones antes de actuar.", "F"),
        5: ("A menudo hace algo hoy porque traerá beneficios en el futuro, aunque no vea resultados de inmediato.", "F"),
        6: ("Se esfuerza por tomar decisiones que sean mejores a largo plazo.", "F"),
        7: ("Antes de elegir, evalúa cómo la opción puede afectarle (o a su familia) dentro de varios años.", "F"),

        8:  ("Solo actúa para satisfacer preocupaciones inmediatas, suponiendo que el futuro se arreglará solo.", "I"),
        9:  ("En general, da más peso a las consecuencias inmediatas que a las futuras.", "I"),
        10: ("Está dispuesto/a a sacrificar beneficios futuros por gratificación inmediata.", "I"),
        11: ("Tiende a descartar advertencias sobre posibles problemas futuros porque probablemente no pasen.", "I"),
        12: ("Cuando decide, piensa principalmente en las consecuencias inmediatas.", "I"),
        13: ("Prefiere resultados pequeños ahora a resultados mayores en el futuro.", "I"),
        14: ("Su comportamiento se guía sobre todo por lo que da beneficio ahora mismo.", "I"),
    }

    labels = [
        "1 – Muy en desacuerdo",
        "2", "3", "4", "5", "6",
        "7 – Muy de acuerdo"
    ]

    with st.form("form_cfc"):
        st.caption("Escala: 1 = Muy en desacuerdo ··· 7 = Muy de acuerdo")

        for i in range(1, 15):
            st.radio(
                label=f"{i}) {cfc_items[i][0]}",
                options=labels,
                index=None,
                key=f"cfc_choice_{i}",
                horizontal=True
            )

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("Guardar y calcular CFC")
        volver  = col2.form_submit_button("Volver a PVQ")

    if volver:
        go_to_and_rerun("pvq")
        return

    if not guardar:
        return

    # Validación
    faltantes = [i for i in range(1, 15) if st.session_state.get(f"cfc_choice_{i}") is None]
    if faltantes:
        st.error("Por favor responde **todos** los ítems antes de continuar.")
        return

    def label_to_int(lbl: str) -> int:
        return int(lbl.split("–")[0].strip().split()[0])

    cfc_vals = {i: label_to_int(st.session_state[f"cfc_choice_{i}"]) for i in range(1, 15)}

    future_ids    = [i for i, t in cfc_items.items() if t[1] == "F"]
    immediate_ids = [i for i, t in cfc_items.items() if t[1] == "I"]

    cfc_future_mean    = float(np.mean([cfc_vals[i] for i in future_ids]))
    cfc_immediate_mean = float(np.mean([cfc_vals[i] for i in immediate_ids]))

    # immediate invertidos (1<->7)
    immediate_rc = [8 - cfc_vals[i] for i in immediate_ids]
    cfc_overall_mean = float(np.mean([cfc_vals[i] for i in future_ids] + immediate_rc))

    idx_future_minus_immediate = round(cfc_future_mean - cfc_immediate_mean, 3)

    st.success("¡CFC calculado!")
    st.subheader("Resultados CFC")
    st.json({
        "CFC_Future (1–7, ↑ = más orientación al futuro)": round(cfc_future_mean, 3),
        "CFC_Immediate (1–7, ↑ = más enfoque inmediato)": round(cfc_immediate_mean, 3),
        "CFC_Overall (1–7, immediate invertido)": round(cfc_overall_mean, 3),
        "Índice (Future − Immediate)": idx_future_minus_immediate
    })

    st.caption(
        "Notas: CFC_Future es el promedio de los ítems F; CFC_Immediate es el promedio de los ítems I. "
        "CFC_Overall invierte los ítems inmediatos (1↔7) y promedia todos; valores más altos = mayor consideración del futuro."
    )

    st.divider()
    # Botón con callback a BPNSFS
    st.button("Continuar a BPNSFS (Necesidades Psicológicas Básicas)", key="btn_bpnsf",
              on_click=go_to_and_rerun, args=("bpnsf",))


# ---------- Paso 4: BPNSFS (Adultos) ----------
def render_bpnsf():
    st.title("Sección 4 — BPNSFS (Adultos) — Satisfacción y Frustración de Necesidades Psicológicas Básicas")

    st.info(
        "Indica cuánto es verdadera cada afirmación para ti EN GENERAL en tu vida.\n"
        "Escala 1–5: 1 = Totalmente falso · 2 = Falso · 3 = Ni falso ni verdadero · 4 = Verdadero · 5 = Totalmente verdadero."
    )

    # Ítems (24). 6 subescalas: AS/AF, CS/CF, RS/RF (4 ítems cada una)
    items = {
        # Autonomía — Satisfacción (AS)
        1:  ("Siento que mis elecciones y acciones reflejan lo que realmente quiero.", "AS"),
        2:  ("Siento que puedo decidir por mí mismo/a cómo vivir mi vida.", "AS"),
        3:  ("Me siento libre para hacer las cosas a mi manera.", "AS"),
        4:  ("Generalmente puedo hacer lo que realmente me interesa.", "AS"),

        # Autonomía — Frustración (AF)
        5:  ("A menudo siento que debo hacer cosas que no elijo realmente.", "AF"),
        6:  ("Siento que otros presionan o controlan lo que hago.", "AF"),
        7:  ("Siento que mis decisiones están más guiadas por obligaciones que por mis intereses.", "AF"),
        8:  ("Me cuesta actuar de acuerdo con lo que yo mismo/a considero importante.", "AF"),

        # Competencia — Satisfacción (CS)
        9:  ("Siento que hago bien la mayoría de las cosas que intento.", "CS"),
        10: ("Con frecuencia me siento capaz y eficaz en lo que hago.", "CS"),
        11: ("Siento que progreso y aprendo cosas nuevas con éxito.", "CS"),
        12: ("En general, me siento competente para manejar mis tareas diarias.", "CS"),

        # Competencia — Frustración (CF)
        13: ("Dudo de mi capacidad para lograr lo que me propongo.", "CF"),
        14: ("A menudo me siento ineficaz e incompetente.", "CF"),
        15: ("Me frustro porque no consigo hacer las cosas tan bien como quisiera.", "CF"),
        16: ("Siento que los desafíos me superan.", "CF"),

        # Relación — Satisfacción (RS)
        17: ("Me siento cercano/a y conectado/a con las personas que me rodean.", "RS"),
        18: ("Siento que hay personas que realmente se preocupan por mí.", "RS"),
        19: ("Me siento valorado/a y aceptado/a por quienes me importan.", "RS"),
        20: ("Experimenté calidez y apoyo de personas significativas.", "RS"),

        # Relación — Frustración (RF)
        21: ("A menudo me siento solo/a o aislado/a de los demás.", "RF"),
        22: ("Siento que las personas cercanas me ignoran o me excluyen.", "RF"),
        23: ("Me cuesta sentirme conectado/a con los demás.", "RF"),
        24: ("Siento que no pertenezco verdaderamente a ningún grupo.", "RF"),
    }

    labels = [
        "1 – Totalmente falso",
        "2 – Falso",
        "3 – Ni falso ni verdadero",
        "4 – Verdadero",
        "5 – Totalmente verdadero",
    ]

    with st.form("form_bpnsf"):
        st.caption("Responde todas las afirmaciones. Escala 1–5 (extremos arriba).")

        for i in range(1, 25):
            st.radio(
                label=f"{i}) {items[i][0]}",
                options=labels,
                index=None,
                key=f"bpnsf_choice_{i}",
                horizontal=True
            )

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("Guardar y calcular BPNSFS")
        volver  = col2.form_submit_button("Volver a CFC")

    if volver:
        go_to_and_rerun("cfc")
        return
    if not guardar:
        return

    # Validación
    faltantes = [i for i in range(1, 25) if st.session_state.get(f"bpnsf_choice_{i}") is None]
    if faltantes:
        st.error("Por favor responde **todos** los ítems antes de continuar.")
        return

    def label_to_int(lbl: str) -> int:
        return int(lbl.split("–")[0].strip())

    vals = {i: label_to_int(st.session_state[f"bpnsf_choice_{i}"]) for i in range(1, 25)}

    groups = {
        "Autonomía_Satisfacción":  [i for i,t in items.items() if t[1] == "AS"],
        "Autonomía_Frustración":   [i for i,t in items.items() if t[1] == "AF"],
        "Competencia_Satisfacción":[i for i,t in items.items() if t[1] == "CS"],
        "Competencia_Frustración": [i for i,t in items.items() if t[1] == "CF"],
        "Relación_Satisfacción":   [i for i,t in items.items() if t[1] == "RS"],
        "Relación_Frustración":    [i for i,t in items.items() if t[1] == "RF"],
    }

    subscale_scores = {}
    for name, idxs in groups.items():
        subscale_scores[name] = float(np.mean([vals[i] for i in idxs]))

    sat_mean  = float(np.mean([subscale_scores["Autonomía_Satisfacción"],
                               subscale_scores["Competencia_Satisfacción"],
                               subscale_scores["Relación_Satisfacción"]]))
    frus_mean = float(np.mean([subscale_scores["Autonomía_Frustración"],
                               subscale_scores["Competencia_Frustración"],
                               subscale_scores["Relación_Frustración"]]))
    diff_idx  = round(sat_mean - frus_mean, 3)

    st.success("¡BPNSFS calculado!")
    st.subheader("Subescalas (promedio 1–5)")
    st.json({k: round(v, 3) for k, v in subscale_scores.items()})

    st.subheader("Índices globales")
    st.json({
        "Satisfacción_necesidades (1–5)": round(sat_mean, 3),
        "Frustración_necesidades (1–5)": round(frus_mean, 3),
        "Índice Satisfacción − Frustración": diff_idx
    })

    st.caption(
        "Interpretación: puntajes mayores en 'Satisfacción' indican que tus necesidades psicológicas básicas "
        "(autonomía, competencia y relación) están más cubiertas; puntajes mayores en 'Frustración' indican "
        "obstáculos o carencias. El índice S−F positivo sugiere balance favorable."
    )

    st.divider()

# ---------- Router ----------
if st.session_state.page == "demo":
    render_demograficos()
elif st.session_state.page == "pvq":
    render_pvq()
elif st.session_state.page == "cfc":
    render_cfc()
elif st.session_state.page == "bpnsf":
    render_bpnsf()
