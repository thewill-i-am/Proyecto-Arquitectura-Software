
# Proyecto:Arquitectura de Streaming con Detección de Imágenes

## 1. Introducción

### 1.1. Propósito
Este documento tiene como objetivo describir la arquitectura del sistema de transmisión y procesamiento de imágenes en tiempo real desarrollado en el marco del proyecto. Este documento está dirigido a arquitectos de software, desarrolladores, investigadores y responsables de operaciones, proporcionando una visión estructurada de los componentes del sistema, sus interacciones, estilos arquitectónicos, preocupaciones clave y decisiones justificadas.

### 1.2. Alcance
El sistema permite la captura, procesamiento y transmisión de imágenes en tiempo real, integrando herramientas de visión por computadora y una arquitectura de procesamiento distribuido basada en Apache Kafka. El sistema está diseñado para ser escalable, compatible con múltiples plataformas y seguro para operar en contextos de transmisión continua de datos visuales.

### 1.3. Definiciones, Acrónimos y Abreviaturas
- **Kafka**: Plataforma distribuida de transmisión de eventos en tiempo real.
- **Zookeeper**: Coordinador distribuido que gestiona la configuración y sincronización de servicios como Kafka.
- **Productor**: Componente que envía datos (frames de imágenes) a un topic de Kafka.
- **Consumidor**: Servicio que recibe datos desde Kafka (por ejemplo, el módulo detector de imágenes).
- **Topic**: Canal de comunicación entre productor y consumidor en Kafka.
- **Streaming**: Transmisión continua de datos en tiempo real.

### 1.4. Referencias
- Bass, L., Clements, P., & Kazman, R. (2021). *Software Architecture in Practice* (4th ed.). Addison-Wesley.
- Repositorio: [https://github.com/thewill-i-am/GoogleDevFest2023](https://github.com/thewill-i-am/GoogleDevFest2023)
- Documentación Apache Kafka: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)

### 1.5. Resumen
Este documento proporciona una descripción general de la arquitectura del sistema de streaming en tiempo real basado en Apache Kafka. A través de una arquitectura orientada a eventos, se garantiza un flujo eficiente de procesamiento distribuido entre el productor de imágenes, la cola de eventos Kafka y el detector de objetos como consumidor.

## 2. Representación Arquitectónica

### 2.1. Estilo Arquitectónico y Justificación
El sistema implementa una **arquitectura basada en eventos** utilizando **Apache Kafka** como middleware para la transmisión de datos. Esta arquitectura desacopla los componentes de captura y detección de imágenes, permitiendo:

- Procesamiento en paralelo y tolerancia a fallos.
- Escalabilidad horizontal de consumidores (detectores).
- Persistencia y replay de eventos (frames) si un componente falla.

La arquitectura se compone de:
- **Productor Kafka**: Publica frames de video capturados.
- **Zookeeper**: Gestiona la coordinación y el clúster de Kafka.
- **Consumidor**: Consume los frames filtados.
- **Detector**: Procesa los frames, ejecutando tareas de detección

## 3. Partes Interesadas y Preocupaciones del Sistema

### 3.1. Partes Interesadas
- **Desarrolladores**: Buscan modularidad y facilidad para pruebas en paralelo.
- **Usuarios finales**: Requieren resultados en tiempo real con alta precisión.

### 3.2. Preocupaciones del Sistema
- **Desacoplamiento**: Separación clara entre productores y consumidores.
- **Rendimiento**: Procesamiento y respuesta en tiempo real.
- **Tolerancia a fallos**: Continuidad operativa ante errores de red o nodos.
- **Escalabilidad horizontal**: Posibilidad de agregar más detectores según demanda.
- **Compatibilidad**: Uso de contenedores y tecnologías multiplataforma.

## 4. Visión General del Sistema

### 4.1. Descripción de Alto Nivel
La arquitectura general incluye los siguientes módulos:

- **Captura de imágenes (Productor Kafka)**: Captura frames y los publica en un topic.
- **Apache Kafka + Zookeeper**: Middleware para transporte y gestión de eventos.
- **Detector de imágenes (Consumidor Kafka)**: Recibe los frames desde el topic, realiza análisis visual (detección de objetos, poses, etc.) con MediaPipe u OpenCV.
- **API de control (Flask)**: Permite gestionar parámetros de operación y exponer resultados.
- **Interfaz visual o consola de monitoreo**: (opcional) para visualizar los resultados de detección y estado del sistema.

# 5. Estrategias Arquitectónicas
## 5.1. Estrategias Clave
Describir las estrategias arquitectónicas clave y cómo abordan las preocupaciones específicas de las partes interesadas.


# 6. Arquitectura del Sistema

## 6.1. Resumen de Capas/Módulos

El sistema se organiza en **capas modulares** que separan claramente la configuración, la lógica de detección, el servidor de streaming en tiempo real, la interfaz cliente y el mecanismo de arranque. Esta separación favorece la mantenibilidad, escalabilidad y facilidad de pruebas.

### Configuración (`config.py`)
- Utiliza una `dataclass` para definir parámetros globales de configuración.
- Incluye configuraciones para:
  - Conexión a Kafka (bootstrap servers, topics).
  - Dispositivo de captura (cámara).
  - Modelo de detección Caffe.
  - Umbral de confianza para detecciones.

###  Módulo de Detección (`detection/`)
- **`strategy.py`**: Define la interfaz `BaseDetector` y la enumeración `DetectionStrategyType`.
- **`detector.py`**: Implementación `CaffeDetector` que realiza:
  - Carga de redes MobileNetSSD con OpenCV.
  - Preprocesamiento (`blobFromImage`), inferencia y filtrado.
  - Postprocesamiento: desenfoque selectivo, bounding boxes y etiquetas.
- **`factory.py`**: `DetectorFactory` que permite inyectar dinámicamente estrategias de detección.
- **`pipeline.py`**: `DetectionPipeline` combina detección cada N frames con tracking CSRT para mejorar rendimiento.

###  Servidor de Streaming Web (`server/`)
- **`app.py`**:
  - `eventlet` para I/O asincrónico.
  - `Flask` + `Flask-SocketIO` (`async_mode='eventlet'`).
  - `ThreadPoolExecutor` para detección paralela.
  - Captura continua con OpenCV y emisión de frames por WebSocket.

### Cliente Web
- **HTML** (`templates/index.html`): Interfaz simple y funcional.
- **JavaScript** (`static/js/app.js`): WebSocket, cálculo de latencia y renderización.
- **CSS** (`static/css/style.css`): Estilos responsive y legibles.

### Arranque del sistema (`main.py`)
- Importa `app` y ejecuta `socketio.run()` para iniciar con `eventlet`.

### Dependencias (`requirements.txt`)
- `flask`, `flask-socketio`, `eventlet`, `kafka-python`
- `opencv-python`, `numpy`, `prometheus-client` (opcional)

### Tecnologías y Herramientas

| Tecnología / Herramienta     | Descripción                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| **Python 3.10+**             | Lenguaje principal del sistema.                                             |
| **OpenCV**                   | Captura de video, procesamiento de imágenes, modelo Caffe, tracking CSRT. |
| **Caffe + MobileNetSSD**     | Modelo preentrenado para detección de objetos.                             |
| **Apache Kafka**             | Middleware de colas para desacoplar captura y procesamiento.              |
| **Flask + Flask-SocketIO**   | Framework web y WebSockets para streaming.                                 |
| **Eventlet**                 | Permite I/O asincrónico con bajo consumo.                                 |
| **ThreadPoolExecutor**       | Ejecuta tareas de detección en paralelo.                                  |
| **Prometheus Client**        | Exposición de métricas del sistema (opcional).                            |
| **Docker / Docker Compose**  | Contenerización y orquestación de servicios.                              |


## 6.2 Diagramas de Componentes
### Diagrama de Contexto
<img src="../diagrama componentes 1.jpeg" alt="Diagrama1" />

### Diagrama de componentes
<img src="../diagrama componentes 2.jpeg" alt="Diagrama1" />

## 6.3 Diseño de la Base de Datos
No cuenta con Base de datos


