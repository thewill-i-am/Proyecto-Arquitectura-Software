
# Requerimientos del Producto - Aplicación de Video Streaming con Procesamiento y Censura en Tiempo Real

---

## 1. Requerimientos del negocio

- **Objetivo del negocio:**  
  Proveer una solución de video streaming en tiempo real que permita la captura, procesamiento y visualización de video, con capacidades avanzadas de detección de objetos y su censura en tiempo real. Esto es útil para aplicaciones en vigilancia, control de contenido, análisis de tráfico o entornos donde se requiera censurar ciertos elementos sensibles.

- **Valor agregado:**  
  La integración de tecnologías como Kafka, OpenCV y Flask permite un procesamiento distribuido y escalable, reduciendo la latencia en la transmisión y habilitando la toma de decisiones en tiempo real sobre el contenido del video, especialmente en lo relacionado con la censura de objetos.

- **Ventaja competitiva:**  
  El sistema destaca por su capacidad de detectar y censurar de forma inmediata regiones específicas de interés (como aplicar desenfoque a botellas) y su arquitectura modular, lo que facilita la integración con otros sistemas y la escalabilidad ante incrementos en la demanda.

- **Impacto en el negocio:**  
  Con este producto se optimiza la gestión del video en vivo, se mejora el control del contenido (mediante la censura de objetos sensibles) y se posibilita la implementación de soluciones de análisis avanzado, generando oportunidades en diversos sectores industriales y comerciales.

---

## 2. Requerimientos funcionales

### A. Captura y procesamiento de video

- **Historia de Usuario 1:**  
  *Como operador, deseo que el sistema capture video en tiempo real desde una cámara, para poder analizar el contenido en vivo.*  
  **Funcionalidad:**  
  - Acceso a la cámara (dispositivo de captura) y captura continua de frames.  
  - Gestión de posibles fallas en la captura (por ejemplo, reconexión en caso de error).

- **Historia de Usuario 2:**  
  *Como sistema, debo procesar cada frame utilizando una red neuronal preentrenada (MobileNetSSD) para detectar objetos en la imagen.*  
  **Funcionalidad:**  
  - Carga del modelo (archivos `.caffemodel` y `.prototxt.txt`) para la detección.  
  - Preprocesamiento de frames y aplicación del modelo para obtener detecciones con sus niveles de confianza.  
  - Implementación del principio SRP: un módulo exclusivo para la detección de objetos.

- **Historia de Usuario 3:**  
  *Como usuario, deseo que se identifiquen y etiqueten los objetos detectados en el video, aplicando un desenfoque específico a las botellas para censurar este contenido en tiempo real.*  
  **Funcionalidad:**  
  - Dibujo de rectángulos y etiquetas (nombre del objeto y porcentaje de confianza) sobre los objetos detectados.  
  - Identificación de la clase "botella" y aplicación de un filtro de desenfoque (usando técnicas como GaussianBlur) en la región correspondiente para censurar el contenido.

### B. Transmisión y comunicación mediante Kafka

- **Historia de Usuario 4:**  
  *Como desarrollador, necesito que el sistema envíe los frames procesados a través de Kafka para asegurar una comunicación asíncrona y escalable entre componentes.*  
  **Funcionalidad:**  
  - Implementar un productor de Kafka que envíe frames codificados en formato JPEG al tópico adecuado (p.ej., `video-frames`).  
  - Asegurar que la transmisión es robusta y tolerante a fallos en la red.

- **Historia de Usuario 5:**  
  *Como sistema, debo contar con un consumidor que reciba los frames enviados y los retransmita a la interfaz web para su visualización en tiempo real.*  
  **Funcionalidad:**  
  - Implementar un consumidor de Kafka que lea continuamente los mensajes del tópico y los formatee para el streaming en la web.  
  - Gestionar el flujo de datos para evitar cuellos de botella en la transmisión.

### C. Visualización en interfaz web

- **Historia de Usuario 6:**  
  *Como usuario final, quiero acceder a una página web sencilla que muestre el video en vivo, con la detección de objetos y la censura aplicada en las botellas.*  
  **Funcionalidad:**  
  - Desarrollo de una interfaz web (HTML, CSS y JavaScript básico) que se conecte a la ruta de video.  
  - Implementar una ruta (p. ej., `/video`) en el servidor Flask que devuelva el stream de video en formato multipart compatible con navegadores.

- **Historia de Usuario 7:**  
  *Como sistema, debo asegurar que la página web se actualice en tiempo real mostrando el video procesado sin interrupciones perceptibles para el usuario.*  
  **Funcionalidad:**  
  - Garantizar un formato de respuesta adecuado (multipart/x-mixed-replace) para la transmisión continua de imágenes.  
  - Manejar la reconexión o actualizaciones en el caso de fallos temporales en la transmisión.

### D. Modularidad y separación de responsabilidades (Principio SRP)

- **Requerimiento:**  
  Cada componente debe tener una única responsabilidad:
  - **Captura y procesamiento:** Responsable de adquirir el video y aplicar la detección de objetos.  
  - **Comunicación con Kafka:** Un módulo específico para el envío y recepción de datos.  
  - **Interfaz web:** Encargado de la presentación y visualización del stream.  
  - **Detección de objetos:** Un servicio independiente que se encargue de procesar, etiquetar y censurar (aplicar desenfoque) cada frame.

---

## 3. Requerimientos No-funcionales o de calidad

- **Rendimiento y latencia:**  
  - El sistema debe procesar y transmitir los frames en tiempo real, minimizando la latencia entre captura, procesamiento y visualización.  
  - Se debe establecer un límite máximo de tiempo para el procesamiento de cada frame (por ejemplo, menos de 50-100 milisegundos, a definir según pruebas de rendimiento).

- **Escalabilidad:**  
  - La arquitectura basada en Kafka permite escalar horizontalmente tanto el productor como el consumidor para manejar incrementos en la carga.  
  - El diseño modular debe facilitar la incorporación de nuevos algoritmos de procesamiento o la integración con otros sistemas.

- **Confiabilidad y disponibilidad:**  
  - El sistema debe ser tolerante a fallos, con mecanismos de reconexión automática en caso de pérdida de conexión con la cámara o el servidor Kafka.  
  - Se deben implementar logs y alertas para detectar y resolver incidentes rápidamente.

- **Seguridad:**  
  - Asegurar la comunicación entre componentes (por ejemplo, utilizando conexiones seguras o autenticación en Kafka y Flask).  
  - Restringir el acceso a la interfaz web mediante autenticación si es necesario, especialmente en entornos sensibles.

- **Mantenibilidad y modularidad:**  
  - El código debe estar bien documentado y estructurado, siguiendo estándares de programación y buenas prácticas.  
  - Utilización de pruebas unitarias y de integración para cada módulo (captura, procesamiento, comunicación y visualización).

- **Compatibilidad y portabilidad:**  
  - La solución debe ser compatible con diferentes sistemas operativos y navegadores modernos.  
  - La integración con tecnologías de terceros (Kafka, OpenCV, Flask) debe permitir la actualización o sustitución de componentes sin afectar el funcionamiento general.

- **Usabilidad:**  
  - La interfaz de usuario debe ser intuitiva, con un diseño claro que permita una fácil interpretación del video y las detecciones realizadas.  
  - Proveer feedback visual en la interfaz en caso de errores o interrupciones en el servicio.

- **Monitorización y logging:**  
  - Implementar un sistema de monitorización que permita supervisar el rendimiento del streaming, la tasa de frames procesados y posibles errores en tiempo real.  
  - Registrar logs de actividad y de errores para facilitar la identificación y solución de incidencias.
