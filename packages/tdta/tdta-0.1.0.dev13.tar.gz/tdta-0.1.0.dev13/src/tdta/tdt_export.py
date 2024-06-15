import os
import sqlite3
import ast
import json
from contextlib import closing
from pathlib import Path
from datetime import datetime

from tdta.utils import read_project_config
from cas.model import (CellTypeAnnotation, Annotation, Labelset, AnnotationTransfer, AutomatedAnnotation, Review)
from cas.file_utils import write_json_file
from cas.matrix_file.resolver import resolve_matrix_file
from cas.populate_cell_ids import add_cell_ids

CONFLICT_TBL_EXT = "_conflict"

cas_table_names = ["annotation", "labelset", "metadata", "annotation_transfer", "review"]


def export_cas_data(sqlite_db: str, output_file: str, dataset_cache_folder: str = None):
    """
    Reads all data from TDT tables and generates CAS json.
    :param sqlite_db: db file path
    :param output_file: output json path
    :param dataset_cache_folder: anndata cache folder path
    """
    cta = CellTypeAnnotation("", list(), "")

    cas_tables = get_table_names(sqlite_db)
    for table_name in cas_tables:
        if table_name == "metadata":
            parse_metadata_data(cta, sqlite_db, table_name)
        elif table_name == "annotation":
            parse_annotation_data(cta, sqlite_db, table_name)
        elif table_name == "labelset":
            parse_labelset_data(cta, sqlite_db, table_name)
        elif table_name == "annotation_transfer":
            parse_annotation_transfer_data(cta, sqlite_db, table_name)
        # elif table_name == "review":
        #     # don't export reviews to the CAS json for now
        #     parse_review_data(cta, sqlite_db, table_name)

    project_config = read_project_config(Path(output_file).parent.absolute())

    if project_config and "matrix_file_id" in project_config:
        matrix_file_id = str(project_config["matrix_file_id"]).strip()
        anndata = resolve_matrix_file(matrix_file_id, dataset_cache_folder)
        labelsets = cta.labelsets.copy()
        labelsets.sort(key=lambda x: x.rank)
        labelset_names = [labelset.name for labelset in labelsets]

        cas_json = add_cell_ids(cta.to_dict(), anndata, labelsets=labelset_names)
        if cas_json is None:
            print("WARN: Cell IDs population operation failed, skipping cell_id population")
            cas_json = cta.to_dict()
        with open(output_file, "w") as json_file:
            json.dump(cas_json, json_file, indent=2)
    else:
        print("WARN: 'matrix_file_id' not specified in the project configuration. Skipping cell_id population")
        write_json_file(cta, output_file, False)

    print("CAS json successfully created at: {}".format(output_file))
    return cta


def parse_metadata_data(cta, sqlite_db, table_name):
    """
    Reads 'Metadata' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    :return : True if metadata can be ingested, False otherwise
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}_view".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            if len(rows) > 0:
                auto_fill_object_from_row(cta, columns, rows[0])
                return True
    return False


def parse_annotation_data(cta, sqlite_db, table_name):
    """
    Reads 'Annotation' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}_view".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            if len(rows) > 0:
                if not cta.annotations:
                    annotations = list()
                else:
                    annotations = cta.annotations
                for row in rows:
                    annotation = Annotation("", "")
                    auto_fill_object_from_row(annotation, columns, row)
                    # handle author_annotation_fields
                    author_annotation_fields = dict()
                    obj_fields = vars(annotation)
                    for column in columns:
                        if column not in obj_fields and column not in ["row_number", "message", "history"]:
                            author_annotation_fields[column] = str(row[columns.index(column)])
                    if author_annotation_fields:
                        annotation.author_annotation_fields = author_annotation_fields

                    annotations.append(annotation)
                cta.annotations = annotations


