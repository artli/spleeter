import io
import os
import subprocess
import tarfile
import tempfile

from flask import abort, Flask, request, send_file


MIME_TO_EXTENSION = {
    'audio/wav': 'wav',
    'audio/wave': 'wav',
    'audio/mpeg': 'mp3',
}


app = Flask(__name__)


@app.route('/split', methods=('POST',))
def split():
    mime_type = request.headers.get('Content-Type')
    if mime_type not in MIME_TO_EXTENSION:
        abort(400)
    extension = MIME_TO_EXTENSION[mime_type]
    audio = request.get_data()

    with tempfile.TemporaryDirectory() as tempdir:
        source_path = os.path.join(tempdir, f'source.{extension}')
        result_dir_path = os.path.join(tempdir, 'result')
        result_path = os.path.join(tempdir, 'result.tar')
        with open(source_path, 'wb') as source:
            source.write(audio)

        process = subprocess.run(f'spleeter separate -i {source_path} -p spleeter:4stems -c mp3 -o {result_dir_path}')
        if process.returncode != 0:
            abort(500)

        with tarfile.open(result_path, 'w') as result:
            to_add = os.path.join(result_dir_path, 'source')
            for filename in os.listdir(to_add):
                result.add(os.path.join(to_add, filename), arcname=filename)
        result.close()

        with open(result_path, 'rb') as result_file:
            result_data = result_file.read()

    return send_file(io.BytesIO(result_data), mimetype='application/x-tar')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
