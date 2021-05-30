from fawkes import protection
import glob
import os


def directory_to_paths(directory):
    image_paths = glob.glob(os.path.join(directory, "*"))
    image_paths = [path for path in image_paths if "_cloaked" not in path.split("/")[-1]]
    
    return image_paths

def convert_image_strange(
                 image_path,
                 feature_extractor="arcface_extractor_0",
                 gpu="0", 
                 batch_size=1, 
                 mode="low",
                 th=0.01,
                 sd=1e6,
                 lr=2,
                 max_step=1000,
                 format="jpg",
                 separate_target="store_true",
                 debug="store_true",
                 no_align="store_true"):
    protector = protection.Fawkes(feature_extractor, gpu, batch_size, mode=mode)
    protector.run_protection(image_path, th=th, sd=sd, lr=lr,
                             max_step=max_step,
                             batch_size=batch_size, format=format,
                             separate_target=separate_target, debug=debug, no_align=no_align)


def convert_image_gui_style(directory):
    image_paths = directory_to_paths(directory)
    my_fawkes = protection.Fawkes("extractor_2", '0', 1)
    status = my_fawkes.run_protection(image_paths, format="jpeg", debug=True)


def test_local(directory="/home/andreea/robert/my_privacy_cloack/images_folder"):

    image_paths = directory_to_paths(directory)

    my_fawkes = protection.Fawkes("extractor_2", '0', 1)
    status = my_fawkes.run_protection(image_paths)
    print(status)


if __name__ == "__main__":
    test_local()