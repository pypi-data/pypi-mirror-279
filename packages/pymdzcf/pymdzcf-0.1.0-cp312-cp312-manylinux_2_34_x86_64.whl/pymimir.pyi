"""
Mimir: Lifted PDDL parsing and expansion library.
"""
from __future__ import annotations
import typing
__all__ = ['AStarSearch', 'Action', 'ActionSchema', 'Atom', 'BreadthFirstSearch', 'Domain', 'DomainParser', 'GoalMatcher', 'GroundedSuccessorGenerator', 'H1Heuristic', 'H2Heuristic', 'Heuristic', 'Implication', 'LiftedSuccessorGenerator', 'Literal', 'LiteralGrounder', 'Object', 'OpenList', 'Predicate', 'PriorityQueueOpenList', 'Problem', 'ProblemParser', 'Search', 'State', 'StateSpace', 'SuccessorGenerator', 'Transition', 'Type']
class AStarSearch(Search):
    def __init__(self, problem: Problem, successor_generator: SuccessorGenerator, heuristic: Heuristic, open_list: OpenList) -> None:
        """
        Creates an A* search object.
        """
class Action:
    @staticmethod
    def new(problem: Problem, schema: ActionSchema, arguments: list[Object]) -> Action:
        ...
    def __repr__(self) -> str:
        ...
    def apply(self, state: State) -> State:
        """
        Creates a new state state based on the given state and the effect of the action.
        """
    def get_arguments(self) -> list[Object]:
        """
        Gets the arguments of the action.
        """
    def get_conditional_effect(self) -> list[Implication]:
        """
        Gets the conditional effect of the action.
        """
    def get_effect(self) -> list[typing.Literal]:
        """
        Gets the unconditional effect of the action.
        """
    def get_name(self) -> str:
        """
        Gets the name of the action.
        """
    def get_precondition(self) -> list[typing.Literal]:
        """
        Gets the precondition of the action.
        """
    def is_applicable(self, state: State) -> bool:
        """
        Tests whether the action is applicable in the state.
        """
    @property
    def cost(self) -> float:
        """
        Gets the cost of the action.
        """
    @property
    def problem(self) -> Problem:
        """
        Gets the problem associated with the action.
        """
    @property
    def schema(self) -> ActionSchema:
        """
        Gets the action schema associated with the action.
        """
class ActionSchema:
    def __repr__(self) -> str:
        ...
    @property
    def arity(self) -> int:
        """
        Gets the arity of the action schema.
        """
    @property
    def conditional_effect(self) -> list[Implication]:
        """
        Gets the conditional effect of the action schema.
        """
    @property
    def effect(self) -> list[typing.Literal]:
        """
        Gets the unconditional effect of the action schema.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the action schema.
        """
    @property
    def parameters(self) -> list[Object]:
        """
        Gets the parameters of the action schema.
        """
    @property
    def precondition(self) -> list[typing.Literal]:
        """
        Gets the precondition of the action schema.
        """
class Atom:
    def __repr__(self) -> str:
        ...
    def get_name(self) -> str:
        """
        Gets the name of the atom.
        """
    def matches_state(self, state: State) -> bool:
        """
        Tests if any atom matches an atom in the state
        """
    def replace_term(self, index: int, object: Object) -> Atom:
        """
        Replaces a term in the atom
        """
    @property
    def predicate(self) -> Predicate:
        """
        Gets the predicate of the atom
        """
    @property
    def terms(self) -> list[Object]:
        """
        Gets the terms of the atom
        """
class BreadthFirstSearch(Search):
    def __init__(self, problem: Problem, successor_generator: SuccessorGenerator) -> None:
        """
        Creates a breadth-first search object.
        """
class Domain:
    def __repr__(self) -> str:
        ...
    def get_constant_map(self) -> dict[str, Object]:
        """
        Gets a dictionary mapping constant name to constant object.
        """
    def get_predicate_id_map(self) -> dict[int, Predicate]:
        """
        Gets a dictionary mapping predicate identifier to predicate object.
        """
    def get_predicate_name_map(self) -> dict[str, Predicate]:
        """
        Gets a dictionary mapping predicate name to predicate object.
        """
    def get_type_map(self) -> dict[str, Type]:
        """
        Gets a dictionary mapping type name to type object.
        """
    @property
    def action_schemas(self) -> list[ActionSchema]:
        """
        Gets the action schemas of the domain.
        """
    @property
    def constants(self) -> list[Object]:
        """
        Gets the constants of the domain.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the domain.
        """
    @property
    def predicates(self) -> list[Predicate]:
        """
        Gets the predicates of the domain.
        """
    @property
    def requirements(self) -> list[str]:
        """
        Gets the requirements of the domain.
        """
    @property
    def static_predicates(self) -> list[Predicate]:
        """
        Gets the static predicates of the domain.
        """
    @property
    def types(self) -> list[Type]:
        """
        Gets the types of the domain.
        """
