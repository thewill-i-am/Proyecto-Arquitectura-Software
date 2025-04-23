
# Requerimientos del Producto - Aplicación de Video Streaming con Procesamiento y Censura en Tiempo Real

---

## 1. Requerimientos del negocio

1. **Proveer análisis visual automatizado en tiempo real**
El sistema debe permitir detectar y analizar objetos, personas o gestos en tiempo real desde una fuente de video, con el fin de automatizar procesos de monitoreo, vigilancia, interacción o análisis visual.
2. **Soportar despliegues multiplataforma**: El sistema debe ser portable y ejecutarse en diferentes entornos operativos (Linux, Windows, MacOS), tanto en entornos locales como en la nube o contenedores, para adaptarse a diversos escenarios de uso.
3. **Garantizar transmisión continua y estable de video**: El sistema debe transmitir imágenes procesadas en tiempo real sin interrupciones perceptibles para el usuario final, asegurando una experiencia fluida y continua.
4. **Permitir visualización y consulta de métricas de procesamiento**: El sistema debe registrar y exponer indicadores clave como FPS (frames por segundo), número de objetos detectados y latencia de procesamiento, permitiendo su análisis y ajuste operativo.
5. **Asegurar protección de acceso y privacidad de la información**: El sistema debe implementar mecanismos de seguridad como autenticación, autorización y control de accesos para prevenir el uso indebido del servicio o la exposición de datos sensibles.
6. **Escalar horizontalmente bajo demanda**: El sistema debe ser capaz de escalar mediante la adición de nuevas instancias de procesamiento (consumidores Kafka) para soportar aumentos de carga sin degradar el rendimiento.
7. **Servir como base para pruebas, demostraciones y proyectos de investigación**: El sistema debe estar diseñado de forma modular y extensible para facilitar su adaptación en ambientes educativos, experimentales o de investigación aplicada.

---

## 2. Requerimientos funcionales

### A. Captura y procesamiento de video

- **Historia de Usuario 1:**  
  *Como operador, deseo que el sistema capture video en tiempo real desde una cámara, para poder analizar el contenido en vivo.*  
  **Funcionalidad:**  
  - Acceso a la cámara (dispositivo de captura) y captura continua de frames.

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
  *Como sistema, los frames procesados deben ser enviados a través de Kafka para asegurar una comunicación asíncrona y escalable entre componentes.*  
  **Funcionalidad:**  
  - Implementar un productor de Kafka que envíe frames codificados en formato JPEG al tópico adecuado (p.ej., `video-frames`).

- **Historia de Usuario 5:**  
  *Como sistema, debo contar con un consumidor que reciba los frames procesados y los retransmita a la interfaz web para su visualización en tiempo real.*  
  **Funcionalidad:**  
  - Implementar un consumidor de Kafka que lea continuamente los mensajes del tópico y los formatee para el streaming en la web.  
  - Gestionar el flujo de datos para evitar cuellos de botella en la transmisión.

### C. Visualización en interfaz web

- **Historia de Usuario 6:**  
  *Como usuario final, quiero acceder a una página web sencilla que muestre el video en vivo, con la detección de objetos y la censura aplicada en las botellas.*  
  **Funcionalidad:**  
  - Desarrollo de una interfaz web (HTML, CSS y JavaScript básico) que se conecte a la ruta de video.  
  - Implementar una ruta (p. ej., `/video`) que devuelva el video en formato multipart compatible con navegadores.

- **Historia de Usuario 7:**  
  *Como sistema, debo asegurar que la página web se actualice en tiempo real mostrando el video procesado sin interrupciones perceptibles para el usuario.*  
  **Funcionalidad:**  
  - Garantizar un formato de respuesta adecuado (multipart/x-mixed-replace) para la transmisión continua de imágenes.  

### D. Modularidad y separación de responsabilidades (Principio SRP)

- **Requerimiento:**  
  Cada componente debe tener una única responsabilidad:
  - **Captura y procesamiento:** Responsable de adquirir el video y aplicar la detección de objetos.  
  - **Comunicación con Kafka:** Un módulo específico para el envío y recepción de datos.  
  - **Interfaz web:** Encargado de la presentación y visualización del stream.  
  - **Detección de objetos:** Un servicio independiente que se encargue de procesar, etiquetar y censurar (aplicar desenfoque) cada frame.

---


## 3. Requerimientos No-funcionales o de calidad
Este apartado presenta los requerimientos no funcionales utilizando la estructura de escenarios de calidad propuesta por Bass, Clements y Kazman (2021):

| Atributo               | Fuente                             | Estímulo                                                                | Entorno                                        | Artefacto                                                   | Respuesta                                                                 | Métrica                                                                                   |
|------------------------|------------------------------------|-------------------------------------------------------------------------|------------------------------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Escalabilidad**      | Aumento de usuarios concurrentes   | Peticiones simultáneas de procesamiento de imágenes                    | Durante picos de transmisión en vivo           | Backend de procesamiento y servidor de streaming             | Escala automáticamente los recursos de cómputo                          | Mantener <70% de uso de CPU y latencia <100 ms            |
| **Compatibilidad**     | Usuario o desarrollador             | Ejecución en Windows, Linux o MacOS                                     | En fase de despliegue                          | Código fuente y entorno de ejecución                         | El sistema se ejecuta sin modificación del código                       | Funcionalidad completa en el 100% de entornos soportados con error ≤ 5%                   |
| **Rendimiento**        | Usuario final                       | Solicita visualización y procesamiento en tiempo real                   | Durante operación continua                     | Captura, procesamiento y transmisión de imágenes             | Procesamiento completo y transmisión con baja latencia                  | Tiempo total de respuesta <100 ms en el 95% de los casos                                 |


