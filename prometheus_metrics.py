from prometheus_client import start_http_server, Gauge, Counter

# Métricas
FRAME_LATENCY = Gauge('frame_latency_ms', 'Latency of processed frames in milliseconds')
BUFFER_SIZE = Gauge('buffer_size', 'Current size of the frame buffer')
PROCESSED_FRAMES = Counter('processed_frames_total', 'Total number of processed frames')
AVG_LATENCY = Gauge('avg_frame_latency_ms', 'Average latency of processed frames in milliseconds')
CAPTURE_FPS = Gauge('capture_fps', 'Average frames per second in capture loop')

# Inicia servidor HTTP para métricas
start_http_server(8000)