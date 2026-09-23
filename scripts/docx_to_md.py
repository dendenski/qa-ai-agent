import sys, zipfile, re, os
from xml.etree import ElementTree as ET

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def get_text(elem):
    return "".join(t.text or "" for t in elem.iter(f"{{{NS['w']}}}t"))

def convert(docx_path, out_md_path, media_dir):
    os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read("word/document.xml")
        root = ET.fromstring(xml_content)
        body = root.find(f"{{{NS['w']}}}body")

        # Map relationship IDs to image filenames (for image placeholders)
        rels = {}
        try:
            rel_xml = z.read("word/_rels/document.xml.rels")
            rel_root = ET.fromstring(rel_xml)
            for rel in rel_root:
                if "image" in rel.get("Type", ""):
                    rels[rel.get("Id")] = rel.get("Target")
        except KeyError:
            pass

        # Extract embedded images to disk
        os.makedirs(media_dir, exist_ok=True)
        image_names = [n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")]
        for img in image_names:
            ext = os.path.splitext(img)[1]
            fname = f"image{image_names.index(img)+1}{ext}"
            with open(os.path.join(media_dir, fname), "wb") as f:
                f.write(z.read(img))

        lines = []
        img_counter = 0
        for elem in body:
            tag = elem.tag.split("}")[1]

            if tag == "p":
                # Check paragraph style for heading level
                style = elem.find(f".//{{{NS['w']}}}pStyle")
                text = get_text(elem)
                has_image = elem.find(f".//{{{NS['w']}}}drawing") is not None

                if has_image and img_counter < len(image_names):
                    fname = os.path.basename(image_names[img_counter])
                    lines.append(f"![Image {img_counter+1}]({os.path.basename(media_dir)}/{fname})")
                    lines.append("")
                    img_counter += 1

                if style is not None:
                    val = style.get(f"{{{NS['w']}}}val", "")
                    if "Heading1" in val or val == "Title":
                        lines.append(f"# {text}")
                    elif "Heading2" in val:
                        lines.append(f"## {text}")
                    elif "Heading3" in val:
                        lines.append(f"### {text}")
                    elif text.strip():
                        lines.append(text)
                elif text.strip():
                    lines.append(text)
                lines.append("")

            elif tag == "tbl":
                rows = elem.findall(f"{{{NS['w']}}}tr")
                for i, row in enumerate(rows):
                    cells = row.findall(f"{{{NS['w']}}}tc")
                    cell_texts = [get_text(c).replace("|", "\\|").strip() for c in cells]
                    lines.append("| " + " | ".join(cell_texts) + " |")
                    if i == 0:
                        lines.append("|" + "|".join([" --- " for _ in cells]) + "|")
                lines.append("")

        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

if __name__ == "__main__":
    docx_path = sys.argv[1]
    out_md_path = sys.argv[2]
    media_dir = sys.argv[3]
    convert(docx_path, out_md_path, media_dir)
    print(f"Converted: {docx_path} -> {out_md_path}")