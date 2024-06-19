from distutils.command.build import build
from subprocess import check_call

import setuptools


def generate_proto_code():
    # python -m grpc_tools.protoc -I ..\..\kes\protobuf\ --python_out=. --grpc_python_out=. --mypy_out=. --mypy_grpc_out=. table.proto project.proto
    proto_interface_dir = "../kes/protobuf"
    files = ["table.proto", "project.proto"]
    out_folder = "./src/kes/proto/"

    check_call(
        ["python"] +
        ["-m", "grpc_tools.protoc"] +
        ["-I", proto_interface_dir] +
        ["--python_out=" + out_folder] +
        ["--grpc_python_out=" + out_folder] +
        ["--mypy_out=" + out_folder] +
        ["--mypy_grpc_out=" + out_folder] +
        files
    )


class CustomBuildCommand(build):
    def run(self):
        generate_proto_code()
        build.run(self)


setuptools.setup(
    # cmdclass={
    #     'build': CustomBuildCommand,
    # }  # type: ignore
    package_data={"kes": ["py.typed"]}
)
