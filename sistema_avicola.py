import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import hashlib
import hmac
import time
import plotly.express as px
import plotly.graph_objects as go

# Configurar la página
st.set_page_config(
    page_title="Sistema Avícola San Marino",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# ESTILOS PROFESIONALES PREMIUM - ROJO Y BLANCO
# =============================================

st.markdown("""
<style>
    /* === ESTILOS GLOBALES === */
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* === HEADER PRINCIPAL === */
    .main-header {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(183, 28, 28, 0.3);
        border: 1px solid #ffcdd2;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ffeb3b, #ff9800, #ff5722);
    }
    
    .company-logo {
        font-family: 'Segoe UI', 'Arial Black', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: 1px;
        background: linear-gradient(135deg, #ffffff 0%, #ffebee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .company-subtitle {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .system-title {
        font-size: 1.3rem;
        margin-top: 1rem;
        opacity: 0.9;
        font-weight: 400;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* === TARJETAS DE MÉTRICAS === */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.1);
        border-left: 5px solid #d32f2f;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border: 1px solid #ffcdd2;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(211, 47, 47, 0.2);
    }
    
    /* === BOTONES PREMIUM === */
    .stButton button {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);
        border: 1px solid #ff8a80;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(211, 47, 47, 0.4);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* === SIDEBAR ELEGANTE === */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #fce4ec 100%);
        border-right: 3px solid #d32f2f;
    }
    
    .css-1d391kg .stRadio label {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
    }
    
    /* === TABS PROFESIONALES === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 500;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #fff3e0;
        border-color: #ff9800;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        color: white;
        border-color: #d32f2f;
        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);
    }
    
    /* === FORMULARIOS ELEGANTES === */
    .stTextInput input, .stSelectbox select, .stDateInput input, .stNumberInput input {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px 12px;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stDateInput input:focus, .stNumberInput input:focus {
        border-color: #d32f2f;
        box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
    }
    
    /* === TABLAS PROFESIONALES === */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%) !important;
        color: white !important;
        font-weight: 600;
        text-align: center;
        border: none;
    }
    
    /* === LOGIN PREMIUM === */
    .login-container {
        max-width: 450px;
        margin: 80px auto;
        padding: 50px;
        border: none;
        border-radius: 20px;
        background: white;
        box-shadow: 0 20px 50px rgba(183, 28, 28, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #d32f2f, #ff5252, #d32f2f);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .login-logo {
        font-family: 'Segoe UI', 'Arial Black', sans-serif;
        font-size: 2.2rem;
        color: #d32f2f;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .login-subtitle {
        font-family: 'Segoe UI', sans-serif;
        color: #666;
        font-size: 1rem;
        letter-spacing: 1px;
    }
    
    /* === TABLAS DE PROGRAMACIÓN === */
    .programacion-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 11px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .programacion-table th {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        color: white;
        padding: 14px 8px;
        text-align: center;
        border: none;
        font-weight: 600;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .programacion-table td {
        padding: 12px 8px;
        border: 1px solid #f0f0f0;
        text-align: center;
        vertical-align: middle;
        transition: all 0.3s ease;
    }
    
    .programacion-table tr:nth-child(even) {
        background-color: #fafafa;
    }
    
    .programacion-table tr:hover {
        background-color: #fff3e0;
        transform: scale(1.01);
    }
    
    .programacion-table .total-row {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        font-weight: 700;
        color: #b71c1c;
        border-top: 3px solid #d32f2f;
    }
    
    .programacion-table .subtotal-row {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        font-weight: 600;
        color: #c2185b;
        border-top: 2px solid #d32f2f;
    }
    
    /* === HEADER DE FECHA === */
    .fecha-header {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 15px 15px 0 0;
        margin-top: 2rem;
        margin-bottom: 0;
        box-shadow: 0 6px 20px rgba(183, 28, 28, 0.2);
        border: 1px solid #ffcdd2;
    }
    
    .fecha-header h3 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .fecha-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }
    
    /* === SECCIÓN DE DESCARGA === */
    .download-section {
        background: linear-gradient(135deg, #fff3e0 0%, #ffebee 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.1);
        border: 1px solid #ffe0b2;
    }
    
    /* === BADGES Y ESTADOS === */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-planned {
        background: #fff3e0;
        color: #ef6c00;
        border: 1px solid #ffb74d;
    }
    
    .status-progress {
        background: #e3f2fd;
        color: #1565c0;
        border: 1px solid #64b5f6;
    }
    
    .status-completed {
        background: #e8f5e8;
        color: #2e7d32;
        border: 1px solid #81c784;
    }
    
    /* === MENÚ LATERAL MEJORADO === */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #fce4ec 100%);
    }
    
    /* === ICONOS ANIMADOS === */
    .icon-animate {
        transition: all 0.3s ease;
        display: inline-block;
    }
    
    .icon-animate:hover {
        transform: scale(1.2) rotate(5deg);
    }
    
    /* === SCROLLBAR PERSONALIZADO === */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
    }
    
    /* === EFECTOS DE SOMBRA Y PROFUNDIDAD === */
    .shadow-premium {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .shadow-deep {
        box-shadow: 0 15px 40px rgba(183, 28, 28, 0.15);
    }
    
    /* === TÍTULOS Y ENCABEZADOS === */
    .section-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #d32f2f;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #ffcdd2;
        display: inline-block;
    }
    
    /* === ALERTAS Y NOTIFICACIONES === */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
    }
    
    .stSuccess {
        border-left-color: #4caf50;
    }
    
    .stError {
        border-left-color: #d32f2f;
    }
    
    .stWarning {
        border-left-color: #ff9800;
    }
    
    .stInfo {
        border-left-color: #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# SISTEMA DE AUTENTICACIÓN SEGURO
# =============================================

def hash_password(password):
    """Encripta la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, provided_password):
    """Verifica si la contraseña coincide"""
    return hmac.compare_digest(
        stored_hash,
        hash_password(provided_password)
    )

# Base de datos de usuarios (en producción esto debería estar en una base de datos)
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        'admin': {
            'password_hash': hash_password('admin123'),
            'nombre': 'Administrador Principal',
            'rol': 'admin',
            'activo': True
        },
        'supervisor': {
            'password_hash': hash_password('super123'),
            'nombre': 'Supervisor de Operaciones',
            'rol': 'supervisor',
            'activo': True
        },
        'conductor': {
            'password_hash': hash_password('cond123'),
            'nombre': 'Conductor Ejemplo',
            'rol': 'conductor',
            'activo': True
        }
    }

# Inicializar datos de la aplicación
if 'clientes' not in st.session_state:
    st.session_state.clientes = [
        {'codigo': 'C001', 'nombre': 'GRANJA SAN MARCOS', 'municipio': 'CUCUTA', 
         'zona': 'NORTE', 'plan_vacunal': 'STANDARD'},
        {'codigo': 'C002', 'nombre': 'AVICOLA EL PROGRESO', 'municipio': 'RIONEGRO', 
         'zona': 'ANTIOQUIA', 'plan_vacunal': 'PREMIUM'},
        {'codigo': 'C003', 'nombre': 'GRANJA LA ESPERANZA', 'municipio': 'GIRON', 
         'zona': 'CENTRO', 'plan_vacunal': 'BASIC'},
    ]

# CONDUCTORES SIMPLIFICADOS - SOLO NOMBRE E IDENTIFICACIÓN
if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {'codigo': 'D001', 'nombre': 'HERRERA OSORIO PEDRO ANGEL', 'identificacion': '123456789'},
        {'codigo': 'D002', 'nombre': 'ALMANZA KENNYG ROLLER', 'identificacion': '987654321'},
        {'codigo': 'D003', 'nombre': 'SÁNCHEZ BARRERA WILMER ALEXANDER', 'identificacion': '456789123'},
    ]

# VEHÍCULOS - SOLO PLACA Y MARCA
if 'vehiculos' not in st.session_state:
    st.session_state.vehiculos = [
        {'placa': 'WOM366', 'marca': 'CHEVROLET'},
        {'placa': 'WFD670', 'marca': 'TOYOTA'},
        {'placa': 'GQU440', 'marca': 'NISSAN'},
    ]

if 'planificacion' not in st.session_state:
    st.session_state.planificacion = []

if 'despachos' not in st.session_state:
    st.session_state.despachos = []

# =============================================
# LISTAS ACTUALIZADAS SEGÚN ESPECIFICACIONES
# =============================================

ZONAS = [
    "Magdalena Medio", "Sur", "Norte", "Babcock distribución", 
    "Ocaña", "Málaga", "Centro", "Gerencia", "Antioquia", "Venezuela"
]

# RUTAS ACTUALIZADAS SEGÚN ESPECIFICACIÓN CON HORAS
RUTAS_CON_HORAS = {
    "Mogotes Huevo (Costa Rica/S German + Primavera)": 7,
    "Dos Hilachas San Gil": 8,
    "El Dorado San Gil": 6,
    "Juan Curi San Gil": 8,
    "La Laguna San Gil": 8,
    "Villa Johana/La Maria San Gil": 6,
    "Miralindo San Gil": 8,
    "Rey David San Gil": 8,
    "San Gil-Huevo Giron": 8,
    "San Roque San Gil": 6,
    "Flandes-Giron H Pollita": 25
}

RUTAS = list(RUTAS_CON_HORAS.keys())

PLANTAS_NACIMIENTO = [
    "Distraves", "Esperanza 1", "San Gil", "Girón", "Otras"
]

PLANES_VACUNALES = [
    "STANDARD", "PREMIUM", "BASIC", "PERSONALIZADO"
]

# =============================================
# FUNCIONES PARA CÁLCULO Y VISUALIZACIÓN DE HORAS
# =============================================

