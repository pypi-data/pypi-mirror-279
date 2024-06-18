from afeng_tools.fastapi_tool.common.po_service.article_po_service_ import ArticlePoService, ArticleDetailPoService
from afeng_tools.fastapi_tool.common.po_service.blacklist_po_service_ import BlacklistPoService
from afeng_tools.fastapi_tool.common.po_service.category_po_service_ import CategoryPoService
from afeng_tools.fastapi_tool.common.po_service.group_po_service_ import GroupPoService
from afeng_tools.fastapi_tool.common.po_service.link_po_service_ import LinkPoService
from afeng_tools.fastapi_tool.common.po_service.relation_po_service_ import RelationPoService
from afeng_tools.fastapi_tool.common.po_service.resource_po_service_ import ResourcePoService
from afeng_tools.fastapi_tool.common.po_service.sitemap_po_service_ import SitemapPoService
from afeng_tools.fastapi_tool.common.po_service.tag_po_service_ import TagPoService, TagRelationPoService
from afeng_tools.fastapi_tool.common.po_service.tmp_po_service_ import TmpSortPoService


class CommonPoService:
    """通用po服务"""

    def __init__(self, db_code: str):
        self.db_code = db_code
        self.article_po_service = ArticlePoService(self.db_code)
        self.article_detail_po_service = ArticleDetailPoService(self.db_code)
        self.blacklist_po_service = BlacklistPoService(self.db_code)
        self.category_po_service = CategoryPoService(self.db_code)
        self.group_po_service = GroupPoService(self.db_code)
        self.link_po_service = LinkPoService(self.db_code)
        self.resource_po_service = ResourcePoService(self.db_code)
        self.sitemap_po_service = SitemapPoService(self.db_code)
        self.tag_po_service = TagPoService(self.db_code)
        self.tag_relation_po_service = TagRelationPoService(self.db_code)
        self.tmp_sort_po_service = TmpSortPoService(self.db_code)
        self.relation_po_service = RelationPoService(self.db_code)


