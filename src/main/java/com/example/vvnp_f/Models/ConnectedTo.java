package com.example.vvnp_f.Models;

import lombok.Data;
import org.springframework.data.neo4j.core.schema.*;

import java.util.List;

@RelationshipProperties
@Data
public class ConnectedTo {

    @Id
    @GeneratedValue
    private Long id;

    @Property(name = "year")
    private List<Integer> years;

    @Property(name = "points_type")
    private List<Integer> pointsTypes;

    @Property(name = "points")
    private List<Integer> points;

    @Property(name = "startNode")
    private String startNode;

    @Property(name = "endNode")
    private String endNode;

    @Property(name = " __elementId__")
    private String elementId;

}