def calcular_horas_programadas_semana():
    """Calcula las horas programadas por conductor para la semana actual"""
    
    # Obtener fecha actual y rango de la semana
    hoy = datetime.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes
    fin_semana = inicio_semana + timedelta(days=6)       # Domingo
    
    # Convertir a strings para comparación
    inicio_semana_str = inicio_semana.strftime("%Y-%m-%d")
    fin_semana_str = fin_semana.strftime("%Y-%m-%d")
    
    # Filtrar planificaciones de la semana actual
    planificaciones_semana = [
        p for p in st.session_state.planificacion 
        if inicio_semana_str <= p['fecha_despacho'] <= fin_semana_str
        and p.get('estado') in ['PLANIFICADO', 'PROGRAMADO']
    ]
    
    if not planificaciones_semana:
        return None
    
    # Calcular horas por conductor
    horas_conductor = {}
    
    for plan in planificaciones_semana:
        conductor = plan['conductor']
        
        # Calcular horas estimadas basadas en la ruta
        horas_estimadas = estimar_horas_por_ruta(plan.get('ruta', 'El Dorado San Gil'))
        
        if conductor not in horas_conductor:
            horas_conductor[conductor] = {
                'total_horas': 0,
                'viajes': 0,
                'detalle_viajes': []
            }
        
        horas_conductor[conductor]['total_horas'] += horas_estimadas
        horas_conductor[conductor]['viajes'] += 1
        horas_conductor[conductor]['detalle_viajes'].append({
            'fecha': plan['fecha_despacho'],
            'ruta': plan.get('ruta', 'N/A'),
            'cliente': plan['cliente'],
            'horas': horas_estimadas
        })
    
    return horas_conductor

def estimar_horas_por_ruta(ruta):
    """Estima las horas de viaje basadas en la ruta asignada"""
    return RUTAS_CON_HORAS.get(ruta, 6)  # 6 horas por defecto

def crear_grafica_horas_conductor(horas_por_conductor):
    """Crea una gráfica de barras de horas programadas por conductor"""
    
    # Preparar datos para la gráfica
    conductores = []
    horas_totales = []
    cantidad_viajes = []
    
    for conductor, datos in horas_por_conductor.items():
        conductores.append(conductor)
        horas_totales.append(datos['total_horas'])
        cantidad_viajes.append(datos['viajes'])
    
    # Crear DataFrame para Plotly
    df = pd.DataFrame({
        'Conductor': conductores,
        'Horas Programadas': horas_totales,
        'Cantidad de Viajes': cantidad_viajes
    })
    
    # Ordenar por horas (descendente)
    df = df.sort_values('Horas Programadas', ascending=False)
    
    # Crear gráfica de barras
    fig = px.bar(
        df,
        x='Conductor',
        y='Horas Programadas',
        title='Horas Programadas por Conductor - Semana Actual',
        color='Horas Programadas',
        color_continuous_scale='reds',
        text='Horas Programadas',
        hover_data={'Cantidad de Viajes': True}
    )
    
    # Personalizar la gráfica
    fig.update_traces(
        texttemplate='%{text:.0f}h',
        textposition='outside',
        marker_line_color='#d32f2f',
        marker_line_width=1.5
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#333'),
        title_font_size=20,
        title_x=0.5,
        xaxis_title="Conductor",
        yaxis_title="Horas Programadas",
        showlegend=False,
        height=500
    )
    
    # Agregar línea de promedio
    promedio_horas = df['Horas Programadas'].mean()
    fig.add_hline(
        y=promedio_horas,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Promedio: {promedio_horas:.1f}h",
        annotation_position="top right"
    )
    
    return fig

def mostrar_tabla_horas_detalle(horas_por_conductor):
    """Muestra una tabla detallada de las horas programadas"""
    
    datos_tabla = []
    for conductor, datos in horas_por_conductor.items():
        datos_tabla.append({
            'Conductor': conductor,
            'Total Horas': f"{datos['total_horas']:.1f}h",
            'Cantidad de Viajes': datos['viajes'],
            'Promedio por Viaje': f"{datos['total_horas']/datos['viajes']:.1f}h"
        })
    
    # Ordenar por total de horas (descendente)
    datos_tabla_ordenados = sorted(datos_tabla, key=lambda x: float(x['Total Horas'].replace('h', '')), reverse=True)
    
    # Mostrar tabla
    df_detalle = pd.DataFrame(datos_tabla_ordenados)
    st.dataframe(df_detalle, use_container_width=True)
    
    # Opción para ver detalles expandidos
    with st.expander("📋 Ver Detalle de Viajes por Conductor"):
        for conductor, datos in horas_por_conductor.items():
            st.markdown(f"**{conductor}** - Total: {datos['total_horas']:.1f}h en {datos['viajes']} viajes")
            
            # Crear tabla de viajes individuales
            viajes_data = []
            for viaje in datos['detalle_viajes']:
                viajes_data.append({
                    'Fecha': viaje['fecha'],
                    'Ruta': viaje['ruta'],
                    'Cliente': viaje['cliente'],
                    'Horas Estimadas': f"{viaje['horas']:.1f}h"
                })
            
            if viajes_data:
                df_viajes = pd.DataFrame(viajes_data)
                st.dataframe(df_viajes, use_container_width=True)
            st.markdown("---")

def mostrar_metricas_horas(horas_por_conductor):
    """Muestra métricas resumen de la distribución de horas"""
    
    total_horas = sum(datos['total_horas'] for datos in horas_por_conductor.values())
    total_viajes = sum(datos['viajes'] for datos in horas_por_conductor.values())
    promedio_horas = total_horas / len(horas_por_conductor) if horas_por_conductor else 0
    
    # Encontrar conductor con más y menos horas
    if horas_por_conductor:
        conductor_max = max(horas_por_conductor.items(), key=lambda x: x[1]['total_horas'])
        conductor_min = min(horas_por_conductor.items(), key=lambda x: x[1]['total_horas'])
    else:
        conductor_max = conductor_min = (None, {'total_horas': 0})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🕐 Total Horas Programadas", f"{total_horas:.1f}h")
    
    with col2:
        st.metric("📦 Total Viajes Programados", total_viajes)
    
    with col3:
        st.metric("👑 Conductor Más Horas", 
                 f"{conductor_max[0][:15]}..." if conductor_max[0] and len(conductor_max[0]) > 15 else conductor_max[0],
                 f"{conductor_max[1]['total_horas']:.1f}h")
    
    with col4:
        st.metric("📊 Promedio por Conductor", f"{promedio_horas:.1f}h")

# =============================================
# SISTEMA DE GENERACIÓN DE NÚMEROS DE DESPACHO
# =============================================

def generar_numero_despacho(fecha_despacho, planta_incubacion, orden_cargue):
    """
    Genera número de despacho según especificación:
    - Primer dígito: día de la semana (1=Lunes, 2=Martes, ..., 6=Sábado)
    - Segundo dígito: planta incubación (1=San Gil, 2=Girón)
    - Últimos dos dígitos: orden de cargue (01, 02, ...)
    """
    # Mapeo de días de la semana
    dias_semana = {
        0: 1,  # Lunes
        1: 2,  # Martes
        2: 3,  # Miércoles
        3: 4,  # Jueves
        4: 5,  # Viernes
        5: 6,  # Sábado
        6: 7   # Domingo (si aplica)
    }
    
    dia_numero = dias_semana.get(fecha_despacho.weekday(), 1)
    
    return f"{dia_numero}{planta_incubacion}{orden_cargue:02d}"

def obtener_orden_cargue_dia(fecha_despacho, planta_incubacion):
    """Obtiene el próximo orden de cargue para un día y planta específicos"""
    despachos_dia = [
        d for d in st.session_state.despachos 
        if d['fecha_despacho'] == fecha_despacho.strftime("%Y-%m-%d") 
        and d['planta_incubacion'] == planta_incubacion
    ]
    return len(despachos_dia) + 1

# =============================================
# GENERACIÓN DE PLANILLAS HTML PROFESIONALES
# =============================================

