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
        {'codigo': 'D001', 'nombre': 'HERRERA OSORIO PEDRO ANGEL', 'placa': 'WOM366', 'ruta': 'CUCUTA', 'activo': True},
        {'codigo': 'D002', 'nombre': 'ALMANZA KENNYG ROLLER', 'placa': 'WFD670', 'ruta': 'ANTIOQUIA', 'activo': True},
        {'codigo': 'D003', 'nombre': 'SÁNCHEZ BARRERA WILMER ALEXANDER', 'placa': 'GQU440', 'ruta': 'GIRON', 'activo': True},
    ]

if 'vehiculos' not in st.session_state:
    st.session_state.vehiculos = [
        {'placa': 'WOM366', 'marca': 'CHEVROLET', 'modelo': 'NKR', 'capacidad': 5000, 'activo': True},
        {'placa': 'WFD670', 'marca': 'TOYOTA', 'modelo': 'DYNA', 'capacidad': 6000, 'activo': True},
        {'placa': 'GQU440', 'marca': 'NISSAN', 'modelo': 'ATLAS', 'capacidad': 4500, 'activo': True},
    ]

if 'planificacion' not in st.session_state:
    st.session_state.planificacion = []

if 'despachos' not in st.session_state:
    st.session_state.despachos = []

# FUNCIONES DE GESTIÓN
def gestion_clientes():
    st.header("👥 Gestión de Clientes")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("➕ Agregar Nuevo Cliente")
        with st.form("nuevo_cliente"):
            codigo = st.text_input("Código", value=f"C{len(st.session_state.clientes)+1:03d}")
            nombre = st.text_input("Nombre del Cliente")
            municipio = st.text_input("Municipio")
            zona = st.selectbox("Zona", ["NORTE", "SUR", "ESTE", "OESTE", "CENTRO", "ANTIOQUIA"])
            ruta = st.text_input("Ruta")
            plan_vacunal = st.selectbox("Plan Vacunal", ["STANDARD", "PREMIUM", "BASIC"])
            
            if st.form_submit_button("💾 Guardar Cliente"):
                nuevo_cliente = {
                    'codigo': codigo,
                    'nombre': nombre,
                    'municipio': municipio,
                    'zona': zona,
                    'ruta': ruta,
                    'plan_vacunal': plan_vacunal
                }
                st.session_state.clientes.append(nuevo_cliente)
                st.success("✅ Cliente guardado exitosamente!")
                st.rerun()
    
    with col2:
        st.subheader("📋 Lista de Clientes")
        if st.session_state.clientes:
            df_clientes = pd.DataFrame(st.session_state.clientes)
            st.dataframe(df_clientes, use_container_width=True)
            
            # Opción para eliminar cliente
            if st.session_state.clientes:
                cliente_a_eliminar = st.selectbox(
                    "Seleccionar cliente a eliminar:",
                    [f"{c['codigo']} - {c['nombre']}" for c in st.session_state.clientes],
                    key="eliminar_cliente"
                )
                
                if st.button("🗑️ Eliminar Cliente Seleccionado"):
                    codigo_eliminar = cliente_a_eliminar.split(" - ")[0]
                    st.session_state.clientes = [c for c in st.session_state.clientes if c['codigo'] != codigo_eliminar]
                    st.success("✅ Cliente eliminado!")
                    st.rerun()
        else:
            st.info("No hay clientes registrados")

