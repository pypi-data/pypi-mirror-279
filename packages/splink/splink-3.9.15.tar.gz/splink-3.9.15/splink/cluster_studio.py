from __future__ import annotations

import json
import os
import random
from typing import TYPE_CHECKING, Any

from jinja2 import Template

from .exceptions import SplinkException
from .misc import EverythingEncoder, read_resource
from .splink_dataframe import SplinkDataFrame
from .unique_id_concat import (
    _composite_unique_id_from_edges_sql,
    _composite_unique_id_from_nodes_sql,
)

# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
if TYPE_CHECKING:
    from .linker import Linker


def _quo_if_str(x):
    if isinstance(x, str):
        return f"'{x}'"
    else:
        return str(x)


def _clusters_sql(df_clustered_nodes, cluster_ids: list) -> str:
    cluster_ids = [_quo_if_str(x) for x in cluster_ids]
    cluster_ids_joined = ", ".join(cluster_ids)

    sql = f"""
    select distinct(cluster_id)
    from {df_clustered_nodes.physical_name}
    where cluster_id in ({cluster_ids_joined})
    """

    return sql


def df_clusters_as_records(
    linker: "Linker", df_clustered_nodes: SplinkDataFrame, cluster_ids: list
):
    """Retrieves distinct clusters which exist in df_clustered_nodes based on
    list of cluster IDs provided and converts them to a record dictionary.

    Args:
        linker: An instance of the Splink Linker class.
        df_clustered_nodes (SplinkDataFrame): Result of
        cluster_pairwise_predictions_at_threshold().
        cluster_ids (list): List of cluster IDs to filter the results.

    Returns:
    dict: A record dictionary of the specified cluster IDs.
    """
    sql = _clusters_sql(df_clustered_nodes, cluster_ids)
    df_clusters = linker._sql_to_splink_dataframe_checking_cache(
        sql, "__splink__scs_clusters"
    )
    return df_clusters.as_record_dict()


def _nodes_sql(df_clustered_nodes, cluster_ids) -> str:
    """Generates SQL query to select all columns from df_clustered_nodes
    for list of cluster IDs provided.

    Args:
        df_clustered_nodes (SplinkDataFrame): result of
        cluster_pairwise_predictions_at_threshold()
        cluster_ids (list): List of cluster IDs to filter the results
    """

    cluster_ids = [_quo_if_str(x) for x in cluster_ids]
    cluster_ids_joined = ", ".join(cluster_ids)

    sql = f"""
    select *
    from {df_clustered_nodes.physical_name}
    where cluster_id in ({cluster_ids_joined})
    """

    return sql


def create_df_nodes(
    linker: "Linker", df_clustered_nodes: SplinkDataFrame, cluster_ids: list
):
    """Retrieves nodes from df_clustered_nodes for list of cluster IDs provided.

    Args:
        linker: An instance of the Splink Linker class.
        df_clustered_nodes (SplinkDataFrame): Result of
        cluster_pairwise_predictions_at_threshold().
        cluster_ids (list): List of cluster IDs to filter the results.

    Returns:
        A SplinkDataFrame containing the nodes for the specified cluster IDs.
    """
    sql = _nodes_sql(df_clustered_nodes, cluster_ids)
    df_nodes = linker._sql_to_splink_dataframe_checking_cache(
        sql, "__splink__scs_nodes"
    )
    return df_nodes


def _edges_sql(
    linker: "Linker", df_predicted_edges: SplinkDataFrame, df_nodes: SplinkDataFrame
):
    unique_id_cols = linker._settings_obj._unique_id_input_columns

    nodes_l_id_expr = _composite_unique_id_from_nodes_sql(unique_id_cols, "nodes_l")
    nodes_r_id_expr = _composite_unique_id_from_nodes_sql(unique_id_cols, "nodes_r")
    edges_l_id_expr = _composite_unique_id_from_edges_sql(
        unique_id_cols, "l", table_prefix="edges"
    )
    edges_r_id_expr = _composite_unique_id_from_edges_sql(
        unique_id_cols, "r", table_prefix="edges"
    )

    # It's in the cluster if BOTH the left and right id are in the cluster
    # So it's a double left join you need

    sql = f"""
    select
        edges.*,
        nodes_l.cluster_id as cluster_id_l,
        nodes_r.cluster_id as cluster_id_r
    from {df_predicted_edges.physical_name} as edges
    inner join
    {df_nodes.physical_name} as nodes_l
    on {edges_l_id_expr} = {nodes_l_id_expr}
    inner join
    {df_nodes.physical_name} as nodes_r
    on {edges_r_id_expr} = {nodes_r_id_expr}
    """
    return sql


