import uuid
import os
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Response, status, Request
from my_privacy_cloak.background_tasks.process_image import convert_image_gui_style
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

IMAGES_FOLDER = "images_folder"

templates = Jinja2Templates(directory="templates/")

app = FastAPI()

os.chdir("..")
current_path = os.getcwd()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload_image/")
def create_upload_file(background_tasks: BackgroundTasks, image: UploadFile = File(...)):
    extension = image.filename.split(".")[1]
    extension_str = f".{extension}"

    operation_id = str(uuid.uuid4())
    image_name = operation_id + extension_str
    
 
    image_folder = os.path.join(current_path,IMAGES_FOLDER, operation_id)
    os.makedirs(image_folder)
    image_path = os.path.join(current_path,IMAGES_FOLDER, operation_id, image_name)

    with open(image_path,'wb+') as f:
        f.write(image.file.read())
        f.close()


    background_tasks.add_task(convert_image_gui_style, image_folder)

    return {"filename": image.filename,
     "image_name": image_name,
      "file_path": image_path,
      "id": operation_id
    }

@app.get("/get_cloaked_image/{image_uuid}")
def get_cloked_image(image_uuid:str, response: Response):
    folder_path = os.path.join(current_path,IMAGES_FOLDER, image_uuid)
    if os.path.exists(folder_path):
        image_path = os.path.join(current_path,IMAGES_FOLDER, image_uuid, image_uuid + "_cloaked" + ".jpeg")
        if os.path.exists(image_path):
            FileResponse(image_path)
        else:
            response.status_code = status.HTTP_202_ACCEPTED
            return {"status": "running",
                   "message": "conversion in progress"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status":"error",
                "message": "operation does not exist"}