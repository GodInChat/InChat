from datetime import datetime
from pathlib import Path
import uuid

#Local save only for test purpose, in production use CDN.

def save_pdf(image_files, user) -> list:
    output = []
    for file in image_files:
        pdf_uuid = uuid.uuid4()
        path = Path(f"user-pdf/user-{user.id}/pdf-{pdf_uuid}.pdf")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        with open(path, "wb") as image:
            image.write(file.file.read())
        output.append({'id': pdf_uuid, 'pdf_url': str(path),'pdf_name': file, 'created_at': datetime.now()})
    return output