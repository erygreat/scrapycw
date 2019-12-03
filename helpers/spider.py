from scrapy.utils.conf import get_config


class ScrapySpiderHelper:

    @classmethod
    def list(cls, project="default"):
        spiders = []
        for s in sorted(self.crawler_process.spider_loader.list()):
            spiders.append({"name": s})
        return {
            "status": "success",
            "spiders": spiders,
            "project": opts.project
        }

