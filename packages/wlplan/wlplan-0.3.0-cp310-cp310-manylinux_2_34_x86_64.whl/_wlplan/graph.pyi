from __future__ import annotations
import typing
__all__ = ['Graph']
class Graph:
    """
    WLPlan graph object.
    
    Graphs have integer node colours and edge labels.
    
    Parameters
    ----------
        node_colours : List[int]
            List of node colours, where `node[i]` is the colour of node `i` indexed from 0.
    
        node_names : List[str], optional
            List of node names, where `node_names[i]` is the name of node `i` indexed from 0.
    
        edges : List[Tuple[int, int]]
            List of labelled edges, where `edges[u] = [(r_1, v_1), ..., (r_k, v_k)]` represents edges from node `u` to nodes `v_1, ..., v_k` with labels `r_1, ..., r_k`, respectively. WLPlan graphs are directed so users must ensure that edges are undirected.
    
    Attributes
    ----------
        node_colours : List[int]
            List of node colours.
    
        edges : List[Tuple[int, int]]
            List of labelled edges.
    
    Methods
    -------
        get_node_name(u: int) -> str
            Get the name of node `u`.
    
        dump() -> None
            Print the graph representation.
    """
    @typing.overload
    def __init__(self, node_colours: list[int], edges: list[list[tuple[int, int]]]) -> None:
        ...
    @typing.overload
    def __init__(self, node_colours: list[int], node_names: list[str], edges: list[list[tuple[int, int]]]) -> None:
        ...
    def __repr__(self) -> str:
        """
        :meta private:
        """
    def dump(self) -> None:
        """
        :meta private:
        """
    def get_node_name(self, u: int) -> str:
        """
        :meta private:
        """
    @property
    def edges(self) -> list[list[tuple[int, int]]]:
        """
        :meta private:
        """
    @property
    def node_colours(self) -> list[int]:
        """
        :meta private:
        """
