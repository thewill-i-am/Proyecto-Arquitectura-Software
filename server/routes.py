from flask import Response, render_template

class VideoRoutes:
    @staticmethod
    def video_feed():
        return render_template('index.html')

    @staticmethod
    def video_stream(generator):
        return Response(
            generator,
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )