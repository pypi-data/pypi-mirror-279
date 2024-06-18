from setuptools import setup, Extension

def main():
    setup(ext_modules=[Extension(
      'dxlparser',
      [ 'src/dxlparser.c', 'src/calc.c', 'src/cadena.c', 'src/stack.c' ],
      #include_dirs=['.'],
    )])

if __name__ == "__main__":
    main()
