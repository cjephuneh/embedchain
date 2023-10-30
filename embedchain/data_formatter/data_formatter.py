from importlib import import_module

from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config import AddConfig
from embedchain.config.add_config import ChunkerConfig, LoaderConfig
from embedchain.helper.json_serializable import JSONSerializable
from embedchain.loaders.base_loader import BaseLoader
from embedchain.models.data_type import DataType


class DataFormatter(JSONSerializable):
    """
    DataFormatter is an internal utility class which abstracts the mapping for
    loaders and chunkers to the data_type entered by the user in their
    .add or .add_local method call
    """

    def __init__(self, data_type: DataType, config: AddConfig):
        """
        Initialize a dataformatter, set data type and chunker based on datatype.

        :param data_type: The type of the data to load and chunk.
        :type data_type: DataType
        :param config: AddConfig instance with nested loader and chunker config attributes.
        :type config: AddConfig
        """
        self.loader = self._get_loader(data_type=data_type, config=config.loader)
        self.chunker = self._get_chunker(data_type=data_type, config=config.chunker)

    def _lazy_load(self, module_path: str):
        module_path, class_name = module_path.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)

    def _get_loader(self, data_type: DataType, config: LoaderConfig) -> BaseLoader:
        """
        Returns the appropriate data loader for the given data type.

        :param data_type: The type of the data to load.
        :type data_type: DataType
        :param config: Config to initialize the loader with.
        :type config: LoaderConfig
        :raises ValueError: If an unsupported data type is provided.
        :return: The loader for the given data type.
        :rtype: BaseLoader
        """
        loaders = {
            DataType.YOUTUBE_VIDEO: "embedchain.loaders.youtube_video.YoutubeVideoLoader",
            DataType.PDF_FILE: "embedchain.loaders.pdf_file.PdfFileLoader",
            DataType.WEB_PAGE: "embedchain.loaders.web_page.WebPageLoader",
            DataType.QNA_PAIR: "embedchain.loaders.local_qna_pair.LocalQnaPairLoader",
            DataType.TEXT: "embedchain.loaders.local_text.LocalTextLoader",
            DataType.DOCX: "embedchain.loaders.docx_file.DocxFileLoader",
            DataType.SITEMAP: "embedchain.loaders.sitemap.SitemapLoader",
            DataType.XML: "embedchain.loaders.xml.XmlLoader",
            DataType.DOCS_SITE: "embedchain.loaders.docs_site_loader.DocsSiteLoader",
            DataType.CSV: "embedchain.loaders.csv.CsvLoader",
            DataType.MDX: "embedchain.loaders.mdx.MdxLoader",
            DataType.IMAGES: "embedchain.loaders.images.ImagesLoader",
            DataType.UNSTRUCTURED: "embedchain.loaders.unstructured_file.UnstructuredLoader",
            DataType.JSON: "embedchain.loaders.json.JSONLoader",
            DataType.OPENAPI: "embedchain.loaders.openapi.OpenAPILoader",
            DataType.GMAIL: "embedchain.loaders.gmail.GmailLoader",
            DataType.NOTION: "embedchain.loaders.notion.NotionLoader",
        }
        if data_type in loaders:
            loader_class: type = self._lazy_load(loaders[data_type])
            return loader_class()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def _get_chunker(self, data_type: DataType, config: ChunkerConfig) -> BaseChunker:
        """Returns the appropriate chunker for the given data type (updated for lazy loading)."""
        chunker_classes = {
            DataType.YOUTUBE_VIDEO: "embedchain.chunkers.youtube_video.YoutubeVideoChunker",
            DataType.PDF_FILE: "embedchain.chunkers.pdf_file.PdfFileChunker",
            DataType.WEB_PAGE: "embedchain.chunkers.web_page.WebPageChunker",
            DataType.QNA_PAIR: "embedchain.chunkers.qna_pair.QnaPairChunker",
            DataType.TEXT: "embedchain.chunkers.text.TextChunker",
            DataType.DOCX: "embedchain.chunkers.docx_file.DocxFileChunker",
            DataType.SITEMAP: "embedchain.chunkers.sitemap.SitemapChunker",
            DataType.XML: "embedchain.chunkers.xml.XmlChunker",
            DataType.DOCS_SITE: "embedchain.chunkers.docs_site.DocsSiteChunker",
            DataType.CSV: "embedchain.chunkers.table.TableChunker",
            DataType.MDX: "embedchain.chunkers.mdx.MdxChunker",
            DataType.IMAGES: "embedchain.chunkers.images.ImagesChunker",
            DataType.UNSTRUCTURED: "embedchain.chunkers.unstructured_file.UnstructuredFileChunker",
            DataType.JSON: "embedchain.chunkers.json.JSONChunker",
            DataType.OPENAPI: "embedchain.chunkers.openapi.OpenAPIChunker",
            DataType.GMAIL: "embedchain.chunkers.gmail.GmailChunker",
            DataType.NOTION: "embedchain.chunkers.notion.NotionChunker",
        }

        if data_type in chunker_classes:
            chunker_class = self._lazy_load(chunker_classes[data_type])
            chunker = chunker_class(config)
            chunker.set_data_type(data_type)
            return chunker
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
