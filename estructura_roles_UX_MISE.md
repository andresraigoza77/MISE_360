# ESTRUCTURA DE ROLES Y DISEÑO DE EXPERIENCIA DE USUARIO
## Sistema MISE - Política Pública de Participación Ciudadana

**Distrito de Medellín**  
**Versión:** 1.0  
**Fecha:** 15 de febrero de 2026

---

## TABLA DE CONTENIDOS

1. [Matriz de Roles y Responsabilidades](#1-matriz-de-roles-y-responsabilidades)
2. [Perfiles de Usuario Detallados](#2-perfiles-de-usuario-detallados)
3. [User Journey Maps por Rol](#3-user-journey-maps-por-rol)
4. [Requisitos Funcionales por Rol](#4-requisitos-funcionales-por-rol)
5. [Arquitectura de Información y Navegación](#5-arquitectura-de-información-y-navegación)
6. [Diseño de Interfaces por Rol](#6-diseño-de-interfaces-por-rol)
7. [Dashboards Diferenciados](#7-dashboards-diferenciados)
8. [Ruta Metodológica para Diseño UX](#8-ruta-metodológica-para-diseño-ux)
9. [Matriz de Accesos y Permisos](#9-matriz-de-accesos-y-permisos)
10. [Plan de Implementación UX](#10-plan-de-implementación-ux)

---

## 1. MATRIZ DE ROLES Y RESPONSABILIDADES

### 1.1 Taxonomía de Roles

```
MISE - Sistema de Seguimiento
│
├── ROL 1: CAPTURISTA
│   └── Responsable de diligenciar indicadores en su dependencia
│
├── ROL 2: VALIDADOR DEPENDENCIA
│   └── Revisa y aprueba datos de su dependencia antes de enviar
│
├── ROL 3: CONSOLIDADOR
│   └── Recibe, valida y consolida información de todas las dependencias
│
├── ROL 4: ANALISTA
│   └── Genera reportes, dashboards y productos analíticos
│
├── ROL 5: DECISOR SECTORIAL
│   └── Secretarios/Directores que consultan información de su sector
│
├── ROL 6: DECISOR ESTRATÉGICO
│   └── Alcalde, Secretario General, DAP - Visión consolidada ciudad
│
├── ROL 7: AUDITOR/CONTROL
│   └── Contraloría, auditoría interna, control político
│
└── ROL 8: CIUDADANO/PÚBLICO
    └── Acceso público a información de rendición de cuentas
```

### 1.2 Matriz Detallada de Roles

| Rol | Acciones Principales | Permisos | Frecuencia de Uso | N° Usuarios Estimado |
|-----|---------------------|----------|-------------------|---------------------|
| **CAPTURISTA** | • Diligenciar indicadores<br>• Adjuntar evidencias<br>• Actualizar resultados trimestrales<br>• Ver histórico de su dependencia | CREAR, EDITAR (solo sus indicadores) | Mensual/Trimestral | 15-20 personas |
| **VALIDADOR DEPENDENCIA** | • Revisar datos capturados<br>• Solicitar correcciones<br>• Aprobar envío<br>• Ver reportes de su dependencia | LEER, COMENTAR, APROBAR (solo su dependencia) | Trimestral | 10-12 personas |
| **CONSOLIDADOR** | • Recibir reportes<br>• Validar calidad de datos<br>• Aprobar consolidado<br>• Gestionar plazos<br>• Solicitar aclaraciones | LEER (todo), VALIDAR, APROBAR, RECHAZAR | Semanal/Quincenal | 2-3 personas |
| **ANALISTA** | • Crear dashboards<br>• Generar reportes<br>• Analizar tendencias<br>• Detectar alertas<br>• Preparar informes ejecutivos | LEER (todo), EXPORTAR, ANALIZAR | Diario/Semanal | 3-5 personas |
| **DECISOR SECTORIAL** | • Consultar avance de su sector<br>• Ver comparativos<br>• Identificar riesgos<br>• Exportar reportes | LEER (su sector), EXPORTAR | Mensual | 10-15 personas |
| **DECISOR ESTRATÉGICO** | • Visión consolidada ciudad<br>• Comparativos intersectoriales<br>• Alertas estratégicas<br>• Informes ejecutivos | LEER (todo), EXPORTAR, CONFIGURAR ALERTAS | Mensual/Ad-hoc | 5-8 personas |
| **AUDITOR/CONTROL** | • Consultar trazabilidad<br>• Verificar evidencias<br>• Auditar cambios<br>• Exportar datos | LEER (todo), AUDITAR, EXPORTAR | Según ciclo de auditoría | 3-5 personas |
| **CIUDADANO/PÚBLICO** | • Consultar avances públicos<br>• Descargar datos abiertos<br>• Ver comparativos territoriales | LEER (dashboard público) | Ad-hoc | Abierto |

### 1.3 Flujo de Responsabilidades por Trimestre

```mermaid
TRIMESTRE EN CURSO
│
├── SEMANA 1-10: EJECUCIÓN DE ACCIONES
│   └── (Dependencias ejecutan actividades de la PPPC)
│
├── SEMANA 11: CAPTURA DE DATOS
│   ├── CAPTURISTA: Diligencia resultados del trimestre
│   │   └── Sistema envía recordatorio automático
│   └── Plazo: 5 días hábiles
│
├── SEMANA 12: VALIDACIÓN INTERNA
│   ├── VALIDADOR DEPENDENCIA: Revisa datos
│   │   ├── Si OK → Aprueba
│   │   └── Si NO → Devuelve a Capturista con comentarios
│   └── Plazo: 3 días hábiles
│
├── SEMANA 12-13: CONSOLIDACIÓN
│   ├── CONSOLIDADOR: Recibe todos los reportes
│   │   ├── Valida consistencia
│   │   ├── Ejecuta reglas de calidad automáticas
│   │   └── Solicita aclaraciones si es necesario
│   └── Plazo: 5 días hábiles
│
├── SEMANA 13: APROBACIÓN FINAL
│   └── CONSOLIDADOR: Publica consolidado oficial
│
└── SEMANA 13 EN ADELANTE: USO DE INFORMACIÓN
    ├── ANALISTA: Genera productos analíticos
    ├── DECISORES: Consultan dashboards
    ├── AUDITOR: Verifica según cronograma
    └── CIUDADANO: Accede a portal público
```

---

## 2. PERFILES DE USUARIO DETALLADOS

### PERFIL 1: CAPTURISTA

**Persona Representativa:**  
📋 **María González** - Profesional Universitaria en Secretaría de las Mujeres

**Características:**
- Edad: 28-45 años
- Formación: Profesional (licenciatura/especialización)
- Experiencia en el cargo: 1-5 años
- Competencia digital: Media-Alta
- Frecuencia de uso del sistema: Mensual (picos trimestrales)

**Contexto de uso:**
- Trabaja en oficina con computador de escritorio
- Conexión a internet estable
- Usa Chrome/Edge
- Tiene múltiples responsabilidades (MISE es una de ellas)
- Presión por cumplir plazos trimestrales

**Motivaciones:**
- ✅ Cumplir requisito institucional
- ✅ Facilitar su trabajo (menos tiempo en captura)
- ✅ Evitar errores y devoluciones
- ✅ Que su trabajo aporte valor

**Frustraciones actuales:**
- ❌ Interfaz Excel confusa (56 columnas)
- ❌ No sabe si está diligenciando bien hasta que se lo devuelven
- ❌ Tiene que buscar información en múltiples sistemas
- ❌ No ve para qué sirve lo que captura
- ❌ Plazos ajustados con otras responsabilidades

**Objetivos en el sistema:**
1. Diligenciar indicadores de manera rápida y sin errores
2. Saber en tiempo real si hay errores
3. Tener ayudas contextuales sobre qué reportar
4. Adjuntar evidencias fácilmente
5. Saber el estado de su reporte

**Frase que resume su experiencia deseada:**
> *"Quiero un sistema que me guíe paso a paso, valide en tiempo real y me ahorre tiempo para dedicarlo a mi trabajo sustantivo"*

---

### PERFIL 2: VALIDADOR DEPENDENCIA

**Persona Representativa:**  
👔 **Carlos Ramírez** - Coordinador de Planeación en Secretaría de Cultura

**Características:**
- Edad: 35-55 años
- Formación: Especialización/Maestría
- Experiencia en el cargo: 3-10 años
- Competencia digital: Media-Alta
- Frecuencia de uso: Trimestral intenso (1 semana)

**Contexto de uso:**
- Revisa reportes de 2-3 capturistas
- Tiempo limitado para validación (máximo 1 día por indicador)
- Necesita ver rápidamente qué está mal
- Debe dar retroalimentación clara

**Motivaciones:**
- ✅ Garantizar calidad de información de su dependencia
- ✅ Evitar devoluciones del consolidador
- ✅ Proceso de validación ágil
- ✅ Trazabilidad de correcciones

**Frustraciones actuales:**
- ❌ Revisar celda por celda en Excel
- ❌ No hay checklist automático de validación
- ❌ Comunicación de correcciones vía email (se pierde trazabilidad)
- ❌ No sabe si el capturista corrigió lo solicitado

**Objetivos en el sistema:**
1. Ver resumen de completitud de datos
2. Alertas automáticas de inconsistencias
3. Aprobar/rechazar con comentarios inline
4. Ver histórico de correcciones
5. Dashboard de estado de validación

**Frase que resume su experiencia deseada:**
> *"Necesito ver rápidamente qué está mal y comunicar correcciones de forma que queden registradas"*

---

### PERFIL 3: CONSOLIDADOR

**Persona Representativa:**  
🎯 **Ana Martínez** - Profesional DAP responsable de MISE

**Características:**
- Edad: 30-45 años
- Formación: Especialización en Planeación/Administración Pública
- Experiencia: Alta en seguimiento de políticas públicas
- Competencia digital: Alta
- Frecuencia de uso: Semanal/Diario en picos

**Contexto de uso:**
- Punto de control de calidad del sistema
- Gestiona plazos de 10 dependencias
- Resuelve inconsistencias entre dependencias
- Presión por entregar consolidado a tiempo

**Motivaciones:**
- ✅ Consolidado de calidad
- ✅ Cumplir plazos
- ✅ Automatizar tareas repetitivas
- ✅ Trazabilidad total

**Frustraciones actuales:**
- ❌ Copy-paste manual de 5,727 celdas
- ❌ Gestión de correos electrónicos
- ❌ No saber quién está atrasado hasta que vence plazo
- ❌ Errores de consolidación no detectados

**Objetivos en el sistema:**
1. Dashboard de estado de reportes (quién envió, quién falta)
2. Consolidación automática
3. Reglas de validación configurables
4. Comunicación dentro del sistema
5. Alertas de plazos próximos

**Frase que resume su experiencia deseada:**
> *"Necesito saber en tiempo real quién ha reportado, qué está pendiente y poder consolidar con un clic"*

---

### PERFIL 4: ANALISTA

**Persona Representativa:**  
📊 **Luis Fernández** - Analista de Datos en Secretaría de Participación Ciudadana

**Características:**
- Edad: 25-40 años
- Formación: Profesional en Estadística/Economía/Ingeniería + especialización en Analytics
- Competencia digital: Muy Alta
- Domina: Excel avanzado, Power BI, Python/R
- Frecuencia de uso: Diario

**Contexto de uso:**
- Genera productos analíticos para decisores
- Prepara informes trimestrales
- Identifica tendencias y alertas
- Responde consultas ad-hoc

**Motivaciones:**
- ✅ Datos limpios y estructurados
- ✅ Acceso a serie histórica completa
- ✅ Posibilidad de análisis multidimensional
- ✅ Automatización de reportes recurrentes

**Frustraciones actuales:**
- ❌ Datos en Excel sin estructura normalizada
- ❌ Encabezados multi-fila que bloquean análisis
- ❌ Imposibilidad de conectar a herramientas de BI
- ❌ Cada trimestre debe "limpiar" datos manualmente

**Objetivos en el sistema:**
1. API o conector directo a Power BI/Tableau
2. Exportación a formatos analíticos (CSV, JSON, Parquet)
3. Diccionario de datos actualizado
4. Segmentación por múltiples dimensiones
5. Acceso a datos en tiempo real

**Frase que resume su experiencia deseada:**
> *"Dame datos limpios en una base de datos relacional y déjame hacer el análisis sin tener que pelear con el formato"*

---

### PERFIL 5: DECISOR SECTORIAL

**Persona Representativa:**  
🏛️ **Patricia Gómez** - Secretaria de las Mujeres

**Características:**
- Edad: 40-60 años
- Formación: Posgrado (Maestría/Doctorado)
- Experiencia en gestión pública: Alta
- Competencia digital: Media
- Frecuencia de uso: Mensual + cuando se requiere rendir cuentas

**Contexto de uso:**
- Necesita información para:
  - Reuniones de gabinete
  - Rendición de cuentas al Concejo
  - Toma de decisiones estratégicas de su sector
- Tiempo limitado (máximo 15 min para consultar)
- Prefiere visualizaciones a tablas

**Motivaciones:**
- ✅ Conocer avance de su sector vs meta
- ✅ Identificar alertas tempranas
- ✅ Tener argumentos basados en evidencia
- ✅ Compararse con otros sectores (benchmarking)

**Frustraciones actuales:**
- ❌ Información llega tarde (rezago de meses)
- ❌ Formato Excel técnico y poco digerible
- ❌ No hay síntesis ejecutiva
- ❌ No puede acceder fácilmente desde cualquier lugar

**Objetivos en el sistema:**
1. Dashboard ejecutivo con semáforo de cumplimiento
2. Acceso desde móvil/tablet
3. Posibilidad de drill-down (de resumen a detalle)
4. Exportar gráficas para presentaciones
5. Suscripción a alertas personalizadas

**Frase que resume su experiencia deseada:**
> *"Necesito ver en 5 minutos cómo va mi sector, qué está en riesgo y tener datos para sustentar decisiones"*

---

### PERFIL 6: DECISOR ESTRATÉGICO

**Persona Representativa:**  
⭐ **Federico Gutiérrez** - Alcalde de Medellín

**Características:**
- Nivel: Máxima autoridad distrital
- Tiempo disponible: Extremadamente limitado
- Competencia digital: Variable
- Requiere: Información ultra-sintética

**Contexto de uso:**
- Consultas ocasionales pero críticas
- Necesita visión de ciudad completa
- Compara sectores, pilares, territorios
- Usa información para comunicación pública

**Motivaciones:**
- ✅ Cumplimiento del Plan de Desarrollo
- ✅ Identificar sectores/territorios rezagados
- ✅ Tener evidencia para defensa política
- ✅ Información para comunicación ciudadana

**Objetivos en el sistema:**
1. Dashboard de máximo nivel (KPIs ciudad)
2. Visualización geográfica (mapa de calor)
3. Ranking de sectores por cumplimiento
4. Alertas críticas (solo lo que necesita atención inmediata)
5. Acceso 24/7 desde cualquier dispositivo

**Frase que resume su experiencia deseada:**
> *"Quiero ver en 2 minutos cómo va Medellín en participación ciudadana y qué requiere mi atención"*

---

### PERFIL 7: AUDITOR/CONTROL

**Persona Representativa:**  
🔍 **Jorge Mendoza** - Auditor Contraloría de Medellín

**Características:**
- Formación: Contador/Abogado + especialización en Control Fiscal
- Enfoque: Legalidad, trazabilidad, evidencia
- Competencia digital: Media-Alta
- Frecuencia: Según plan de auditoría (trimestral/anual)

**Contexto de uso:**
- Necesita verificar cumplimiento normativo
- Requiere trazabilidad de cambios
- Valida coherencia con otros sistemas (SIRPRE)
- Genera observaciones y hallazgos

**Motivaciones:**
- ✅ Trazabilidad completa de datos
- ✅ Acceso a evidencias originales
- ✅ Coherencia entre sistemas
- ✅ Cumplimiento de plazos

**Frustraciones actuales:**
- ❌ Sin registro de quién modificó qué
- ❌ Evidencias sin enlace directo
- ❌ Imposibilidad de auditar proceso de consolidación
- ❌ Inconsistencias sin explicación

**Objetivos en el sistema:**
1. Log de auditoría completo (quién, qué, cuándo)
2. Exportación de trazabilidad
3. Enlace directo a evidencias documentales
4. Comparativo automático con SIRPRE
5. Reporte de inconsistencias

**Frase que resume su experiencia deseada:**
> *"Necesito poder reconstruir todo el proceso de un dato desde su captura hasta el consolidado"*

---

### PERFIL 8: CIUDADANO/PÚBLICO

**Persona Representativa:**  
👥 **Comunidad de Medellín** - Ciudadanos, veedores, organizaciones sociales

**Características:**
- Diversidad demográfica total
- Competencia digital: Variable (baja a alta)
- Acceso: Principalmente móvil
- Motivación: Control social y participación informada

**Contexto de uso:**
- Consultas esporádicas
- Interés en su comuna/corregimiento
- Puede no tener conocimiento técnico
- Usa desde celular/tablet

**Motivaciones:**
- ✅ Saber qué se está haciendo en participación ciudadana
- ✅ Ver cumplimiento de compromisos
- ✅ Datos de su territorio
- ✅ Transparencia

**Frustraciones actuales:**
- ❌ Información no disponible públicamente
- ❌ Si está, es en formato técnico incomprensible
- ❌ No saben dónde buscar
- ❌ Sin desagregación territorial visible

**Objetivos en el sistema:**
1. Portal público amigable
2. Visualizaciones simples (sin jerga técnica)
3. Filtro por territorio (mi comuna)
4. Datos abiertos descargables
5. Acceso sin necesidad de registro

**Frase que resume su experiencia deseada:**
> *"Quiero saber qué se está haciendo en participación ciudadana en mi comuna, sin tener que ser experto"*

---

## 3. USER JOURNEY MAPS POR ROL

### 3.1 JOURNEY MAP - CAPTURISTA

**Escenario:** Diligenciamiento de indicadores del Trimestre II - 2025

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 1: PREPARACIÓN (ANTES DE CAPTURA)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Recibe notificación que se abrió ventana de captura                      │
│ • Revisa instructivo/ayudas                                                │
│ • Recopila evidencias físicas/digitales                                    │
│ • Consulta con ejecutores de actividades                                   │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ No sabe cuándo debe reportar    │ ✅ Notificación automática 5 días antes│
│ ❌ No encuentra instructivo        │ ✅ Ayuda contextual en cada campo      │
│ ❌ Evidencias dispersas            │ ✅ Checklist de evidencias necesarias  │
│                                                                             │
│ EMOCIONES: 😰 Estrés, 😕 Confusión                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 2: INGRESO AL SISTEMA                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Abre link del sistema                                                    │
│ • Inicia sesión (SSO con credenciales institucionales)                     │
│ • Llega a dashboard personalizado                                          │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ Abrir Excel pesado              │ ✅ Aplicación web ligera               │
│ ❌ Buscar su archivo en carpetas   │ ✅ Login directo, ve sus indicadores   │
│                                                                             │
│ EXPECTATIVA: Ver claramente qué debe reportar                              │
│ EMOCIONES: 😊 Alivio si es intuitivo                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 3: NAVEGACIÓN Y EXPLORACIÓN                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Revisa lista de indicadores asignados                                    │
│ • Ve estado: 0/8 diligenciados                                             │
│ • Identifica cuáles son urgentes (próximos a vencer)                       │
│ • Selecciona primer indicador                                              │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ No sabe por dónde empezar       │ ✅ Orden sugerido con priorización     │
│ ❌ No ve cuánto ha avanzado        │ ✅ Barra de progreso 0/8 (0%)          │
│ ❌ Todo parece urgente             │ ✅ Semáforo: 🔴 vence en 2 días        │
│                                                                             │
│ EMOCIONES: 😓 Agobio si son muchos, 😌 Tranquilidad si hay guía             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 4: DILIGENCIAMIENTO DE INDICADOR                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Ve formulario del indicador                                              │
│ • Secciones colapsables: Metadatos (pre-llenos) | Resultado Trimestre II   │
│ • Diligencia resultado numérico                                            │
│ • Escribe observación cualitativa                                          │
│ • Sube archivo de evidencia                                                │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ 56 columnas, no sabe cuáles     │ ✅ Solo campos editables visibles      │
│    llenar                          │    Metadatos colapsados                │
│ ❌ No sabe si formato es correcto  │ ✅ Validación en tiempo real:          │
│                                    │    "✓ Dato válido" / "❌ Debe ser 0-100│
│ ❌ Evidencia por email aparte      │ ✅ Upload directo en el formulario     │
│ ❌ Se pierde el trabajo si cierra  │ ✅ Auto-guardado cada 30 seg           │
│                                                                             │
│ EXPECTATIVA: Formulario claro, validaciones en tiempo real                 │
│ EMOCIONES: 😅 Alivio con validaciones, 😡 Frustración si hay errores tarde  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 5: GUARDAR Y CONTINUAR                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Botón "Guardar borrador" (sin enviar aún)                                │
│ • Vuelve a lista de indicadores                                            │
│ • Ve progreso actualizado: 1/8 diligenciados (12%)                         │
│ • Continúa con siguiente                                                   │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ Perder datos si no guarda       │ ✅ Notificación: "✓ Guardado a 14:32"  │
│ ❌ No sabe cuánto le falta         │ ✅ Progreso visible 1/8 (12%)          │
│                                                                             │
│ EMOCIONES: 😊 Satisfacción por avance visible                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 6: REVISIÓN PROPIA                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Termina de diligenciar los 8 indicadores (8/8)                           │
│ • Sistema muestra: "✅ Todos los indicadores diligenciados"                 │
│ • Opción: "Revisar antes de enviar"                                        │
│ • Ve resumen de completitud                                                │
│ • Identifica: Indicador #3 sin evidencia adjunta                           │
│ • Regresa, adjunta evidencia faltante                                      │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ No sabe si olvidó algo          │ ✅ Checklist automático de completitud │
│ ❌ Descubre errores tarde          │ ✅ Pre-validación antes de enviar      │
│                                                                             │
│ EMOCIONES: 😌 Alivio al ver checklist completo                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 7: ENVÍO A VALIDACIÓN                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Botón "Enviar a validación"                                              │
│ • Confirmación: "¿Seguro? No podrás editar después"                        │
│ • Confirma                                                                 │
│ • Sistema notifica a Validador de dependencia                              │
│ • Capturista recibe confirmación con # de radicado                         │
│                                                                             │
│ EXPECTATIVA: Claridad de que se envió exitosamente                         │
│ EMOCIONES: 😌 Alivio, 😰 Ansiedad por esperar aprobación                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 8: ESPERA Y CORRECCIONES (SI APLICA)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ ESCENARIO A: APROBADO                                                      │
│ • Recibe notificación: "✅ Tu reporte fue aprobado por Carlos Ramírez"     │
│ • Puede ver versión final enviada al consolidador                          │
│ EMOCIONES: 😊 Satisfacción                                                  │
│                                                                             │
│ ESCENARIO B: DEVUELTO CON CORRECCIONES                                     │
│ • Recibe notificación: "🔴 Requiere correcciones"                          │
│ • Ve comentarios inline en cada campo problemático:                        │
│   "Indicador #3: El resultado no coincide con evidencia adjunta"          │
│ • Corrige                                                                  │
│ • Re-envía                                                                 │
│ EMOCIONES: 😓 Frustración (menor si comentarios son claros)                 │
│                                                                             │
│ PUNTOS DE DOLOR ACTUALES          │ SOLUCIÓN PROPUESTA                     │
│ ❌ Corrección llega por email      │ ✅ Comentarios dentro del sistema      │
│    genérico                        │    con referencia exacta al campo     │
│ ❌ No sabe si ya corrigió todo     │ ✅ Checklist de correcciones           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 9: POST-ENVÍO                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES (DESEABLES)                                                        │
│ • Ve dashboard con su histórico de reportes                                │
│ • Compara sus resultados vs trimestre anterior                             │
│ • Descarga certificado de cumplimiento                                     │
│                                                                             │
│ EXPECTATIVA: Reconocimiento de su trabajo + Retroalimentación útil         │
│ EMOCIONES: 😊 Orgullo si ve que su trabajo se usa                           │
└─────────────────────────────────────────────────────────────────────────────┘

INDICADORES DE ÉXITO DE LA EXPERIENCIA:
✅ Tiempo de diligenciamiento: < 30 min por indicador
✅ Tasa de errores: < 5% de indicadores devueltos
✅ Satisfacción: > 80% considera el proceso "fácil" o "muy fácil"
✅ Adopción: 100% de capturistas usan el sistema (vs Excel paralelo)
```

---

### 3.2 JOURNEY MAP - CONSOLIDADOR

**Escenario:** Consolidación del reporte Trimestre II - 2025

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 1: APERTURA DE VENTANA DE REPORTE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Configura fechas del período de reporte en el sistema                    │
│ • Define plazos por fase: Captura (5 días) | Validación dep (3 días)      │
│ • Sistema envía notificaciones automáticas a todas las dependencias        │
│ • Activa dashboard de monitoreo de plazos                                  │
│                                                                             │
│ PUNTO DE DOLOR ACTUAL             │ SOLUCIÓN PROPUESTA                     │
│ ❌ Enviar emails manualmente       │ ✅ Notificaciones automáticas del      │
│    a cada dependencia              │    sistema al abrir ventana            │
│                                                                             │
│ EMOCIONES: 😊 Tranquilidad por automatización                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 2: MONITOREO DE AVANCE                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Consulta dashboard de estado diariamente:                                │
│   ┌───────────────────────────────────────────────────────────┐            │
│   │ DEPENDENCIA    │ ESTADO        │ AVANCE │ DÍAS RESTANTES │            │
│   ├───────────────────────────────────────────────────────────┤            │
│   │ SPC            │ ✅ Aprobado   │ 53/53  │ -              │            │
│   │ Mujeres        │ 🟡 Validación │  8/8   │ 2 días         │            │
│   │ Cultura        │ 🟢 Capturando │  4/6   │ 3 días         │            │
│   │ Étnica         │ 🔴 Sin iniciar│  0/8   │ 3 días ⚠️      │            │
│   └───────────────────────────────────────────────────────────┘            │
│                                                                             │
│ • Envía recordatorio manual a Étnica (opción "Enviar recordatorio")        │
│                                                                             │
│ PUNTO DE DOLOR ACTUAL             │ SOLUCIÓN PROPUESTA                     │
│ ❌ No sabe quién va atrasado       │ ✅ Dashboard en tiempo real            │
│    hasta que vence plazo           │    Alertas automáticas 2 días antes   │
│ ❌ Revisar 10 emails para saber    │ ✅ Todo en un solo dashboard           │
│                                                                             │
│ EMOCIONES: 😌 Control vs 😰 Ansiedad actual                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 3: RECEPCIÓN Y VALIDACIÓN TÉCNICA                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Recibe notificación: "Nueva validación de Secretaría de Mujeres (8 ind)"│
│ • Accede a módulo de validación                                            │
│ • Sistema ejecuta validaciones automáticas:                                │
│   ✅ Campos obligatorios completos                                          │
│   ✅ Rangos numéricos correctos                                             │
│   ✅ Evidencias adjuntas                                                    │
│   ⚠️  Alerta: Indicador #3 - resultado muy diferente vs trim anterior      │
│   ⚠️  Alerta: Indicador #5 - presupuesto ejecutado > programado            │
│                                                                             │
│ • Revisa alertas manualmente                                               │
│ • Solicita aclaración a Mujeres sobre Indicador #5                         │
│   (comentario inline: "Por favor explicar sobreejecución")                 │
│ • Mujeres responde en el sistema                                           │
│ • Aprueba el reporte completo de Mujeres                                   │
│                                                                             │
│ PUNTO DE DOLOR ACTUAL             │ SOLUCIÓN PROPUESTA                     │
│ ❌ Validar manualmente 5,727 datos │ ✅ Validaciones automáticas + alertas  │
│ ❌ No detecta inconsistencias      │    de valores atípicos                 │
│ ❌ Comunicación por email          │ ✅ Chat contextual dentro del sistema  │
│                                                                             │
│ TIEMPO AHORRADO: De 6 horas a 1 hora por dependencia                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 4: CONSOLIDACIÓN AUTOMÁTICA                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Todas las dependencias aprobadas (10/10)                                 │
│ • Botón: "Generar Consolidado Oficial"                                     │
│ • Sistema ejecuta proceso automático:                                      │
│   1. Compila todos los datos en tabla consolidada                         │
│   2. Valida coherencia global                                             │
│   3. Genera reporte de calidad de datos                                   │
│   4. Crea snapshot versionado (fecha + hora)                              │
│   5. Publica en módulo de consulta                                        │
│   6. Notifica a Analistas y Decisores                                     │
│                                                                             │
│ • Tiempo de proceso: 30 segundos                                          │
│                                                                             │
│ PUNTO DE DOLOR ACTUAL             │ SOLUCIÓN PROPUESTA                     │
│ ❌ Copy-paste manual (48 horas)    │ ✅ Consolidación automática (30 seg)   │
│ ❌ Errores de transcripción        │ ✅ Sin intervención manual = 0 errores │
│ ❌ Sin versionamiento              │ ✅ Snapshot automático con timestamp   │
│                                                                             │
│ EMOCIONES: 😊😊😊 Alivio extremo                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 5: PUBLICACIÓN Y COMUNICACIÓN                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACCIONES                                                                     │
│ • Descarga reporte de consolidación (PDF automático)                       │
│ • Envía email a Secretarios: "Consolidado Trim II disponible en sistema"  │
│ • Actualiza portal público ciudadano                                       │
│                                                                             │
│ EMOCIONES: 😊 Satisfacción por cumplir plazo sin estrés                     │
└─────────────────────────────────────────────────────────────────────────────┘

IMPACTO EN TIEMPO:
ANTES: 4-7 semanas | DESPUÉS: 2 semanas
REDUCCIÓN: 60-70% del tiempo total
```

---

### 3.3 JOURNEY MAP RESUMIDO - OTROS ROLES

#### DECISOR SECTORIAL

**Escenario:** Preparación de reunión de gabinete

```
1. NECESIDAD
   ↓ Debo presentar avance de mi sector en gabinete mañana
   
2. ACCESO
   ↓ Abro app desde mi tablet (estoy en movimiento)
   ↓ Login con mis credenciales distritales
   
3. VISUALIZACIÓN
   ↓ Dashboard ejecutivo con KPIs:
     • 📊 Cumplimiento global: 78% ⚠️
     • 🎯 Indicadores en meta: 6/8
     • 🔴 Indicadores en riesgo: 2/8
     • 💰 Ejecución presupuestal: 62%
   
4. DRILL-DOWN
   ↓ Click en indicadores en riesgo
   ↓ Veo detalle + Observaciones del equipo
   
5. EXPORTACIÓN
   ↓ Botón "Exportar para presentación"
   ↓ Descargo PowerPoint con gráficas
   
6. PREPARACIÓN
   ↓ Tengo argumentos basados en evidencia
   
TIEMPO TOTAL: 10 minutos
EMOCIÓN: 😊 Confianza para rendir cuentas
```

#### ANALISTA

**Escenario:** Generar informe trimestral para Alcaldía

```
1. EXTRACCIÓN
   ↓ Conecto Power BI al sistema vía API
   ↓ O descargo dataset en CSV
   
2. ANÁLISIS
   ↓ Cruzo con datos de SIRPRE (presupuesto)
   ↓ Genero visualizaciones personalizadas
   ↓ Identifico correlaciones
   
3. INSIGHTS
   ↓ Descubro: Dependencias con > ejecución tienen < cumplimiento
   ↓ Hipótesis: Problema no es presupuesto, es diseño de acciones
   
4. COMUNICACIÓN
   ↓ Genero informe ejecutivo 5 páginas
   ↓ Incluyo recomendaciones basadas en datos
   
TIEMPO: 1 día (vs 3 días limpiando datos antes)
EMOCIÓN: 😊 Satisfacción por enfocarse en análisis, no en limpieza
```

#### CIUDADANO

**Escenario:** Verificar qué se hace en mi comuna

```
1. BÚSQUEDA
   ↓ Google: "participación ciudadana Medellín comuna 10"
   ↓ Llego a portal público MISE
   
2. NAVEGACIÓN
   ↓ Filtro por "Comuna 10 - La Candelaria"
   ↓ Veo mapa de calor con actividades
   
3. VISUALIZACIÓN
   ↓ 12 actividades en mi comuna este trimestre
   ↓ Gráfica de participantes: 340 personas
   ↓ Tipo: 8 talleres, 3 asambleas, 1 feria
   
4. DATOS ABIERTOS
   ↓ Descargo dataset en Excel
   ↓ Lo comparto con mi JAC
   
TIEMPO: 5 minutos
EMOCIÓN: 😊 Empoderamiento por acceso a información
```

---

## 4. REQUISITOS FUNCIONALES POR ROL

### 4.1 CAPTURISTA

#### Funcionalidades Esenciales (Must Have)

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| CAP-01 | Inicio de sesión único (SSO) | Autenticación con credenciales institucionales | P0 |
| CAP-02 | Dashboard personalizado | Ver solo indicadores asignados a su dependencia | P0 |
| CAP-03 | Formulario de captura intuitivo | Campos claros, ayudas contextuales, secciones colapsables | P0 |
| CAP-04 | Validación en tiempo real | Alertas inmediatas de errores de formato o rango | P0 |
| CAP-05 | Auto-guardado | Guardar automáticamente cada 30 seg | P0 |
| CAP-06 | Adjuntar evidencias | Upload de archivos (PDF, Word, Excel, imágenes) | P0 |
| CAP-07 | Indicador de progreso | Barra visual: "3/8 indicadores (37%)" | P1 |
| CAP-08 | Guardar borrador | Poder cerrar y continuar después | P1 |
| CAP-09 | Pre-validación antes de enviar | Checklist de completitud | P1 |
| CAP-10 | Notificaciones de estado | Alertas de aprobación/rechazo | P1 |

#### Funcionalidades Deseables (Nice to Have)

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| CAP-11 | Histórico de reportes | Ver trim anteriores para referencia | P2 |
| CAP-12 | Sugerencias inteligentes | Auto-completar campos con base en histórico | P3 |
| CAP-13 | Modo offline | Capturar sin internet, sincronizar después | P3 |
| CAP-14 | Plantillas de observaciones | Textos predefinidos para agilizar | P3 |

---

### 4.2 VALIDADOR DEPENDENCIA

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| VAL-01 | Vista de reportes pendientes | Lista de indicadores enviados por capturistas | P0 |
| VAL-02 | Detalle de indicador | Ver toda la información capturada | P0 |
| VAL-03 | Aprobar/Rechazar | Botones claros de decisión | P0 |
| VAL-04 | Comentarios inline | Agregar observaciones en campos específicos | P0 |
| VAL-05 | Dashboard de validación | Estado: 2 aprobados, 1 pendiente, 0 rechazados | P0 |
| VAL-06 | Historial de correcciones | Ver qué se solicitó y qué se corrigió | P1 |
| VAL-07 | Alertas de calidad | Valores atípicos, campos vacíos | P1 |
| VAL-08 | Notificar a capturista | Envío automático de correcciones solicitadas | P1 |

---

### 4.3 CONSOLIDADOR

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| CON-01 | Dashboard de monitoreo | Estado en tiempo real de las 10 dependencias | P0 |
| CON-02 | Alertas de plazos | Notificaciones automáticas 2 días antes | P0 |
| CON-03 | Validación técnica automática | Reglas configurables de calidad | P0 |
| CON-04 | Solicitar aclaraciones | Chat con validadores de dependencia | P0 |
| CON-05 | Consolidación automática | Botón "Generar consolidado" | P0 |
| CON-06 | Versionamiento | Snapshots fechados del consolidado | P0 |
| CON-07 | Reporte de calidad | Dashboard de completitud y errores | P1 |
| CON-08 | Exportar consolidado | Descargar en Excel, CSV, PDF | P1 |
| CON-09 | Comparativo trimestral | Ver evolución vs periodos anteriores | P2 |

---

### 4.4 ANALISTA

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| ANA-01 | API de datos | Endpoint REST para consultar datos | P0 |
| ANA-02 | Conector Power BI | Plugin/Conector directo | P0 |
| ANA-03 | Exportación multi-formato | CSV, JSON, Parquet, Excel | P0 |
| ANA-04 | Diccionario de datos | Documentación de campos y catálogos | P0 |
| ANA-05 | Consultas SQL directas | Acceso de lectura a BD (con permisos) | P1 |
| ANA-06 | Serie histórica completa | Acceso a todos los trimestres | P1 |
| ANA-07 | Datos abiertos públicos | Endpoint sin autenticación para datos públicos | P2 |

---

### 4.5 DECISOR (SECTORIAL Y ESTRATÉGICO)

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| DEC-01 | Dashboard ejecutivo | KPIs sintéticos con semáforos | P0 |
| DEC-02 | Drill-down interactivo | Click para ver detalle | P0 |
| DEC-03 | Alertas configurables | Notificación de indicadores críticos | P0 |
| DEC-04 | Exportar gráficas | Descarga PNG/SVG para presentaciones | P0 |
| DEC-05 | Acceso móvil responsive | Funcional en tablet/smartphone | P0 |
| DEC-06 | Comparativos sectoriales | Benchmarking entre dependencias | P1 |
| DEC-07 | Evolución temporal | Gráficas de tendencia | P1 |
| DEC-08 | Mapa de calor territorial | Visualización geográfica | P2 |

---

### 4.6 AUDITOR/CONTROL

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| AUD-01 | Log de auditoría completo | Registro de CRUD (Crear, Leer, Actualizar, Eliminar) | P0 |
| AUD-02 | Trazabilidad de cambios | Qué cambió, quién, cuándo, por qué | P0 |
| AUD-03 | Acceso a evidencias | Enlaces directos a archivos originales | P0 |
| AUD-04 | Exportar log de auditoría | Descargar para análisis externo | P0 |
| AUD-05 | Comparativo con SIRPRE | Cruce automático de presupuestos | P1 |
| AUD-06 | Reporte de inconsistencias | Alertas de datos no coherentes | P1 |

---

### 4.7 CIUDADANO/PÚBLICO

#### Funcionalidades Esenciales

| # | Requisito | Descripción | Prioridad |
|---|-----------|-------------|-----------|
| CIU-01 | Portal público sin login | Acceso sin necesidad de registro | P0 |
| CIU-02 | Filtros simples | Por: Comuna, Tipo de acción, Población | P0 |
| CIU-03 | Visualizaciones amigables | Gráficas simples, sin jerga técnica | P0 |
| CIU-04 | Datos abiertos descargables | CSV/Excel con licencia abierta | P0 |
| CIU-05 | Mapa territorial | Ver actividades por comuna/corregimiento | P1 |
| CIU-06 | Glosario | Explicación de términos técnicos | P1 |
| CIU-07 | Versión móvil | Responsive design | P1 |

---

## 5. ARQUITECTURA DE INFORMACIÓN Y NAVEGACIÓN

### 5.1 Estructura de Menú Principal por Rol

```
┌─────────────────────────────────────────────────────────────────────┐
│ CAPTURISTA                                                          │
├─────────────────────────────────────────────────────────────────────┤
│ 🏠 Inicio                                                            │
│    └─ Dashboard con mis indicadores                                 │
│ 📝 Mis Indicadores                                                   │
│    ├─ Pendientes de diligenciar (5)                                │
│    ├─ Borradores (2)                                               │
│    ├─ Enviados a validación (1)                                    │
│    └─ Aprobados (0)                                                │
│ 📊 Mi Histórico                                                      │
│    └─ Ver trim anteriores para referencia                          │
│ 📚 Ayuda                                                             │
│    ├─ Instructivo                                                  │
│    ├─ Videos tutoriales                                           │
│    └─ Preguntas frecuentes                                        │
│ ⚙️  Mi Perfil                                                        │
│    └─ Cambiar contraseña, configurar notificaciones                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ VALIDADOR DEPENDENCIA                                               │
├─────────────────────────────────────────────────────────────────────┤
│ 🏠 Inicio                                                            │
│    └─ Dashboard de validación                                       │
│ 🔍 Por Validar (3)                                                   │
│    └─ Indicadores enviados por mis capturistas                     │
│ ✅ Aprobados (5)                                                     │
│ 🔄 Devueltos (1)                                                     │
│ 📊 Reporte de mi Dependencia                                         │
│    └─ Dashboard sectorial                                          │
│ 📚 Ayuda                                                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ CONSOLIDADOR                                                        │
├─────────────────────────────────────────────────────────────────────┤
│ 🏠 Monitor de Avance                                                 │
│    └─ Dashboard de estado de 10 dependencias                       │
│ 🔍 Validación Técnica                                                │
│    ├─ Pendientes de aprobar (2)                                    │
│    └─ Alertas de calidad                                           │
│ 📦 Consolidados                                                      │
│    ├─ Generar nuevo consolidado                                    │
│    └─ Histórico de versiones                                       │
│ ⚙️  Configuración                                                    │
│    ├─ Gestionar plazos                                             │
│    ├─ Configurar reglas de validación                             │
│    └─ Gestionar usuarios                                          │
│ 📊 Reportes de Calidad                                               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ANALISTA                                                            │
├─────────────────────────────────────────────────────────────────────┤
│ 📊 Dashboards                                                        │
│    ├─ Consolidado ciudad                                           │
│    ├─ Por sector                                                   │
│    ├─ Por territorio                                               │
│    └─ Por población                                                │
│ 📈 Análisis Avanzado                                                 │
│    ├─ Tendencias                                                   │
│    ├─ Correlaciones                                                │
│    └─ Proyecciones                                                 │
│ 💾 Exportar Datos                                                    │
│    ├─ CSV, JSON, Excel                                             │
│    └─ Conectar Power BI                                            │
│ 📚 Documentación                                                     │
│    └─ Diccionario de datos, API docs                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ DECISOR SECTORIAL / ESTRATÉGICO                                     │
├─────────────────────────────────────────────────────────────────────┤
│ 🎯 Mi Dashboard Ejecutivo                                            │
│    └─ KPIs principales con semáforos                               │
│ 📊 Reportes                                                          │
│    ├─ Informe trimestral automático                               │
│    ├─ Comparativo sectorial                                        │
│    └─ Evolución temporal                                           │
│ 🗺️  Mapa Territorial                                                 │
│ 🔔 Mis Alertas                                                       │
│    └─ Configurar notificaciones personalizadas                     │
│ 💾 Exportar                                                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ AUDITOR/CONTROL                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ 🔍 Consultar Datos                                                   │
│    └─ Todos los indicadores (solo lectura)                        │
│ 📜 Log de Auditoría                                                  │
│    ├─ Buscar por usuario, fecha, acción                           │
│    └─ Exportar log                                                │
│ 📎 Evidencias                                                        │
│    └─ Acceso a archivos adjuntos                                  │
│ 💰 Cruce con SIRPRE                                                  │
│    └─ Validar coherencia presupuestal                             │
│ 💾 Exportar                                                          │
│    └─ Descarga para análisis externo                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ CIUDADANO/PÚBLICO (Portal Público - Sin Login)                      │
├─────────────────────────────────────────────────────────────────────┤
│ 🏠 Inicio                                                            │
│    └─ "¿Qué se hace en Participación Ciudadana?"                   │
│ 🗺️  Ver por Comuna/Corregimiento                                     │
│    └─ Filtrar actividades de mi territorio                        │
│ 📊 Avances Generales                                                 │
│    └─ Gráficas simples de cumplimiento                            │
│ 💾 Datos Abiertos                                                    │
│    └─ Descargar dataset completo                                  │
│ ❓ ¿Qué es la PPPC?                                                  │
│    └─ Explicación ciudadana de la política                        │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Flujo de Navegación - Capturista (Ejemplo Detallado)

```
LOGIN
  │
  └─► DASHBOARD INICIAL
        │
        ├─► "Mis Indicadores Pendientes (5)"
        │     │
        │     └─► LISTA DE INDICADORES
        │           │
        │           ├─ Indicador #1: [Nombre] - 🔴 Vence en 2 días
        │           ├─ Indicador #2: [Nombre] - 🟡 Vence en 5 días
        │           ├─ Indicador #3: [Nombre] - 🟢 Vence en 10 días
        │           │
        │           └─► CLICK EN INDICADOR #1
        │                 │
        │                 └─► FORMULARIO DE CAPTURA
        │                       │
        │                       ├─► Sección 1: Metadatos (colapsada por defecto)
        │                       │     └─ Nombre, Fórmula, Meta (solo lectura)
        │                       │
        │                       ├─► Sección 2: Resultado Trimestre II (expandida)
        │                       │     ├─ Campo: Resultado numérico [____] ✓ Válido
        │                       │     ├─ Campo: Observaciones [textarea]
        │                       │     └─ Campo: Evidencia [Upload] ✅ archivo.pdf
        │                       │
        │                       ├─► Sección 3: Desagregación (opcional, colapsada)
        │                       │
        │                       └─► BOTONES
        │                             ├─ [Guardar Borrador] ← auto-guardado a 14:32
        │                             └─ [Enviar a Validación]
        │                                   │
        │                                   └─► CONFIRMACIÓN
        │                                         "✓ Enviado exitosamente"
        │                                         "Radicado: MISE-2025-0234"
        │                                         │
        │                                         └─► VOLVER A LISTA
        │                                               (ahora muestra 4 pendientes)
        │
        └─► Barra lateral:
              • Progreso global: 1/5 (20%)
              • Notificaciones (2)
              • Ayuda rápida
```

---

## 6. DISEÑO DE INTERFACES POR ROL

### 6.1 WIREFRAMES CONCEPTUALES

#### CAPTURISTA - Dashboard Inicial

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🏛️ MISE - Medellín          [María González] [🔔2] [⚙️] [Salir]       │
├────────────────────────────────────────────────────────────────────────┤
│  📝 Mis Indicadores                                                     │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 📊 TU PROGRESO                                                    │  │
│  │ ████████░░░░░░░░░░░░░░░░  3/8 indicadores (37%)                  │  │
│  │                                                                   │  │
│  │ ⏰ Faltan 3 días para cierre de captura                           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  PENDIENTES DE DILIGENCIAR (5)                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 🔴 [#401] Mesa Contra el Racismo           🕐 Vence en 2 días    │  │
│  │    Última actualización: Nunca                                    │  │
│  │    [Diligenciar] ───────────────────────────────────────────────►│  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │ 🟡 [#402] Colectivos Afros Fortalecidos   🕐 Vence en 5 días     │  │
│  │    Última actualización: Nunca                                    │  │
│  │    [Diligenciar] ───────────────────────────────────────────────►│  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  BORRADORES (2)                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 📝 [#403] Acciones Enfoque Diferencial                           │  │
│  │    Guardado: Hoy 14:32 - 70% completo                            │  │
│  │    [Continuar] ─────────────────────────────────────────────────►│  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ENVIADOS A VALIDACIÓN (1)                                             │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 🔄 [#404] Expresiones Artísticas                                 │  │
│  │    Enviado: Ayer 16:45 - En revisión por Carlos Ramírez          │  │
│  │    [Ver detalles] ──────────────────────────────────────────────►│  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

#### CAPTURISTA - Formulario de Captura

```
┌────────────────────────────────────────────────────────────────────────┐
│ ← Volver a mis indicadores                                             │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📋 INDICADOR #401                                                      │
│  Mesa Interinstitucional Contra el Racismo y la Discriminación         │
│  en funcionamiento                                                      │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ 🕐 Vence en 2 días                                              │    │
│  │ 📊 Avance: 60% completo                                         │    │
│  │ 💾 Último guardado: Hoy 14:32 (auto-guardado)                   │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ▼ INFORMACIÓN DEL INDICADOR (Solo lectura)                            │
│    Meta 2025: 1 mesa en funcionamiento                                 │
│    Fórmula: V1 (Funcionamiento de mesa)                                │
│    Población objetivo: Población Negra, Afro, Raizal, Palenquera       │
│    [Ver más detalles ▼]                                                │
│                                                                         │
│  ▼ RESULTADO TRIMESTRE II - 2025                                       │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ Resultado Numérico *                                            │    │
│  │ ┌──────────┐                                                    │    │
│  │ │    0     │  ℹ️ Mesa no constituida aún                        │    │
│  │ └──────────┘                                                    │    │
│  │ ✓ Valor válido (0-1)                                            │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ Observaciones *                                                 │    │
│  │ ┌──────────────────────────────────────────────────────────┐   │    │
│  │ │Durante el segundo trimestre se avanzó en el proceso      │   │    │
│  │ │precontractual para selección del operador que apoyará    │   │    │
│  │ │la conformación de la mesa. Se espera iniciar en trim III│   │    │
│  │ └──────────────────────────────────────────────────────────┘   │    │
│  │ 215/500 caracteres                                              │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ Fuente de Verificación *                                        │    │
│  │ [📎 informe_supervision_trimII.pdf] [x Eliminar]                │    │
│  │ [+ Adjuntar archivo]                                            │    │
│  │ Formatos: PDF, Word, Excel, JPG (Máx 10MB)                      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ▶ DESAGREGACIÓN (Opcional)                                            │
│                                                                         │
│  * Campos obligatorios                                                 │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐       │
│  │ [Guardar Borrador]   │  │ [Enviar a Validación] ─────────► │       │
│  └──────────────────────┘  └──────────────────────────────────┘       │
└────────────────────────────────────────────────────────────────────────┘
```

#### CONSOLIDADOR - Dashboard de Monitoreo

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🏛️ MISE - Consolidador     [Ana Martínez] [🔔5] [⚙️] [Salir]          │
├────────────────────────────────────────────────────────────────────────┤
│  📊 MONITOR DE AVANCE - TRIMESTRE II 2025                               │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 🎯 RESUMEN GENERAL                                                │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  70% Completitud global        │  │
│  │                                                                   │  │
│  │ ✅ Aprobadas: 6/10    🟡 En validación: 2/10    🔴 Pendientes: 2/10│  │
│  │ ⏰ Faltan 3 días para cierre                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ESTADO POR DEPENDENCIA                        [🔄 Actualizar]         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ DEPENDENCIA       │INDICADORES│  ESTADO    │DÍAS RESTANTES│ACCIÓN│   │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │✅ SPC             │  53/53    │ Aprobado   │      -       │[Ver] │   │
│  │✅ Mujeres         │   8/8     │ Aprobado   │      -       │[Ver] │   │
│  │✅ Educación       │   7/7     │ Aprobado   │      -       │[Ver] │   │
│  │🟡 DAP             │   9/9     │ En validac │   2 días     │[►]   │   │
│  │🟡 Cultura         │   6/6     │ En validac │   3 días     │[►]   │   │
│  │🟢 Juventud        │   4/6     │ Capturando │   3 días     │[📨] │   │
│  │🟢 PazDH           │   3/4     │ Capturando │   3 días     │[📨] │   │
│  │🔴 Étnica          │   0/8     │ Sin iniciar│   3 días ⚠️  │[📨📨]│   │
│  │🔴 GH              │   0/3     │ Sin iniciar│   3 días ⚠️  │[📨📨]│   │
│  │🔴 SISF            │   2/4     │ Atrasado   │   3 días ⚠️  │[📨📨]│   │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  PENDIENTES DE APROBAR (2)                                             │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ 🟡 DAP - 9 indicadores                                          │    │
│  │    Enviado: Hoy 10:15                                           │    │
│  │    ⚠️ 2 alertas de calidad detectadas                           │    │
│  │    [Revisar y Aprobar] ────────────────────────────────────────►│    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  [📦 GENERAR CONSOLIDADO]  [📊 Reporte de Calidad]  [⚙️ Config]        │
└────────────────────────────────────────────────────────────────────────┘
```

#### DECISOR - Dashboard Ejecutivo

```
┌────────────────────────────────────────────────────────────────────────┐
│ 🏛️ MISE - Dashboard Ejecutivo          [Patricia Gómez - Sec Mujeres] │
├────────────────────────────────────────────────────────────────────────┤
│  📊 SECRETARÍA DE LAS MUJERES - TRIMESTRE II 2025                      │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 🎯 CUMPLIMIENTO GLOBAL              ┌─────────────────────────┐  │  │
│  │                                      │  78%                    │  │  │
│  │ ████████████████████░░░░░░░░░        │  ⚠️ Alerta             │  │  │
│  │                                      │  Meta: 85%              │  │  │
│  │ 6/8 indicadores en meta              └─────────────────────────┘  │  │
│  │ 2/8 indicadores en riesgo 🔴                                     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  RESUMEN DE INDICADORES                                                │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ✅ En meta (6):                                                 │    │
│  │   • Escuelas de formación (120% - 180/150)                      │    │
│  │   • Mujeres certificadas (105% - 210/200)                       │    │
│  │   • Espacios de participación (100% - 12/12)                    │    │
│  │   ... [Ver todos ▼]                                             │    │
│  ├────────────────────────────────────────────────────────────────┤    │
│  │ 🔴 En riesgo (2):                                               │    │
│  │   • Casas de Igualdad (60% - 3/5) ⚠️                            │    │
│  │   • Presupuesto ejecutado (55% - $550M/$1.000M) ⚠️              │    │
│  │   [Ver detalle y acciones ►]                                    │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  COMPARATIVO INTERSECTORIAL                                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ Ranking de cumplimiento:                                        │    │
│  │ 1. SPC           ███████████████████░ 95%                       │    │
│  │ 2. Educación     ██████████████████░░ 90%                       │    │
│  │ 3. Cultura       █████████████████░░░ 85%                       │    │
│  │ 4. Mujeres (tú)  ████████████████░░░░ 78% ⚠️                    │    │
│  │ 5. Juventud      ███████████████░░░░░ 75%                       │    │
│  │ ... [Ver ranking completo ▼]                                    │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  [📊 Ver Detalle Completo]  [💾 Exportar para Presentación]  [🔔]      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. DASHBOARDS DIFERENCIADOS

### 7.1 Especificaciones de Dashboards

#### DASHBOARD CAPTURISTA

**Propósito:** Facilitar y hacer eficiente el proceso de diligenciamiento

**KPIs principales:**
- Progreso personal (X/Y indicadores)
- Días restantes para cierre
- Estado de cada indicador (pendiente/borrador/enviado/aprobado/devuelto)

**Widgets:**
1. Barra de progreso global
2. Lista priorizada de indicadores (por urgencia)
3. Alertas de correcciones solicitadas
4. Ayuda contextual

**Interactividad:**
- Click en indicador → Abre formulario de captura
- Filtros: Por estado (pendientes/borradores/enviados)

---

#### DASHBOARD CONSOLIDADOR

**Propósito:** Monitorear avance en tiempo real y facilitar gestión de plazos

**KPIs principales:**
- Completitud global (%)
- Dependencias que han reportado vs pendientes
- Días restantes para cierre
- Alertas de calidad (# de validaciones automáticas fallidas)

**Widgets:**
1. Mapa de calor de avance por dependencia
2. Timeline de plazos
3. Cola de aprobaciones pendientes
4. Gráfica de evolución de reportes recibidos

**Interactividad:**
- Click en dependencia → Ver detalle de sus indicadores
- Botón "Enviar recordatorio" para dependencias atrasadas
- Botón "Aprobar lote" para dependencias sin alertas

---

#### DASHBOARD DECISOR SECTORIAL

**Propósito:** Visión ejecutiva de cumplimiento de su sector

**KPIs principales:**
- % de cumplimiento global del sector
- # de indicadores en meta / en riesgo / críticos
- Comparativo vs trimestre anterior
- Ranking vs otros sectores

**Widgets:**
1. Gauge de cumplimiento (semáforo)
2. Listado de indicadores en riesgo (para atención prioritaria)
3. Gráfica de evolución trimestral
4. Tabla comparativa intersectorial

**Interactividad:**
- Click en indicador → Drill-down a detalle con observaciones
- Toggle: Vista agregada ↔ Vista detallada
- Exportar como PowerPoint

---

#### DASHBOARD DECISOR ESTRATÉGICO

**Propósito:** Visión de ciudad completa, priorización de atención

**KPIs principales:**
- Cumplimiento Plan de Desarrollo en PPPC (%)
- Sectores en meta / en riesgo
- Inversión ejecutada vs programada
- Cobertura territorial (comunas atendidas)

**Widgets:**
1. Mapa de calor geográfico (actividades por comuna)
2. Ranking de sectores por cumplimiento
3. Gráfica de evolución anual
4. Top 5 alertas críticas

**Interactividad:**
- Click en sector → Drill-down a dashboard sectorial
- Click en comuna en mapa → Ver actividades específicas
- Configurar alertas personalizadas

---

#### DASHBOARD CIUDADANO (PORTAL PÚBLICO)

**Propósito:** Rendición de cuentas y transparencia

**KPIs principales:**
- ¿Cuántas personas participaron este trimestre? (agregado)
- ¿Cuántas actividades se realizaron?
- Top 3 comunas con más actividades

**Widgets:**
1. Mapa interactivo por comuna
2. Gráficas de barras simples (sin jerga)
3. Línea de tiempo de hitos
4. Historias de éxito (opcional)

**Interactividad:**
- Filtros simples: Por comuna, por tipo de actividad
- Descargar datos abiertos
- Sin login requerido

---

## 8. RUTA METODOLÓGICA PARA DISEÑO UX

### 8.1 Fases del Proceso de Diseño

```
FASE 0: FUNDAMENTOS (Completado en este documento)
  ├─ Matriz de roles y responsabilidades
  ├─ Perfiles de usuario detallados
  ├─ Requisitos funcionales por rol
  └─ User Journey Maps
        ↓
FASE 1: INVESTIGACIÓN Y VALIDACIÓN (2 semanas)
  ├─ Entrevistas con usuarios reales (2-3 por rol)
  ├─ Observación de proceso actual (shadowing)
  ├─ Validación de User Journeys
  └─ Priorización de requisitos (MoSCoW)
        ↓
FASE 2: ARQUITECTURA DE INFORMACIÓN (1 semana)
  ├─ Card sorting con usuarios
  ├─ Definición de sitemap final
  ├─ Flujos de navegación detallados
  └─ Nomenclatura y microcopy
        ↓
FASE 3: DISEÑO DE INTERACCIÓN (2 semanas)
  ├─ Wireframes de baja fidelidad (papel/Balsamiq)
  ├─ Pruebas de usabilidad con wireframes
  ├─ Iteración basada en feedback
  └─ Wireframes de mediana fidelidad (Figma)
        ↓
FASE 4: DISEÑO VISUAL (2 semanas)
  ├─ Sistema de diseño (colores, tipografía, componentes)
  ├─ Mockups de alta fidelidad
  ├─ Diseño responsive (desktop, tablet, móvil)
  └─ Guía de estilos
        ↓
FASE 5: PROTOTIPADO (1 semana)
  ├─ Prototipo interactivo en Figma
  ├─ Flujos completos clickeables
  └─ Preparación para pruebas de usabilidad
        ↓
FASE 6: TESTING DE USABILIDAD (2 semanas)
  ├─ Pruebas con 5 usuarios por rol crítico
  ├─ Métricas: Tasa de éxito, tiempo en tarea, satisfacción
  ├─ Identificación de pain points
  └─ Iteración de diseño
        ↓
FASE 7: ESPECIFICACIONES TÉCNICAS (1 semana)
  ├─ Documentación de componentes para desarrollo
  ├─ Especificaciones de interacción
  ├─ Casos de uso técnicos
  └─ Matriz de trazabilidad (requisitos → pantallas)
        ↓
FASE 8: ENTREGA A DESARROLLO (Continuo)
  ├─ Handoff a equipo de desarrollo
  ├─ Acompañamiento durante implementación
  ├─ Revisión de calidad (QA de UX)
  └─ Ajustes finales
        ↓
FASE 9: CAPACITACIÓN Y ADOPCIÓN (2 semanas)
  ├─ Videos tutoriales por rol
  ├─ Manuales de usuario
  ├─ Sesiones de capacitación presenciales
  └─ Soporte durante primeras semanas
        ↓
FASE 10: MONITOREO POST-LANZAMIENTO (Continuo)
  ├─ Analítica de uso (Google Analytics, Hotjar)
  ├─ Encuestas de satisfacción
  ├─ Identificación de mejoras
  └─ Iteración continua

DURACIÓN TOTAL ESTIMADA: 13 semanas (3.5 meses)
```

---

### 8.2 Herramientas Recomendadas por Fase

| Fase | Herramienta | Propósito |
|------|-------------|-----------|
| Investigación | Miro, Zoom | Entrevistas remotas, mapas de empatía |
| Arquitectura | Optimal Workshop, Miro | Card sorting, sitemaps |
| Wireframes | Balsamiq, Figma | Bocetos rápidos, iteración |
| Diseño Visual | Figma, Adobe XD | Mockups, sistema de diseño |
| Prototipado | Figma, InVision | Prototipos interactivos |
| Testing | Maze, UserTesting | Pruebas de usabilidad remotas |
| Documentación | Figma, Zeplin, Notion | Especificaciones para dev |
| Analítica | Google Analytics, Hotjar | Monitoreo de uso |

---

### 8.3 Técnicas de Investigación por Rol

#### Investigación con CAPTURISTAS

**Técnicas:**
1. **Shadowing:** Observar 2-3 capturistas diligenciando Excel actual
2. **Entrevista contextual:** Mientras diligencian, preguntar sobre decisiones
3. **Análisis de tareas:** Cronometrar cada paso del proceso
4. **Cuestionario de pain points:** Escala 1-5 de frustración por aspecto

**Preguntas clave:**
- ¿Cuánto tiempo te toma diligenciar un indicador?
- ¿Qué es lo más confuso del formato actual?
- ¿Qué información te falta frecuentemente?
- ¿Cómo sabes si lo estás haciendo bien?
- ¿Qué harías diferente si pudieras rediseñar el proceso?

---

#### Investigación con CONSOLIDADOR

**Técnicas:**
1. **Diario de actividades:** Pedirle que registre una semana de consolidación
2. **Análisis de email:** Revisar comunicaciones para entender fricciones
3. **Mapeo de proceso actual:** Co-crear diagrama de flujo de su trabajo

**Preguntas clave:**
- ¿Cuánto tiempo dedicas a consolidación vs otros procesos?
- ¿Cuál es el error más frecuente que detectas?
- ¿Qué dependencias son más problemáticas y por qué?
- Si pudieras automatizar 3 cosas, ¿cuáles serían?

---

#### Investigación con DECISORES

**Técnicas:**
1. **Entrevista semi-estructurada:** 30 min
2. **Análisis de necesidades de información:** ¿Qué preguntas necesitan responder?
3. **Evaluación de dashboards de referencia:** Mostrar ejemplos de otras ciudades

**Preguntas clave:**
- ¿Cada cuánto consultas información de MISE?
- ¿Qué decisiones has tomado (o no) por falta de información?
- ¿Cómo prefieres recibir información: tabla/gráfica/mapa?
- ¿Qué dispositivo usas más: desktop/tablet/móvil?

---

### 8.4 Métricas de Éxito UX por Rol

| Rol | Métrica | Meta | Método de Medición |
|-----|---------|------|--------------------|
| **CAPTURISTA** | Tiempo de diligenciamiento por indicador | < 20 min | Analítica de tiempo en formulario |
| | Tasa de errores | < 5% devueltos | % de indicadores rechazados |
| | Satisfacción (SUS Score) | > 70/100 | Encuesta estandarizada |
| | Tasa de adopción | 100% usan sistema | Ningún capturista usa Excel paralelo |
| **VALIDADOR** | Tiempo de validación por indicador | < 5 min | Analítica |
| | % uso de comentarios inline | > 80% | vs email externo |
| **CONSOLIDADOR** | Tiempo de consolidación | < 1 hora | vs 48h actual |
| | Satisfacción | > 80/100 | Encuesta SUS |
| **DECISOR** | Tiempo para encontrar KPI clave | < 2 min | Test de usabilidad |
| | Frecuencia de uso | Mensual | Google Analytics |
| | % que exportan para presentaciones | > 50% | Tracking de exportaciones |
| **CIUDADANO** | Comprensión de visualizaciones | > 80% respuestas correctas | Test de comprensión |
| | Tasa de rebote | < 40% | Google Analytics |

---

### 8.5 Checklist de Accesibilidad

El sistema debe cumplir con WCAG 2.1 Nivel AA:

**Principios:**
- ✅ **Perceptible:** Contraste mínimo 4.5:1, texto alternativo en imágenes
- ✅ **Operable:** Navegable por teclado, no depender solo de mouse
- ✅ **Comprensible:** Lenguaje claro, mensajes de error específicos
- ✅ **Robusto:** Compatible con lectores de pantalla

**Elementos críticos:**
- [ ] Formularios con labels claros
- [ ] Orden lógico de tabulación
- [ ] Feedback visual Y textual de errores
- [ ] Botones con tamaño mínimo 44x44px (móvil)
- [ ] Zoom hasta 200% sin pérdida de funcionalidad

---

## 9. MATRIZ DE ACCESOS Y PERMISOS

### 9.1 Tabla de Permisos por Rol

```
ENTIDAD: Indicador

┌──────────────────────┬────────┬────────┬────────────┬─────────┬─────────┐
│ ROL                  │ CREAR  │ LEER   │ ACTUALIZAR │ ELIMINAR│ APROBAR │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Capturista           │   ✅   │ Solo   │ Solo sus   │   ❌    │   ❌    │
│                      │        │ suyos  │ borradores │         │         │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Validador Dep        │   ❌   │ Solo   │     ❌     │   ❌    │Solo su  │
│                      │        │ su dep │            │         │   dep   │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Consolidador         │   ❌   │ Todos  │     ❌     │   ❌    │ Todos   │
│                      │        │        │            │         │(post-val│
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Analista             │   ❌   │ Todos  │     ❌     │   ❌    │   ❌    │
│                      │        │(solo   │            │         │         │
│                      │        │leer)   │            │         │         │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Decisor Sectorial    │   ❌   │ Su     │     ❌     │   ❌    │   ❌    │
│                      │        │ sector │            │         │         │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Decisor Estratégico  │   ❌   │ Todos  │     ❌     │   ❌    │   ❌    │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Auditor              │   ❌   │ Todos+ │     ❌     │   ❌    │   ❌    │
│                      │        │ log    │            │         │         │
├──────────────────────┼────────┼────────┼────────────┼─────────┼─────────┤
│ Ciudadano            │   ❌   │ Público│     ❌     │   ❌    │   ❌    │
│                      │        │ solo   │            │         │         │
└──────────────────────┴────────┴────────┴────────────┴─────────┴─────────┘
```

### 9.2 Estados del Indicador y Transiciones

```
MÁQUINA DE ESTADOS

┌─────────────┐
│   BORRADOR  │ ← Capturista puede editar
└──────┬──────┘
       │ [Enviar a Validación]
       ↓
┌─────────────────┐
│ EN VALIDACIÓN   │ ← Validador Dep revisa
└────┬───────┬────┘
     │       │
     │       │ [Aprobar]
     │       ↓
     │   ┌──────────────────┐
     │   │ VALIDADO (Dep)   │ ← Consolidador revisa
     │   └────┬───────┬─────┘
     │        │       │
     │        │       │ [Aprobar Consolidador]
     │        │       ↓
     │        │   ┌────────────────┐
     │        │   │ CONSOLIDADO    │ ← Oficial, publicado
     │        │   └────────────────┘
     │        │
     │        │ [Solicitar aclaración]
     │        ↓
     │   ┌──────────────────────┐
     │   │ REQUIERE ACLARACIÓN  │ → Validador Dep responde
     │   └──────────────────────┘
     │
     │ [Rechazar]
     ↓
┌──────────────────┐
│ DEVUELTO         │ → Capturista corrige → EN VALIDACIÓN
└──────────────────┘

REGLAS:
- Solo Capturista puede editar en estado BORRADOR
- Solo Validador Dep puede cambiar EN VALIDACIÓN → VALIDADO o DEVUELTO
- Solo Consolidador puede cambiar VALIDADO → CONSOLIDADO
- Una vez CONSOLIDADO, el indicador es inmutable (solo consulta)
```

### 9.3 Matriz de Visibilidad de Campos

Algunos campos deben ser visibles solo para ciertos roles:

| Campo | Capturista | Validador | Consolidador | Analista | Decisor | Auditor | Ciudadano |
|-------|-----------|-----------|--------------|----------|---------|---------|-----------|
| Metadatos (nombre, fórmula, meta) | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver |
| Resultado trimestral | ✅ Editar | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver |
| Observaciones cualitativas | ✅ Editar | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ⚠️ Resumidas |
| Evidencias adjuntas | ✅ Upload | ✅ Ver | ✅ Ver | ❌ | ❌ | ✅ Ver | ❌ |
| Presupuesto programado | ✅ Editar | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver |
| Presupuesto ejecutado | ✅ Editar | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver | ✅ Ver |
| Comentarios de validación | ✅ Ver (si es suyo) | ✅ Ver/Crear | ✅ Ver/Crear | ❌ | ❌ | ✅ Ver | ❌ |
| Log de cambios | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Ver | ❌ |

---

## 10. PLAN DE IMPLEMENTACIÓN UX

### 10.1 Roadmap de Implementación

```
MES 1: INVESTIGACIÓN Y DISEÑO
├─ Semana 1-2: Investigación con usuarios (entrevistas, shadowing)
├─ Semana 3: Arquitectura de información (card sorting, sitemaps)
└─ Semana 4: Wireframes de baja fidelidad + primer round de testing

MES 2: DISEÑO VISUAL Y PROTOTIPADO
├─ Semana 5-6: Sistema de diseño + Mockups de alta fidelidad
├─ Semana 7: Prototipo interactivo en Figma
└─ Semana 8: Testing de usabilidad + iteración

MES 3: ESPECIFICACIONES Y HANDOFF
├─ Semana 9: Documentación técnica para desarrollo
├─ Semana 10-11: Handoff a dev + Inicio de implementación
└─ Semana 12: QA de UX en versión desarrollada

MES 4: CAPACITACIÓN Y LANZAMIENTO
├─ Semana 13-14: Capacitación por roles + Videos tutoriales
├─ Semana 15: Piloto con 2-3 dependencias
└─ Semana 16: Lanzamiento general + Monitoreo intensivo

POST-LANZAMIENTO: OPTIMIZACIÓN CONTINUA
└─ Sprints quincenales de mejora basados en analítica y feedback
```

### 10.2 Entregables por Fase

| Fase | Entregables | Responsable | Formato |
|------|-------------|-------------|---------|
| **Investigación** | • Reportes de entrevistas<br>• User Personas actualizadas<br>• Journey Maps validados | UX Researcher | PDF + Miro |
| **Arquitectura** | • Sitemap final<br>• Flujos de navegación<br>• Glosario de términos | UX Architect | Figma |
| **Wireframes** | • Wireframes por rol<br>• Reporte de testing inicial | UX Designer | Figma |
| **Diseño Visual** | • Sistema de diseño<br>• Mockups de todas las pantallas<br>• Guía de estilos | UI Designer | Figma + Notion |
| **Prototipo** | • Prototipo interactivo<br>• Casos de uso documentados | UX Designer | Figma |
| **Testing** | • Reporte de usabilidad<br>• Matriz de issues priorizados | UX Researcher | Google Sheets |
| **Especificaciones** | • Specs técnicas por componente<br>• Matriz de trazabilidad<br>• Assets exportados | UX/UI + Dev Lead | Figma + Zeplin |
| **Capacitación** | • Videos tutoriales (5-10 min c/u)<br>• Manuales de usuario<br>• FAQs | UX Writer + Instructional Designer | Video + PDF |

---

### 10.3 Equipo Recomendado

**Core Team:**
- 1 UX Lead / Product Designer (coordinación general)
- 1 UX Researcher (investigación y testing)
- 1 UI Designer (diseño visual)
- 1 UX Writer (microcopy y contenidos)
- 1 Front-end Developer (acompañamiento técnico)

**Tiempo Dedicado:**
- Meses 1-3: Tiempo completo
- Mes 4+: Medio tiempo (soporte y optimización)

---

### 10.4 Criterios de Aceptación UX

Antes de dar por concluida cada fase, verificar:

**Fase de Investigación:**
- [ ] Al menos 2 entrevistas por rol crítico (Capturista, Consolidador, Decisor)
- [ ] Journey Maps validados con usuarios reales
- [ ] Pain points documentados y priorizados

**Fase de Diseño:**
- [ ] Wireframes testeados con 3+ usuarios por rol
- [ ] Tasa de éxito en tareas > 80%
- [ ] Sistema de diseño define colores, tipografía, componentes

**Fase de Prototipo:**
- [ ] Prototipo permite completar flujos críticos end-to-end
- [ ] Feedback de usabilidad incorporado
- [ ] Validación de stakeholders (DAP, SPC)

**Pre-Lanzamiento:**
- [ ] QA de UX sin critical bugs
- [ ] Capacitaciones completadas con 80%+ asistencia
- [ ] Documentación de usuario disponible

**Post-Lanzamiento (1 mes):**
- [ ] Tasa de adopción > 90%
- [ ] SUS Score > 70
- [ ] < 5% de errores de captura

---

## ANEXOS

### ANEXO A: Plantilla de Entrevista - Capturista

**Objetivo:** Entender pain points y oportunidades en proceso de captura

**Sección 1: Contexto**
1. ¿Cuánto tiempo llevas diligenciando la MISE?
2. ¿Cuántos indicadores tienes a cargo?
3. ¿Qué otras responsabilidades tienes además de MISE?

**Sección 2: Proceso Actual**
4. Descríbeme paso a paso cómo diligencias un indicador (observar mientras lo hace)
5. ¿Cuánto tiempo te toma en promedio?
6. ¿Qué parte del proceso encuentras más confusa/difícil?
7. ¿Qué información te falta frecuentemente?

**Sección 3: Pain Points**
8. En una escala 1-5, ¿qué tan frustrante es el proceso actual? ¿Por qué?
9. ¿Has cometido errores al diligenciar? ¿De qué tipo?
10. ¿Cómo sabes si lo estás haciendo bien?
11. ¿Recibes retroalimentación? ¿Cómo?

**Sección 4: Ideal**
12. Si pudieras cambiar 3 cosas del proceso, ¿cuáles serían?
13. ¿Has usado otros sistemas de reporte que te hayan parecido mejores? ¿Cuáles?
14. ¿Qué te motivaría a diligenciar con más entusiasmo?

---

### ANEXO B: Plantilla de Card Sorting

**Instrucciones para participantes:**
"Agrupa estas funcionalidades en categorías que tengan sentido para ti. Puedes crear tus propias categorías."

**Tarjetas (Ejemplo para Capturista):**
- Diligenciar indicador nuevo
- Ver indicadores pendientes
- Ver borradores guardados
- Ver histórico de trimestres anteriores
- Cambiar mi contraseña
- Descargar instructivo
- Ver videos de ayuda
- Enviar indicador a validación
- Ver estado de mis indicadores
- Recibir notificaciones
- Adjuntar evidencias
- Contactar soporte
- Ver progreso global
- Exportar mi reporte

**Análisis:**
- Identificar patrones de agrupación
- Validar nomenclatura de menús
- Detectar funcionalidades que no encajan

---

### ANEXO C: Script de Prueba de Usabilidad

**Prueba con Capturista - Prototipo**

**Escenario:**
"Imagina que debes diligenciar el indicador #401 'Mesa Contra el Racismo'. El resultado del trimestre es 0 porque la mesa no se constituyó aún, pero se avanzó en proceso precontractual. Tienes un informe de supervisión como evidencia."

**Tareas:**
1. Inicia sesión en el sistema
2. Encuentra el indicador #401
3. Diligencia el resultado (0)
4. Escribe observación explicando la situación
5. Adjunta el informe de evidencia
6. Envía a validación

**Observar:**
- ¿Completa la tarea sin ayuda?
- ¿Cuánto tiempo toma?
- ¿En qué puntos duda o se confunde?
- ¿Qué dice en voz alta (think aloud)?

**Preguntas post-tarea:**
- En escala 1-5, ¿qué tan fácil fue?
- ¿Qué fue lo más confuso?
- ¿Qué mejorarías?

---

## CONCLUSIÓN

Este documento establece las **bases sólidas** para el diseño de experiencia de usuario del sistema MISE transformado. La estructura de roles, perfiles de usuario detallados, user journeys, y requisitos funcionales proporcionan una **hoja de ruta clara** para:

1. **Diseñadores UX/UI:** Saben qué diseñar para cada rol
2. **Desarrolladores:** Tienen requisitos funcionales claros
3. **Gestores del proyecto:** Pueden estimar tiempos y recursos
4. **Stakeholders:** Visualizan el producto final

**Próximos pasos inmediatos:**
1. Validar esta estructura con muestra de usuarios reales (1 semana)
2. Ajustar perfiles y journeys según feedback
3. Iniciar fase de wireframing de baja fidelidad (2 semanas)
4. Testear wireframes con usuarios (1 semana)
5. Iterar hacia diseño de alta fidelidad

**El éxito del sistema dependerá de:**
- Mantener al **usuario en el centro** del diseño
- **Validar constantemente** con usuarios reales, no asumir
- **Iterar** basados en evidencia, no en opiniones
- **Medir** adopción y satisfacción post-lanzamiento

---

**Documento elaborado por:** Equipo de Transformación Digital MISE  
**Fecha:** 15 de febrero de 2026  
**Versión:** 1.0  
**Próxima revisión:** Tras validación con usuarios