def generar_html_planilla(despacho):
    """Genera HTML de planilla de distribución profesional"""
    
    # Obtener información del vehículo
    vehiculo_placa = despacho['vehiculo'].split(' - ')[0] if ' - ' in despacho['vehiculo'] else despacho['vehiculo']
    
    # Determinar planta de cargue
    planta_cargue = "San Gil" if despacho['planta_incubacion'] == '1' else "Girón"
    
    # Calcular totales por producto
    total_azur = 0
    total_polita = 0
    total_polito = 0
    total_polito_sasso = 0
    
    if 'detalle_productos' in despacho:
        for detalle in despacho['detalle_productos']:
            total_azur += detalle.get('azur', 0)
            total_polita += detalle.get('polita', 0)
            total_polito += detalle.get('polito', 0)
            total_polito_sasso += detalle.get('polito_sasso', 0)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Planilla de Distribución {despacho['numero_despacho']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 15px;
                font-size: 12px;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #000;
                padding-bottom: 10px;
            }}
            .company-name {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .document-title {{
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0;
            }}
            .info-section {{
                margin: 15px 0;
            }}
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 15px;
                font-size: 11px;
            }}
            .info-table td {{
                padding: 6px;
                border: 1px solid #000;
                vertical-align: top;
            }}
            .info-table th {{
                padding: 6px;
                border: 1px solid #000;
                background-color: #f0f0f0;
                font-weight: bold;
            }}
            .products-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 10px;
            }}
            .products-table th, .products-table td {{
                border: 1px solid #000;
                padding: 5px;
                text-align: center;
            }}
            .products-table th {{
                background-color: #f0f0f0;
                font-weight: bold;
            }}
            .totals-row {{
                background-color: #e0e0e0;
                font-weight: bold;
            }}
            .signature-section {{
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
            }}
            .signature-box {{
                text-align: center;
                width: 45%;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 10px;
                text-align: center;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="company-name">AGROAVÍCOLA SAN MARINO S.A.</div>
            <div class="document-title">Planilla de Distribución y Transporte Regional Oriente</div>
            <div><strong>Cost. SGST - IBIS - Fecha y Hora de Impresión de Planilla:</strong> {datetime.now().strftime('%d/%m/%Y %I:%M %p')}</div>
            <div><strong>Gráfico:</strong> 1704-4070-02</div>
        </div>

        <table class="info-table">
            <tr>
                <td style="width: 20%"><strong>Hora Aspecto</strong></td>
                <td style="width: 30%">6:00 AM</td>
                <td style="width: 20%"><strong>Ruta Asignada</strong></td>
                <td style="width: 30%">{despacho.get('ruta', 'CENTRO')}</td>
            </tr>
            <tr>
                <td><strong>Placa Programada</strong></td>
                <td>{vehiculo_placa}</td>
                <td><strong>Fecha de Cargue</strong></td>
                <td>{datetime.strptime(despacho['fecha_despacho'], '%Y-%m-%d').strftime('%d/%m/%Y')}</td>
            </tr>
            <tr>
                <td><strong>Conductor</strong></td>
                <td colspan="3">{despacho.get('conductor', 'N/A')}</td>
            </tr>
        </table>

        <div class="info-section">
            <strong>No. Despacho: {despacho['numero_despacho']}</strong>
        </div>

        <div class="info-section">
            <strong>Productos de Planilla</strong>
            <table class="info-table">
                <tr>
                    <td><strong>Cantidades Totales</strong></td>
                    <td>AZUR: {total_azur:,}</td>
                    <td>POLITA: {total_polita:,}</td>
                    <td>POLITO: {total_polito:,}</td>
                    <td>POLITO SASSO: {total_polito_sasso:,}</td>
                </tr>
            </table>
        </div>

        <table class="products-table">
            <thead>
                <tr>
                    <th>Municipio/Provincia</th>
                    <th>Destino Granja</th>
                    <th>Nombre Cliente</th>
                    <th>Descripción Plan Vacunal</th>
                    <th>Fecha Nac.</th>
                    <th>Lote</th>
                    <th>Cant.</th>
                    <th>AZUR</th>
                    <th>POLITA</th>
                    <th>POLITO</th>
                    <th>POLITO SASSO</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Agregar filas de productos
    if 'detalle_productos' in despacho:
        for detalle in despacho['detalle_productos']:
            html += f"""
                <tr>
                    <td>{detalle.get('municipio', 'N/A')}</td>
                    <td>{detalle.get('destino_granja', 'N/A')}</td>
                    <td>{detalle.get('nombre_cliente', 'N/A')}</td>
                    <td>{detalle.get('plan_vacunal', 'N/A')}</td>
                    <td>{detalle.get('fecha_nacimiento', 'N/A')}</td>
                    <td>{detalle.get('lote', 'N/A')}</td>
                    <td>{detalle.get('cantidad', 0):,}</td>
                    <td>{detalle.get('azur', 0):,}</td>
                    <td>{detalle.get('polita', 0):,}</td>
                    <td>{detalle.get('polito', 0):,}</td>
                    <td>{detalle.get('polito_sasso', 0):,}</td>
                </tr>
            """
    
    # Fila de totales
    total_general = total_azur + total_polita + total_polito + total_polito_sasso
    html += f"""
                <tr class="totals-row">
                    <td colspan="6"><strong>TOTALES</strong></td>
                    <td><strong>{total_general:,}</strong></td>
                    <td><strong>{total_azur:,}</strong></td>
                    <td><strong>{total_polita:,}</strong></td>
                    <td><strong>{total_polito:,}</strong></td>
                    <td><strong>{total_polito_sasso:,}</strong></td>
                </tr>
            </tbody>
        </table>

        <div class="signature-section">
            <div class="signature-box">
                <p>Firma Conductor: _________________________</p>
                <p>Nombre: {despacho.get('conductor', '')}</p>
                <p>C.C. _________________________</p>
            </div>
            <div class="signature-box">
                <p>Firma Cliente: _________________________</p>
                <p>Nombre: _________________________</p>
                <p>C.C. _________________________</p>
            </div>
        </div>

        <div class="info-section">
            <p><strong>Observaciones:</strong> ___________________________________________________</p>
            <p>_________________________________________________________________________________</p>
        </div>

        <div class="footer">
            <p>AGROAVÍCOLA SAN MARINO S.A. - Área de Distribución y Transportes Regional Oriente</p>
            <p>Despacho {despacho['numero_despacho']} - Planta de Cargue: {planta_cargue} - Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </body>
    </html>
    """
    
    return html

def generar_html_programacion(planificaciones_filtradas, fecha_str):
    """Genera HTML profesional de la programación diaria"""
    
    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
    fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
    dia_semana = fecha_obj.strftime("%A")
    
    # Calcular totales
    total_general = sum(p['cantidad'] for p in planificaciones_filtradas)
    conductores_unicos = len(set(p['conductor'] for p in planificaciones_filtradas))
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Programación de Despachos - {fecha_formateada}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 20px;
                font-size: 12px;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 3px solid #d32f2f;
            }}
            .company-name {{
                font-size: 24px;
                font-weight: bold;
                color: #d32f2f;
                margin-bottom: 5px;
            }}
            .company-subtitle {{
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }}
            .report-title {{
                font-size: 18px;
                font-weight: bold;
                color: #b71c1c;
                margin: 15px 0;
            }}
            .report-info {{
                background: #ffebee;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #d32f2f;
            }}
            .programacion-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .programacion-table th {{
                background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%);
                color: white;
                padding: 12px 8px;
                text-align: center;
                border: 1px solid #b71c1c;
                font-weight: bold;
                font-size: 9px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .programacion-table td {{
                padding: 10px 8px;
                border: 1px solid #ddd;
                text-align: center;
                vertical-align: middle;
            }}
            .programacion-table .total-row {{
                background-color: #ffebee;
                font-weight: bold;
                color: #b71c1c;
                border-top: 2px solid #d32f2f;
            }}
            .programacion-table .subtotal-row {{
                background-color: #fce4ec;
                font-weight: bold;
                color: #c2185b;
                border-top: 1px solid #d32f2f;
            }}
            .programacion-table tr:nth-child(even) {{
                background-color: #fafafa;
            }}
            .programacion-table tr:hover {{
                background-color: #fff3e0;
            }}
            .summary {{
                background: #ffebee;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                border: 1px solid #d32f2f;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 10px;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="company-name">AGROAVÍCOLA SAN MARINO S.A.</div>
            <div class="company-subtitle">ÁREA DE DISTRIBUCIÓN Y TRANSPORTES REGIONAL ORIENTE</div>
            <div class="report-title">PROGRAMACIÓN DE DESPACHOS</div>
        </div>
        
        <div class="report-info">
            <strong>Fecha:</strong> {dia_semana} {fecha_formateada} | 
            <strong>Total Viajes:</strong> {len(planificaciones_filtradas)} | 
            <strong>Conductores:</strong> {conductores_unicos} | 
            <strong>Total Pollos:</strong> {total_general:,}
        </div>
        
        <table class="programacion-table">
            <thead>
                <tr>
                    <th>N° Viaje</th>
                    <th>Conductor</th>
                    <th>Placa</th>
                    <th>Ruta</th>
                    <th>Zona</th>
                    <th>Nombre cliente</th>
                    <th>Granja</th>
                    <th>Tipo</th>
                    <th>Cantidad</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Variables para calcular totales
    total_general_calc = 0
    planta_actual = None
    subtotal_planta = 0
    
    # Ordenar por planta para agrupar
    planificaciones_ordenadas = sorted(planificaciones_filtradas, key=lambda x: x['planta_incubacion'])
    
    for i, plan in enumerate(planificaciones_ordenadas):
        # Número de viaje (número de despacho)
        numero_viaje = plan.get('numero_despacho', f"PL{i+1:04d}")
        
        # Determinar nombre de la planta
        planta_nombre = "San Gil" if plan['planta_incubacion'] == '1' else "Girón"
        
        # Si cambió de planta, mostrar subtotal
        if planta_actual and planta_actual != plan['planta_incubacion']:
            planta_nombre_anterior = "San Gil" if planta_actual == '1' else "Girón"
            html += f"""
                <tr class="subtotal-row">
                    <td colspan="8"><strong>Total Planta de Cargue {planta_nombre_anterior}</strong></td>
                    <td><strong>{subtotal_planta:,}</strong></td>
                </tr>
            """
            subtotal_planta = 0
        
        planta_actual = plan['planta_incubacion']
        subtotal_planta += plan['cantidad']
        total_general_calc += plan['cantidad']
        
        # Extraer solo la placa del vehículo
        vehiculo_placa = plan['vehiculo'].split(' - ')[0] if ' - ' in plan['vehiculo'] else plan['vehiculo']
        
        # Fila de datos
        html += f"""
            <tr>
                <td>{numero_viaje}</td>
                <td>{plan['conductor']}</td>
                <td>{vehiculo_placa}</td>
                <td>{plan.get('ruta', 'N/A')}</td>
                <td>{plan.get('zona', 'N/A')}</td>
                <td>{plan['cliente']}</td>
                <td>{plan.get('destino_granja', 'N/A')}</td>
                <td>{plan['producto']}</td>
                <td>{plan['cantidad']:,}</td>
            </tr>
        """
    
    # Mostrar último subtotal
    if planta_actual and subtotal_planta > 0:
        planta_nombre_final = "San Gil" if planta_actual == '1' else "Girón"
        html += f"""
            <tr class="subtotal-row">
                <td colspan="8"><strong>Total Planta de Cargue {planta_nombre_final}</strong></td>
                <td><strong>{subtotal_planta:,}</strong></td>
            </tr>
        """
    
    # Mostrar total general
    html += f"""
            <tr class="total-row">
                <td colspan="8"><strong>TOTAL GENERAL</strong></td>
                <td><strong>{total_general_calc:,}</strong></td>
            </tr>
            </tbody>
        </table>
        
        <div class="summary">
            <strong>RESUMEN EJECUTIVO:</strong><br>
            • Fecha de programación: {fecha_formateada}<br>
            • Total de viajes programados: {len(planificaciones_filtradas)}<br>
            • Número de conductores asignados: {conductores_unicos}<br>
            • Cantidad total de pollos: {total_general_calc:,}<br>
            • Plantas involucradas: {', '.join(set('San Gil' if p['planta_incubacion'] == '1' else 'Girón' for p in planificaciones_filtradas))}
        </div>
        
        <div class="footer">
            AGROAVÍCOLA SAN MARINO S.A. - Área de Distribución y Transportes Regional Oriente<br>
            Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
            Este reporte fue generado automáticamente por el sistema de programación de despachos.
        </div>
    </body>
    </html>
    """
    
    return html

def mostrar_programacion_diaria(planificaciones_filtradas):
    """Muestra la programación diaria en formato de tabla profesional"""
    
    # Agrupar por fecha de despacho
    fechas_despacho = sorted(set(p['fecha_despacho'] for p in planificaciones_filtradas))
    
    for fecha_str in fechas_despacho:
        # Convertir fecha string a objeto datetime para formatear
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
        dia_semana = fecha_obj.strftime("%A")
        
        # Filtrar planificaciones para esta fecha
        planificaciones_fecha = [p for p in planificaciones_filtradas if p['fecha_despacho'] == fecha_str]
        
        # Mostrar header de la fecha
        st.markdown(f"""
        <div class="fecha-header">
            <h3>🗓️ Programación de Despachos - {dia_semana} {fecha_formateada}</h3>
            <p>📊 {len(planificaciones_fecha)} viajes programados | 👤 {len(set(p['conductor'] for p in planificaciones_fecha))} conductores</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear tabla de programación
        st.markdown("""
        <table class="programacion-table">
            <thead>
                <tr>
                    <th>N° Viaje</th>
                    <th>Conductor</th>
                    <th>Placa</th>
                    <th>Ruta</th>
                    <th>Zona</th>
                    <th>Nombre cliente</th>
                    <th>Granja</th>
                    <th>Tipo</th>
                    <th>Cantidad</th>
                </tr>
            </thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        # Variables para calcular totales
        total_general = 0
        planta_actual = None
        subtotal_planta = 0
        
        # Ordenar por planta para agrupar
        planificaciones_ordenadas = sorted(planificaciones_fecha, key=lambda x: x['planta_incubacion'])
        
        for i, plan in enumerate(planificaciones_ordenadas):
            # Número de viaje (número de despacho)
            numero_viaje = plan.get('numero_despacho', f"PL{i+1:04d}")
            
            # Determinar nombre de la planta
            planta_nombre = "San Gil" if plan['planta_incubacion'] == '1' else "Girón"
            
            # Si cambió de planta, mostrar subtotal
            if planta_actual and planta_actual != plan['planta_incubacion']:
                planta_nombre_anterior = "San Gil" if planta_actual == '1' else "Girón"
                st.markdown(f"""
                <tr class="subtotal-row">
                    <td colspan="8"><strong>Total Planta de Cargue {planta_nombre_anterior}</strong></td>
                    <td><strong>{subtotal_planta:,}</strong></td>
                </tr>
                """, unsafe_allow_html=True)
                subtotal_planta = 0
            
            planta_actual = plan['planta_incubacion']
            subtotal_planta += plan['cantidad']
            total_general += plan['cantidad']
            
            # Extraer solo la placa del vehículo
            vehiculo_placa = plan['vehiculo'].split(' - ')[0] if ' - ' in plan['vehiculo'] else plan['vehiculo']
            
            # Fila de datos
            st.markdown(f"""
            <tr>
                <td>{numero_viaje}</td>
                <td>{plan['conductor']}</td>
                <td>{vehiculo_placa}</td>
                <td>{plan.get('ruta', 'N/A')}</td>
                <td>{plan.get('zona', 'N/A')}</td>
                <td>{plan['cliente']}</td>
                <td>{plan.get('destino_granja', 'N/A')}</td>
                <td>{plan['producto']}</td>
                <td>{plan['cantidad']:,}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        # Mostrar último subtotal
        if planta_actual and subtotal_planta > 0:
            planta_nombre_final = "San Gil" if planta_actual == '1' else "Girón"
            st.markdown(f"""
            <tr class="subtotal-row">
                <td colspan="8"><strong>Total Planta de Cargue {planta_nombre_final}</strong></td>
                <td><strong>{subtotal_planta:,}</strong></td>
            </tr>
            """, unsafe_allow_html=True)
        
        # Mostrar total general
        st.markdown(f"""
        <tr class="total-row">
            <td colspan="8"><strong>TOTAL GENERAL</strong></td>
            <td><strong>{total_general:,}</strong></td>
        </tr>
        </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        # Mostrar estadísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Viajes", len(planificaciones_fecha))
        with col2:
            st.metric("Total Pollos", f"{total_general:,}")
        with col3:
            conductores_unicos = len(set(p['conductor'] for p in planificaciones_fecha))
            st.metric("Conductores", conductores_unicos)
        with col4:
            plantas = len(set(p['planta_incubacion'] for p in planificaciones_fecha))
            st.metric("Plantas", plantas)
        
        # Sección de descarga
        st.markdown("---")
        st.markdown("""
        <div class="download-section">
            <h4>📥 Descargar Programación</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            # Generar HTML para descarga
            html_content = generar_html_programacion(planificaciones_fecha, fecha_str)
            
            st.download_button(
                label="💾 Descargar HTML Profesional",
                data=html_content,
                file_name=f"programacion_despachos_{fecha_str}.html",
                mime="text/html",
                help="Descarga un reporte HTML profesional listo para imprimir"
            )
        
        with col_dl2:
            # También ofrecer descarga en CSV
            datos_csv = []
            for plan in planificaciones_fecha:
                vehiculo_placa = plan['vehiculo'].split(' - ')[0] if ' - ' in plan['vehiculo'] else plan['vehiculo']
                datos_csv.append({
                    'N_Viaje': plan.get('numero_despacho', 'N/A'),
                    'Conductor': plan['conductor'],
                    'Placa': vehiculo_placa,
                    'Ruta': plan.get('ruta', 'N/A'),
                    'Zona': plan.get('zona', 'N/A'),
                    'Cliente': plan['cliente'],
                    'Granja': plan.get('destino_granja', 'N/A'),
                    'Producto': plan['producto'],
                    'Cantidad': plan['cantidad']
                })
            
            df_csv = pd.DataFrame(datos_csv)
            csv = df_csv.to_csv(index=False, encoding='utf-8')
            
            st.download_button(
                label="📊 Descargar CSV",
                data=csv,
                file_name=f"programacion_despachos_{fecha_str}.csv",
                mime="text/csv",
                help="Descarga los datos en formato CSV para análisis"
            )

# =============================================
# SISTEMA DE LOGIN PREMIUM
# =============================================

def mostrar_login():
    """Interfaz de login premium"""
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 450px;
            margin: 80px auto;
            padding: 50px;
            border: none;
            border-radius: 20px;
            background: white;
            box-shadow: 0 20px 50px rgba(183, 28, 28, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #d32f2f, #ff5252, #d32f2f);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .login-logo {
            font-family: 'Segoe UI', 'Arial Black', sans-serif;
            font-size: 2.2rem;
            color: #d32f2f;
            margin-bottom: 0.5rem;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .login-subtitle {
            font-family: 'Segoe UI', sans-serif;
            color: #666;
            font-size: 1rem;
            letter-spacing: 1px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Header del login
        st.markdown(
            """
            <div class="login-header">
                <div class="login-logo">AGROAVÍCOLA SAN MARINO S.A.</div>
                <div class="login-subtitle">ÁREA DE DISTRIBUCIÓN Y TRANSPORTES REGIONAL ORIENTE</div>
                <div style="margin-top: 1rem; color: #333; font-size: 1.1rem; font-weight: 500;">
                    Sistema de Gestión de Despachos
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingrese su contraseña")
            
            if st.form_submit_button("🚀 Ingresar al Sistema", use_container_width=True):
                if usuario and password:
                    if usuario in st.session_state.usuarios:
                        usuario_data = st.session_state.usuarios[usuario]
                        if usuario_data['activo'] and check_password(usuario_data['password_hash'], password):
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = usuario
                            st.session_state.rol_actual = usuario_data['rol']
                            st.session_state.nombre_usuario = usuario_data['nombre']
                            st.session_state.intentos_login = 0
                            st.success(f"✅ Bienvenido, {usuario_data['nombre']}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.session_state.intentos_login = st.session_state.get('intentos_login', 0) + 1
                            st.error("❌ Usuario o contraseña incorrectos")
                    else:
                        st.session_state.intentos_login = st.session_state.get('intentos_login', 0) + 1
                        st.error("❌ Usuario no encontrado")
                else:
                    st.warning("⚠️ Complete todos los campos")
        
        # Mostrar información de usuarios demo
        with st.expander("👥 Usuarios de Prueba"):
            st.write("**Admin:** usuario: `admin` - contraseña: `admin123`")
            st.write("**Supervisor:** usuario: `supervisor` - contraseña: `super123`")
            st.write("**Conductor:** usuario: `conductor` - contraseña: `cond123`")
        
        st.markdown('</div>', unsafe_allow_html=True)

def verificar_autenticacion():
    """Verifica si el usuario está autenticado"""
    if not st.session_state.get('autenticado'):
        mostrar_login()
        st.stop()

def tiene_permiso(roles_permitidos):
    """Verifica si el usuario tiene permisos para acceder a una sección"""
    return st.session_state.get('rol_actual') in roles_permitidos

def mostrar_logout():
    """Muestra la barra de usuario y opción de logout"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.write(f"👋 **Bienvenido:** {st.session_state.get('nombre_usuario', 'Usuario')}")
    
    with col2:
        st.write(f"🎯 **Rol:** {st.session_state.get('rol_actual', 'N/A').title()}")
    
    with col3:
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = None
            st.session_state.rol_actual = None
            st.rerun()

# =============================================
# HEADER PROFESIONAL PREMIUM
# =============================================

def mostrar_header_profesional():
    """Muestra el header profesional premium con el logo de la empresa"""
    st.markdown(
        """
        <div class="main-header">
            <div class="company-logo">AGROAVÍCOLA SAN MARINO S.A.</div>
            <div class="company-subtitle">ÁREA DE DISTRIBUCIÓN Y TRANSPORTES REGIONAL ORIENTE</div>
            <div class="system-title">Sistema de Gestión de Despachos Avícolas</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================
# GESTIÓN DE USUARIOS (SOLO ADMIN)
# =============================================

def gestion_usuarios():
    """Gestión de usuarios del sistema (solo admin)"""
    if not tiene_permiso(['admin']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">👥 Gestión de Usuarios del Sistema</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Usuarios Existentes", "➕ Crear Nuevo Usuario"])
    
    with tab1:
        st.subheader("Lista de Usuarios")
        usuarios_data = []
        for usuario, datos in st.session_state.usuarios.items():
            usuarios_data.append({
                'Usuario': usuario,
                'Nombre': datos['nombre'],
                'Rol': datos['rol'],
                'Activo': '✅' if datos['activo'] else '❌'
            })
        
        if usuarios_data:
            df_usuarios = pd.DataFrame(usuarios_data)
            st.dataframe(df_usuarios, use_container_width=True)
        else:
            st.info("No hay usuarios registrados")
    
    with tab2:
        st.subheader("Crear Nuevo Usuario")
        with st.form("nuevo_usuario"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_usuario = st.text_input("Nombre de usuario")
                nombre_completo = st.text_input("Nombre completo")
            
            with col2:
                rol = st.selectbox("Rol", ["admin", "supervisor", "conductor"])
                password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("💾 Crear Usuario"):
                if nuevo_usuario and password and nombre_completo:
                    if nuevo_usuario not in st.session_state.usuarios:
                        st.session_state.usuarios[nuevo_usuario] = {
                            'password_hash': hash_password(password),
                            'nombre': nombre_completo,
                            'rol': rol,
                            'activo': True
                        }
                        st.success(f"✅ Usuario {nuevo_usuario} creado exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ El usuario ya existe")
                else:
                    st.warning("⚠️ Complete todos los campos")

# =============================================
# GESTIÓN DE CLIENTES MEJORADA (SIN RUTA ASIGNADA)
# =============================================

def gestion_clientes():
    """Gestión de clientes - VERSIÓN MEJORADA SIN RUTA ASIGNADA"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">👥 Gestión de Clientes</div>', unsafe_allow_html=True)
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs([
        "➕ Agregar Cliente Manual", 
        "📤 Cargar desde Excel", 
        "📋 Lista de Clientes"
    ])
    
    with tab1:
        st.subheader("➕ Agregar Nuevo Cliente Manualmente")
        with st.form("nuevo_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo = st.text_input("Código", value=f"C{len(st.session_state.clientes)+1:03d}")
                nombre_cliente = st.text_input("Nombre del Cliente*")
                identificacion = st.text_input("Identificación*")
                municipio_entrega = st.text_input("Municipio de Entrega*")
                granja = st.text_input("Granja*")
            
            with col2:
                zona = st.selectbox("Zona*", ZONAS)
                codigo_vendedor = st.text_input("Código de Vendedor")
                codigo_vacunal = st.text_input("Código Vacunal*")
                plan_vacunal = st.selectbox("Plan Vacunal*", PLANES_VACUNALES)
                planta_nacimiento = st.selectbox("Planta de Nacimiento*", PLANTAS_NACIMIENTO)
                if planta_nacimiento == "Otras":
                    planta_nacimiento = st.text_input("Especificar planta")
                
                observaciones = st.text_area("Observaciones")
            
            st.markdown("**Campos obligatorios***")
            
            if st.form_submit_button("💾 Guardar Cliente"):
                if (nombre_cliente and identificacion and municipio_entrega and 
                    granja and zona and codigo_vacunal and plan_vacunal and planta_nacimiento):
                    
                    # Verificar si el código ya existe
                    if any(c['codigo'] == codigo for c in st.session_state.clientes):
                        st.error("❌ El código de cliente ya existe")
                    else:
                        nuevo_cliente = {
                            'codigo': codigo,
                            'nombre': nombre_cliente,
                            'identificacion': identificacion,
                            'municipio_entrega': municipio_entrega,
                            'granja': granja,
                            'zona': zona,
                            'codigo_vendedor': codigo_vendedor,
                            'codigo_vacunal': codigo_vacunal,
                            'plan_vacunal': plan_vacunal,
                            'planta_nacimiento': planta_nacimiento,
                            'observaciones': observaciones,
                            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'registrado_por': st.session_state.usuario_actual
                        }
                        st.session_state.clientes.append(nuevo_cliente)
                        st.success("✅ Cliente guardado exitosamente!")
                        st.rerun()
                else:
                    st.warning("⚠️ Complete todos los campos obligatorios")
    
    with tab2:
        st.subheader("📤 Cargar Clientes desde Archivo Excel")
        
        st.info("""
        **Formato requerido del archivo Excel:**
        
        El archivo debe contener las siguientes columnas (en cualquier orden):
        - **Nombre de cliente** (obligatorio)
        - **Identificación** (obligatorio)
        - **Municipio de entrega** (obligatorio)
        - **Granja** (obligatorio)
        - **Zona** (obligatorio)
        - **Código de vendedor** (opcional)
        - **Código vacunal** (obligatorio)
        - **Plan Vacunal** (obligatorio)
        - **Planta de Nacimiento** (obligatorio)
        - **Observaciones** (opcional)
        
        **Zonas válidas:** Magdalena Medio, Sur, Norte, Babcock distribución, Ocaña, Málaga, Centro, Gerencia, Antioquia, Venezuela
        
        **Plantas válidas:** Distraves, Esperanza 1, San Gil, Girón, Otras
        """)
        
        archivo_excel = st.file_uploader(
            "Seleccionar archivo Excel", 
            type=['xlsx', 'xls'],
            help="Suba un archivo Excel con las columnas especificadas"
        )
        
        if archivo_excel is not None:
            try:
                # Leer el archivo Excel
                df = pd.read_excel(archivo_excel)
                
                st.success("✅ Archivo cargado correctamente")
                st.write("**Vista previa del archivo:**")
                st.dataframe(df.head())
                
                # Verificar columnas requeridas (sin ruta)
                columnas_requeridas = [
                    'nombre de cliente', 'identificación', 'municipio de entrega', 
                    'granja', 'zona', 'código vacunal', 'plan vacunal', 'planta de nacimiento'
                ]
                
                # Normalizar nombres de columnas (minúsculas y sin espacios extras)
                df.columns = df.columns.str.strip().str.lower()
                
                columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
                
                if columnas_faltantes:
                    st.error(f"❌ Faltan las siguientes columnas obligatorias: {', '.join(columnas_faltantes)}")
                    st.info("💡 Asegúrese de que los nombres de las columnas coincidan exactamente")
                else:
                    st.success("✅ Todas las columnas requeridas están presentes")
                    
                    # Validar zonas
                    zonas_validas = set(ZONAS)
                    zonas_archivo = set(df['zona'].dropna().unique())
                    zonas_invalidas = zonas_archivo - zonas_validas
                    
                    if zonas_invalidas:
                        st.warning(f"⚠️ Se encontraron zonas no válidas: {', '.join(zonas_invalidas)}")
                        st.info(f"💡 Zonas válidas: {', '.join(ZONAS)}")
                    
                    # Validar plantas
                    plantas_validas = set(PLANTAS_NACIMIENTO)
                    plantas_archivo = set(df['planta de nacimiento'].dropna().unique())
                    plantas_invalidas = plantas_archivo - plantas_validas
                    
                    if plantas_invalidas:
                        st.warning(f"⚠️ Se encontraron plantas no válidas: {', '.join(plantas_invalidas)}")
                        st.info(f"💡 Plantas válidas: {', '.join(PLANTAS_NACIMIENTO)}")
                    
                    # Mostrar resumen de datos a importar
                    st.subheader("📊 Resumen de Importación")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    
                    with col_res1:
                        st.metric("Registros a importar", len(df))
                    
                    with col_res2:
                        clientes_nuevos = len([row for _, row in df.iterrows() 
                                             if not any(c['identificacion'] == str(row['identificación']) 
                                                      for c in st.session_state.clientes)])
                        st.metric("Clientes nuevos", clientes_nuevos)
                    
                    with col_res3:
                        clientes_existentes = len(df) - clientes_nuevos
                        st.metric("Clientes existentes", clientes_existentes)
                    
                    # Opciones de importación
                    st.subheader("⚙️ Opciones de Importación")
                    
                    politica_duplicados = st.radio(
                        "¿Qué hacer con clientes existentes?",
                        ["Mantener existentes y agregar nuevos", "Reemplazar clientes existentes"],
                        help="Los clientes existentes se identifican por el número de identificación"
                    )
                    
                    if st.button("📥 Importar Clientes", type="primary"):
                        clientes_importados = 0
                        clientes_actualizados = 0
                        errores = 0
                        
                        for index, fila in df.iterrows():
                            try:
                                # Preparar datos del cliente
                                identificacion_str = str(fila['identificación'])
                                
                                # Validar zona
                                zona_fila = fila['zona']
                                if zona_fila not in ZONAS:
                                    st.warning(f"Fila {index + 2}: Zona '{zona_fila}' no válida. Se omitirá.")
                                    continue
                                
                                # Validar planta
                                planta_fila = fila['planta de nacimiento']
                                if planta_fila not in PLANTAS_NACIMIENTO:
                                    st.warning(f"Fila {index + 2}: Planta '{planta_fila}' no válida. Se omitirá.")
                                    continue
                                
                                # Buscar si el cliente ya existe
                                cliente_existente = next(
                                    (c for c in st.session_state.clientes 
                                     if c['identificacion'] == identificacion_str), 
                                    None
                                )
                                
                                if cliente_existente:
                                    if politica_duplicados == "Reemplazar clientes existentes":
                                        # Actualizar cliente existente
                                        cliente_existente.update({
                                            'nombre': fila['nombre de cliente'],
                                            'municipio_entrega': fila['municipio de entrega'],
                                            'granja': fila['granja'],
                                            'zona': zona_fila,
                                            'codigo_vendedor': fila.get('código de vendedor', ''),
                                            'codigo_vacunal': fila['código vacunal'],
                                            'plan_vacunal': fila['plan vacunal'].upper(),
                                            'planta_nacimiento': planta_fila,
                                            'observaciones': fila.get('observaciones', ''),
                                            'fecha_actualizacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            'actualizado_por': st.session_state.usuario_actual
                                        })
                                        clientes_actualizados += 1
                                    # Si es "Mantener existentes", no hacemos nada
                                else:
                                    # Crear nuevo cliente
                                    nuevo_cliente = {
                                        'codigo': f"C{len(st.session_state.clientes)+1:03d}",
                                        'nombre': fila['nombre de cliente'],
                                        'identificacion': identificacion_str,
                                        'municipio_entrega': fila['municipio de entrega'],
                                        'granja': fila['granja'],
                                        'zona': zona_fila,
                                        'codigo_vendedor': fila.get('código de vendedor', ''),
                                        'codigo_vacunal': fila['código vacunal'],
                                        'plan_vacunal': fila['plan vacunal'].upper(),
                                        'planta_nacimiento': planta_fila,
                                        'observaciones': fila.get('observaciones', ''),
                                        'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        'registrado_por': st.session_state.usuario_actual
                                    }
                                    st.session_state.clientes.append(nuevo_cliente)
                                    clientes_importados += 1
                                    
                            except Exception as e:
                                errores += 1
                                st.warning(f"Error en fila {index + 2}: {str(e)}")
                        
                        # Mostrar resultados
                        st.success(f"✅ Importación completada!")
                        st.write(f"**Resultados:**")
                        st.write(f"- 📥 Clientes nuevos importados: {clientes_importados}")
                        if politica_duplicados == "Reemplazar clientes existentes":
                            st.write(f"- 🔄 Clientes actualizados: {clientes_actualizados}")
                        st.write(f"- ❌ Errores: {errores}")
                        
                        st.rerun()
                        
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {str(e)}")
                st.info("💡 Asegúrese de que el archivo sea un Excel válido y tenga el formato correcto")
    
    with tab3:
        st.subheader("📋 Lista de Clientes")
        
        if st.session_state.clientes:
            # Crear DataFrame para mostrar
            datos_tabla = []
            for cliente in st.session_state.clientes:
                datos_tabla.append({
                    'Código': cliente['codigo'],
                    'Nombre': cliente['nombre'],
                    'Identificación': cliente.get('identificacion', 'N/A'),
                    'Municipio': cliente.get('municipio_entrega', 'N/A'),
                    'Granja': cliente.get('granja', 'N/A'),
                    'Zona': cliente.get('zona', 'N/A'),
                    'Código Vacunal': cliente.get('codigo_vacunal', 'N/A'),
                    'Plan Vacunal': cliente.get('plan_vacunal', 'N/A'),
                    'Planta Nac.': cliente.get('planta_nacimiento', 'N/A')
                })
            
            df_clientes = pd.DataFrame(datos_tabla)
            st.dataframe(df_clientes, use_container_width=True)
            
            # Estadísticas
            st.subheader("📊 Estadísticas de Clientes")
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total Clientes", len(st.session_state.clientes))
            
            with col_stat2:
                por_zona = df_clientes['Zona'].value_counts()
                zona_mayor = por_zona.index[0] if len(por_zona) > 0 else "N/A"
                st.metric("Zona con más clientes", zona_mayor)
            
            with col_stat3:
                planes = df_clientes['Plan Vacunal'].value_counts()
                plan_mayor = planes.index[0] if len(planes) > 0 else "N/A"
                st.metric("Plan más común", plan_mayor)
            
            # Exportar datos
            st.subheader("📤 Exportar Datos")
            csv = df_clientes.to_csv(index=False, encoding='utf-8')
            
            st.download_button(
                label="📥 Descargar Lista de Clientes (CSV)",
                data=csv,
                file_name=f"clientes_agroavicola_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Opción para eliminar cliente (solo admin)
            st.markdown("---")
            st.subheader("🗑️ Gestión de Clientes")
            
            if tiene_permiso(['admin']):
                col_elim1, col_elim2 = st.columns(2)
                
                with col_elim1:
                    cliente_a_eliminar = st.selectbox(
                        "Seleccionar cliente a eliminar:",
                        [f"{c['codigo']} - {c['nombre']}" for c in st.session_state.clientes],
                        key="eliminar_cliente"
                    )
                    
                    if st.button("🗑️ Eliminar Cliente Seleccionado", type="primary"):
                        codigo_eliminar = cliente_a_eliminar.split(" - ")[0]
                        st.session_state.clientes = [c for c in st.session_state.clientes if c['codigo'] != codigo_eliminar]
                        st.success("✅ Cliente eliminado!")
                        st.rerun()
                
                with col_elim2:
                    if st.button("🗑️ Eliminar TODOS los clientes", type="secondary"):
                        if st.checkbox("⚠️ Confirmar eliminación de TODOS los clientes"):
                            st.session_state.clientes = []
                            st.success("✅ Todos los clientes eliminados!")
                            st.rerun()
        else:
            st.info("No hay clientes registrados")

# =============================================
# GESTIÓN DE CONDUCTORES
# =============================================

def gestion_conductores_vehiculos():
    """Gestión de conductores SIMPLIFICADA - solo nombre e identificación"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">👤 Gestión de Conductores</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("➕ Agregar Conductor")
        with st.form("nuevo_conductor"):
            codigo = st.text_input("Código Conductor", value=f"D{len(st.session_state.conductores)+1:03d}")
            nombre = st.text_input("Nombre Completo")
            identificacion = st.text_input("Número de Identificación")
            
            if st.form_submit_button("💾 Guardar Conductor"):
                if codigo and nombre and identificacion:
                    # Verificar si el código ya existe
                    if any(c['codigo'] == codigo for c in st.session_state.conductores):
                        st.error("❌ El código de conductor ya existe")
                    else:
                        nuevo_conductor = {
                            'codigo': codigo,
                            'nombre': nombre,
                            'identificacion': identificacion
                        }
                        st.session_state.conductores.append(nuevo_conductor)
                        st.success("✅ Conductor guardado exitosamente!")
                        st.rerun()
                else:
                    st.warning("⚠️ Complete todos los campos")
        
        st.markdown("---")
        st.subheader("📤 Importar desde CSV")
        
        archivo_csv = st.file_uploader("Subir archivo CSV con conductores", type=['csv'])
        
        if archivo_csv is not None:
            try:
                df = pd.read_csv(archivo_csv)
                st.write("Vista previa del archivo:")
                st.dataframe(df.head())
                
                # Verificar columnas requeridas
                columnas_requeridas = ['codigo', 'nombre', 'identificacion']
                if all(col in df.columns for col in columnas_requeridas):
                    if st.button("📥 Importar Conductores"):
                        nuevos = 0
                        for _, fila in df.iterrows():
                            if not any(c['codigo'] == fila['codigo'] for c in st.session_state.conductores):
                                st.session_state.conductores.append({
                                    'codigo': fila['codigo'],
                                    'nombre': fila['nombre'],
                                    'identificacion': fila['identificacion']
                                })
                                nuevos += 1
                        st.success(f"✅ Importados {nuevos} nuevos conductores!")
                        st.rerun()
                else:
                    st.error("❌ El archivo debe contener las columnas: codigo, nombre, identificacion")
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")
    
    with col2:
        st.subheader("📋 Lista de Conductores")
        
        if st.session_state.conductores:
            # Crear DataFrame para mostrar
            datos_tabla = []
            for conductor in st.session_state.conductores:
                datos_tabla.append({
                    'Código': conductor['codigo'],
                    'Nombre': conductor['nombre'],
                    'Identificación': conductor['identificacion']
                })
            
            df_conductores = pd.DataFrame(datos_tabla)
            st.dataframe(df_conductores, use_container_width=True)
            
            # Botón para exportar a CSV
            csv = df_conductores.to_csv(index=False)
            
            st.download_button(
                label="📥 Descargar Lista de Conductores (CSV)",
                data=csv,
                file_name=f"conductores_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Opción para eliminar conductor
            st.markdown("---")
            st.subheader("🗑️ Eliminar Conductor")
            
            if st.session_state.conductores:
                conductor_a_eliminar = st.selectbox(
                    "Seleccionar conductor a eliminar:",
                    [f"{c['codigo']} - {c['nombre']}" for c in st.session_state.conductores],
                    key="eliminar_conductor"
                )
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("🗑️ Eliminar Conductor Seleccionado", type="primary"):
                        codigo_eliminar = conductor_a_eliminar.split(" - ")[0]
                        st.session_state.conductores = [c for c in st.session_state.conductores if c['codigo'] != codigo_eliminar]
                        st.success("✅ Conductor eliminado!")
                        st.rerun()
                
                with col_btn2:
                    if st.button("🗑️ Eliminar TODOS los conductores"):
                        st.session_state.conductores = []
                        st.success("✅ Todos los conductores eliminados!")
                        st.rerun()
        else:
            st.info("No hay conductores registrados")

# =============================================
# GESTIÓN DE VEHÍCULOS (NUEVA SECCIÓN)
# =============================================

def gestion_vehiculos():
    """Gestión de vehículos - SOLO PLACA Y MARCA"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">🚗 Gestión de Vehículos</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("➕ Agregar Vehículo")
        with st.form("nuevo_vehiculo"):
            placa = st.text_input("Placa del Vehículo*", placeholder="Ej: ABC123")
            marca = st.text_input("Marca del Vehículo*", placeholder="Ej: TOYOTA")
            
            if st.form_submit_button("💾 Guardar Vehículo"):
                if placa and marca:
                    # Verificar si la placa ya existe
                    if any(v['placa'] == placa for v in st.session_state.vehiculos):
                        st.error("❌ La placa ya existe")
                    else:
                        nuevo_vehiculo = {
                            'placa': placa,
                            'marca': marca
                        }
                        st.session_state.vehiculos.append(nuevo_vehiculo)
                        st.success("✅ Vehículo guardado exitosamente!")
                        st.rerun()
                else:
                    st.warning("⚠️ Complete todos los campos")
        
        st.markdown("---")
        st.subheader("📤 Importar desde CSV")
        
        archivo_csv = st.file_uploader("Subir archivo CSV con vehículos", type=['csv'], key="vehiculos_csv")
        
        if archivo_csv is not None:
            try:
                df = pd.read_csv(archivo_csv)
                st.write("Vista previa del archivo:")
                st.dataframe(df.head())
                
                # Verificar columnas requeridas
                columnas_requeridas = ['placa', 'marca']
                if all(col in df.columns for col in columnas_requeridas):
                    if st.button("📥 Importar Vehículos"):
                        nuevos = 0
                        for _, fila in df.iterrows():
                            if not any(v['placa'] == fila['placa'] for v in st.session_state.vehiculos):
                                st.session_state.vehiculos.append({
                                    'placa': fila['placa'],
                                    'marca': fila['marca']
                                })
                                nuevos += 1
                        st.success(f"✅ Importados {nuevos} nuevos vehículos!")
                        st.rerun()
                else:
                    st.error("❌ El archivo debe contener las columnas: placa, marca")
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")
    
    with col2:
        st.subheader("📋 Lista de Vehículos")
        
        if st.session_state.vehiculos:
            # Crear DataFrame para mostrar
            datos_tabla = []
            for vehiculo in st.session_state.vehiculos:
                datos_tabla.append({
                    'Placa': vehiculo['placa'],
                    'Marca': vehiculo['marca']
                })
            
            df_vehiculos = pd.DataFrame(datos_tabla)
            st.dataframe(df_vehiculos, use_container_width=True)
            
            # Botón para exportar a CSV
            csv = df_vehiculos.to_csv(index=False)
            
            st.download_button(
                label="📥 Descargar Lista de Vehículos (CSV)",
                data=csv,
                file_name=f"vehiculos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Opción para eliminar vehículo
            st.markdown("---")
            st.subheader("🗑️ Eliminar Vehículo")
            
            if st.session_state.vehiculos:
                vehiculo_a_eliminar = st.selectbox(
                    "Seleccionar vehículo a eliminar:",
                    [f"{v['placa']} - {v['marca']}" for v in st.session_state.vehiculos],
                    key="eliminar_vehiculo"
                )
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("🗑️ Eliminar Vehículo Seleccionado", type="primary"):
                        placa_eliminar = vehiculo_a_eliminar.split(" - ")[0]
                        st.session_state.vehiculos = [v for v in st.session_state.vehiculos if v['placa'] != placa_eliminar]
                        st.success("✅ Vehículo eliminado!")
                        st.rerun()
                
                with col_btn2:
                    if st.button("🗑️ Eliminar TODOS los vehículos"):
                        st.session_state.vehiculos = []
                        st.success("✅ Todos los vehículos eliminados!")
                        st.rerun()
        else:
            st.info("No hay vehículos registrados")

# =============================================
# SISTEMA DE PROGRAMACIÓN DE DESPACHOS (ACTUALIZADO)
# =============================================

def planificacion_semanal():
    """Planificación semanal mejorada - VERSIÓN SIMPLIFICADA"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">📅 Programación de Despachos</div>', unsafe_allow_html=True)
    
    # Tabs para diferentes funcionalidades
    tab1, tab2 = st.tabs([
        "➕ Nueva Planificación", 
        "📋 Programación Diaria"
    ])
    
    with tab1:
        st.subheader("➕ Nueva Planificación de Despacho")
        
        with st.form("nueva_planificacion", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Información Básica**")
                lote = st.text_input("Número de Lote*", placeholder="Ej: L2024-001")
                producto = st.selectbox("Producto*", ["POLITA", "POLITO", "SASSO", "AZUR", "CHICKENMIX", "OTRO"])
                if producto == "OTRO":
                    producto = st.text_input("Especificar producto")
                
                cliente = st.selectbox("Cliente*", [c['nombre'] for c in st.session_state.clientes])
                cantidad = st.number_input("Cantidad de Pollos*", min_value=1, value=1000, step=100)
                
                # Información de ubicación
                municipio = st.text_input("Municipio/Provincia*", value="BUCARAMANGA, SANTANDER")
                destino_granja = st.text_input("Granja/Destino*", placeholder="Ej: VILLA OFELIA")
                zona = st.selectbox("Zona*", ZONAS)
            
            with col2:
                st.markdown("**📅 Fechas y Transporte**")
                fecha_nacimiento = st.date_input("Fecha de Nacimiento*", min_value=datetime.now().date())
                fecha_despacho = st.date_input("Fecha de Despacho*", min_value=datetime.now().date())
                
                st.markdown("**🚚 Información de Transporte**")
                conductor = st.selectbox("Conductor Asignado*", [c['nombre'] for c in st.session_state.conductores])
                vehiculo = st.selectbox("Vehículo*", [f"{v['placa']} - {v['marca']}" for v in st.session_state.vehiculos])
                ruta = st.selectbox("Ruta Asignada*", RUTAS)
                
                planta_incubacion = st.selectbox("Planta de Incubación*", ["1", "2"], 
                                               format_func=lambda x: "San Gil" if x == "1" else "Girón")
                
                # Información adicional
                observaciones = st.text_area("Observaciones")
            
            st.markdown("**Campos obligatorios***")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button("💾 Guardar Planificación", type="primary"):
                    if lote and cliente and municipio and destino_granja:
                        # Verificar si el lote ya existe
                        lote_existente = any(p.get('lote') == lote for p in st.session_state.planificacion)
                        if lote_existente:
                            st.error("❌ El número de lote ya existe")
                        else:
                            nueva_planificacion = {
                                'id': f"PL{len(st.session_state.planificacion)+1:04d}",
                                'lote': lote,
                                'producto': producto,
                                'cliente': cliente,
                                'cantidad': cantidad,
                                'municipio': municipio,
                                'destino_granja': destino_granja,
                                'zona': zona,
                                'fecha_nacimiento': fecha_nacimiento.strftime("%Y-%m-%d"),
                                'fecha_despacho': fecha_despacho.strftime("%Y-%m-%d"),
                                'conductor': conductor,
                                'vehiculo': vehiculo,
                                'ruta': ruta,
                                'planta_incubacion': planta_incubacion,
                                'observaciones': observaciones,
                                'estado': 'PLANIFICADO',
                                'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'creado_por': st.session_state.usuario_actual
                            }
                            st.session_state.planificacion.append(nueva_planificacion)
                            st.success("✅ Planificación guardada exitosamente!")
                            st.rerun()
                    else:
                        st.warning("⚠️ Complete todos los campos obligatorios")
            
            with col_btn2:
                if st.form_submit_button("🔄 Limpiar Formulario"):
                    st.rerun()
    
    with tab2:
        st.subheader("📋 Programación Diaria de Despachos")
        
        if not st.session_state.planificacion:
            st.info("No hay planificaciones registradas")
        else:
            # Filtros simplificados
            st.markdown("### 🔍 Filtros")
            col_filtro1, col_filtro2 = st.columns(2)
            
            with col_filtro1:
                # Filtro por fecha específica
                filtro_fecha = st.date_input("Filtrar por fecha:", value=datetime.now().date())
                fecha_filtro_str = filtro_fecha.strftime("%Y-%m-%d")
            
            with col_filtro2:
                filtro_estado = st.selectbox("Filtrar por Estado", ["TODOS", "PLANIFICADO", "PROGRAMADO", "EN CURSO", "COMPLETADO"])
            
            # Aplicar filtros
            planificaciones_filtradas = st.session_state.planificacion.copy()
            
            if fecha_filtro_str:
                planificaciones_filtradas = [p for p in planificaciones_filtradas if p['fecha_despacho'] == fecha_filtro_str]
            
            if filtro_estado != "TODOS":
                planificaciones_filtradas = [p for p in planificaciones_filtradas if p['estado'] == filtro_estado]
            
            # Mostrar programación
            if planificaciones_filtradas:
                mostrar_programacion_diaria(planificaciones_filtradas)
                
                # Opciones de gestión
                st.markdown("---")
                st.subheader("🛠️ Gestión de Planificaciones")
                
                col_gest1, col_gest2 = st.columns(2)
                
                with col_gest1:
                    planificacion_seleccionada = st.selectbox(
                        "Seleccionar planificación:",
                        [f"{p['id']} - {p['lote']} - {p['cliente']}" for p in planificaciones_filtradas],
                        key="seleccion_planificacion"
                    )
                    
                    nuevo_estado = st.selectbox(
                        "Cambiar estado:",
                        ["PLANIFICADO", "PROGRAMADO", "EN CURSO", "COMPLETADO"],
                        key="cambiar_estado"
                    )
                    
                    if st.button("🔄 Actualizar Estado"):
                        id_cambiar = planificacion_seleccionada.split(" - ")[0]
                        for plan in st.session_state.planificacion:
                            if plan['id'] == id_cambiar:
                                plan['estado'] = nuevo_estado
                                st.success(f"✅ Estado actualizado a {nuevo_estado}")
                                st.rerun()
                                break
                
                with col_gest2:
                    if st.button("🗑️ Eliminar Planificación Seleccionada", type="secondary"):
                        id_eliminar = planificacion_seleccionada.split(" - ")[0]
                        st.session_state.planificacion = [p for p in st.session_state.planificacion if p['id'] != id_eliminar]
                        st.success("✅ Planificación eliminada!")
                        st.rerun()
            else:
                st.info("No hay planificaciones que coincidan con los filtros aplicados")

# =============================================
# SISTEMA MEJORADO DE DESPACHOS Y PLANILLAS
# =============================================

def generar_despacho():
    """Generar despacho diario con números de despacho automáticos"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">🚚 Generar Despacho Diario</div>', unsafe_allow_html=True)
    
    fecha = st.date_input("Fecha para despacho", datetime.now())
    planta_incubacion = st.selectbox("Planta de Incubación", ["1", "2"], 
                                   format_func=lambda x: "San Gil" if x == "1" else "Girón")
    
    if st.button("🔄 Generar Despacho Automático"):
        # Filtrar planificaciones para esta fecha
        planificaciones_hoy = [
            p for p in st.session_state.planificacion 
            if p['fecha_despacho'] == fecha.strftime("%Y-%m-%d") 
            and p['planta_incubacion'] == planta_incubacion
            and p['estado'] in ['PLANIFICADO', 'PROGRAMADO']
        ]
        
        if not planificaciones_hoy:
            st.warning("No hay planificaciones para hoy en esta planta")
            return
        
        # Obtener orden de cargue
        orden_cargue = obtener_orden_cargue_dia(fecha, planta_incubacion)
        
        # Generar número de despacho
        numero_despacho = generar_numero_despacho(fecha, planta_incubacion, orden_cargue)
        
        # Preparar detalle de productos para la planilla
        detalle_productos = []
        for plan in planificaciones_hoy:
            # Crear detalle por producto
            detalle = {
                'municipio': plan.get('municipio', 'N/A'),
                'destino_granja': plan.get('destino_granja', 'N/A'),
                'nombre_cliente': plan['cliente'],
                'plan_vacunal': plan.get('plan_vacunal', 'N/A'),
                'fecha_nacimiento': plan['fecha_nacimiento'],
                'lote': plan['lote'],
                'cantidad': plan['cantidad'],
                'azur': plan['cantidad'] if plan['producto'] == 'AZUR' else 0,
                'polita': plan['cantidad'] if plan['producto'] == 'POLITA' else 0,
                'polito': plan['cantidad'] if plan['producto'] == 'POLITO' else 0,
                'polito_sasso': plan['cantidad'] if plan['producto'] == 'SASSO' else 0
            }
            detalle_productos.append(detalle)
        
        # Crear despacho consolidado
        despacho_consolidado = {
            'numero_despacho': numero_despacho,
            'fecha_despacho': fecha.strftime("%Y-%m-%d"),
            'planta_incubacion': planta_incubacion,
            'orden_cargue': orden_cargue,
            'conductor': planificaciones_hoy[0]['conductor'],
            'vehiculo': planificaciones_hoy[0]['vehiculo'],
            'ruta': planificaciones_hoy[0].get('ruta', 'N/A'),
            'detalle_productos': detalle_productos,
            'total_pollos': sum(p['cantidad'] for p in planificaciones_hoy),
            'estado_despacho': 'ASIGNADO',
            'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar a despachos
        st.session_state.despachos.append(despacho_consolidado)
        
        # Actualizar estados de planificaciones
        for plan in planificaciones_hoy:
            plan['estado'] = 'PROGRAMADO'
            plan['numero_despacho'] = numero_despacho
        
        st.success(f"✅ Despacho {numero_despacho} generado exitosamente!")
        st.success(f"📋 Incluye {len(planificaciones_hoy)} planificaciones")
        st.success(f"🐔 Total de pollos: {despacho_consolidado['total_pollos']:,}")

def planillas_distribucion():
    """Planillas de distribución profesionales"""
    if not tiene_permiso(['admin', 'supervisor', 'conductor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">📋 Planillas de Distribución</div>', unsafe_allow_html=True)
    
    if not st.session_state.despachos:
        st.info("No hay despachos generados")
        return
    
    # Mostrar lista de despachos disponibles
    st.subheader("🚚 Despachos Generados")
    
    despachos_data = []
    for despacho in st.session_state.despachos:
        despachos_data.append({
            'N° Despacho': despacho['numero_despacho'],
            'Fecha': despacho['fecha_despacho'],
            'Planta': 'San Gil' if despacho['planta_incubacion'] == '1' else 'Girón',
            'Conductor': despacho['conductor'],
            'Vehículo': despacho['vehiculo'].split(' - ')[0] if ' - ' in despacho['vehiculo'] else despacho['vehiculo'],
            'Ruta': despacho['ruta'],
            'Total Pollos': f"{despacho['total_pollos']:,}",
            'Estado': despacho['estado_despacho']
        })
    
    df_despachos = pd.DataFrame(despachos_data)
    st.dataframe(df_despachos, use_container_width=True)
    
    # Seleccionar despacho para ver detalles y generar planilla
    st.subheader("📄 Generar Planilla de Despacho")
    
    if st.session_state.despachos:
        despacho_seleccionado = st.selectbox(
            "Seleccionar despacho:",
            [f"{d['numero_despacho']} - {d['fecha_despacho']} - {d['conductor']}" for d in st.session_state.despachos],
            key="seleccion_despacho"
        )
        
        numero_despacho_seleccionado = despacho_seleccionado.split(" - ")[0]
        despacho = next((d for d in st.session_state.despachos if d['numero_despacho'] == numero_despacho_seleccionado), None)
        
        if despacho:
            # Mostrar detalles del despacho
            st.markdown("### 📋 Detalles del Despacho")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Número de Despacho:** {despacho['numero_despacho']}")
                st.write(f"**Fecha de Despacho:** {despacho['fecha_despacho']}")
                st.write(f"**Planta de Incubación:** {'San Gil' if despacho['planta_incubacion'] == '1' else 'Girón'}")
                st.write(f"**Orden de Cargue:** {despacho['orden_cargue']}")
            
            with col2:
                st.write(f"**Conductor:** {despacho['conductor']}")
                st.write(f"**Vehículo:** {despacho['vehiculo']}")
                st.write(f"**Ruta:** {despacho['ruta']}")
                st.write(f"**Total Pollos:** {despacho['total_pollos']:,}")
            
            # Mostrar detalle de productos
            st.markdown("### 🐔 Detalle de Productos")
            if 'detalle_productos' in despacho:
                df_detalle = pd.DataFrame(despacho['detalle_productos'])
                st.dataframe(df_detalle, use_container_width=True)
            
            # Generar HTML de planilla
            st.markdown("### 🖨️ Generar Planilla")
            
            if st.button("📄 Generar Planilla para Conductor"):
                html_planilla = generar_html_planilla(despacho)
                
                # Mostrar vista previa
                st.markdown("### 👁️ Vista Previa de la Planilla")
                st.components.v1.html(html_planilla, height=800, scrolling=True)
                
                # Descargar HTML
                st.download_button(
                    label="📥 Descargar Planilla (HTML)",
                    data=html_planilla,
                    file_name=f"planilla_{despacho['numero_despacho']}_{despacho['fecha_despacho']}.html",
                    mime="text/html"
                )
                
                st.success("✅ Planilla generada exitosamente!")
                st.info("💡 **Nota:** Descarga el archivo HTML y ábrelo en tu navegador para imprimir la planilla")

def seguimiento_despachos():
    """Seguimiento de despachos"""
    if not tiene_permiso(['admin', 'supervisor', 'conductor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.markdown('<div class="section-title">📍 Seguimiento de Despachos</div>', unsafe_allow_html=True)
    
    if not st.session_state.despachos:
        st.info("No hay despachos para seguir")
        return
    
    for i, despacho in enumerate(st.session_state.despachos):
        with st.expander(f"Despacho {despacho['numero_despacho']} - {despacho['conductor']} - {despacho['ruta']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                estado = st.selectbox(
                    "Estado del Despacho",
                    ["ASIGNADO", "EN RUTA", "ENTREGADO", "PROBLEMA"],
                    index=["ASIGNADO", "EN RUTA", "ENTREGADO", "PROBLEMA"].index(despacho['estado_despacho']),
                    key=f"estado_{i}"
                )
            
            with col2:
                observaciones = st.text_input("Observaciones", 
                                            value=despacho.get('observaciones', ''),
                                            key=f"obs_{i}")
            
            if st.button("Actualizar Estado", key=f"btn_{i}"):
                st.session_state.despachos[i]['estado_despacho'] = estado
                st.session_state.despachos[i]['observaciones'] = observaciones
                st.success("✅ Estado actualizado!")

# =============================================
# DASHBOARD PRINCIPAL PREMIUM (ACTUALIZADO)
# =============================================

def mostrar_dashboard():
    """Dashboard principal premium con gráfica de horas programadas"""
    st.markdown('<div class="section-title">📊 Dashboard</div>', unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Clientes", len(st.session_state.clientes))
    with col2:
        st.metric("👤 Conductores", len(st.session_state.conductores))
    with col3:
        st.metric("🚗 Vehículos", len(st.session_state.vehiculos))
    with col4:
        pendientes = len([p for p in st.session_state.planificacion if p.get('estado') in ['PLANIFICADO', 'PROGRAMADO']])
        st.metric("📅 Planificaciones Pendientes", pendientes)
    
    # SECCIÓN NUEVA: GRÁFICA DE HORAS PROGRAMADAS POR CONDUCTOR
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Horas Programadas por Conductor (Semana Actual)</div>', unsafe_allow_html=True)
    
    # Calcular horas programadas por conductor para la semana actual
    horas_por_conductor = calcular_horas_programadas_semana()
    
    if horas_por_conductor:
        # Crear gráfica
        fig = crear_grafica_horas_conductor(horas_por_conductor)
        
        # Mostrar gráfica
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar tabla de datos detallada
        st.markdown("### 📋 Detalle de Horas Programadas")
        mostrar_tabla_horas_detalle(horas_por_conductor)
        
        # Métricas resumen
        st.markdown("### 📊 Métricas de Distribución de Horas")
        mostrar_metricas_horas(horas_por_conductor)
    else:
        st.info("ℹ️ No hay horas programadas para la semana actual. Las horas se calculan automáticamente basándose en las planificaciones de despacho.")
    
    # Información adicional solo para admin/supervisor
    if tiene_permiso(['admin', 'supervisor']):
        st.markdown("---")
        st.subheader("📈 Información Detallada")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👥 Usuarios Conectados:**")
            st.markdown(f"- **{st.session_state.get('nombre_usuario', 'N/A')}** ({st.session_state.get('rol_actual', 'N/A')})")
        
        with col2:
            st.markdown("**📊 Estadísticas del Sistema:**")
            st.markdown(f"- **Total despachos:** {len(st.session_state.despachos)}")
            st.markdown(f"- **Planificación total:** {len(st.session_state.planificacion)}")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%); border-radius: 15px; border: 2px solid #ffcdd2;">
        <h3 style="color: #d32f2f; margin-bottom: 1rem;">🚀 Sistema de Gestión v4.0</h3>
        <p style="color: #666; font-size: 1.1rem; margin: 0;"><strong>AGROAVÍCOLA SAN MARINO S.A.</strong></p>
        <p style="color: #888; margin-top: 0.5rem;">Área de Distribución y Transportes Regional Oriente</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# MENÚ PRINCIPAL PREMIUM
# =============================================

def main():
    # Verificar autenticación
    if not st.session_state.get('autenticado'):
        mostrar_login()
        return
    
    # Mostrar barra de usuario
    mostrar_logout()
    
    # Mostrar header profesional premium
    mostrar_header_profesional()
    
    # Menú en sidebar según permisos
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%); border-radius: 10px; color: white;">
            <h3 style="margin: 0; font-size: 1.2rem;">🧭 Navegación</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Distribución y Transportes</p>
        </div>
        """, unsafe_allow_html=True)
        
        opciones_menu = ["📊 Dashboard"]
        
        # Opciones para admin y supervisor
        if tiene_permiso(['admin', 'supervisor']):
            opciones_menu.extend([
                "👥 Gestión Clientes", 
                "👤 Gestión Conductores", 
                "🚗 Gestión Vehículos",
                "📅 Programación", 
                "🚚 Despacho"
            ])
        
        # Opciones para todos los roles autenticados
        opciones_menu.extend([
            "📋 Planillas", 
            "📍 Seguimiento"
        ])
        
        # Opción solo para admin
        if tiene_permiso(['admin']):
            opciones_menu.append("🔐 Gestión Usuarios")
        
        opcion = st.radio("Seleccione:", opciones_menu)
    
    # Navegar entre secciones
    if opcion == "📊 Dashboard":
        mostrar_dashboard()
    elif opcion == "👥 Gestión Clientes":
        gestion_clientes()
    elif opcion == "👤 Gestión Conductores":
        gestion_conductores_vehiculos()
    elif opcion == "🚗 Gestión Vehículos":
        gestion_vehiculos()
    elif opcion == "🔐 Gestión Usuarios":
        gestion_usuarios()
    elif opcion == "📅 Programación":
        planificacion_semanal()
    elif opcion == "🚚 Despacho":
        generar_despacho()
    elif opcion == "📋 Planillas":
        planillas_distribucion()
    elif opcion == "📍 Seguimiento":
        seguimiento_despachos()

if __name__ == "__main__":
    main()
