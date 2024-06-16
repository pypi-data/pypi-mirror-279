from setuptools import setup, find_packages

setup(
    name="deepgaze-python",
    version="1.0.9",
    author="DeepGaze",
    author_email="zhugc2016@gmail.com",
    description="DeepGaze Library",
    url="https://deep-gaze.com/sdk/python",
    packages=find_packages(),

    # # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        ('deepgaze-python/local_config', ['deepgaze-python/local_config/deep_config.json']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/DeepGazeET.dll']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/configR.mvcfg']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/configL.mvcfg']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/dp_camera_config.bin']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/dp_camera_tunning.bin']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/dp_config.json']),
        ('deepgaze-python/lib', ['deepgaze-python/lib/libfilter.dll']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/deep_gaze_favicon.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/windmill.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/beep.wav']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/frowning-face.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/smiling-face.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/dot.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_1.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_2.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_3.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_4.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_5.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_6.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_7.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_8.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_9.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/figure_0.png']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/calibration_instruction.wav']),
        ('deepgaze-python/asset', ['deepgaze-python/asset/adjust_position.wav']),
    ],

    install_requires=[
        'numpy', 'pygame', 'websockets'
    ],

)