def df_edges_as_records(
    linker: "Linker", df_predicted_edges: SplinkDataFrame, df_nodes: SplinkDataFrame
):
    sql = _edges_sql(linker, df_predicted_edges, df_nodes)
    df_edges = linker._sql_to_splink_dataframe_checking_cache(
        sql, "__splink__scs_edges"
    )
    return df_edges.as_record_dict()


def _get_random_cluster_ids(
    linker: "Linker", connected_components: SplinkDataFrame, sample_size: int, seed=None
):
    sql = f"""
    select count(distinct cluster_id) as count
    from {connected_components.physical_name}
    """
    df_cluster_count = linker._sql_to_splink_dataframe_checking_cache(
        sql, "__splink__cluster_count"
    )
    cluster_count = df_cluster_count.as_record_dict()[0]["count"]
    df_cluster_count.drop_table_from_database_and_remove_from_cache()

    proportion = sample_size / cluster_count

    random_sample_sql = linker._random_sample_sql(
        proportion,
        sample_size,
        seed,
        table=connected_components.physical_name,
        unique_id="cluster_id",
    )

    sql = f"""
    with distinct_clusters as (
    select distinct(cluster_id)
    from {connected_components.physical_name}
    )
    select cluster_id from distinct_clusters
    {random_sample_sql}
    """

    df_sample = linker._sql_to_splink_dataframe_checking_cache(
        sql,
        "__splink__df_concat_with_tf_sample",
    )
    return [r["cluster_id"] for r in df_sample.as_record_dict()]


def _get_cluster_id_of_each_size(
    linker: "Linker", connected_components: SplinkDataFrame, rows_per_partition: int
):
    sql = f"""
    select
        cluster_id,
        count(*) as cluster_size,
        max({linker._settings_obj._unique_id_column_name}) as ordering
    from {connected_components.physical_name}
    group by cluster_id
    having count(*)>1
    """

    linker._enqueue_sql(sql, "__splink__cluster_count")

    # Assign unique row number to each row in partition
    sql = """
    select
        cluster_id,
        cluster_size,
        row_number() over (partition by cluster_size order by ordering) as row_num
    from __splink__cluster_count
    """

    linker._enqueue_sql(sql, "__splink__cluster_count_row_numbered")

    sql = f"""
    select
        cluster_id,
        cluster_size
    from __splink__cluster_count_row_numbered
    where row_num <= {rows_per_partition}
    """

    linker._enqueue_sql(sql, "__splink__cluster_count_row_numbered")
    df_cluster_sample_with_size = linker._execute_sql_pipeline()

    return df_cluster_sample_with_size.as_record_dict()


def _get_lowest_density_clusters(
    linker: "Linker",
    df_cluster_metrics: SplinkDataFrame,
    rows_per_partition: int,
    min_nodes: int,
):
    """Returns lowest density clusters of different sizes by
    performing stratified sampling.

    Args:
        linker: An instance of the Splink Linker class.
        df_cluster_metrics (SplinkDataFrame): dataframe containing
        cluster metrics including density.
        rows_per_partition (int): number of rows in each strata (partition)
        min_nodes (int): minimum number of nodes a cluster must contain
        to be included in the sample.

    Returns:
        list: A list of record dictionaries containing cluster ids, densities
        and sizes of lowest density clusters.
    """

    sql = f"""
    select
        cluster_id,
        n_nodes,
        density,
        row_number() over (partition by n_nodes order by density, cluster_id) as row_num
    from {df_cluster_metrics.physical_name}
    where n_nodes >= {min_nodes}
    """

    linker._enqueue_sql(sql, "__splink__partition_clusters_by_size")

    sql = f"""
    select
        cluster_id,
        round(density, 4) as density_4dp,
        n_nodes as cluster_size
    from __splink__partition_clusters_by_size
    where row_num <= {rows_per_partition}
    """

    linker._enqueue_sql(sql, "__splink__lowest_density_clusters")
    df_lowest_density_clusters = linker._execute_sql_pipeline()

    return df_lowest_density_clusters.as_record_dict()