class DomainParser:
    def __init__(self, path: str) -> None:
        ...
    def parse(self) -> Domain:
        """
        Parses the associated file and creates a new domain.
        """
class GoalMatcher:
    def __init__(self, state_space: StateSpace) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @typing.overload
    def best_match(self, goal: list[Atom]) -> tuple[State, int]:
        ...
    @typing.overload
    def best_match(self, state: State, goal: list[Atom]) -> tuple[State, int]:
        ...
class GroundedSuccessorGenerator(SuccessorGenerator):
    def __init__(self, problem: Problem) -> None:
        ...
class H1Heuristic(Heuristic):
    def __init__(self, problem: Problem, successor_generator: SuccessorGenerator) -> None:
        """
        Creates a h1 heuristic function object.
        """
class H2Heuristic(Heuristic):
    def __init__(self, problem: Problem, successor_generator: SuccessorGenerator) -> None:
        """
        Creates a h2 heuristic function object.
        """
class Heuristic:
    pass
class Implication:
    def __repr__(self) -> str:
        ...
    @property
    def antecedent(self) -> list[typing.Literal]:
        """
        Gets the antecedent of the implication.
        """
    @property
    def consequence(self) -> list[typing.Literal]:
        """
        Gets the consequence of the implication.
        """
class LiftedSuccessorGenerator(SuccessorGenerator):
    def __init__(self, problem: Problem) -> None:
        ...
class Literal:
    def __repr__(self: typing.Literal) -> str:
        ...
    @property
    def atom(self) -> Atom:
        """
        Gets the atom of the literal.
        """
    @property
    def negated(self) -> bool:
        """
        Returns whether the literal is negated.
        """
class LiteralGrounder:
    def __init__(self, problem: Problem, atom_list: list[Atom]) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def ground(self, state: State) -> list[tuple[list[Atom], list[tuple[str, Object]]]]:
        """
        Gets a list of instantiations of the associated atom list that are true in the given state.
        """
class Object:
    def __init__(self, id: int, name: str, type: Type) -> None:
        """
        Creates a new object with the given id, name and type.
        """
    def __repr__(self) -> str:
        ...
    def is_constant(self) -> bool:
        """
        Returns whether the term is a constant.
        """
    def is_variable(self) -> bool:
        """
        Returns whether the term is a variable.
        """
    @property
    def id(self) -> int:
        """
        Gets the identifier of the object.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the object.
        """
    @property
    def type(self) -> Type:
        """
        Gets the type of the object.
        """
class OpenList:
    pass
class Predicate:
    def __repr__(self) -> str:
        ...
    def as_atom(self) -> Atom:
        """
        Creates a new atom where all terms are variables.
        """
    @property
    def arity(self) -> int:
        """
        Gets the arity of the predicate.
        """
    @property
    def id(self) -> int:
        """
        Gets the identifier of the predicate.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the predicate.
        """
    @property
    def parameters(self) -> list[Object]:
        """
        Gets the parameters of the predicate.
        """
class PriorityQueueOpenList(OpenList):
    def __init__(self) -> None:
        """
        Creates a priority queue open list object.
        """
class Problem:
    def __repr__(self) -> str:
        ...
    def create_state(self, arg0: list[Atom]) -> State:
        """
        Creates a new state given a list of atoms.
        """
    def get_encountered_atoms(self) -> list[Atom]:
        """
        Gets all atoms seen so far.
        """
    def replace_initial(self, initial: list[Atom]) -> Problem:
        """
        Gets a new object with the given initial atoms.
        """
    @property
    def domain(self) -> Domain:
        """
        Gets the domain associated with the problem.
        """
    @property
    def goal(self) -> list[typing.Literal]:
        """
        Gets the goal of the problem.
        """
    @property
    def initial(self) -> list[Atom]:
        """
        Gets the initial atoms of the problem.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the problem.
        """
    @property
    def objects(self) -> list[Object]:
        """
        Gets the objects of the problem.
        """
class ProblemParser:
    def __init__(self, path: str) -> None:
        ...
    def parse(self, arg0: Domain) -> Problem:
        """
        Parses the associated file and creates a new problem.
        """
class Search:
    def abort(self) -> None:
        ...
    def get_statistics(self) -> dict[str, int | float]:
        """
        Get statistics of the search so far.
        """
    def plan(self) -> tuple[bool, list[Action]]:
        ...
    def register_callback(self, callback_function: typing.Callable[[], None]) -> None:
        """
        The callback function will be invoked as the search algorithm progresses.
        """
    def set_initial_state(self, state: State) -> None:
        """
        Sets the initial state of the search.
        """
