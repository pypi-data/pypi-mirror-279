import os, ctypes
_current_dir = os.path.abspath(os.path.dirname(__file__))
_dll_dir = os.path.join(_current_dir, "lib")
os.add_dll_directory(_dll_dir)
os.environ['PATH'] = _dll_dir + ';' + os.environ['PATH']

et_dll = ctypes.CDLL(os.path.join(_dll_dir, 'DeepGazeET.dll'), winmode=0)
print(et_dll.deep_gaze_init())
