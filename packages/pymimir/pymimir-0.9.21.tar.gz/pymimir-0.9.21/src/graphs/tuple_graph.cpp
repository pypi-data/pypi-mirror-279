/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#include "mimir/graphs/tuple_graph.hpp"

namespace mimir
{

/**
 * TupleGraphVertex
 */

TupleGraphVertex::TupleGraphVertex(VertexIndex identifier, TupleIndex tuple_index, StateList states) :
    m_identifier(identifier),
    m_tuple_index(tuple_index),
    m_states(std::move(states))
{
}

VertexIndex TupleGraphVertex::get_identifier() const { return m_identifier; }

TupleIndex TupleGraphVertex::get_tuple_index() const { return m_tuple_index; }

const StateList& TupleGraphVertex::get_states() const { return m_states; }

/**
 * TupleGraph
 */

TupleGraph::TupleGraph(std::shared_ptr<StateSpaceImpl> state_space,
                       std::shared_ptr<FluentAndDerivedMapper> atom_index_mapper,
                       std::shared_ptr<TupleIndexMapper> tuple_index_mapper,
                       State root_state,
                       TupleGraphVertexList vertices,
                       std::vector<VertexIndexList> forward_successors,
                       std::vector<VertexIndexList> backward_successors,
                       std::vector<VertexIndexList> vertex_indices_by_distance,
                       std::vector<StateList> states_by_distance) :
    m_state_space(std::move(state_space)),
    m_atom_index_mapper(std::move(atom_index_mapper)),
    m_tuple_index_mapper(std::move(tuple_index_mapper)),
    m_root_state(root_state),
    m_vertices(std::move(vertices)),
    m_forward_successors(std::move(forward_successors)),
    m_backward_successors(std::move(backward_successors)),
    m_vertex_indices_by_distance(std::move(vertex_indices_by_distance)),
    m_states_by_distance(std::move(states_by_distance))
{
}

std::optional<VertexIndexList> TupleGraph::compute_admissible_chain(const GroundAtomList<Fluent>& fluent_atoms, const GroundAtomList<Derived>& derived_atoms)
{
    // Construct the explict tuple representation
    auto atom_indices = AtomIndexList {};
    for (const auto& atom : fluent_atoms)
    {
        const auto atom_index = atom->get_identifier();
        assert(atom_index < m_atom_index_mapper->get_fluent_remap().size());

        const auto remapped_atom_index = m_atom_index_mapper->get_fluent_remap()[atom_index];
        assert(remapped_atom_index != -1);

        atom_indices.push_back(remapped_atom_index);
    }
    for (const auto& atom : derived_atoms)
    {
        const auto atom_index = atom->get_identifier();
        assert(atom_index < m_atom_index_mapper->get_derived_remap().size());

        const auto remapped_atom_index = m_atom_index_mapper->get_derived_remap()[atom_index];
        assert(remapped_atom_index != -1);

        atom_indices.push_back(remapped_atom_index);
    }
    std::sort(atom_indices.begin(), atom_indices.end());

    if (static_cast<int>(atom_indices.size()) > m_tuple_index_mapper->get_arity())
    {
        // Size of tuple exceeds width, hence, it cannot be in the tuple graph.
        return std::nullopt;
    }
    // Construct the implicit tuple representation by adding placeholders and using the perfect hash function.
    atom_indices.resize(m_tuple_index_mapper->get_arity(), m_tuple_index_mapper->get_num_atoms());
    assert(std::is_sorted(atom_indices.begin(), atom_indices.end()));
    const auto tuple_index = m_tuple_index_mapper->to_tuple_index(atom_indices);

    for (const auto& vertex : m_vertices)
    {
        if (vertex.get_tuple_index() == tuple_index)
        {
            // Backtrack admissible chain until the root and return an admissible chain that proves the width.
            auto cur_vertex_index = vertex.get_identifier();
            auto admissible_chain = VertexIndexList { cur_vertex_index };
            while (!m_backward_successors[cur_vertex_index].empty())
            {
                cur_vertex_index = m_backward_successors[cur_vertex_index].front();
                admissible_chain.push_back(cur_vertex_index);
            }
            std::reverse(admissible_chain.begin(), admissible_chain.end());
            return admissible_chain;
        }
    }
    // Tuple was not found in the tuple graph.
    return std::nullopt;
}

std::shared_ptr<StateSpaceImpl> TupleGraph::get_state_space() const { return m_state_space; }

std::shared_ptr<FluentAndDerivedMapper> TupleGraph::get_atom_index_mapper() const { return m_atom_index_mapper; }

std::shared_ptr<TupleIndexMapper> TupleGraph::get_tuple_index_mapper() const { return m_tuple_index_mapper; }

State TupleGraph::get_root_state() const { return m_root_state; }

const TupleGraphVertexList& TupleGraph::get_vertices() const { return m_vertices; }

const std::vector<VertexIndexList>& TupleGraph::get_forward_successors() const { return m_forward_successors; }

const std::vector<VertexIndexList>& TupleGraph::get_backward_successors() const { return m_backward_successors; }

const std::vector<VertexIndexList>& TupleGraph::get_vertex_indices_by_distances() const { return m_vertex_indices_by_distance; }

const std::vector<StateList>& TupleGraph::get_states_by_distance() const { return m_states_by_distance; }

/**
 * TupleGraphFactory
 */

TupleGraphFactory::TupleGraphArityZeroComputation::TupleGraphArityZeroComputation(std::shared_ptr<FluentAndDerivedMapper> atom_index_mapper,
                                                                                  std::shared_ptr<TupleIndexMapper> tuple_index_mapper,
                                                                                  std::shared_ptr<StateSpaceImpl> state_space,
                                                                                  const State root_state,
                                                                                  bool prune_dominated_tuples) :
    m_atom_index_mapper(std::move(atom_index_mapper)),
    m_tuple_index_mapper(std::move(tuple_index_mapper)),
    m_state_space(std::move(state_space)),
    m_root_state(root_state),
    m_prune_dominated_tuples(prune_dominated_tuples)
{
}

void TupleGraphFactory::TupleGraphArityZeroComputation::compute_root_state_layer()
{
    const auto empty_tuple_index = m_tuple_index_mapper->get_empty_tuple_index();
    const auto root_state_vertex_id = 0;
    m_vertices.emplace_back(root_state_vertex_id, empty_tuple_index, StateList { m_root_state });
    m_vertex_indices_by_distances.push_back({ empty_tuple_index });
    m_states_by_distance.push_back({ m_root_state });
}

void TupleGraphFactory::TupleGraphArityZeroComputation::compute_first_layer()
{
    const auto empty_tuple_index = m_tuple_index_mapper->get_empty_tuple_index();
    const auto root_state_vertex_id = 0;

    const auto& transitions = m_state_space->get_forward_transitions().at(m_root_state.get_id());
    m_forward_successors.resize(m_vertices.size() + transitions.size());
    m_backward_successors.resize(m_vertices.size() + transitions.size());
    auto vertex_indices_layer = VertexIndexList {};
    auto states_layer = StateList {};
    for (const auto& transition : transitions)
    {
        const auto succ_state = transition.get_successor_state();
        const auto succ_state_vertex_id = m_vertices.size();
        m_vertices.emplace_back(succ_state_vertex_id, empty_tuple_index, StateList { succ_state });
        m_forward_successors[root_state_vertex_id].push_back(succ_state_vertex_id);
        m_backward_successors[succ_state_vertex_id].push_back(root_state_vertex_id);
        vertex_indices_layer.push_back(succ_state_vertex_id);
        states_layer.push_back(succ_state);
    }
    m_vertex_indices_by_distances.push_back(std::move(vertex_indices_layer));
    m_states_by_distance.push_back(std::move(states_layer));
}

TupleGraph TupleGraphFactory::TupleGraphArityZeroComputation::extract_tuple_graph()
{
    return TupleGraph(std::move(m_state_space),
                      std::move(m_atom_index_mapper),
                      std::move(m_tuple_index_mapper),
                      m_root_state,
                      std::move(m_vertices),
                      std::move(m_forward_successors),
                      std::move(m_backward_successors),
                      std::move(m_vertex_indices_by_distances),
                      std::move(m_states_by_distance));
}

TupleGraphFactory::TupleGraphArityKComputation::TupleGraphArityKComputation(std::shared_ptr<FluentAndDerivedMapper> atom_index_mapper_,
                                                                            std::shared_ptr<TupleIndexMapper> tuple_index_mapper_,
                                                                            std::shared_ptr<StateSpaceImpl> state_space_,
                                                                            const State root_state_,
                                                                            bool prune_dominated_tuples_) :
    atom_index_mapper(std::move(atom_index_mapper_)),
    tuple_index_mapper(std::move(tuple_index_mapper_)),
    state_space(std::move(state_space_)),
    root_state(root_state_),
    prune_dominated_tuples(prune_dominated_tuples_),
    novelty_table(atom_index_mapper, tuple_index_mapper)
{
}

void TupleGraphFactory::TupleGraphArityKComputation::compute_root_state_layer()
{
    // Clear data structures
    cur_vertices.clear();
    cur_states.clear();

    cur_states.push_back(root_state);
    novelty_table.compute_novel_tuple_indices(root_state, novel_tuple_indices);
    if (prune_dominated_tuples)
    {
        const int vertex_id = vertices.size();
        vertices.emplace_back(vertex_id, novel_tuple_indices.front(), StateList { root_state });
        cur_vertices.push_back(vertex_id);
    }
    else
    {
        for (const auto& novel_tuple_index : novel_tuple_indices)
        {
            const int vertex_id = vertices.size();
            vertices.emplace_back(vertex_id, novel_tuple_index, StateList { root_state });
            cur_vertices.push_back(vertex_id);
        }
    }
    vertex_indices_by_distances.push_back(cur_vertices);
    states_by_distance.push_back(cur_states);
    novelty_table.insert_tuple_indices(novel_tuple_indices);
}

void TupleGraphFactory::TupleGraphArityKComputation::compute_next_state_layer()
{
    // Clear data structures
    cur_states.clear();

    for (const auto& state : states_by_distance.back())
    {
        for (const auto& transition : state_space->get_forward_transitions().at(state.get_id()))
        {
            const auto succ_state = transition.get_successor_state();

            if (!visited_states.count(succ_state))
            {
                cur_states.push_back(succ_state);
            }
            visited_states.insert(succ_state);
        }
    }
}

void TupleGraphFactory::TupleGraphArityKComputation::compute_next_novel_tuple_indices()
{
    // Clear data structures
    novel_tuple_indices_set.clear();
    novel_tuple_indices.clear();
    novel_tuple_index_to_states.clear();
    state_to_novel_tuple_indices.clear();

    for (const auto& state : cur_states)
    {
        novelty_table.compute_novel_tuple_indices(state, novel_tuple_indices);
        for (const auto& tuple_index : novel_tuple_indices)
        {
            novel_tuple_index_to_states[tuple_index].insert(state);
        }
        state_to_novel_tuple_indices.emplace(state, novel_tuple_indices);
        novel_tuple_indices_set.insert(novel_tuple_indices.begin(), novel_tuple_indices.end());
    }
    novel_tuple_indices.clear();
    novel_tuple_indices.insert(novel_tuple_indices.end(), novel_tuple_indices_set.begin(), novel_tuple_indices_set.end());
    novelty_table.insert_tuple_indices(novel_tuple_indices);
}

void TupleGraphFactory::TupleGraphArityKComputation::extend_optimal_plans_from_prev_layer()
{
    // Clear data structures
    cur_extended_novel_tuple_indices_set.clear();
    cur_extended_novel_tuple_indices.clear();
    cur_extended_novel_tuple_index_to_prev_vertices.clear();

    const auto& forward_transitions = state_space->get_forward_transitions();

    for (auto& prev_vertex : cur_vertices)
    {
        cur_novel_tuple_index_to_extended_state.clear();

        // Compute extended plans
        for (const auto state : vertices.at(prev_vertex).get_states())
        {
            for (const auto& transition : forward_transitions.at(state.get_id()))
            {
                const auto succ_state = transition.get_successor_state();

                if (state_to_novel_tuple_indices.count(succ_state))
                {
                    for (const auto target_tuple_index : state_to_novel_tuple_indices.at(succ_state))
                    {
                        cur_novel_tuple_index_to_extended_state[target_tuple_index].insert(state);
                    }
                }
            }
        }

        // Check whether all plans for tuple t_{i-1} were extended into optimal plan for tuple t_i.
        for (const auto& [cur_novel_tuple_index, extended_states] : cur_novel_tuple_index_to_extended_state)
        {
            bool all_optimal_plans_extended = (extended_states.size() == vertices.at(prev_vertex).get_states().size());

            if (all_optimal_plans_extended)
            {
                cur_extended_novel_tuple_indices_set.insert(cur_novel_tuple_index);
                cur_extended_novel_tuple_index_to_prev_vertices[cur_novel_tuple_index].insert(prev_vertex);
            }
        }
    }
    cur_extended_novel_tuple_indices.insert(cur_extended_novel_tuple_indices.end(),
                                            cur_extended_novel_tuple_indices_set.begin(),
                                            cur_extended_novel_tuple_indices_set.end());
}

void TupleGraphFactory::TupleGraphArityKComputation::instantiate_next_layer()
{
    // Clear data structures
    tuple_index_to_dominating_tuple_indices.clear();
    cur_vertices.clear();

    if (prune_dominated_tuples)
    {
        for (size_t i = 0; i < cur_extended_novel_tuple_indices.size(); ++i)
        {
            const auto tuple_index_1 = cur_extended_novel_tuple_indices[i];

            const auto& states_1 = novel_tuple_index_to_states.at(tuple_index_1);

            for (size_t j = i + 1; j < cur_extended_novel_tuple_indices.size(); ++j)
            {
                const auto tuple_index_2 = cur_extended_novel_tuple_indices[j];

                const auto& states_2 = novel_tuple_index_to_states.at(tuple_index_2);

                if (states_1 == states_2)
                {
                    // Keep only one tuple_index with a specific set of underlying states.
                    cur_extended_novel_tuple_indices_set.erase(tuple_index_2);
                    continue;
                }

                const auto is_subseteq = std::all_of(states_2.begin(), states_2.end(), [&states_1](const auto& element) { return states_1.count(element); });

                if (is_subseteq)
                {
                    // tuple_index_2 is dominated by tuple_index_1 because states_2 < states_1.
                    tuple_index_to_dominating_tuple_indices[tuple_index_1].insert(tuple_index_2);
                }
            }
        }

        // Keep only tuple indices whose underlying states is a smallest subset.
        for (const auto& [tuple_index, dominated_by_tuple_indices] : tuple_index_to_dominating_tuple_indices)
        {
            if (dominated_by_tuple_indices.empty())
            {
                cur_extended_novel_tuple_indices_set.erase(tuple_index);
            }
        }
    }

    for (const auto& tuple_index : cur_extended_novel_tuple_indices_set)
    {
        auto cur_vertex_index = vertices.size();
        const auto& cur_states = novel_tuple_index_to_states.at(tuple_index);
        vertices.emplace_back(cur_vertex_index, tuple_index, StateList(cur_states.begin(), cur_states.end()));
        cur_vertices.push_back(cur_vertex_index);

        for (const auto prev_vertex_index : cur_extended_novel_tuple_index_to_prev_vertices[tuple_index])
        {
            forward_successors.resize(cur_vertex_index + 1);
            backward_successors.resize(cur_vertex_index + 1);

            forward_successors[prev_vertex_index].push_back(cur_vertex_index);
            backward_successors[cur_vertex_index].push_back(prev_vertex_index);
        }
    }

    states_by_distance.push_back(cur_states);
    vertex_indices_by_distances.push_back(cur_vertices);
}

bool TupleGraphFactory::TupleGraphArityKComputation::compute_next_layer()
{
    compute_next_state_layer();
    if (cur_states.empty())
    {
        return false;
    }

    compute_next_novel_tuple_indices();
    if (novel_tuple_indices.empty())
    {
        return false;
    }

    extend_optimal_plans_from_prev_layer();
    if (cur_extended_novel_tuple_indices_set.empty())
    {
        return false;
    }

    instantiate_next_layer();

    return true;
}

TupleGraph TupleGraphFactory::TupleGraphArityKComputation::extract_tuple_graph()
{
    return TupleGraph(std::move(state_space),
                      std::move(atom_index_mapper),
                      std::move(tuple_index_mapper),
                      root_state,
                      std::move(vertices),
                      std::move(forward_successors),
                      std::move(backward_successors),
                      std::move(vertex_indices_by_distances),
                      std::move(states_by_distance));
}

TupleGraph TupleGraphFactory::create_for_arity_zero(const State root_state) const
{
    auto computation = TupleGraphArityZeroComputation(m_atom_index_mapper, m_tuple_index_mapper, m_state_space, root_state, m_prune_dominated_tuples);

    computation.compute_root_state_layer();

    computation.compute_first_layer();

    return computation.extract_tuple_graph();
}

TupleGraph TupleGraphFactory::create_for_arity_k(const State root_state) const
{
    auto computation = TupleGraphArityKComputation(m_atom_index_mapper, m_tuple_index_mapper, m_state_space, root_state, m_prune_dominated_tuples);

    computation.compute_root_state_layer();

    while (true)
    {
        auto is_empty = computation.compute_next_layer();

        if (!is_empty)
        {
            break;
        }
    }

    return computation.extract_tuple_graph();
}

TupleGraphFactory::TupleGraphFactory(std::shared_ptr<StateSpaceImpl> state_space, int arity, bool prune_dominated_tuples) :
    m_state_space(state_space),
    m_prune_dominated_tuples(prune_dominated_tuples),
    m_atom_index_mapper(std::make_shared<FluentAndDerivedMapper>(m_state_space->get_aag()->get_pddl_factories().get_ground_atom_factory<Fluent>(),
                                                                 m_state_space->get_aag()->get_pddl_factories().get_ground_atom_factory<Derived>())),
    m_tuple_index_mapper(std::make_shared<TupleIndexMapper>(arity,
                                                            m_state_space->get_aag()->get_pddl_factories().get_num_ground_atoms<Fluent>()
                                                                + m_state_space->get_aag()->get_pddl_factories().get_num_ground_atoms<Derived>()))
{
}

TupleGraph TupleGraphFactory::create(const State root_state) const
{
    return (m_tuple_index_mapper->get_arity() > 0) ? create_for_arity_k(root_state) : create_for_arity_zero(root_state);
}

std::shared_ptr<StateSpaceImpl> TupleGraphFactory::get_state_space() const { return m_state_space; }

std::shared_ptr<FluentAndDerivedMapper> TupleGraphFactory::get_atom_index_mapper() const { return m_atom_index_mapper; }

std::shared_ptr<TupleIndexMapper> TupleGraphFactory::get_tuple_index_mapper() const { return m_tuple_index_mapper; }

std::ostream& operator<<(std::ostream& out, std::tuple<const TupleGraph&, const Problem, const PDDLFactories&> data)
{
    const auto& [tuple_graph, problem, pddl_factories] = data;
    auto combined_atom_indices = AtomIndexList {};
    auto fluent_atom_indices = AtomIndexList {};
    auto derived_atom_indices = AtomIndexList {};

    out << "digraph {\n"
        << "rankdir=\"LR\""
        << "\n";

    // 3. Tuple nodes.
    for (int node_index : tuple_graph.get_vertex_indices_by_distances().front())
    {
        out << "Dangling" << node_index << " [ label = \"\", style = invis ]\n";
    }
    for (const auto& vertex_ids : tuple_graph.get_vertex_indices_by_distances())
    {
        for (int vertex_id : vertex_ids)
        {
            const auto& vertex = tuple_graph.get_vertices()[vertex_id];
            out << "t" << vertex.get_identifier() << "[";
            out << "label=<";
            out << "index=" << vertex.get_identifier() << "<BR/>";
            out << "tuple index=" << vertex.get_tuple_index() << "<BR/>";

            tuple_graph.get_tuple_index_mapper()->to_atom_indices(vertex.get_tuple_index(), combined_atom_indices);
            tuple_graph.get_atom_index_mapper()->remap_and_separate(combined_atom_indices, fluent_atom_indices, derived_atom_indices);
            const auto fluent_atoms = pddl_factories.get_ground_atoms_from_ids<Fluent>(fluent_atom_indices);
            const auto derived_atoms = pddl_factories.get_ground_atoms_from_ids<Derived>(derived_atom_indices);
            out << "fluent_atoms=" << fluent_atoms << ", derived_atoms=" << derived_atoms << "<BR/>";
            out << "states=[";
            for (size_t i = 0; i < vertex.get_states().size(); ++i)
            {
                const auto& state = vertex.get_states()[i];
                if (i != 0)
                {
                    out << "<BR/>";
                }
                out << std::make_tuple(problem, state, std::cref(pddl_factories));
            }
            out << "]>]\n";
        }
    }
    // 4. Group states with same distance together
    // 5. Tuple edges
    out << "{\n";
    for (const auto& vertex_id : tuple_graph.get_vertex_indices_by_distances().front())
    {
        const auto& vertex = tuple_graph.get_vertices()[vertex_id];
        out << "Dangling" << vertex.get_identifier() << "->t" << vertex.get_identifier() << "\n";
    }
    out << "}\n";
    for (const auto& vertex_ids : tuple_graph.get_vertex_indices_by_distances())
    {
        out << "{\n";
        for (const auto& vertex_id : vertex_ids)
        {
            for (const auto& succ_vertex_id : tuple_graph.get_forward_successors()[vertex_id])
            {
                out << "t" << vertex_id << "->"
                    << "t" << succ_vertex_id << "\n";
            }
        }
        out << "}\n";
    }
    out << "}\n";  // end digraph

    return out;
}

}
