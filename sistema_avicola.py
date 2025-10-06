import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configurar la página
st.set_page_config(
    page_title="Sistema Avícola San Marino",
    page_icon="🐔",
    layout="wide"
)

# Inicializar datos
if 'clientes' not in st.session_state:
    st.session_state.clientes = [
        {'codigo': 'C001', 'nombre': 'GRANJA SAN MARCOS', 'municipio': 'CUCUTA', 
         'zona': 'NORTE', 'ruta': 'CUCUTA', 'plan_vacunal': 'STANDARD'},
        {'codigo': 'C002', 'nombre': 'AVICOLA EL PROGRESO', 'municipio': 'RIONEGRO', 
         'zona': 'ANTIOQUIA', 'ruta': 'ANTIOQUIA', 'plan_vacunal': 'PREMIUM'},
        {'codigo': 'C003', 'nombre': 'GRANJA LA ESPERANZA', 'municipio': 'GIRON', 
         'zona': 'CENTRO', 'ruta': 'GIRON', 'plan_vacunal': 'BASIC'},
    ]

if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {'codigo': 'D001', 'nombre': 'HERRERA OSORIO PEDRO ANGEL', 'placa': 'WOM366', 'ruta': 'CUCUTA'},
        {'codigo': 'D002', 'nombre': 'ALMANZA KENNYG ROLLER', 'placa': 'WFD670', 'ruta': 'ANTIOQUIA'},
        {'codigo': 'D003', 'nombre': 'SÁNCHEZ BARRERA WILMER ALEXANDER', 'placa': 'GQU440', 'ruta': 'GIRON'},
    ]

if 'planificacion' not in st.session_state:
    st.session_state.planificacion = []

if 'despachos' not in st.session_state:
    st.session_state.despachos = []

# FUNCIONES PRINCIPALES
def mostrar_dashboard():
    st.header("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clientes", len(st.session_state.clientes))
    with col2:
        st.metric("Planificación", len(st.session_state.planificacion))
    with col3:
        st.metric("Despachos Hoy", len(st.session_state.despachos))

def planificacion_semanal():
    st.header("📅 Planificación Semanal")
    
    with st.form("nueva_planificacion"):
        col1, col2 = st.columns(2)
        
        with col1:
            lote = st.text_input("Número de Lote")
            producto = st.selectbox("Producto", ["POLITO", "SASSO", "AZUR", "CHICKENMIX"])
            cliente = st.selectbox("Cliente", [c['nombre'] for c in st.session_state.clientes])
        
        with col2:
            cantidad = st.number_input("Cantidad", min_value=1, value=100)
            fecha = st.date_input("Fecha de Nacimiento")
            prioridad = st.selectbox("Prioridad", ["ALTA", "MEDIA", "BAJA"])
        
        if st.form_submit_button("💾 Guardar Planificación"):
            nueva = {
                'lote': lote,
                'producto': producto,
                'cliente': cliente,
                'cantidad': cantidad,
                'fecha': fecha.strftime("%Y-%m-%d"),
                'prioridad': prioridad,
                'estado': 'PENDIENTE'
            }
            st.session_state.planificacion.append(nueva)
            st.success("✅ Planificación guardada!")
    
    # Mostrar planificación existente
    if st.session_state.planificacion:
        st.subheader("Planificación Registrada")
        df = pd.DataFrame(st.session_state.planificacion)
        st.dataframe(df)

def generar_despacho():
    st.header("🚚 Generar Despacho Diario")
    
    fecha = st.date_input("Fecha para despacho", datetime.now())
    
    if st.button("🔄 Generar Despacho Automático"):
        # Filtrar planificaciones para esta fecha
        planificaciones_hoy = [
            p for p in st.session_state.planificacion 
            if p['fecha'] == fecha.strftime("%Y-%m-%d") and p['estado'] == 'PENDIENTE'
        ]
        
        if not planificaciones_hoy:
            st.warning("No hay planificaciones para hoy")
            return
        
        # Asignar conductor automáticamente
        despachos_generados = []
        for i, plan in enumerate(planificaciones_hoy):
            # Buscar cliente para saber la ruta
            cliente = next((c for c in st.session_state.clientes if c['nombre'] == plan['cliente']), None)
            if cliente:
                conductor = next((d for d in st.session_state.conductores if d['ruta'] == cliente['ruta']), None)
                if conductor:
                    despacho = {
                        **plan,
                        'nrovia': f"{i+1:04d}",
                        'conductor': conductor['nombre'],
                        'placa': conductor['placa'],
                        'ruta': cliente['ruta'],
                        'estado_despacho': 'ASIGNADO'
                    }
                    despachos_generados.append(despacho)
                    plan['estado'] = 'PROGRAMADO'
        
        st.session_state.despachos = despachos_generados
        st.success(f"✅ Generados {len(despachos_generados)} despachos")

def planillas_distribucion():
    st.header("📋 Planillas de Distribución")
    
    if not st.session_state.despachos:
        st.info("No hay despachos generados")
        return
    
    # Mostrar tabla de despachos
    df = pd.DataFrame(st.session_state.despachos)
    
    # Seleccionar columnas para mostrar (como tu Excel)
    columnas = ['nrovia', 'conductor', 'placa', 'ruta', 'cliente', 'producto', 'cantidad', 'prioridad']
    st.dataframe(df[columnas])
    
    # Botones de descarga
    col1, col2 = st.columns(2)
    
    with col1:
        # Descargar Excel
        excel_buffer = io.BytesIO()
        df[columnas].to_excel(excel_buffer, index=False)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_buffer.getvalue(),
            file_name=f"despacho_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col2:
        # Descargar CSV
        csv = df[columnas].to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV", 
            data=csv,
            file_name=f"despacho_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def seguimiento_despachos():
    st.header("📍 Seguimiento de Despachos")
    
    if not st.session_state.despachos:
        st.info("No hay despachos para seguir")
        return
    
    for i, despacho in enumerate(st.session_state.despachos):
        with st.expander(f"{despacho['nrovia']} - {despacho['cliente']} - {despacho['producto']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                estado = st.selectbox(
                    "Estado",
                    ["ASIGNADO", "EN RUTA", "ENTREGADO", "PROBLEMA"],
                    key=f"estado_{i}"
                )
            
            with col2:
                observaciones = st.text_input("Observaciones", key=f"obs_{i}")
            
            if st.button("Actualizar", key=f"btn_{i}"):
                st.session_state.despachos[i]['estado_despacho'] = estado
                st.session_state.despachos[i]['observaciones'] = observaciones
                st.success("✅ Actualizado!")

# MENÚ PRINCIPAL
def main():
    st.title("🐔 Sistema de Gestión - Agroavícola San Marino")
    st.markdown("---")
    
    # Menú en sidebar
    with st.sidebar:
        st.subheader("Navegación")
        opcion = st.radio(
            "Seleccione:",
            ["📊 Dashboard", "📅 Planificación", "🚚 Despacho", "📋 Planillas", "📍 Seguimiento"]
        )
    
    # Navegar entre secciones
    if opcion == "📊 Dashboard":
        mostrar_dashboard()
    elif opcion == "📅 Planificación":
        planificacion_semanal()
    elif opcion == "🚚 Despacho":
        generar_despacho()
    elif opcion == "📋 Planillas":
        planillas_distribucion()
    elif opcion == "📍 Seguimiento":
        seguimiento_despachos()

if __name__ == "__main__":
    main()
