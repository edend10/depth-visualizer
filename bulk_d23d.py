import sys
import os
import subprocess as pipe

input_dir = sys.argv[1] if len(sys.argv) > 1 else 'test_input'
output_dir = sys.argv[2] if len(sys.argv) > 2 else 'test_output'
bg_threshold = int(sys.argv[3]) if len(sys.argv) > 3 else -2 # -1 is get np.max, -2 is 150 for fake and -1 for real
gif_length = int(sys.argv[4]) if len(sys.argv) > 4 else 100
point_size = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0

script_name = 'depth_to_3d.py'

def update_argv_for_script(script_name, depth_image_filename, gif_output_filename, bg_threshold=-2, img_dim=256, gif_length=100, point_size=2.0):
    sys.argv = [script_name]
    if bg_threshold == -2:
        if 'fake_B' in depth_image_filename:
            bg_threshold = 150
        elif 'real_B' in depth_image_filename:
            bg_threshold = -1
        else:
            return
    for cmd_arg in [gif_length, img_dim, img_dim, point_size, bg_threshold, depth_image_filename, gif_output_filename]:
        sys.argv.append(cmd_arg)

    pipe.Popen(["python"] + [str(x) for x in sys.argv]).communicate()

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    input_file_path = '{}/{}'.format(input_dir, filename)
    filename_no_ext = filename.split('.')[0]
    output_file_path = '{}/{}.gif'.format(output_dir, filename_no_ext)
    update_argv_for_script(script_name, input_file_path, output_file_path, bg_threshold=bg_threshold, gif_length=gif_length, point_size=point_size)