def gestion_conductores_vehiculos():
    st.header("🚚 Gestión de Conductores y Vehículos")
    
    tab1, tab2 = st.tabs(["👤 Conductores", "🚛 Vehículos"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ Agregar Conductor")
            with st.form("nuevo_conductor"):
                codigo = st.text_input("Código Conductor", value=f"D{len(st.session_state.conductores)+1:03d}")
                nombre = st.text_input("Nombre Completo")
                placa = st.text_input("Placa del Vehículo").upper()
                ruta = st.text_input("Ruta Asignada")
                activo = st.checkbox("Activo", value=True)
                
                if st.form_submit_button("💾 Guardar Conductor"):
                    nuevo_conductor = {
                        'codigo': codigo,
                        'nombre': nombre,
                        'placa': placa,
                        'ruta': ruta,
                        'activo': activo
                    }
                    st.session_state.conductores.append(nuevo_conductor)
                    st.success("✅ Conductor guardado exitosamente!")
                    st.rerun()
        
        with col2:
            st.subheader("📋 Lista de Conductores")
            if st.session_state.conductores:
                df_conductores = pd.DataFrame(st.session_state.conductores)
                st.dataframe(df_conductores, use_container_width=True)
                
                # Opción para eliminar conductor
                if st.session_state.conductores:
                    conductor_a_eliminar = st.selectbox(
                        "Seleccionar conductor a eliminar:",
                        [f"{c['codigo']} - {c['nombre']}" for c in st.session_state.conductores],
                        key="eliminar_conductor"
                    )
                    
                    if st.button("🗑️ Eliminar Conductor Seleccionado", key="btn_eliminar_conductor"):
                        codigo_eliminar = conductor_a_eliminar.split(" - ")[0]
                        st.session_state.conductores = [c for c in st.session_state.conductores if c['codigo'] != codigo_eliminar]
                        st.success("✅ Conductor eliminado!")
                        st.rerun()
            else:
                st.info("No hay conductores registrados")
    
    with tab2:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ Agregar Vehículo")
            with st.form("nuevo_vehiculo"):
                placa = st.text_input("Placa").upper()
                marca = st.text_input("Marca")
                modelo = st.text_input("Modelo")
                capacidad = st.number_input("Capacidad (unidades)", min_value=1, value=1000)
                activo = st.checkbox("Vehículo Activo", value=True)
                
                if st.form_submit_button("💾 Guardar Vehículo"):
                    nuevo_vehiculo = {
                        'placa': placa,
                        'marca': marca,
                        'modelo': modelo,
                        'capacidad': capacidad,
                        'activo': activo
                    }
                    st.session_state.vehiculos.append(nuevo_vehiculo)
                    st.success("✅ Vehículo guardado exitosamente!")
                    st.rerun()
        
        with col2:
            st.subheader("📋 Lista de Vehículos")
            if st.session_state.vehiculos:
                df_vehiculos = pd.DataFrame(st.session_state.vehiculos)
                st.dataframe(df_vehiculos, use_container_width=True)
                
                # Opción para eliminar vehículo - CORREGIDO CON VALORES POR DEFECTO
                if st.session_state.vehiculos:
                    # Usar get() para evitar KeyError
                    vehiculo_a_eliminar = st.selectbox(
                        "Seleccionar vehículo a eliminar:",
                        [f"{v['placa']} - {v.get('marca', 'SIN MARCA')} {v.get('modelo', 'SIN MODELO')}" for v in st.session_state.vehiculos],
                        key="eliminar_vehiculo"
                    )
                    
                    if st.button("🗑️ Eliminar Vehículo Seleccionado", key="btn_eliminar_vehiculo"):
                        placa_eliminar = vehiculo_a_eliminar.split(" - ")[0]
                        st.session_state.vehiculos = [v for v in st.session_state.vehiculos if v['placa'] != placa_eliminar]
                        st.success("✅ Vehículo eliminado!")
                        st.rerun()
            else:
                st.info("No hay vehículos registrados")

# FUNCIONES PRINCIPALES EXISTENTES
def mostrar_dashboard():
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Clientes", len(st.session_state.clientes))
    with col2:
        st.metric("Conductores", len([c for c in st.session_state.conductores if c.get('activo', True)]))
    with col3:
        st.metric("Vehículos", len([v for v in st.session_state.vehiculos if v.get('activo', True)]))
    with col4:
        pendientes = len([p for p in st.session_state.planificacion if p.get('estado') == 'PENDIENTE'])
        st.metric("Planificaciones Pendientes", pendientes)
    
    st.markdown("---")
    st.markdown("**Sistema de Gestión v2.0**")

def planificacion_semanal():
    st.header("📅 Planificación Semanal")
    
    with st.form("nueva_planificacion"):
        col1, col2 = st.columns(2)
        
        with col1:
            lote = st.text_input("Número de Lote")
            producto = st.selectbox("Producto", ["POLITA", "POLITO", "SASSO", "AZUR", "CHICKENMIX"])
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
                conductor = next((d for d in st.session_state.conductores if d['ruta'] == cliente['ruta'] and d.get('activo', True)), None)
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

def generar_planilla_detallada(despacho):
    """Genera una planilla detallada como la imagen"""
    
    # Datos de ejemplo para la planilla detallada
    planilla_data = {
        'RESUMEN DE PLANILLA': [f"Nro. {despacho['nrovia']} - Ruta {despacho['ruta']}", "", "", ""],
        'Fecha de Cargue': [datetime.now().strftime("%d/%m/%Y"), "", "", ""],
        'Conductores': [despacho['conductor'], "", "", ""],
        'Nro Despacho': [despacho['nrovia'], "", "", ""],
        'Producto': [despacho['producto'], "", "", ""],
        '': ["", "", "", ""],  # Línea en blanco
        'Productos de Planilla': ["", "POLITA", "POLITO", "SASSO"],
        'Cantidades Totales': ["Total", "1,050", "3,200", "50"],
        '': ["", "", "", ""],  # Línea en blanco
        'Planta de Origen': ["ESPERANZA 1", "", "", ""],
        'Fecha Origen': ["21/07/2025", "", "", ""],
        'Producto': [despacho['producto'], "", "", ""],
        'Descripción Plan Vacunal': ["RISMAVAC + NOFUSION ND+NDC2", "", "", ""],
        'Lote': [despacho['lote'], "", "", ""],
        'Total': [f"{despacho['cantidad']:,}", "", "", ""]
    }
    
    return pd.DataFrame(planilla_data)

def planillas_distribucion():
    st.header("📋 Planillas de Distribución")
    
    if not st.session_state.despachos:
        st.info("No hay despachos generados")
        return
    
    # Mostrar tabla de despachos
    df = pd.DataFrame(st.session_state.despachos)
    
    # Seleccionar columnas para mostrar
    columnas = ['nrovia', 'conductor', 'placa', 'ruta', 'cliente', 'producto', 'cantidad', 'prioridad']
    st.dataframe(df[columnas])
    
    # Generar planillas individuales detalladas
    st.subheader("📄 Planillas Detalladas por Despacho")
    
    for despacho in st.session_state.despachos:
        with st.expander(f"Planilla {despacho['nrovia']} - {despacho['cliente']}"):
            # Mostrar información detallada
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Nro. Planilla:** {despacho['nrovia']}")
                st.write(f"**Ruta:** {despacho['ruta']}")
                st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
                st.write(f"**Conductor:** {despacho['conductor']}")
            
            with col2:
                st.write(f"**Placa:** {despacho['placa']}")
                st.write(f"**Cliente:** {despacho['cliente']}")
                st.write(f"**Producto:** {despacho['producto']}")
                st.write(f"**Cantidad:** {despacho['cantidad']:,}")
            
            # Generar planilla detallada para descargar
            planilla_detallada = generar_planilla_detallada(despacho)
            
            # Mostrar vista previa
            st.write("**Vista Previa de Planilla:**")
            st.dataframe(planilla_detallada, hide_index=True)
            
            # Botones de descarga
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                # Descargar Excel de planilla detallada
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    planilla_detallada.to_excel(writer, sheet_name=f"Planilla_{despacho['nrovia']}", index=False)
                
                st.download_button(
                    label=f"📥 Descargar Planilla {despacho['nrovia']} (Excel)",
                    data=excel_buffer.getvalue(),
                    file_name=f"planilla_{despacho['nrovia']}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel",
                    key=f"excel_{despacho['nrovia']}"
                )
            
            with col_d2:
                # Descargar CSV de planilla detallada
                csv = planilla_detallada.to_csv(index=False)
                st.download_button(
                    label=f"📥 Descargar Planilla {despacho['nrovia']} (CSV)", 
                    data=csv,
                    file_name=f"planilla_{despacho['nrovia']}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key=f"csv_{despacho['nrovia']}"
                )
    
    # Botones de descarga general
    st.subheader("📦 Descargas Masivas")
    col1, col2 = st.columns(2)
    
    with col1:
        # Descargar Excel general
        excel_buffer = io.BytesIO()
        df[columnas].to_excel(excel_buffer, index=False)
        st.download_button(
            label="📥 Descargar Todos los Despachos (Excel)",
            data=excel_buffer.getvalue(),
            file_name=f"despachos_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col2:
        # Descargar CSV general
        csv = df[columnas].to_csv(index=False)
        st.download_button(
            label="📥 Descargar Todos los Despachos (CSV)", 
            data=csv,
            file_name=f"despachos_{datetime.now().strftime('%Y%m%d')}.csv",
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
            ["📊 Dashboard", "👥 Gestión Clientes", "🚚 Gestión Conductores", 
             "📅 Planificación", "🚚 Despacho", "📋 Planillas", "📍 Seguimiento"]
        )
    
    # Navegar entre secciones
    if opcion == "📊 Dashboard":
        mostrar_dashboard()
    elif opcion == "👥 Gestión Clientes":
        gestion_clientes()
    elif opcion == "🚚 Gestión Conductores":
        gestion_conductores_vehiculos()
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
