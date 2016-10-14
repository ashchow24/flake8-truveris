from flake8.formatting import base

from flake8_truveris import (
    trailing_commas,
)

error_modules = {
    "T812": trailing_commas,
}


class FormatTruveris(base.BaseFormatter):

    error_format = "%(path)s:%(row)d:%(col)d: %(code)s %(text)s"

    def format(self, error):
        return self.error_format % {
            "code": error.code,
            "text": error.text,
            "path": error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }

    def handle(self, error):
        line = self.format(error)
        source = self.show_source(error)
        self.write(line, source)

        if error.code[0] == "T" and error.code[1:].isdigit():
            # error was generated by flake8-truveris
            with open(error.filename, 'r') as file:
                # read a list of lines into data
                data = file.readlines()

            data = error_modules[error.code].fix(data, error)

            with open(error.filename, 'w') as file:
                file.writelines(data)