def render_splink_cluster_studio_html(
    linker: "Linker",
    df_predicted_edges: SplinkDataFrame,
    df_clustered_nodes: SplinkDataFrame,
    out_path: str,
    sampling_method="random",
    sample_size=10,
    sample_seed=None,
    cluster_ids: list = None,
    cluster_names: list = None,
    overwrite: bool = False,
    _df_cluster_metrics: SplinkDataFrame = None,
):
    bundle_observable_notebook = True

    svu_options = {
        "cluster_colname": "cluster_id",
        "prob_colname": "match_probability",
    }
    named_clusters_dict = None
    if cluster_ids is None:
        if sampling_method == "random":
            cluster_ids = _get_random_cluster_ids(
                linker, df_clustered_nodes, sample_size, sample_seed
            )
        if sampling_method == "by_cluster_size":
            cluster_ids = _get_cluster_id_of_each_size(linker, df_clustered_nodes, 1)
            if len(cluster_ids) > sample_size:
                cluster_ids = random.sample(cluster_ids, k=sample_size)
            cluster_names = [
                f"Cluster ID: {c['cluster_id']}, size:  {c['cluster_size']}"
                for c in cluster_ids
            ]
            cluster_ids = [c["cluster_id"] for c in cluster_ids]
            named_clusters_dict = dict(zip(cluster_ids, cluster_names))
        if sampling_method == "lowest_density_clusters_by_size":
            if _df_cluster_metrics is None:
                raise SplinkException(
                    """To sample by density, you must provide a cluster metrics table
                      containing density. This can be generated by calling the
                      _compute_graph_metrics method on the linker."""
                )
            # Using sensible default for min_nodes. Might become option
            # for users in future
            cluster_ids = _get_lowest_density_clusters(
                linker, _df_cluster_metrics, rows_per_partition=1, min_nodes=3
            )
            if len(cluster_ids) > sample_size:
                cluster_ids = random.sample(cluster_ids, k=sample_size)
            cluster_names = [
                f"""Cluster ID: {c['cluster_id']}, density (4dp): {c['density_4dp']},
                size: {c['cluster_size']}"""
                for c in cluster_ids
            ]
            cluster_ids = [c["cluster_id"] for c in cluster_ids]
            named_clusters_dict = dict(zip(cluster_ids, cluster_names))

    cluster_recs = df_clusters_as_records(linker, df_clustered_nodes, cluster_ids)
    df_nodes = create_df_nodes(linker, df_clustered_nodes, cluster_ids)
    nodes_recs = df_nodes.as_record_dict()
    edges_recs = df_edges_as_records(linker, df_predicted_edges, df_nodes)

    # Render template with cluster, nodes and edges
    template_path = "files/splink_cluster_studio/cluster_template.j2"
    template = Template(read_resource(template_path))

    template_data: dict[str, Any] = {
        "raw_edge_data": json.dumps(edges_recs, cls=EverythingEncoder),
        "raw_node_data": json.dumps(nodes_recs, cls=EverythingEncoder),
        "raw_clusters_data": json.dumps(cluster_recs, cls=EverythingEncoder),
        "splink_settings": json.dumps(
            linker._settings_obj._as_completed_dict(), cls=EverythingEncoder
        ),
        "svu_options": json.dumps(svu_options, cls=EverythingEncoder),
    }

    if cluster_names:
        named_clusters_dict = dict(zip(cluster_ids, cluster_names))

    if named_clusters_dict:
        template_data["named_clusters"] = json.dumps(
            named_clusters_dict, cls=EverythingEncoder
        )

    files = {
        "embed": "files/external_js/vega-embed@6.20.2",
        "stdlib": "files/external_js/stdlib.js@5.8.3",
        "vega": "files/external_js/vega@5.21.0",
        "vegalite": "files/external_js/vega-lite@5.2.0",
        "svu_text": "files/splink_vis_utils/splink_vis_utils.js",
        "custom_css": "files/splink_cluster_studio/custom.css",
    }
    for k, v in files.items():
        template_data[k] = read_resource(v)

    template_data["bundle_observable_notebook"] = bundle_observable_notebook

    rendered = template.render(**template_data)

    if os.path.isfile(out_path) and not overwrite:
        raise ValueError(
            f"The path {out_path} already exists. Please provide a different path."
        )
    else:
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            from pyspark.dbutils import DBUtils
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.getOrCreate()
            dbutils = DBUtils(spark)
            dbutils.fs.put(out_path, rendered, overwrite=True)
            # to view the dashboard inline in notebook displayHTML(rendered)
            return rendered
        else:
            with open(out_path, "w", encoding="utf-8") as html_file:
                html_file.write(rendered)
            # return the rendered dashboard html for inline viewing in the notebook
            return rendered
