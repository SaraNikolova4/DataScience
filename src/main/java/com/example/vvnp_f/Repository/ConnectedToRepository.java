package com.example.vvnp_f.Repository;

import com.example.vvnp_f.Models.ConnectedTo;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ConnectedToRepository extends Neo4jRepository<ConnectedTo, Long> {

    @Query("MATCH (start:Country)-[r:CONNECTED_TO]->(end:Country) " +
            "RETURN r{.year, .points_type, .points, startNode: start.name, endNode: end.name, __elementId__: elementId(r)}")
    List<ConnectedTo> findAllConnections();

    List<ConnectedTo> findAllByStartNode(String stringNode);

    ConnectedTo findByEndNode(String endNode);
}
