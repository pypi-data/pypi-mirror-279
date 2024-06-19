from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .exceptions import MissingDependencyException
from .graph_metrics import (
    _basic_edge_metrics_sql,
    _bridges_from_igraph_sql,
    _edges_for_igraph_sql,
    _full_bridges_sql,
    _node_mapping_table_sql,
    _truncated_edges_sql,
)
from .splink_dataframe import SplinkDataFrame
from .unique_id_concat import (
    _composite_unique_id_from_edges_sql,
)

if TYPE_CHECKING:
    from .linker import Linker

logger = logging.getLogger(__name__)


def compute_edge_metrics(
    linker: Linker,
    df_node_metrics: SplinkDataFrame,
    df_predict: SplinkDataFrame,
    df_clustered: SplinkDataFrame,
    threshold_match_probability: float,
) -> SplinkDataFrame:
    try:
        df_edge_metrics = compute_igraph_metrics(
            linker,
            df_node_metrics,
            df_predict,
            df_clustered,
            threshold_match_probability,
        )
    except MissingDependencyException:
        logger.warning(
            "To compute edge metrics you must install the `igraph` package. "
            "Continuing without computing edge metrics."
        )
        df_edge_metrics = compute_basic_edge_metrics(
            linker, df_predict, threshold_match_probability
        )
    return df_edge_metrics


def compute_basic_edge_metrics(
    linker: Linker, df_predict: SplinkDataFrame, threshold_match_probability: float
):
    sql_info = _truncated_edges_sql(df_predict, threshold_match_probability)
    linker._enqueue_sql(**sql_info)

    truncated_edges_table_name = sql_info["output_table_name"]
    uid_cols = linker._settings_obj._unique_id_input_columns

    composite_uid_edges_l = _composite_unique_id_from_edges_sql(uid_cols, "l")
    composite_uid_edges_r = _composite_unique_id_from_edges_sql(uid_cols, "r")
    sql_info = _basic_edge_metrics_sql(
        composite_uid_edges_l, composite_uid_edges_r, truncated_edges_table_name
    )
    linker._enqueue_sql(**sql_info)

    df_truncated_edges = linker._execute_sql_pipeline()
    return df_truncated_edges


def compute_igraph_metrics(
    linker: Linker,
    df_node_metrics: SplinkDataFrame,
    df_predict: SplinkDataFrame,
    df_clustered: SplinkDataFrame,
    threshold_match_probability: float,
) -> SplinkDataFrame:
    try:
        import igraph as ig
    except ImportError:
        raise MissingDependencyException(
            "You need to install the 'igraph' package to compute "
            "the edge metric 'is_bridge'."
        ) from None
    uid_cols = linker._settings_obj._unique_id_input_columns
    # need composite unique ids
    composite_uid_edges_l = _composite_unique_id_from_edges_sql(uid_cols, "l")
    composite_uid_edges_r = _composite_unique_id_from_edges_sql(uid_cols, "r")

    # firstly we (arbitrarily) map node ids to 1-indexed integers with no gaps
    # this is how igraph deals with nodes
    sql_infos = _node_mapping_table_sql(df_node_metrics)
    for sql_info in sql_infos:
        linker._enqueue_sql(**sql_info)
    df_node_mappings = linker._execute_sql_pipeline()

    # we keep only edges at or above relevant threshold
    sql_info = _truncated_edges_sql(df_predict, threshold_match_probability)
    linker._enqueue_sql(**sql_info)
    df_truncated_edges = linker._execute_sql_pipeline()

    # we map the truncated edges to the integer encoding for nodes above,
    # keeping only the list of endpoints
    sql_info = _edges_for_igraph_sql(
        df_node_mappings,
        df_truncated_edges.physical_name,
        composite_uid_edges_l,
        composite_uid_edges_r,
    )
    linker._enqueue_sql(**sql_info)
    edges_for_igraph = linker._execute_sql_pipeline()
    # we will need to manually register a table, so we use the hash from this table
    igraph_edges_hash = edges_for_igraph.physical_name[-9:]
    # NB: for large data we may have to revise this and process in chunks
    df_edges_for_igraph = edges_for_igraph.as_pandas_dataframe()
    # feed our edges to igraph, get the edges which are bridges as a pandas frame,
    # and register this table with our backend
    igraph_df = ig.Graph.DataFrame(df_edges_for_igraph, directed=False)
    bridges_indices = igraph_df.bridges()
    df_bridges_pd = df_edges_for_igraph.iloc[bridges_indices, :]
    df_bridges = linker.register_table(
        df_bridges_pd, f"__splink__bridges_{igraph_edges_hash}"
    )
    # map our bridge edges back to the original node labelling
    sql_info = _bridges_from_igraph_sql(df_node_mappings, df_bridges)
    linker._enqueue_sql(**sql_info)
    # and adjoin edges which are _not_ bridges, labelling them as such
    sql_info = _full_bridges_sql(
        df_truncated_edges,
        sql_info["output_table_name"],
        composite_uid_edges_l,
        composite_uid_edges_r,
    )
    linker._enqueue_sql(**sql_info)
    df_edge_metrics = linker._execute_sql_pipeline()
    return df_edge_metrics