def parse_labelset_data(cta, sqlite_db, table_name):
    """
    Reads 'Labelset' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}_view".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            if len(rows) > 0:
                if not cta.labelsets:
                    labelsets = list()
                else:
                    labelsets = cta.labelsets
                renamed_columns = [str(c).replace("automated_annotation_", "") for c in columns]
                for row in rows:
                    labelset = Labelset("", "")
                    auto_fill_object_from_row(labelset, columns, row)
                    # handle automated_annotation
                    if row[renamed_columns.index("algorithm_name")]:
                        automated_annotation = AutomatedAnnotation("", "", "", "")
                        auto_fill_object_from_row(automated_annotation, renamed_columns, row)
                        labelset.automated_annotation = automated_annotation
                    labelsets.append(labelset)
                cta.labelsets = labelsets


def parse_annotation_transfer_data(cta, sqlite_db, table_name):
    """
    Reads 'Annotation Transfer' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}_view".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            if len(rows) > 0:
                for row in rows:
                    if "target_node_accession" in columns and row[columns.index("target_node_accession")]:
                        filtered_annotations = [a for a in cta.annotations
                                                if a.cell_set_accession == row[columns.index("target_node_accession")]]
                        if filtered_annotations:
                            at = AnnotationTransfer("", "", "", "", "")
                            auto_fill_object_from_row(at, columns, row)
                            if filtered_annotations[0].transferred_annotations:
                                filtered_annotations[0].transferred_annotations.append(at)
                            else:
                                filtered_annotations[0].transferred_annotations = [at]


def parse_review_data(cta, sqlite_db, table_name):
    """
    Reads 'Annotation Review' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}_view".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            if len(rows) > 0:
                for row in rows:
                    if "target_node_accession" in columns and row[columns.index("target_node_accession")]:
                        filtered_annotations = [a for a in cta.annotations
                                                if a.cell_set_accession == row[columns.index("target_node_accession")]]
                        if filtered_annotations:
                            ar = Review(None, "", "", "")
                            auto_fill_object_from_row(ar, columns, row)
                            if ar.datestamp and isinstance(ar.datestamp, str):
                                ar.datestamp = datetime.strptime(ar.datestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                            if filtered_annotations[0].reviews:
                                filtered_annotations[0].reviews.append(ar)
                            else:
                                filtered_annotations[0].reviews = [ar]

def get_table_names(sqlite_db):
    """
    Queries 'table' table to get all CAS related table names
    :param sqlite_db: db file path
    :return: list of CAS related table names
    """
    cas_tables = list()
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM table_view").fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            table_column_index = columns.index('table')
            for row in rows:
                if str(row[table_column_index]) in cas_table_names:
                    cas_tables.append(str(row[table_column_index]))
    return cas_tables


def auto_fill_object_from_row(obj, columns, row):
    """
    Automatically sets attribute values of the obj from the given db table row.
    :param obj: object to fill
    :param columns: list of the db table columns
    :param row: db record
    """
    for column in columns:
        if hasattr(obj, column):
            value = row[columns.index(column)]
            if value:
                if isinstance(type(getattr(obj, column)), list):
                    if value.strip().startswith("\"") and value.strip().endswith("\""):
                        value = value.strip()[1:-1].strip()
                    elif value.strip().startswith("'") and value.strip().endswith("'"):
                        value = value.strip()[1:-1].strip()
                    values = value.split("|")
                    list_value = []
                    for item in values:
                        if item.strip().startswith("\"") and item.strip().endswith("\""):
                            item = item.strip()[1:-1].strip()
                        elif item.strip().startswith("'") and item.strip().endswith("'"):
                            item = item.strip()[1:-1].strip()
                        list_value.append(item)
                    value = list_value
                    # value = ast.literal_eval(value)
                setattr(obj, column, value)
        if 'message' in columns and row[columns.index('message')]:
            # process invalid data
            messages = json.loads(row[columns.index('message')])
            for msg in messages:
                if msg["column"] in columns:
                    setattr(obj, msg["column"], msg["value"])

