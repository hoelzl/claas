import time
import xml.etree.ElementTree as ET
from pathlib import Path

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from claas.html_converter import HtmlConverter
from claas.markdown_converter import MarkdownConverter
from claas.table_html_converter import TableHtmlConverter
from claas.table_word_converter import TableWordConverter
from claas.word_converter import WordConverter


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, input_file, output_formats, output_dir, skip_time, kinds):
        self.input_file = input_file
        self.output_formats = output_formats
        self.output_dir = output_dir
        self.skip_time = skip_time
        self.kinds = kinds

    def on_modified(self, event):
        if event.src_path == str(self.input_file):
            print(f"Detected change in {self.input_file}. Converting...")
            main_generate_outputs(
                self.input_file,
                self.output_formats,
                self.output_dir,
                self.skip_time,
                self.kinds,
            )


converters = {
    "markdown": (MarkdownConverter, ".md", "Markdown file"),
    "html": (HtmlConverter, ".html", "HTML file"),
    "word": (WordConverter, ".docx", "Word document"),
    "html-table": (TableHtmlConverter, ".tab.html", "HTML tables"),
    "word-table": (TableWordConverter, ".tab.docx", "Word tables"),
}


def main_generate_outputs(input_file, output_formats, output_dir, skip_time, kinds):
    try:
        input_path = Path(input_file)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        input_tree = ET.parse(input_path)
        if "all" in output_formats:
            output_formats = list(converters.keys())
        if "both" in kinds:
            kinds = ["summary", "detailed"]

        for fmt in output_formats:
            for kind in kinds:
                detailed = kind == "detailed"
                converter_class, suffix, doc_name = converters[fmt]
                converter = converter_class(
                    input_tree, include_time=not skip_time, detailed=detailed
                )
                output_path = (
                    output_dir / f"{input_path.stem}"
                    f"{'_detailed' if detailed else '_summary'}{suffix}"
                )
                converter.save(output_path)
                print(f"{doc_name} saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output-formats",
    "-o",
    multiple=True,
    type=click.Choice(["markdown", "html", "word", "html-table", "word-table", "all"]),
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
@click.option(
    "--skip-time",
    "-t",
    is_flag=False,
    help="Do not include time information in the output",
)
@click.option(
    "--kinds",
    "-k",
    multiple=True,
    type=click.Choice(["summary", "detailed", "both"]),
    default=["both"],
    help="Kind of data to include in the output",
)
def generate_outputs(input_file, output_formats, output_dir, watch, skip_time, kinds):
    main_generate_outputs(input_file, output_formats, output_dir, skip_time, kinds)

    if watch:
        event_handler = FileChangeHandler(
            input_file, output_formats, output_dir, skip_time, kinds
        )
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
