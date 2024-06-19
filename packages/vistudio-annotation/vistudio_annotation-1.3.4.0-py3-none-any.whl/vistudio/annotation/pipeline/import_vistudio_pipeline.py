#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
export_pipeline.py
"""
import sys
import os

__work_dir__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, __work_dir__)
from vistudio.annotation.processor.importer.annoation.vistudio_preprocessor import VistudioFormatterPreprocessor

from vistudio.annotation.config.arg_parser import ArgParser

from vistudio.annotation.operator.reader import Reader
from vistudio.annotation.processor.importer.image.image_preprocessor import ImageFormatterPreprocessor

from vistudio.annotation.pipeline.base_import_pipeline import BaseImportPipline

import ray

import argparse
import logit

logit.base_logger.setup_logger({})


class ImportVistudioPipeline(BaseImportPipline):
    """
        标注格式转换类
        :param param_dict: 公共的字段
        :param annotation_file_path: 标注文件本地路径
        :param image_uri: 图像s3地址
        :param image_path: 图像本地路径
        :param annotation_format: 标注格式
        """

    def __init__(self,
                 args,
                 ):
        super().__init__(args)

    def _import_annoation(self):
        """
        导入标注文件
        :return:
        """

        # 读取json 文件
        vistudio_reader = Reader(filesystem=self.config.filesystem, annotation_set_id=self.annotation_set_id)
        file_uris = vistudio_reader.get_file_uris(data_uri=self.data_uri,
                                                  data_types=self.data_types,
                                                  import_type='vistudio')
        ds = vistudio_reader.read_json(file_uris)
        logit.info("import annotation from vistudio.dataset count = {}".format(ds.count()))

        # 处理 ds
        vistudio_formater = VistudioFormatterPreprocessor(
            config=self.config,
            labels=self.labels,
            annotation_set_id=self.annotation_set_id,
            annotation_set_name=self.annotation_set_name,
            data_uri=self.data_uri,
            data_type="Image",
            tag=self.tag
        )
        image_ds = vistudio_formater.fit(ds).stats_
        if image_ds.count() > 0:
            image_ds.write_mongo(uri=self.mongo_uri,
                                 database=self.config.mongodb_database,
                                 collection=self.config.mongodb_collection)

        vistudio_formater = VistudioFormatterPreprocessor(
            config=self.config,
            labels=self.labels,
            annotation_set_id=self.annotation_set_id,
            annotation_set_name=self.annotation_set_name,
            data_uri=self.data_uri,
            data_type="Annotation"
        )
        anno_ds = vistudio_formater.fit(ds).stats_
        if anno_ds.count() > 0:
            anno_ds.write_mongo(uri=self.mongo_uri,
                                database=self.config.mongodb_database,
                                collection=self.config.mongodb_collection)

    def _import_image(self):
        """
        导入图片
        :return:
        """
        vistudio_reader = Reader(filesystem=self.config.filesystem, annotation_set_id=self.annotation_set_id)
        file_uris = vistudio_reader.get_file_uris(data_uri=self.data_uri, data_types=self.data_types)

        ds = ray.data.from_items(file_uris)
        logit.info("import vistudio image from json.dataset count = {}".format(ds.count()))

        image_formater = ImageFormatterPreprocessor(
            config=self.config,
            annotation_set_id=self.annotation_set_id,
            annotation_set_name=self.annotation_set_name,
            tag=self.tag
        )
        final_ds = image_formater.fit(ds).stats_
        logit.info("format dataset.dataset count = {}".format(final_ds.count()))
        # 写入数据
        final_ds.write_mongo(uri=self.mongo_uri,
                             database=self.config.mongodb_database,
                             collection=self.config.mongodb_collection)

    def run(self):
        """
        run this piepline
        :return:
        """
        if len(self.data_types) == 1 and self.data_types[0] == "annotation":
            self._import_annoation()

        elif len(self.data_types) == 1 and self.data_types[0] == "image":
            self._import_image()

        elif len(self.data_types) == 2 and "image" in self.data_types and "annotation" in self.data_types:
            self._import_annoation()
        else:
            raise Exception("The data_types: '{}' is not support.".format(self.data_types))


def run(args):
    """
    pipeline run
    :param args:
    :return:
    """
    pipeline = ImportVistudioPipeline(args)
    pipeline.run()


if __name__ == "__main__":
    arg_parser = ArgParser(kind='Import')
    args = arg_parser.parse_args()
    run(args)
