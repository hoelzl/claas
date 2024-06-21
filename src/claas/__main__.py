import xml.etree.ElementTree as ET
from pathlib import Path

import click

from claas.html_converter import HtmlConverter
from claas.markdown_converter import MarkdownConverter
from claas.word_converter import WordConverter
from claas.table_word_converter import TableWordConverter


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
def generate_outputs(input_file, output_formats, output_dir):
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
            print(f"Word document saved to {output_path}")


if __name__ == "__main__":
    generate_outputs()
