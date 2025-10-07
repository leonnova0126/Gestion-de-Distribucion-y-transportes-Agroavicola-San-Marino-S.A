import streamlit as st
import pandas as pd
from datetime import datetime
import io
import hashlib
import hmac
import time

# Configurar la página
st.set_page_config(
    page_title="Sistema Avícola San Marino",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
         'zona': 'NORTE', 'ruta': 'CUCUTA', 'plan_vacunal': 'STANDARD'},
        {'codigo': 'C002', 'nombre': 'AVICOLA EL PROGRESO', 'municipio': 'RIONEGRO', 
         'zona': 'ANTIOQUIA', 'ruta': 'ANTIOQUIA', 'plan_vacunal': 'PREMIUM'},
        {'codigo': 'C003', 'nombre': 'GRANJA LA ESPERANZA', 'municipio': 'GIRON', 
         'zona': 'CENTRO', 'ruta': 'GIRON', 'plan_vacunal': 'BASIC'},
    ]

# CONDUCTORES SIMPLIFICADOS - SOLO NOMBRE E IDENTIFICACIÓN
if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {'codigo': 'D001', 'nombre': 'HERRERA OSORIO PEDRO ANGEL', 'identificacion': '123456789'},
        {'codigo': 'D002', 'nombre': 'ALMANZA KENNYG ROLLER', 'identificacion': '987654321'},
        {'codigo': 'D003', 'nombre': 'SÁNCHEZ BARRERA WILMER ALEXANDER', 'identificacion': '456789123'},
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

# =============================================
# SISTEMA DE LOGIN
# =============================================

def mostrar_login():
    """Interfaz de login"""
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.title("🐔 San Marino")
        st.subheader("Sistema de Gestión Avícola")
        st.markdown("---")
        
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingrese su contraseña")
            
            if st.form_submit_button("🚀 Ingresar al Sistema"):
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
# GESTIÓN DE USUARIOS (SOLO ADMIN)
# =============================================

def gestion_usuarios():
    """Gestión de usuarios del sistema (solo admin)"""
    if not tiene_permiso(['admin']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.header("👥 Gestión de Usuarios del Sistema")
    
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
# FUNCIONES PRINCIPALES CON PERMISOS
# =============================================

def mostrar_dashboard():
    """Dashboard principal"""
    st.header("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Clientes", len(st.session_state.clientes))
    with col2:
        st.metric("Conductores", len(st.session_state.conductores))
    with col3:
        st.metric("Vehículos", len([v for v in st.session_state.vehiculos if v.get('activo', True)]))
    with col4:
        pendientes = len([p for p in st.session_state.planificacion if p.get('estado') == 'PENDIENTE'])
        st.metric("Planificaciones Pendientes", pendientes)
    
    # Información adicional solo para admin/supervisor
    if tiene_permiso(['admin', 'supervisor']):
        st.markdown("---")
        st.subheader("📈 Información Detallada")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Usuarios Conectados:**")
            st.write(f"- {st.session_state.get('nombre_usuario', 'N/A')} ({st.session_state.get('rol_actual', 'N/A')})")
        
        with col2:
            st.write("**Estadísticas del Sistema:**")
            st.write(f"- Total despachos: {len(st.session_state.despachos)}")
            st.write(f"- Planificación total: {len(st.session_state.planificacion)}")
    
    st.markdown("---")
    st.markdown("**Sistema de Gestión v3.0 - Con Seguridad**")

def gestion_clientes():
    """Gestión de clientes"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
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
            
            # Opción para eliminar cliente (solo admin)
            if st.session_state.clientes and tiene_permiso(['admin']):
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
    """Gestión de conductores SIMPLIFICADA - solo nombre e identificación"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.header("👤 Gestión de Conductores")
    
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

def planificacion_semanal():
    """Planificación semanal"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
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
    """Generar despacho diario"""
    if not tiene_permiso(['admin', 'supervisor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
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
        
        # Asignar conductor automáticamente (si hay conductores)
        despachos_generados = []
        for i, plan in enumerate(planificaciones_hoy):
            # Asignar conductor rotativamente si hay conductores disponibles
            if st.session_state.conductores:
                conductor_idx = i % len(st.session_state.conductores)
                conductor = st.session_state.conductores[conductor_idx]
                
                despacho = {
                    **plan,
                    'nrovia': f"{i+1:04d}",
                    'conductor': conductor['nombre'],
                    'identificacion_conductor': conductor['identificacion'],
                    'estado_despacho': 'ASIGNADO'
                }
                despachos_generados.append(despacho)
                plan['estado'] = 'PROGRAMADO'
        
        st.session_state.despachos = despachos_generados
        st.success(f"✅ Generados {len(despachos_generados)} despachos")

def planillas_distribucion():
    """Planillas de distribución"""
    if not tiene_permiso(['admin', 'supervisor', 'conductor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
    st.header("📋 Planillas de Distribución")
    
    if not st.session_state.despachos:
        st.info("No hay despachos generados")
        return
    
    # Mostrar tabla de despachos
    df = pd.DataFrame(st.session_state.despachos)
    
    # Seleccionar columnas para mostrar
    columnas = ['nrovia', 'conductor', 'identificacion_conductor', 'cliente', 'producto', 'cantidad', 'prioridad']
    columnas_disponibles = [col for col in columnas if col in df.columns]
    
    if columnas_disponibles:
        st.dataframe(df[columnas_disponibles])
    else:
        st.dataframe(df)
    
    # Generar planillas individuales detalladas
    st.subheader("📄 Planillas Detalladas por Despacho")
    
    for despacho in st.session_state.despachos:
        with st.expander(f"Planilla {despacho['nrovia']} - {despacho['cliente']}"):
            # Mostrar información detallada
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Nro. Planilla:** {despacho['nrovia']}")
                st.write(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
                st.write(f"**Conductor:** {despacho.get('conductor', 'N/A')}")
                st.write(f"**Identificación:** {despacho.get('identificacion_conductor', 'N/A')}")
            
            with col2:
                st.write(f"**Cliente:** {despacho['cliente']}")
                st.write(f"**Producto:** {despacho['producto']}")
                st.write(f"**Cantidad:** {despacho['cantidad']:,}")
                st.write(f"**Prioridad:** {despacho['prioridad']}")

def seguimiento_despachos():
    """Seguimiento de despachos"""
    if not tiene_permiso(['admin', 'supervisor', 'conductor']):
        st.error("⛔ No tienes permisos para acceder a esta sección")
        return
    
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

# =============================================
# MENÚ PRINCIPAL
# =============================================

def main():
    # Verificar autenticación
    if not st.session_state.get('autenticado'):
        mostrar_login()
        return
    
    # Mostrar barra de usuario
    mostrar_logout()
    
    st.title("🐔 Sistema de Gestión - Agroavícola San Marino")
    st.markdown("---")
    
    # Menú en sidebar según permisos
    with st.sidebar:
        st.subheader("🧭 Navegación")
        
        opciones_menu = ["📊 Dashboard"]
        
        # Opciones para admin y supervisor
        if tiene_permiso(['admin', 'supervisor']):
            opciones_menu.extend([
                "👥 Gestión Clientes", 
                "👤 Gestión Conductores", 
                "📅 Planificación", 
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
    elif opcion == "🔐 Gestión Usuarios":
        gestion_usuarios()
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
