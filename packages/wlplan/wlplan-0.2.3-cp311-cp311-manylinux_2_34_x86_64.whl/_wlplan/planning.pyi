from __future__ import annotations
import typing
__all__ = ['Atom', 'Domain', 'Object', 'Predicate', 'Problem', 'State']
class Atom:
    """
    Parameters
    ----------
        predicate : Predicate
            Predicate object.
    
        objects : List[Object]
            List of object names.
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Atom) -> bool:
        ...
    def __init__(self, predicate: Predicate, objects: list[str]) -> None:
        ...
    def __repr__(self) -> str:
        ...
class Domain:
    """
    Parameters
    ----------
        name : str
            Domain name.
    
        predicates : List[Predicate]
            List of predicates.
    
        constant_objects : List[Object], optional
            List of constant objects.
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Domain) -> bool:
        ...
    @typing.overload
    def __init__(self, name: str, predicates: list[Predicate], constant_objects: list[str]) -> None:
        ...
    @typing.overload
    def __init__(self, name: str, predicates: list[Predicate]) -> None:
        ...
    def __repr__(self) -> str:
        ...
class Object:
    """
    Object is a type alias for a str.
    """
class Predicate:
    """
    Parameters
    ----------
        name : str
            Predicate name.
    
        arity : int
            Predicate arity.
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Predicate) -> bool:
        ...
    def __init__(self, name: str, arity: int) -> None:
        ...
    def __repr__(self) -> str:
        ...
class Problem:
    """
    Parameters
    ----------
        domain : Domain
            Domain object.
    
        objects : List[Object]
            List of object names.
    
        positive_goals : List[Atom]
            List of positive goal atoms.
    
        negative_goals : List[Atom]
            List of negative goal atoms.
    """
    def __init__(self, domain: Domain, objects: list[str], positive_goals: list[Atom], negative_goals: list[Atom]) -> None:
        ...
class State:
    """
    State is a type alias for a list of Atoms.
    """
