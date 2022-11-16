from pathlib import Path
import hashlib

from podder_task_foundation import Context, Payload
from podder_task_foundation import Process as ProcessBase
from pdfminer.high_level import extract_text


class Process(ProcessBase):
    def initialize(self, context: Context) -> None:
        pass

    def execute(self, input_payload: Payload, output_payload: Payload,
                context: Context):
        pdf = input_payload.get(name="file", object_type="pdf")

        hash = hashlib.md5()
        with open(pdf.path, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                hash.update(block)

        text = extract_text(pdf.path)

        output = {"pdf_name": pdf.path.name, 'md5hash': hash.hexdigest(), 'text': text}
        output_payload.add_dictionary(output, name="output")
