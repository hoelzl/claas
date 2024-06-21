import xml.etree.ElementTree as ET
from pathlib import Path
import time

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from claas.html_converter import HtmlConverter
from claas.markdown_converter import MarkdownConverter
from claas.word_converter import WordConverter
from claas.table_word_converter import TableWordConverter


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, input_file, output_formats, output_dir):
        self.input_file = input_file
        self.output_formats = output_formats
        self.output_dir = output_dir

    def on_modified(self, event):
        if event.src_path == str(self.input_file):
            print(f"Detected change in {self.input_file}. Converting...")
            main_generate_outputs(self.input_file, self.output_formats, self.output_dir)


def main_generate_outputs(input_file, output_formats, output_dir):
    input_path = Path(input_file)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_tree = ET.parse(input_path)
    if "all" in output_formats:
        output_formats = ["markdown", "html", "word", "table-word"]

    converters = {
        "markdown": MarkdownConverter,
        "html": HtmlConverter,
        "word": WordConverter,
        "table-word": TableWordConverter,
    }

    for fmt in output_formats:
        converter_class = converters[fmt]
        converter = converter_class(input_tree)
        output_content = converter.convert()

        if fmt == "markdown":
            output_path = output_dir / f"{input_path.stem}.md"
            with open(output_path, "w") as f:
                f.write(output_content)
            print(f"Markdown file saved to {output_path}")

        elif fmt == "html":
            output_path = output_dir / f"{input_path.stem}.html"
            with open(output_path, "w") as f:
                f.write(output_content)
            print(f"HTML file saved to {output_path}")

        elif fmt in ["word"]:
            output_path = output_dir / f"{input_path.stem}.docx"
            converter.save(output_path)
            print(f"Word document saved to {output_path}")

        elif fmt in ["table-word"]:
            output_path = output_dir / f"{input_path.stem}_tab.docx"
            converter.save(output_path)
            print(f"Word tables saved to {output_path}")


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output-formats",
    "-o",
    multiple=True,
    type=click.Choice(["markdown", "html", "word", "table-word", "all"]),
    default=["html"],
    help="Output formats to generate",
)
@click.option(
    "--output-dir", "-d", type=click.Path(), default=".", help="Output directory"
)
@click.option(
    "--watch",
    "-w",
    is_flag=True,
    help="Watch the file for changes and convert on modification",
)
def generate_outputs(input_file, output_formats, output_dir, watch):
    main_generate_outputs(input_file, output_formats, output_dir)

    if watch:
        event_handler = FileChangeHandler(input_file, output_formats, output_dir)
        observer = Observer()
        observer.schedule(
            event_handler, path=str(Path(input_file).parent), recursive=False
        )
        observer.start()
        print(f"Watching {input_file} for changes...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    generate_outputs()
