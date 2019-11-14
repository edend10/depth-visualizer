import sys
import os
import subprocess as pipe

input_dir = sys.argv[1] if len(sys.argv) > 1 else 'test_input'
output_dir = sys.argv[2] if len(sys.argv) > 2 else 'test_output'
bg_threshold = sys.argv[3] if len(sys.argv) > 3 else -1
gif_length = sys.argv[4] if len(sys.argv) > 4 else 100

script_name = 'depth_to_3d.py'

def update_argv_for_script(script_name, depth_image_filename, gif_output_filename, bg_threshold=-1, img_dim=256, gif_length=100, point_size=2.0):
    sys.argv = [script_name]
    for cmd_arg in [gif_length, img_dim, img_dim, point_size, bg_threshold, depth_image_filename, gif_output_filename]:
        sys.argv.append(cmd_arg)
    pipe.Popen(["python"] + [str(x) for x in sys.argv]).communicate()


for filename in os.listdir(input_dir):
    print(filename)
    input_file_path = '{}/{}'.format(input_dir, filename)
    filename_no_ext = filename.split('.')[0]
    output_file_path = '{}/{}.gif'.format(output_dir, filename_no_ext)
    update_argv_for_script(script_name, input_file_path, output_file_path, bg_threshold=bg_threshold, gif_length=gif_length)
    #exec(open(script_name).read()) # this cannot be in a method as it changes the namespace and then imports aren't recognized in called script
    #pipe.Popen(["python]

