import os
import re
from io import StringIO

import click
import requests


def read_xml_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        return f.read()


title_re = re.compile(r"<titel>.*?</titel>", re.DOTALL)
module_re = re.compile(r"<modul>.*?</modul>", re.DOTALL)
xml_re = re.compile(r"<.*>", re.DOTALL)


def split_into_modules(root: str):
    modules = re.findall(module_re, root)
    return modules


def convert_module(summary_xml, detail_xml):

    prompt = f"""
    Convert the following two XML snippets into a single XML snippet in the new format.
    The new format should combine the summary and detailed information as follows:

    - Each 'thema' in the summary should become a 'themengruppe'
    - The content of each summary 'thema' should become the 'zusammenfassung' in the new format
    - The corresponding detailed 'thema' elements should be nested under 'detailthemen'
    - 'dauer', 'methodik', and 'material' should only be included in the detailed information
    - 'woche' and 'abschnitt' elements should remain at the same level as 'themengruppe'

    Summary XML:
    {summary_xml}

    Detailed XML:
    {detail_xml}

    Please provide the converted XML snippet in the new format. Output only the new XML
    snippet.
    """

    # Get API key from environment variable
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")

    # Make API call to OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    if response.status_code == 200:
        full_response = response.json()["choices"][0]["message"]["content"]

        # Extract only the XML part
        xml_match = xml_re.search(full_response)

        if xml_match:
            # Join all matches and wrap them in a root element if necessary
            extracted_xml = xml_match.group(0)

            # If the extracted XML doesn't start with '<modul>', wrap it
            if not extracted_xml.startswith("<modul"):
                extracted_xml = f"<modul>{extracted_xml}</modul>"

            return extracted_xml
        else:
            raise ValueError("No XML content found in the response")
    else:
        raise Exception(
            f"API call failed with status code {response.status_code}: {response.text}"
        )


KURS_HEADER = """\
<kurs xmlns="http://xsd.coding-academy.com/claas/azav-kurs"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://xsd.coding-academy.com/claas/azav-kurs https://raw.githubusercontent.com/hoelzl/claas/master/src/claas/azav-kurs.xsd">
"""


@click.command()
@click.option(
    "--summary",
    required=True,
    type=click.Path(exists=True),
    help="Path to the summary XML file",
)
@click.option(
    "--detail",
    required=True,
    type=click.Path(exists=True),
    help="Path to the detail XML file",
)
@click.option(
    "--output", required=True, type=click.Path(), help="Path for the output XML file"
)
def main(summary, detail, output):
    try:
        summary_root = read_xml_file(summary)
        detail_root = read_xml_file(detail)

        summary_modules = split_into_modules(summary_root)
        detail_modules = split_into_modules(detail_root)

        new_root = StringIO()
        new_root.write(KURS_HEADER)

        # Copy the course title
        title_match = re.search(title_re, summary_root)
        title = title_match.group(0) if title_match else ""
        new_root.write(f"{title}\n")

        for summary_module, detail_module in zip(summary_modules, detail_modules):
            try:
                converted_xml = convert_module(summary_module, detail_module)
                print(f"{'=' * 72}\nConverted module: {converted_xml}\n\n")
                new_root.write(converted_xml)
            except Exception as e:
                click.echo(f"Error converting module: {str(e)}", err=True)
                continue  # Skip this module and continue with the next one

        new_root.write("</kurs>\n")
        with open(output, "w") as f:
            f.write(new_root.getvalue())
        click.echo(f"Converted curriculum saved to {output}")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)


if __name__ == "__main__":
    main()