# 7. Decisiones Arquitectónicas Clave

## 7.1. Registro de Decisiones

### 7.1.1 Uso de Apache Kafka como middleware para captura y transmisión de frames

#### Pros
- Desacopla la lógica de captura de imágenes y su procesamiento.
- Permite escalar los consumidores sin afectar el productor.
- Soporta almacenamiento temporal de eventos y recuperación ante fallos.

#### Contras
- Aumenta la complejidad del sistema (requiere Zookeeper).
- Necesita administración del clúster Kafka.

#### Alternativas
- Comunicación directa (Python `Queue`), menos escalable.
- RabbitMQ o ZeroMQ como alternativas más ligeras.

#### Problemas Potenciales
- Latencia de arranque y sincronización de offset.
- Configuración incorrecta de persistencia de topics.

#### Dependencias
- kafka-python, zookeeper, configuración del broker y topics.

### 7.1.2 Uso de modelo Caffe + MobileNetSSD para detección

#### Pros
- Ligero, rápido y bien soportado por OpenCV.
- Ideal para CPU sin necesidad de GPU.

#### Contras
- Precisión limitada.
- Difícil de entrenar o personalizar por usuarios.

#### Alternativas
- YOLOv5, TensorFlow Lite + Coral.

#### Problemas Potenciales
- Bajo rendimiento en condiciones complejas.
- Obsolescencia del modelo Caffe.

#### Dependencias
- opencv-python, prototxt, `.caffemodel`.

# 8. Atributos de Calidad

Esta sección describe dos atributos clave de calidad del sistema: **Rendimiento** y **Escalabilidad**, incluyendo cómo la arquitectura propuesta los aborda.

## 8.1. Rendimiento

### Requisitos de Rendimiento

- Procesar y transmitir imágenes en tiempo real con una **latencia total menor a 100 ms**.
- Mantener una frecuencia de procesamiento de al menos **15 FPS** en dispositivos con CPU.
- Garantizar una experiencia sin interrupciones perceptibles para el usuario final.

### Apoyo desde la Arquitectura

- **Procesamiento asincrónico y paralelo** con `ThreadPoolExecutor`.
- **Desacoplamiento mediante Apache Kafka**, permitiendo buffering y procesamiento independiente.
- **Uso de tracking CSRT** para reducir carga de procesamiento por inferencia.
- **Transmisión con WebSockets** para menor sobrecarga frente a HTTP tradicional.

## 8.2. Escalabilidad

### Consideraciones de Escalabilidad

- Escalar a múltiples cámaras o fuentes de video.
- Soportar múltiples usuarios accediendo simultáneamente.
- Posibilidad de despliegue distribuido en varios nodos o servicios.

### Estrategias de Escalabilidad en la Arquitectura

- **Kafka como middleware escalable**, permite múltiples consumidores.
- **Contenerización con Docker** para replicar componentes fácilmente.
- **Separación de responsabilidades** en captura, procesamiento y transmisión.
- **Broadcast de WebSocket** que puede escalar con Redis como backend para múltiples clientes.


## 8.3. Seguridad
No se desarrollo seguridad para presente implementación ya que representa un módelo de prueba e investigativo.
## 8.4. Mantenibilidad
Describir cómo se ha diseñado el sistema para facilitar su mantenimiento.

# 9. Riesgos y Deuda Técnica 
## 9.1. Riesgos Identificados
Enumerar los riesgos identificados y su posible impacto en el proyecto.

## 9.2. Deuda Técnica
Como deuda técnica se identifican los siguientes desarrollos para la aplicación:
- **Módulo de seguridad**: implementación de seguridad y autenticación para los streming filtrados.
- **Exponer la API via REST**: implementación de la aplicación para ser expuesta para su uso por medio de internet, configurando para ello una API via REST. 

# 10. Apéndices 
##10.1. Glosario
Proporcionar un glosario de términos utilizados a lo largo del documento.

## 10.2. Índice
Incluir un índice de términos y secciones para facilitar la navegación.

# 10.3. Historial de Revisión
Documentar el historial de revisiones de este documento.

