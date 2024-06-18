import csv
import json
import os
import pathlib
from bs4 import BeautifulSoup
from lxml import etree


from py2neo import Node, Relationship

SEMPER_TEI = os.getenv("SEMPER_TEI", "../semper-tei")


def get_img_folder_for_filename(filename):
    """Depending on the filename, we've got different image folders
    on the IIIF Server
    """
    folder = ""
    if filename.startswith("Stil_Bd.1_Aufl_I_1860a"):
        folder = "e-rara_stil_1860a_b1"
    elif filename.startswith("Stil_Bd.1_Aufl_II_1878"):
        folder = "e-rara_stil_1878_b1"
    else:
        folder = "_".join(filename.split("_")[0:3])
    return folder


class TOC:
    toc: dict
    filename2path: dict
    image2identifier: dict
    iiif_base_url_gta: str = "https://iiif.gta.arch.ethz.ch/iiif/2"
    iiif_base_url_library: str = "https://iiif.library.ethz.ch/iiif/2/editionen!semper"
    iiif_thumbnail_default: str = "full/,150/0/default.jpg"

    def save_toc_to_graph(self, graph):
        """Starts a new graph session, deletes all existing TOC entries and
        creates new TOC entries based on information in semper-tei/TOC and
        all the TEI files."""
        tx = graph.begin()
        print("delete existing TOC graph...")
        graph.run("MATCH (t :TOC) DETACH DELETE t")
        print("create new TOC graph from TOC...")
        self.create_graph_from_toc(toc=self.toc, tx=tx)
        print("write graph to Neo4j databse...")
        tx.commit()
        print("done.")

    def create_graph_from_toc(
        self,
        toc,
        tx,
        no=None,
        depth=0,
    ) -> Node:
        """this method imports the table of contents (a JSON file)
        and creates the graph structure in the Neo4j database
        """

        if not toc:
            return None
        if "xml:id" not in toc:
            print(toc)
            print("xml:id is missing! Please fix it in the corresponding TOC JSON file")
            toc["xml:id"] = ""
        toc_node = Node(
            "TOC",
            depth=depth,
            collection=toc["xml:id"],
            **{"xml:id": toc["xml:id"], "no": no or 0},
        )
        tx.create(toc_node)

        for title in toc.get("titles", []):
            title_node = Node(
                "TOC", "TITLE", depth=depth, collection=toc["xml:id"], **title
            )
            tx.create(title_node)
            tx.create(Relationship(toc_node, "HAS_TITLE", title_node))

        # prev_file_node = None
        files = toc.get("files", [])

        for i, filename in enumerate(toc.get("files", [])):
            # Create a TOC node with file, first, last, prev, next properties
            props = {"file": filename, "no": i, "first": files[0], "last": files[-1]}
            if i > 0:
                props["prev"] = files[i - 1]
            if i < len(files) - 1:
                props["next"] = files[i + 1]

            graphic_info = self.get_graphic_info_from_tei(
                self.filename2path.get(filename)
            )
            props = {**props, **graphic_info}

            file_node = Node(
                "TOC", "FILE", depth=depth, collection=toc["xml:id"], **props
            )
            tx.create(file_node)
            tx.create(Relationship(toc_node, "HAS_FILE", file_node))

        for i, content in enumerate(toc.get("contents", [])):
            content_node = self.create_graph_from_toc(
                toc=content, tx=tx, no=i, depth=depth + 1
            )
            if content_node:
                # create parent-child relationship
                tx.create(Relationship(toc_node, "HAS_CONTENT", content_node))

        return toc_node

    def get_image_url_for_image_name(self, image_name):
        image_url = ""
        if image_name.lower() in self.image2identifier:
            image_url = self.image2identifier[image_name.lower()]
        else:
            folder = get_img_folder_for_filename(image_name)
            image_url = f"{self.iiif_base_url_library}!{folder}!{image_name}/info.json"
        return image_url

    def get_graphic_info_from_tei(self, filepath: pathlib.Path) -> dict:
        """Reads a XML file and extracts these elements
        - label
        - locus
        - graphic
        - id
        - thumbnail
        returns a dict
        """
        if not filepath:
            return {}
        if not filepath.exists():
            print(f"    #### FILE NOT FOUND: {filepath.resolve()}")
            return {}
        print(f"parse TEI: {filepath.resolve()}")
        parser = etree.XMLParser(dtd_validation=True, recover=True)
        tree = etree.parse(filepath, parser)
        unicode_string = etree.tostring(tree.getroot(), encoding="unicode")
        soup = BeautifulSoup(unicode_string, "lxml-xml")

        if not soup:
            return {}

        page_info = {}
        label = soup.find("label")
        if label:
            page_info["label"] = label.text

        locus = soup.find("locus")
        if locus:
            page_info["locus"] = locus.text

        graphic = soup.find("graphic")
        if graphic:
            image_name = graphic.attrs.get("url", "")
            page_info["image"] = self.get_image_url_for_image_name(image_name)

        return page_info

    @classmethod
    def new_from_file(cls, toc_filepath: pathlib.Path):
        """Reads the TOC json file and recursively all
        related TOC files to build one big TOC
        Also loads the imagename -> GTA IIF identifier mapper
        """
        toc_obj = cls()

        if not isinstance(toc_filepath, pathlib.Path):
            toc_filepath = pathlib.Path(toc_filepath)

        print(f"loading TOC from: {toc_filepath.resolve()}")
        toc = cls._load_toc_from_file(toc_filepath=toc_filepath)
        cls._build_toc(toc, toc_filepath.parent)
        toc_obj.toc = toc
        toc_obj.image2identifier = cls._image2identifier()
        toc_obj.filename2path = cls._read_teis(os.getenv("SEMPER_TEI", "../semper-tei"))

        return toc_obj

    @classmethod
    def _load_toc_from_file(cls, toc_filepath: pathlib.Path) -> dict:
        with open(toc_filepath, "r", encoding="utf-8") as fh:
            try:
                content = json.load(fh)
            except json.decoder.JSONDecodeError as exc:
                raise ValueError(
                    f"Error trying to decode JSON file {toc_filepath}: {exc}"
                ) from exc
        return content

    @classmethod
    def _build_toc(cls, toc: dict, parent_dir: pathlib.Path) -> dict:
        new_contents = []
        for content in toc.get("contents", []):
            if isinstance(content, str):
                try:
                    toc_filepath = parent_dir / content
                    new_content = cls._load_toc_from_file(toc_filepath)
                except FileNotFoundError:
                    print(f"    ### FILE NOT FOUND: {content}")
                    new_content = {}
                except json.decoder.JSONDecodeError:
                    print(f"    ### JSON ERROR: {content}")
                    new_content = {}
                new_contents.append(new_content)
            else:
                cls._build_toc(content, parent_dir)
        if new_contents:
            toc["contents"] = new_contents

    @classmethod
    def _image2identifier(cls) -> dict:
        """Some images (e.g. the facsimiles of the printed books) are stored on the ETH image server.
        Other images, such as the manuscripts, are hosted on the GTA IIIF server.
        This method opens semper_backend/iiif-mapping/digital_semper_iiif_links.csv
        and creates a dict: self.image2identifier

        e.g. self.image2identifier["20_ms_161.4recto.jpg"] = "147486/full/max/0/default.tif"
        """
        csv_filepath = (
            pathlib.Path(os.path.dirname(__file__))
            / "iiif-mapping"
            / "digital_semper_iiif_links.csv"
        )

        image2identifier = {}
        print(f"load filename-identifier mappings from: {csv_filepath.resolve()}")
        with open(csv_filepath, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                identifier = row["iiif_link"]
                image2identifier[row["filename_orig"].lower()] = identifier
        print(f"    {len(image2identifier)} mappings loaded.")
        return image2identifier

    @classmethod
    def _read_teis(cls, tei_folder) -> dict:
        """recursively reads all xml files in the given SEMPER_TEI path
        and stores the absolute path of every TEI file.
        """
        teipath = pathlib.Path(tei_folder)
        print(f"find all TEI documents in path: {teipath.resolve()}")
        if not teipath.exists():
            raise ValueError(
                f"PATH '{tei_folder}' does not exist. Please check the SEMPER_TEI variable."
            )

        i = 0
        filename2path = {}
        for teifile in teipath.rglob("*.xml"):
            filename2path[teifile.name] = teifile.absolute()
            i += 1

        print(f"    {i} TEI files found.")
        return filename2path