class State:
    def __eq__(self, arg0: State) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
    def get_atoms(self) -> list[Atom]:
        """
        Gets the atoms of the state.
        """
    def get_atoms_by_predicate(self) -> dict[Predicate, list[Atom]]:
        """
        Gets a dictionary mapping predicates to ground atoms of the given predicate that are true in the state.
        """
    def get_fluent_atoms(self) -> list[Atom]:
        """
        Gets the fluent atoms of the state.
        """
    def get_problem(self) -> Problem:
        """
        Gets the problem associated with the state.
        """
    def get_static_atoms(self) -> list[Atom]:
        """
        Gets the static atoms of the state.
        """
    def literals_hold(self, literals: list[typing.Literal]) -> bool:
        """
        Tests whether all ground literals hold with respect to their polarity in the state.
        """
    def matches_all(self, atom_list: list[Atom]) -> bool:
        """
        Tests whether all atoms matches an atom in the state.
        """
    def matching_bindings(self, atom_list: list[Atom]) -> list[tuple[list[Atom], list[tuple[str, Object]]]]:
        """
        Gets all instantiations (and bindings) of the atom list that matches the state.
        """
    def pack_object_ids_by_predicate_id(self, include_types: bool, include_goal: bool) -> tuple[dict[int, list[int]], dict[int, tuple[str, int]]]:
        """
        Gets a dictionary mapping predicate identifiers to a flattened list of object ids, implicitly denoting the atoms true in the state, and a dictionary mapping identifiers to names.
        """
class StateSpace:
    @staticmethod
    def new(problem: Problem, successor_generator: SuccessorGenerator, max_expanded: int = 1000000) -> StateSpace:
        ...
    def __repr__(self) -> str:
        ...
    def get_backward_transitions(self, state: State) -> list[Transition]:
        """
        Gets the possible backward transitions of the given state.
        """
    def get_distance_between_states(self, from_state: State, to_state: State) -> int:
        """
        Gets the distance between the "from state" to the "to state".
        """
    def get_distance_from_initial_state(self, state: State) -> int:
        """
        Gets the distance from the initial state to the given state.
        """
    def get_distance_to_goal_state(self, state: State) -> int:
        """
        Gets the distance from the given state to the closest goal state.
        """
    def get_forward_transitions(self, state: State) -> list[Transition]:
        """
        Gets the possible forward transitions of the given state.
        """
    def get_goal_states(self) -> list[State]:
        """
        Gets all goal states of the state space.
        """
    def get_initial_state(self) -> State:
        """
        Gets the initial state of the state space.
        """
    def get_longest_distance_to_goal_state(self) -> int:
        """
        Gets the longest distance from a state to its closest goal state.
        """
    def get_states(self) -> list[State]:
        """
        Gets all states in the state space.
        """
    def get_unique_id(self, state: State) -> int:
        """
        Gets an unique identifier of the given from 0 to N - 1, where N is the number of states in the state space.
        """
    def is_dead_end_state(self, state: State) -> bool:
        """
        Tests whether the given state is a dead end state.
        """
    def is_goal_state(self, state: State) -> bool:
        """
        Tests whether the given state is a goal state.
        """
    def num_dead_end_states(self) -> int:
        """
        Gets the number of dead end states in the state space.
        """
    def num_goal_states(self) -> int:
        """
        Gets the number of goal states in the state space.
        """
    def num_states(self) -> int:
        """
        Gets the number of states in the state space.
        """
    def num_transitions(self) -> int:
        """
        Gets the number of transitions in the state space.
        """
    def sample_dead_end_state(self) -> State:
        """
        Gets a uniformly random dead end state from the state space.
        """
    def sample_state(self) -> State:
        """
        Gets a uniformly random state from the state space.
        """
    def sample_state_with_distance_to_goal(self, distance: int) -> State:
        """
        Gets a uniformly random state from the state space with the given distance to its closest goal state.
        """
    @property
    def domain(self) -> Domain:
        """
        Gets the domain associated with the state space.
        """
    @property
    def problem(self) -> Problem:
        """
        Gets the problem associated with the state space.
        """
class SuccessorGenerator:
    def __repr__(self) -> str:
        ...
    def get_applicable_actions(self, state: State) -> list[Action]:
        """
        Gets all ground actions applicable in the given state.
        """
class Transition:
    def __repr__(self) -> str:
        ...
    @property
    def action(self) -> Action:
        """
        Gets the action associated with the transition.
        """
    @property
    def source(self) -> State:
        """
        Gets the source of the transition.
        """
    @property
    def target(self) -> State:
        """
        Gets the target of the transition.
        """
class Type:
    def __repr__(self) -> str:
        ...
    @property
    def base(self) -> Type:
        """
        Gets the base type of the type.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the type.
        """
