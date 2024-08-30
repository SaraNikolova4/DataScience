package com.example.vvnp_f.Models;

import lombok.Data;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Property;

@Node("Country")
@Data
public class Country {

    @Id
    private String name;

    @Property("finals")
    private Object finals;

    @Property("semi_1")
    private Object semi1;

    @Property("semi_2")
    private Object semi2;
    @Property("semi_count_1")
    private Integer semiCount1;

    @Property("semi_count_2")
    private Integer semiCount2;

    @Property("finals_count")
    private Integer finalsCount;

}