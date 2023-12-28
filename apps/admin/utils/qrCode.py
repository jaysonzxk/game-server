import qrcode
import os

from application import settings
from apps.admin.utils.string_util import uuid


def generate_qr_code(data):
    img = qrcode.make(data=data)
    filename = f'{uuid().hex[:10]}' + '.png'
    image_path = os.path.join('qrcode', filename)
    save_path = os.path.join(settings.MEDIA_ROOT, image_path)
    with open(save_path, 'wb') as f:
        img.save(f)
    return 'media/' + image_path


if __name__ == '__main__':
    res = generate_qr_code('sdaDdfdcdKJHGhhjbhh6566JJh')
    print(res)

